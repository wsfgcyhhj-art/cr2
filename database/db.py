import aiosqlite
from database import queries
from config import path_db

async def init_db():
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(queries.create_books_table)
        await conn.execute(queries.create_books_detail_table)
        await conn.commit()

async def add_book_db(book_id, title, author, genre):
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(queries.insert_book, (book_id, title, author))
        await conn.execute(queries.insert_book_detail, (book_id, genre))
        await conn.commit()

async def book_exists(book_id):
    async with aiosqlite.connect(path_db) as conn:
        cursor = await conn.execute(queries.select_book_id, (book_id,))
        row = await cursor.fetchone()
        return row is not None

async def get_books_db():
    async with aiosqlite.connect(path_db) as conn:
        cursor = await conn.execute(queries.get_books)
        return await cursor.fetchall()
