from durak_bot.durak.instance import durak
from durak_bot.util.logger import logger


@durak.event(command='fl_update')
def on_friend_list_update(data: dict):
    if data['kind'] != 'INVITE':
        return

    durak.friend.accept(data['user']['id'])
    logger.warning(f"Accepted friend with id {data['user']['id']}")
