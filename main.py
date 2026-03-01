import asyncio
from telegram import Bot
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def main():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="🔥 TEST DIRETTO FUNZIONA")

asyncio.run(main())
