from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from database import db

router_commands = Router()


@router_commands.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        f"Я бот «Каталог книг».\n\n"
        f"Команды:\n"
        f"/add_book - добавить книгу\n"
        f"/books - каталог всех книг"
    )


@router_commands.message(Command('books'))
async def cmd_books(message: Message):
    books = await db.get_books_db()

    if not books:
        await message.answer('В каталоге пока нет ни одной книги!')
        return

    for book_id, title, author, genre in books:
        await message.answer(
            f"Номер книги: {book_id}\n"
            f"Название: {title}\n"
            f"Автор: {author}\n"
            f"Жанр: {genre}"
        )
