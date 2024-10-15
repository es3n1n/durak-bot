import sqlite3
import atexit

from contextlib import contextmanager
from datetime import datetime

from durak_bot import ctx, __version__
from durak_bot.util.fs import ROOT_DIR
from durak_bot.database.models.game import EGameResult


INIT_PLAYERS = """
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    seen_times INTEGER NOT NULL,
    last_seen_time DATETIME NOT NULL
);
"""

INIT_GAMES = """
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    finished_at_utc DATETIME NOT NULL,
    bot_version TEXT,
    result TEXT NOT NULL,
    players_count INTEGER NOT NULL,
    deck_size INTEGER NOT NULL,
    bet INTEGER NOT NULL,
    passing_enabled BOOLEAN NOT NULL,
    tricks_enabled BOOLEAN NOT NULL,
    draw_enabled BOOLEAN NOT NULL,
    fast BOOLEAN NOT NULL
);
"""

INIT_GAME_INDEX = """
CREATE INDEX IF NOT EXISTS idx_games_result ON games(result);
"""


class Client:
    def __init__(self) -> None:
        self._conn: sqlite3.Connection | None = None
        self._initialized = False

        atexit.register(self.shutdown)

    @contextmanager
    def _get_cursor(self):
        if self._conn is None:
            raise ValueError('Database is not connected')

        cursor = self._conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def _setup(self) -> None:
        assert self._conn is not None

        with self._get_cursor() as cursor:
            cursor.execute(INIT_PLAYERS)
            cursor.execute(INIT_GAMES)
            cursor.execute(INIT_GAME_INDEX)
        self._conn.commit()

    def record_game_result(self, result: EGameResult) -> None:
        assert self._conn is not None
        game_data = {
            'finished_at_utc': datetime.utcnow(),
            'bot_version': f'v{__version__}',
            'result': result.value,
            'players_count': ctx.lobby.players_count,
            'deck_size': ctx.lobby.deck_size,
            'bet': ctx.lobby.bet,
            'passing_enabled': ctx.lobby.is_passing_enabled,
            'tricks_enabled': ctx.lobby.is_tricks_enabled,
            'draw_enabled': ctx.lobby.is_draw_enabled,
            'fast': ctx.lobby.is_fast,
        }

        with self._get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO games (
                    finished_at_utc, bot_version, result, players_count, 
                    deck_size, bet, passing_enabled, tricks_enabled, 
                    draw_enabled, fast
                ) VALUES (
                    :finished_at_utc, :bot_version, :result, :players_count,
                    :deck_size, :bet, :passing_enabled, :tricks_enabled,
                    :draw_enabled, :fast
                );""",
                game_data,
            )
        self._conn.commit()

    def remember_player(self, player_id: int, player_name: str) -> None:
        assert self._conn is not None
        player_data = {
            'player_id': player_id,
            'player_name': player_name,
            'last_seen_time': datetime.utcnow(),
        }

        with self._get_cursor() as cursor:
            cursor.execute(
                """
                INSERT OR REPLACE INTO players (id, name, seen_times, last_seen_time)
                VALUES (
                    :player_id,
                    :player_name,
                    COALESCE(
                        (SELECT seen_times + 1 FROM players WHERE id = :player_id),
                        1
                    ),
                    :last_seen_time
                );""",
                player_data,
            )
        self._conn.commit()

    def get_game_stats(self) -> dict[EGameResult, int]:
        assert self._conn is not None

        stats = {
            k: v
            for k, v in self._conn.execute('SELECT result, COUNT(*) AS count FROM games GROUP BY result').fetchall()
        }
        return {k: stats.get(k.value, 0) for k in EGameResult.all()}

    def connect(self) -> None:
        self.shutdown()

        self._conn = sqlite3.connect(ROOT_DIR / 'db.db')
        self._setup()
        self._initialized = True

    def shutdown(self) -> None:
        if self._initialized:
            self._initialized = False

        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __del__(self) -> None:
        self.shutdown()
