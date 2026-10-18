from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import db

router_delete = Router()


class DeleteProduct(StatesGroup):
    product_id = State()


@router_delete.callback_query(F.data.startswith('delete:'))
async def delete_product_callback(call: CallbackQuery):
    if not await db.is_staff_db(call.from_user.id):
        await call.message.answer('У вас нет доступа к этой команде!')
        await call.answer()
        return

    product_id = call.data.split(":")[1]

    if not await db.product_exists(product_id):
        await call.message.answer('Товар не найден!')
        await call.answer()
        return

    await db.delete_product(product_id=product_id)
    await call.message.answer(f'Товар с артикулом {product_id} успешно удален!')
    await call.answer()


@router_delete.message(Command('delete'))
async def delete_cmd(message: Message, state: FSMContext):
    if not await db.is_staff_db(message.from_user.id):
        await message.answer('У вас нет доступа к этой команде!')
        return

    await message.answer('Введите артикул товара для удаления:')
    await state.set_state(DeleteProduct.product_id)


@router_delete.message(DeleteProduct.product_id, F.text)
async def delete_by_article(message: Message, state: FSMContext):
    product_id = message.text.strip()

    if not product_id.isdigit():
        await message.answer('Артикул должен быть числом. Введите еще раз!')
        return

    if not await db.product_exists(product_id):
        await message.answer('Товар с таким артикулом не найден!')
        await state.clear()
        return

    await db.delete_product(product_id=product_id)
    await message.answer(f'Товар с артикулом {product_id} успешно удален!')
    await state.clear()
