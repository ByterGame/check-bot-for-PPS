import asyncio
from create_bot import bot, dp
from config import logger, ADMINS
from checker.checker import checker_inst
from handlers.check_handler import check_router
from handlers.start_handler import start_router
from handlers.admin_handler import admin_router
from database import init_db


async def main():
    try:
        await init_db()
        logger.info("База данных инициализированна, инициализация тестировщика...")

        is_checker_ready = await checker_inst.set_client()        
        if not is_checker_ready:
            logger.critical("Не удалось инициализировать тестовые аккаунты. Запуск бота отменен.")
            await bot.send_message(chat_id=ADMINS[0], text="Ни один тестовый аккаунт не смог стать клиентом при запуске основного бота.")
            return
        logger.info("Тестирововащик инициализирован, запуск бота...")

        dp.include_routers(start_router, 
                           check_router,
                           admin_router)
        await bot.delete_webhook()
        await dp.start_polling(bot)
    finally:
        await checker_inst.stop_client()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
