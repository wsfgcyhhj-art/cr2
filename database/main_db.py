import aiosqlite
from database import queries
from config import path_db
from database.db import (
    init_db,
    add_product_db,
    product_exists,
    get_products_db,
    update_product,
    is_staff_db,
    add_staff_db,
    get_staff_list,
)


async def delete_product(product_id):
    async with aiosqlite.connect(path_db) as conn:
        await conn.execute(queries.delete_product.format(table='products_detail'), (product_id,))
        await conn.execute(queries.delete_product.format(table='products'), (product_id,))
        await conn.commit()


delete_product_db = delete_product
