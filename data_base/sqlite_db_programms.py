import sqlite3 as sq
from glass import dp, bot


def sql_start():
    global base, cur
    base = sq.connect('programms.db')
    cur = base.cursor()
    if base:
        print('DBP connection ok')
    base.execute('CREATE TABLE IF NOT EXISTS menu(name TEXT PRIMARY KEY, tutor TEXT, description TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_message(message.from_user.id,
                               f'{ret[0]}\nПреподаватель: {ret[1]}\nОписание: {ret[2]}\nСтоимость: {ret[3]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
