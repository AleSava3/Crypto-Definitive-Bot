import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import SYMBOLS
from signal_engine import generate_signal
from telegram_bot import send


async def scan():
    for symbol in SYMBOLS:
        result = generate_signal(symbol)
        if result:
            signal, risk = result

            msg = f"""
🚨 {signal['level']} SIGNAL – {signal['symbol']}

Direzione: {signal['direction']}

ENTRY: {round(signal['entry'],2)}
STOP: {round(signal['stop'],2)}
TP: {round(signal['tp'],2)}

Leva: {risk['leverage']}x
Size: {risk['size']} USDT
Margine: {risk['margin']}€

Rischio: {risk['risk']}€
Target Profit: 20€
R:R: {risk['rr']}

Score: {signal['score']}/100
"""
            await send(msg)


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scan, "interval", minutes=15)
    scheduler.start()

    print("Bot avviato correttamente 🚀")

    # Mantiene il loop vivo
    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
