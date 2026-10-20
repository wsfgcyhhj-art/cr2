from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import db


class AddBook(StatesGroup):
    book_id = State()
    title = State()
    author = State()
    genre = State()


router_add_book = Router()


@router_add_book.message(Command('add_book'))
async def add_book_start(message: Message, state: FSMContext):
    await message.answer('Введите номер книги:')
    await state.set_state(AddBook.book_id)


@router_add_book.message(AddBook.book_id)
async def process_book_id(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer('Номер книги должен быть числом! Введите еще раз:')
        return

    if await db.book_exists(int(message.text)):
        await message.answer('Книга с таким номером уже есть! Введите другой:')
        return

    await state.update_data(book_id=int(message.text))
    await message.answer('Введите название книги:')
    await state.set_state(AddBook.title)


@router_add_book.message(AddBook.title)
async def process_title(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Введите текстовое название книги:')
        return

    await state.update_data(title=message.text)
    await message.answer('Введите автора книги:')
    await state.set_state(AddBook.author)


@router_add_book.message(AddBook.author)
async def process_author(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Введите автора текстом:')
        return

    await state.update_data(author=message.text)
    await message.answer('Введите жанр книги:')
    await state.set_state(AddBook.genre)


@router_add_book.message(AddBook.genre)
async def process_genre(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Введите жанр текстом:')
        return

    await state.update_data(genre=message.text)
    data = await state.get_data()

    await db.add_book_db(
        book_id=data['book_id'],
        title=data['title'],
        author=data['author'],
        genre=data['genre']
    )

    await message.answer(
        f"Книга успешно добавлена!\n"
        f"Номер: {data['book_id']}\n"
        f"Название: {data['title']}\n"
        f"Автор: {data['author']}\n"
        f"Жанр: {data['genre']}"
    )
    await state.clear()
