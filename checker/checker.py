import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait, PeerIdInvalid, PhoneNumberBanned, UserDeactivatedBan
from config import logger, API_IDS, API_HASHS, REAL_PHONES, ADMINS
from create_bot import bot

class Checker:
    def __init__(self) -> None:
        self.client = None
        self.is_started = False

    async def set_client(self) -> bool:
        for api_id, api_hash, phone in zip(API_IDS, API_HASHS, REAL_PHONES):
            try:
                session_name = f"test_{api_id}"
                self.client = Client(session_name,
                                     api_id=api_id,
                                     api_hash=api_hash,
                                     device_model="Desktop (Python Script)",
                                     system_version="Windows 11",
                                     app_version="2.0.106",
                                     lang_code="ru")
                
                await self.client.start()
                await self.client.get_me()
                logger.info(f"Клиент с номером {phone} успешно получен.")
                await self.client.stop()
                break
            except (PhoneNumberBanned, UserDeactivatedBan):
                logger.error(f"Тестовый аккаунт с номером {phone} заблокирован")
                await bot.send_message(chat_id=ADMINS[0], text=f"Тестовый аккаунт с номером {phone} заблокирован")
                self.client = None
                continue
        else:
            if self.client is None:
                logger.error(f"Все тестовые аккаунты заблокированы")
                await bot.send_message(chat_id=ADMINS[0], text=f"Все тестовые аккаунты заблакированы")
                return False
        return True
    
    async def start_client(self):
        if not self.is_started:
            await self.client.start()
            self.is_started = True

    async def stop_client(self):
        if self.is_started:
            await self.client.stop()
            self.is_started = False

    async def check_client(self) -> bool:
        try:
            await self.start_client()
            await self.client.get_me()
            return True
        except (PhoneNumberBanned, UserDeactivatedBan):
            self.client = None
            return False
        
    async def test_bot(self, target_username: str, scenarios: list[dict]) -> dict:
        """
        Begins testing the target bot  

        :param scenarios: [{'input': Сколько видео в период..., 'output': 124 (ожидаемый ответ)}, {'input': ..., 'output': ...}, ...]
        :return: {'success' : True/False, 'error': optional[str] (text ans message)}
        """
        try:
            await self.start_client()

            try:
                clean_username = target_username.replace('@', '')
                chat = await self.client.get_chat(clean_username)
                if not chat:
                    raise PeerIdInvalid("Бот не найден")
                chat_id = chat.id
            except PeerIdInvalid as e:
                return {"success": False, "error": f"""Бот с тегом {target_username} не найден или недоступен.\n\n
                                                    Если вы считаете, что делаете все верно, свяжитесь лично @byter1"""}

            result = {"success": True, "error": None}

            for i, step in enumerate(scenarios):
                input_msg = step["input"]
                expected = step.get("output")
                wait_time = 10.0

                await self.client.send_message(chat_id, input_msg)
                await asyncio.sleep(wait_time)
                messages = [msg async for msg in self.client.get_chat_history(chat_id, limit=1)]
                
                if not messages:
                    result["success"] = False
                    error_msg = f"Шаг {i+1}: Бот не ответил на '{input_msg}'"
                    result["error"] = error_msg
                    break
                
                last_msg = messages[0]

                if last_msg.from_user and last_msg.from_user.is_bot:
                    response_text = last_msg.text or (last_msg.caption if last_msg.caption else "")
                    if expected not in response_text:
                        result["success"] = False
                        result["error"] = f"Шаг {i+1}: Ошибка валидации. Ожидалось содержимое '{expected}', получено '{response_text}'\n\nВходной тест: {input_msg}"
                        break
                else:
                     result["success"] = False
                     result["error"] = f"Шаг {i+1}: Не получен ответ от бота."
                     break
        except FloodWait as e:
            result["success"] = False
            result["error"] = f"Бот достиг лимита запросов, попробуйте залить ответ снова немного позднее."
        except Exception as e:
            logger.error(f"Ошибка в test_bot: {e}")
            result["success"] = False
            result["error"] = f"Неизвестная ошибка, попробуйте залить ответ снова немного позднее."
        
        return result
            
        
checker_inst = Checker()
            