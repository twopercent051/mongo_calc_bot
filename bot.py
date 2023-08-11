import asyncio
import logging

from tgbot.handlers.user import register_user
from tgbot.handlers.echo import register_echo
from tgbot.middlewares.environment import EnvironmentMiddleware

from create_bot import bot, dp, config, logger


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    pass


def register_all_handlers(dp):
    register_user(dp)


async def main():
    logger.info("Starting bot")

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:

        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
