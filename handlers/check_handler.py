from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import logger, scenarios, ADMINS
from checker.checker import checker_inst
from create_bot import bot
from database.repository import upsert_user

check_router = Router()

@check_router.message(Command("check"))
async def check_handler(message: Message) -> None:
    exception_text = "Требуемый формат запроса /check @yourbotnickname https://github.com/yourrepo Фамилия\n\nЕсли вы считаете, что делаете все верно, то обратитесь лично @byter1"
    try:
        # Ожидаемый формат "/check @yourbotnickname https://github.com/yourrepo Фамилия"
        args = message.text.split()
        if len(args) != 4:
            await message.answer(exception_text)
            raise Exception(f"Некорректный ввод {message}")
        
        await message.answer("Запуск тестирования. Это может занять несколько минут. 🧙‍♂️✨")
        check_client = await checker_inst.check_client()
        if not check_client:
            check_set_client = await checker_inst.set_client()
            if not check_set_client:
                await message.answer("К сожалению сейчас нет доступных чекеров, повторите попытку позже.")
                return
            
        result = await checker_inst.test_bot(args[1], scenarios)
        if result.get("success", False):
            await message.answer("Все тесты пройдены успешно, желаю успехов при решении контеста 👧🐕🌪️ ➡️ 🏰💚")
            await bot.send_message(chat_id=ADMINS[0], text=f"Пользователь {message.from_user.username} успешно прошел все тесты.\n\nСсылка на гитхаб: {args[2]}\n\nтег бота: {args[1]}")
        else:
            await message.answer(result.get("error", "Неизвестная ошибка при тестировании, убедитесь, что вы все сделали верно.\n\nЕсил вы уверены в своих действиях свяжитесь лично @byter1"))

        await upsert_user(username=message.from_user.username,
                          surname=args[3],
                          link=args[2],
                          bot_name=args[1],
                          tests_passed=result.get("tests_passed", 0)
                          )
        return
    except Exception as e:
        await message.answer(exception_text)
        logger.error(f"Ошибка у пользователя {message.from_user.username}\n{e}")
        return