import asyncio
from create_bot import bot, dp
from config import logger


async def main():
    try:
        logger.info("Starting bot")
        await bot.delete_webhook()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())