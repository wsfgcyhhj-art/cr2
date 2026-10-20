import asyncio
import logging
from config import bot, dp
from database import db
from handlers import commands, fsm_book


async def main():
    await db.init_db()
    dp.include_router(commands.router_commands)
    dp.include_router(fsm_book.router_add_book)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
