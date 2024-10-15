from time import sleep

from durak_bot.util.logger import logger
from durak_bot.durak.handlers import init_handlers
from durak_bot.durak.instance import create_durak_connection, close_durak_connection


def main() -> None:
    logger.info('Hi')
    logger.debug(f'Loaded {init_handlers()} handler sources')

    logger.info('Initializing durak connection')
    create_durak_connection()

    try:
        while True:
            sleep(5)
    except KeyboardInterrupt:
        pass

    logger.info('Bye')
    close_durak_connection()


if __name__ == '__main__':
    main()
