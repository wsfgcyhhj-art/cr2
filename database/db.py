# функции для связи с бд
import aiosqlite
from database import queries
from config import path_db


async def init_db():
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(queries.products_table)
        await conn.execute(queries.products_detail_table)
        await conn.execute(queries.create_staff_table)
        await conn.commit()
    print('База данных успешно подключена!')


async def add_product_db(name, price, description, photo, category, color, product_id):
    async with aiosqlite.connect(path_db) as conn:
        # await conn.execute(queries.insert_product, (name, price, photo, product_id))
        await conn.execute(queries.insert_product_detail, (category, color, product_id, description))
        await conn.commit()


async def product_exists(product_id):
    async with aiosqlite.connect(path_db) as conn:
        cursor = await conn.execute(queries.select_product_id, (product_id, ))
        return await cursor.fetchone() is not None


async def get_products_db():
    async with aiosqlite.connect(path_db) as conn:
        cursor = await conn.execute(queries.get_products)
        products = await cursor.fetchall()
    return products

async def update_product(field, value, product_id):
    if field in ('name', 'price'):
        table = 'products'
    elif field in ('description', 'category', 'color'):
        table = 'products_detail'
    else:
        return

    query = queries.update_product.format(table=table, field=field)

    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(query, (value, product_id))
        await conn.commit()


async def is_staff_db(user_id: int):
    async with aiosqlite.connect(path_db) as conn:
        cursor = await conn.execute(queries.check_staff, (user_id, ))
        row = await cursor.fetchone()
    return row is not None


async def add_staff_db(user_id, full_name):
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(queries.insert_staff, (user_id, full_name))
        await conn.commit()


async def get_staff_list():
    async with aiosqlite.connect(path_db) as conn:
        cursor = await conn.execute(queries.get_staff_list)
        staff_list = await cursor.fetchall()
        return staff_list


async def delete_product(product_id):
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(queries.delete_product.format(table='products_detail'), (product_id,))
        await conn.execute(queries.delete_product.format(table='products'), (product_id,))
        await conn.commit()


delete_product_db = delete_product


# =====================================================================================
# import sqlite3
# from database import queries

# path_db = "database/sqlite3.db"

# def init_db():
#     conn = sqlite3.connect(path_db)
#     cursor = conn.cursor()
#     cursor.execute(queries.products_table)
#     print('DB connect')
#     conn.commit()
#     conn.close()

# def add_product_db(name, price, description, photo):
#     conn = sqlite3.connect(path_db)
#     cursor = conn.cursor()
#     cursor.execute(queries.insert_product, (name, price, description, photo))
#     # cursor.execute(queries.insert_product, (name,))
#     conn.commit()
#     conn.close()
