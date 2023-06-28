from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.confige import confige_file

storege = MemoryStorage()
bot = Bot(token=confige_file['token'])
dp = Dispatcher(bot, storage=storege)

