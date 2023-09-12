from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from glass import dp, bot
from data_base import sqlite_db_programms, sqlite_db_tutors, sqlite_db_products
from keyboards import admin_kb
import secrets
import string

ID = None


class FSMAdminPrograms(StatesGroup):
    name = State()
    tutor = State()
    description = State()
    price = State()


class FSMAdminTutors(StatesGroup):
    photo = State()
    name = State()
    description = State()
    link = State()


class FSMAdminProducts(StatesGroup):
    name = State()
    description = State()
    link = State()
    password = State()


async def make_change_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что надо, хозяин?', reply_markup=admin_kb.button_case_admin)
    await message.delete()


# Начало диалога загрузки программы
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminPrograms.name.set()
        await message.reply('Введи название услуги:')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ок!')


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdminPrograms.next()
        await message.reply('Введи преподавателя:')


async def load_tutor(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['tutor'] = message.text
        await FSMAdminPrograms.next()
        await message.reply('Введи описание:')


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdminPrograms.next()
        await message.reply('Введи цену:')


async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            try:
                price = float(message.text)
            except:
                await message.reply('Неккоректно:(')
                await state.finish()

            data['price'] = str(price) + ' руб/час.'

        await sqlite_db_programms.sql_add_command(state)
        await message.reply('Успешно')
        await state.finish()


# Начало диалога загрузки препода
async def cm_start2(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminTutors.photo.set()
        await message.reply('Пришлите фото:')


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            print(data)
        await FSMAdminTutors.next()
        await message.reply('Теперь введи имя:')


async def load_name2(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text

        await FSMAdminTutors.next()
        await message.reply('Введи описание:')


async def load_description2(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text

        await FSMAdminTutors.next()
        await message.reply('Введи ссылку:')


async def load_link(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['link'] = message.text

        await sqlite_db_tutors.sql_add_command(state)
        await message.reply('Успешно')
        await state.finish()


# Загрузка продуктов в магазин
async def cm_start3(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminProducts.name.set()
        await message.reply('Введи название курса:')


async def load_name3(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text

        await FSMAdminProducts.next()
        await message.reply('Введи описание:')


async def load_description3(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text

        await FSMAdminProducts.next()
        await message.reply('Введи ссылку:')


async def load_link2(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['link'] = message.text

        await FSMAdminProducts.next()
        await message.reply('Введи пароль:')
        await message.reply(
            'Возможный пароль: ' + ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(10)))


async def load_password(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['password'] = message.text

        await sqlite_db_tutors.sql_add_command(state)
        await message.reply('Успешно')
        await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def callback_query_handler(callback_query: types.CallbackQuery):
    await sqlite_db_programms.sql_delete_command(callback_query.data.replace('del ', ''))
    await sqlite_db_tutors.sql_delete_command(callback_query.data.replace('del ', ''))
    await sqlite_db_products.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удален.', show_alert=True)


async def delete_program(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db_programms.sql_read2()
        for ret in read:
            await bot.send_message(message.from_user.id, f'{ret[0]}\nОписание: {ret[1]}\nСтоимость: {ret[2]}')
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Удалить {ret[0]}', callback_data=f'del {ret[0]}')))


async def delete_tutor(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db_tutors.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'Преподаватель: {ret[1]}\n{ret[2]}\n{ret[3]}')
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


async def delete_product(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db_products.sql_read2()
        for ret in read:
            await bot.send_message(message.from_user.id, f'{ret[0]}\nСсылка: {ret[1]}\nПароль: {ret[2]}')
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Удалить {ret[0]}', callback_data=f'del {ret[0]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Загрузить_программу', state=None)
    dp.register_message_handler(cm_start2, commands='Загрузить_тьютора', state=None)
    dp.register_message_handler(cm_start3, commands='Загрузить_видеокурс', state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=FSMAdminPrograms.name)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdminTutors.photo)
    dp.register_message_handler(load_name2, state=FSMAdminTutors.name)
    dp.register_message_handler(load_name3, state=FSMAdminProducts.name)
    dp.register_message_handler(load_tutor, state=FSMAdminPrograms.tutor)
    dp.register_message_handler(load_description, state=FSMAdminPrograms.description)
    dp.register_message_handler(load_description2, state=FSMAdminTutors.description)
    dp.register_message_handler(load_description3, state=FSMAdminProducts.description)
    dp.register_message_handler(load_price, state=FSMAdminPrograms.price)
    dp.register_message_handler(load_link, state=FSMAdminTutors.link)
    dp.register_message_handler(load_link2, state=FSMAdminProducts.link)
    dp.register_message_handler(load_password, state=FSMAdminProducts.password)
    dp.register_message_handler(make_change_command, commands=['moderator'], is_chat_admin=True)
    # dp.register_message_handler(callback_query_handler, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_program, commands='Удалить_программу')
    dp.register_message_handler(delete_tutor, commands='Удалить_тьютора')
    dp.register_message_handler(delete_product, commands='Удалить_видео')
