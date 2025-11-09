import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start as start_handler, admin as admin_handler, shop as shop_handler, balance as balance_handler, history as history_handler

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# ✅ Routerlarni ro‘yxatdan o‘tkazish
dp.include_router(start_handler.router)
dp.include_router(admin_handler.router)
dp.include_router(shop_handler.router)
dp.include_router(balance_handler.router)
dp.include_router(history_handler.router)

async def main():
    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
