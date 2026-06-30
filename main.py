"""
Alpha Bot — Main Entry Point
Run with: python main.py  (inside the venv)
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from logger import setup_logging
from config import BOT_TOKEN
from middlewares import BotMiddleware
from scheduler import setup_scheduler
import database as db

# ── Import all routers ────────────────────────────────────────────────────────
from handlers.start import router as start_router
from handlers.shop import router as shop_router
from handlers.profile import router as profile_router
from handlers.referral import router as referral_router
from handlers.reviews import router as reviews_router
from handlers.support import router as support_router
from handlers.admin import router as admin_router

log = logging.getLogger(__name__)


async def main():
    # ── Logging ───────────────────────────────────────────────────────────────
    setup_logging("INFO")
    log.info("Starting Alpha Bot...")

    # ── Validate config ───────────────────────────────────────────────────────
    if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
        log.critical("BOT_TOKEN is not set. Please edit your .env file.")
        return

    # ── Init DB ───────────────────────────────────────────────────────────────
    await db.get_db()
    log.info("Database ready.")

    # ── Bot + Dispatcher ──────────────────────────────────────────────────────
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # ── Middlewares ───────────────────────────────────────────────────────────
    dp.message.middleware(BotMiddleware())
    dp.callback_query.middleware(BotMiddleware())

    # ── Routers ───────────────────────────────────────────────────────────────
    dp.include_router(start_router)
    dp.include_router(shop_router)
    dp.include_router(profile_router)
    dp.include_router(referral_router)
    dp.include_router(reviews_router)
    dp.include_router(support_router)
    dp.include_router(admin_router)

    # ── Scheduler ─────────────────────────────────────────────────────────────
    scheduler = setup_scheduler(bot)
    scheduler.start()
    log.info("Scheduler started.")

    # ── Start polling ─────────────────────────────────────────────────────────
    log.info("Bot is running. Press Ctrl+C to stop.")
    try:
        await dp.start_polling(bot, allowed_updates=["message", "callback_query"])
    finally:
        scheduler.shutdown()
        await db.close_db()
        await bot.session.close()
        log.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
