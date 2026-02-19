import asyncio
from create_bot import bot, dp
from config import logger, ADMINS
from checker.checker import checker_inst
from handlers.check_handler import check_router


async def main():
    try:
        logger.info("Starting bot")
        is_checker_ready = await checker_inst.set_client()

        dp.include_router(check_router)
        
        if not is_checker_ready:
            logger.critical("Не удалось инициализировать тестовые аккаунты. Запуск бота отменен.")
            await bot.send_message(chat_id=ADMINS[0], text="Ни один тестовый аккаунт не смог стать клиентом при запуске основного бота.")
            return
        print("Тестировщик создан, запуск бота")
        await bot.delete_webhook()
        await dp.start_polling(bot)
    finally:
        await checker_inst.stop_client()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())