from aiogram import types, Dispatcher
from glass import bot, dp
from keyboards import kb_client
from data_base import sqlite_db_tutors, sqlite_db_programms, sqlite_db_products


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать!', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Tutor_from_EKB_bot')


async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Данный бот предоставляет информацию об услугах, предоставляемых нашей командой, в сфере дополнительного образования.\nТак же с помощью него Вы сможете приобрести наши специальные курсы видеоуроков.\nНажмите /start , чтобы начать.')
    await message.delete()


async def command_communication(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'По всем дополнительным вопросам пишите напрямую мне:\nhttps://t.me/Kadtsin')
    await message.delete()


async def programms_menu_command(message: types.Message):
    await sqlite_db_programms.sql_read(message)
    await message.delete()


async def tutors_menu_command(message: types.Message):
    await sqlite_db_tutors.sql_read(message)


async def products_menu_command(message: types.Message):
    await sqlite_db_products.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_communication, commands=['Связь'])
    dp.register_message_handler(programms_menu_command, commands=['Репетиторство'])
    dp.register_message_handler(tutors_menu_command, commands=['Наша_команда'])
    dp.register_message_handler(products_menu_command, commands=['Наши_видеокурсы'])
    dp.register_message_handler(command_help, commands=['Помощь'])
