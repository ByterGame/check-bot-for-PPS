from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from config import ADMINS, TXT_PATH
from database.repository import export_all_to_txt


admin_router = Router()


@admin_router.message(F.text=="Получить список результатов")
async def get_results(message: Message):
    if message.from_user.id in ADMINS:
        await export_all_to_txt(TXT_PATH)
        await message.answer_document(FSInputFile(TXT_PATH), caption="Результаты тестов")