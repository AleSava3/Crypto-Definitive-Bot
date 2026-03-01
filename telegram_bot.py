from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

async def send(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)
