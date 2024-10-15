from durak_bot.durak.instance import durak
from durak_bot.database import db


@durak.event(command='init')
def on_init() -> None:
    db.connect()
