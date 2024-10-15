from durak_bot import ctx
from durak_bot.durak.instance import durak
from durak_bot.util.logger import logger


def diff_nums(prev: int, cur: int) -> str:
    diff = cur - prev
    if diff < 0:
        return str(diff)
    return f'+{diff}'


@durak.event(command='uu')
def on_uu(data: dict) -> None:
    item_type: str = data['k']
    if item_type != 'points':
        return

    value: int = data['v']
    if ctx.stats.initial_balance is None:
        ctx.stats.initial_balance = value
        ctx.stats.last_balance = value
        logger.info(f'Received initial balance: {value}pts')
        logger.info('Ready to join lobbies')
        return

    diff_prev = diff_nums(ctx.stats.last_balance or 0, value)
    diff_init = diff_nums(ctx.stats.initial_balance, value)
    logger.info(f'Balance changed from {ctx.stats.last_balance} to {value}pts ({diff_prev}, {diff_init} since start)')
    ctx.stats.last_balance = value
