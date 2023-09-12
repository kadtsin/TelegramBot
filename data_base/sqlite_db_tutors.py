import sqlite3 as sq
from glass import dp, bot


def sql_start():
    global base, cur
    base = sq.connect('tutors.db')
    cur = base.cursor()
    if base:
        print('DBT connection ok')
    base.execute('CREATE TABLE IF NOT EXISTS menu(photo TEXT, name TEXT PRIMARY KEY, description TEXT, link TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'Преподаватель: {ret[1]}\n{ret[2]}\n{ret[3]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
