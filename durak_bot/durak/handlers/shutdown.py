from durak_bot.durak.instance import durak
from durak_bot.database import db


@durak.event(command='shutdown')
def on_shutdown() -> None:
    db.shutdown()
