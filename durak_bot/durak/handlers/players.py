from durak_bot.database import db
from durak_bot.durak.instance import durak
from durak_bot.util.logger import logger


@durak.event(command='p')
def on_player_join(data: dict):
    if data.get('swap'):
        logger.info('Player swapped their place')
        return

    if data['user'] is None:
        return

    user_id: int = data['user']['id']
    user_name: str = data['user']['name']

    logger.info(f'Player {user_id} ({user_name}) has joined')
    db.remember_player(player_id=user_id, player_name=user_name)

    durak.game.ready()
