import asyncio, os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers import router

load_dotenv('.env')

dp = Dispatcher()


async def main():
    dp.include_router(router)
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError('BOT_TOKEN environment variable not found')
    bot = Bot(token=token)
    print('starting bot...')
    try:
        await dp.start_polling(bot)
    finally:
        print('closing bot...')


if __name__ == '__main__':
    asyncio.run(main())
