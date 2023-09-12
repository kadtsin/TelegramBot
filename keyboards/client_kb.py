from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_1 = KeyboardButton('/Связь')
button_2 = KeyboardButton('/Репетиторство')
button_3 = KeyboardButton('/Помощь')
button_4 = KeyboardButton('/Наша_команда')
button_5 = KeyboardButton('/Наши_видеокурсы')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(button_1, button_3).add(button_2, button_4).add(button_5)
