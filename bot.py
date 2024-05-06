# -*- coding: utf-8 -*-

import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from init import bot, logging
from bot_router import router


dp = Dispatcher(storage=MemoryStorage())

async def main() -> None:
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    print('<--Start bot!-->')
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())