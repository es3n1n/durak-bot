import threading

from durakonline.utils import Server

from durak_bot.durak.instance import durak, create_durak_connection
from durak_bot.util.logger import logger


@durak.event(command='invite_to_game')
def on_invite(data: dict):
    game_id = data['game_id']
    password: str | None = data.get('password')
    lobby_server: Server = Server(data['server'])

    def non_blocking_join():
        nonlocal game_id, password, lobby_server

        current_server = durak.get_server()
        if lobby_server != current_server:
            logger.info(f'Switching server from {current_server} to {lobby_server}')
            durak.shutdown()

            durak.server_id = lobby_server

            logger.info('Recreating connection')
            create_durak_connection()

        logger.info('Joining the lobby')
        durak.game.join(password, game_id)
        logger.info('Joined the game')

    threading.Thread(target=non_blocking_join).start()
