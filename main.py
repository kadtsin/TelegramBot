from aiogram.utils import executor
from glass import dp
from handlers import client, admin, other
from data_base import sqlite_db_tutors, sqlite_db_programms, sqlite_db_products


async def on_startup(_):
    print('бот онлайн')
    sqlite_db_programms.sql_start()
    sqlite_db_tutors.sql_start()
    sqlite_db_products.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
