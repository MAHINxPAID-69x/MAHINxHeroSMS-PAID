import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web

import database as db
from handlers import (
    handle_herosms_webhook,
    router,
    set_bot_instance,
)

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8080))


async def start_web_server():
    """Webhook / Healthcheck Server for Render"""
    app = web.Application()
    app.router.add_get("/", lambda r: web.Response(text="Bot is running!"))
    app.router.add_get("/webhook", handle_herosms_webhook)
    app.router.add_post("/webhook", handle_herosms_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logging.info(f"Web server started on port {PORT}")


async def clear_webhook_with_retry(bot: Bot, retries: int = 5):
    for attempt in range(1, retries + 1):
        try:
            await bot.delete_webhook(drop_pending_updates=True, request_timeout=30)
            logging.info("Webhook cleared successfully.")
            return
        except Exception as e:
            wait_sec = min(attempt * 3, 15)
            logging.warning(
                f"delete_webhook attempt {attempt}/{retries} failed: {e}. Retrying in {wait_sec}s..."
            )
            await asyncio.sleep(wait_sec)
    logging.warning("Could not clear webhook after retries; continuing to polling...")


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set!")

    # Initialize Database Schema
    await db.init_db()

    # Initialize Bot & Dispatcher
    bot = Bot(token=BOT_TOKEN)
    set_bot_instance(bot)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    # Start Aiohttp Web Server (Render Web Service Port Binding)
    await start_web_server()
    await clear_webhook_with_retry(bot)

    logging.info("Bot is starting polling...")
    try:
        while True:
            try:
                await dp.start_polling(bot, request_timeout=30)
                break
            except (asyncio.CancelledError, KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                logging.error(f"Polling error: {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
