from .durakonline import Client
from .authorization import Authorization
from .game import Game
from .friend import Friend
from .socket_listener import SocketListener

from .utils import objects
from .utils import enums

__all__ = (
    'Client',
    'Authorization',
    'Game',
    'Friend',
    'SocketListener',
    'objects',
    'enums',
)

__title__ = 'durakonline.py'
__author__ = 'Zakovskiy, es3n1n'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-2024 Zakovskiy'
__version__ = '3.6.0'
