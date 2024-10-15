import threading
import time

from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.util.logger import logger
from durak_bot.types.card import Card


@durak.event(command='rt')
def on_rt_event(data: dict):
    # Cannot turn, probably should've been f instead of t
    if data['e'] == 1:
        logger.critical('Rejected, shouldve been f instead of t')
        logger.critical(str(data))
        assert False

    # Can't add more cards - no space left
    if data['e'] in (4, 12):
        logger.error('Rejected, cant add more cards - no space left')
        logger.error(str(data))
        ctx.cards.add_to_our_hand(Card.parse(data['c']))
        return

    # e = 2, can't add this card because it isnt on the table
    def non_blocking_handle():
        # No such cards on the table
        if data['e'] == 2:
            logger.critical('Rejected, no such card on the table')
            durak.client.send_server({'command': 'get_table'})

            time.sleep(5)
            assert False

        # Unknown
        logger.critical('Turn rejected')
        logger.critical(str(data))

        durak.client.send_server({'command': 'get_table'})
        durak.client.send_server({'command': 'get_hands'})

        time.sleep(5)
        assert False

    threading.Thread(target=non_blocking_handle).start()


@durak.event(command='rs')
def on_rs_event(data: dict):
    # e = 11 - opponent doesnt have enough cards to beat
    def non_blocking_handle():
        durak.client.send_server({'command': 'get_hands'})
        durak.game.forward_card(data['c'])

        logger.critical('Forward/transfer rejected')
        logger.critical(str(data))

        from time import sleep

        sleep(5)
        assert False

    threading.Thread(target=non_blocking_handle).start()


@durak.event(command='rb')
def on_rb_event(data: dict):
    if data['e'] == 7:
        logger.critical('Beat rejected, cant beat with this card')
        logger.critical(str(data))
        assert False

    # e = 7 means we cant beat with that card
    logger.critical('Beat rejected')
    logger.critical(str(data))
    assert False
