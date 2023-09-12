from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
#import markups as mk
import os
import glass
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import glass

from random import randint

yootoken = Bot(os.environ['SHOP_ID'])



dp = glass.dp


async def start(message, inf):
    our_kb = InlineKeyboardMarkup(row_width=1)
    global arr
    arr = inf
    btn_1 = InlineKeyboardButton(text=str(arr[0]), callback_data="mm")
    our_kb.insert(btn_1)
    await glass.bot.send_message(message.from_user.id, "Курс" + str(arr[0]), reply_markup=our_kb)


@dp.callback_query_handler(text="mm")
async def ss(call: types.CallbackQuery):

    await glass.bot.delete_message(call.from_user.id, call.message.message_id)
    await glass.bot.send_invoice(chat_id=call.from_user.id, title="Купить курс", description=arr[1], payload=arr[0],
                                 provider_token='381764678:TEST:32128', currency="RUB", start_parameter="test_bot",
                                 prices=[{"label": "Руб", "amount": randint(50000, 1000000)}])


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await glass.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "":
        await glass.bot.send_message(message.from_user.id, "Оплата прошла успешно")
        await glass.bot.send_message(message.from_user.id, arr[2] + ' ' + arr[3])
