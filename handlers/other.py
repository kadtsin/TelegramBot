from aiogram import types, Dispatcher
from glass import dp
import json
import string


async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split()}.intersection(
            set(json.load(open('censorship.json')))) != set():
        await message.reply('Нецензурная лексика запрезена!')
    else:
        await message.answer('Команды не найдено:(')

    await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
