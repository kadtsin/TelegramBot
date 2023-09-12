from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import dotenv
import os

storage = MemoryStorage()

dotenv.load_dotenv('.env')
bot = Bot(os.environ['BOT_TOKEN'])
dp = Dispatcher(bot, storage=storage)
