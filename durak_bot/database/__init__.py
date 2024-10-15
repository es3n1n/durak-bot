from durak_bot.database.client import Client
from durak_bot.database.models import EGameResult


__all__ = (
    'db',
    'EGameResult',
)

db = Client()
