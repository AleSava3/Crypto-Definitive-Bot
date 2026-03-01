async def main():
    print("Test invio messaggio...")
    await send("✅ TEST BOT ATTIVO")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(scan, "interval", minutes=15)
    scheduler.start()

    print("Bot avviato correttamente 🚀")

    while True:
        await asyncio.sleep(60)
