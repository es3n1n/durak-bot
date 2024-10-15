from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.types.player_state import EPlayerState

from durak_bot.algorithm.actions.add_card import try_add_cards
from durak_bot.algorithm.actions.defense import try_defend
from durak_bot.algorithm.actions.attack import try_attack

from durak_bot.util.logger import debug_pprint, logger


def start_turn() -> None:
    logger.info('Starting turn')
    if not try_attack():
        logger.critical('Unable to attack')
        assert False

    logger.info('Attacked')


def defend() -> None:
    logger.info('Defending')

    if not try_defend():
        durak.game.take()
        logger.warning('Unable to defend, took the cards')
        return

    logger.info('Defended')


def add_cards() -> None:
    logger.info('Adding cards')

    if not try_add_cards():
        if ctx.players.are_we(EPlayerState.SHOULD_MOVE):
            logger.warning('No cards to add, pressing done')
            durak.game.done()
            return

        logger.warning('No cards to add, pressing pass')
        durak.game.do_pass()
        return

    logger.info('Added cards')


@durak.event(command='mode')
def on_mode_event(data: dict):
    logger.debug('Unseen cards:')
    debug_pprint(ctx.cards.unseen_cards)

    ctx.players.player_states = [EPlayerState(data[str(i)]) for i in range(ctx.lobby.players_count)]

    logger.debug('Player states:')
    debug_pprint(ctx.players.player_states)
    logger.debug('Known cards:')
    debug_pprint(ctx.cards.known_cards)
    logger.debug('Number of cards:')
    debug_pprint(ctx.cards.number_of_cards)

    # fixme: Kostil
    if ctx.cards.forwarding:
        # fixme: Kostil
        ctx.cards.forwarding = False
        logger.warning('Dropping mode update due to forwarding being set to true')
        return

    someone_defends = ctx.players.is_someone(EPlayerState.DEFENDS)
    someone_will_defend = ctx.players.is_someone(EPlayerState.WILL_DEFEND)
    ctx.players.is_someone(EPlayerState.IDLING_PASS_PRESSED)

    can_add_cards = ctx.players.are_we(EPlayerState.CAN_ADD_MORE_CARDS)
    can_add_cards = can_add_cards or (ctx.players.are_we(EPlayerState.SHOULD_MOVE) and someone_defends)
    can_add_cards = can_add_cards or (
        ctx.players.are_we(EPlayerState.SHOULD_MOVE) and someone_will_defend and len(ctx.cards.cards_on_table) > 0
    )

    attackers_count = ctx.players.player_states.count(EPlayerState.SHOULD_MOVE)
    we_should_move = ctx.players.are_we(EPlayerState.SHOULD_MOVE)

    we_are_defending = ctx.players.are_we(EPlayerState.DEFENDS)
    we_are_defending_or_will = we_are_defending or ctx.players.are_we(EPlayerState.WILL_DEFEND)

    # Try add cards
    if can_add_cards or (
        attackers_count > 1
        and not we_are_defending_or_will  # someone defends, we can add more cards
        and not ctx.players.are_we(EPlayerState.IDLING)  # can't add cards while idling
    ):
        # If we got tricked with a card, we should skip one update
        #   to make sure that we aren't adding cards until the opponent
        #   beats any of our cards
        if ctx.cards.got_tricked:
            ctx.cards.got_tricked = False
            logger.warning('Skipping tricked update')
            return

        add_cards()
        return

    # Should start the turn
    if we_should_move and someone_will_defend and not len(ctx.cards.cards_on_table):
        start_turn()
        return

    # Should defend
    if we_are_defending:
        defend()
        return
