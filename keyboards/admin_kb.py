from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load_program = KeyboardButton('/Загрузить_программу')
button_load_tutor = KeyboardButton('/Загрузить_тьютора')
button_load_product = KeyboardButton('/Загрузить_видеокурс')
button_delete_program = KeyboardButton('/Удалить_программу')
button_delete_tutor = KeyboardButton('/Удалить_тьютора')
button_delete_product = KeyboardButton('/Удалить_видео')
button_user = KeyboardButton('/start')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)
button_case_admin.add(button_load_program, button_delete_program).add(button_load_tutor, button_delete_tutor).add(
    button_load_product, button_delete_product).add(button_user)
