import asyncio
import logging
from handlers import commands, echo, fsm_add_product, fsm_edit_product, fsm_add_staff, fsm_delete
from config import bot, dp
from database import db 


async def main():
    await db.init_db()
    # регистрация обработчиков
    dp.include_router(commands.router_commands)
    dp.include_router(fsm_add_product.router_add_product)
    dp.include_router(fsm_edit_product.router_edit)
    dp.include_router(fsm_add_staff.router_add_staff)
    dp.include_router(fsm_delete.router_delete)
    

    # Обработчик на ВСЁ 
    dp.include_router(echo.router_echo)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
