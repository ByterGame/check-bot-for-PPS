from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.admin_keyboard import admin_kb
from config import ADMINS


start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: Message) -> None:
    text = "Привет!\n\nДля проверки своего задания отправь сообщение в следующем формате:\n/check @yourbotnickname https://github.com/yourrepo Фамилия"
    if message.from_user.id in ADMINS:
        await message.answer(text, reply_markup=admin_kb())
    else:
        await message.answer(text)
