from aiogram import Dispatcher, Bot
from logging import basicConfig, INFO
import os
from dotenv import load_dotenv
from handlers.routes import router
from aiogram.types import BotCommand
import asyncio
from middleware.rate_limit import RateLimitMiddleware
from database.engine import init_db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)

basicConfig(level=INFO)

async def main():

    dp = Dispatcher()

    await init_db()

    dp.message.middleware(RateLimitMiddleware(limit_seconds=1.0))
    dp.callback_query.middleware(RateLimitMiddleware(limit_seconds=1.0))



    dp.include_router(router)


    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="my_notes", description="Мои записи"),
        BotCommand(command="sign_up", description="Записаться")
    ]
    
    await bot.set_my_commands(commands)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main()) 
