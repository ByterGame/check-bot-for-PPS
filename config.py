import logging
import os
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = list(map(int, os.getenv("ADMINS").split(",")))
API_IDS = os.getenv("API_IDS").split(",")
API_HASHS = os.getenv("API_HASHS").split(",")
REAL_PHONES = os.getenv("REAL_PHONES").split(",")
DB_NAME = os.getenv("DB_NAME")
TXT_PATH = os.getenv("TXT_PATH")

scenarios = [
    {"input": "Какое общее количество лайков набрали все видео?", "output": "99025"},
    {"input": "Сколько видео появилось на платформе за май 2025", "output": "2"},
    {"input": "Сколько всего видео есть в системе?", "output": "358"},
    {"input": "Какое суммарное количество просмотров набрали все видео, опубликованные в июне 2025 года?", "output": "17668"},
    {"input": "Сколько видео у креатора с id aca1061a9d324ecf8c3fa2bb32d7be63 набрали больше 10 000 просмотров по итоговой статистике?", "output": "4"},
    {"input": "На сколько просмотров в сумме выросли все видео 28 ноября 2025 года?", "output": "14639"},
    {"input": "Какой суммарный прирост лайков получили все видео за ноябрь 2025 года?", "output": "98954"},
    {"input": "Какой суммарный прирост комментариев получили все видео за первые 3 часа после публикации каждого из них?", "output": "6"}
]