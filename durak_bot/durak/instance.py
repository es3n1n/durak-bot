from durak_bot.core.config import config

from durakonline import Client
from durakonline.utils import Server

durak = Client(server_id=Server.AMBER)


def create_durak_connection() -> None:
    durak.create_connection()
    durak.auth_sign()
    durak.authorization.signin_by_access_token(config.BOT_TOKEN)


def close_durak_connection() -> None:
    durak.shutdown()
