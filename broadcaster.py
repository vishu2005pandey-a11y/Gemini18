"""
Alpha Bot — Broadcaster
Sends purchase notifications to channel and group.

Key rule:
  - WebApp buttons (web_app=) DON'T work in groups/channels — use url= instead
  - URL buttons are always GREEN in Telegram
  - So we always use URL buttons for green color
"""
import os
import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import BOT_TOKEN, CHANNEL_ID, GROUP_ID
from locales.en import E_CART, E_STAR

log = logging.getLogger(__name__)


async def _get_buttons(bot: Bot, product_name: str, mini_app_url: str) -> InlineKeyboardBuilder:
    """Build green URL buttons for channel/group broadcast."""
    builder = InlineKeyboardBuilder()

    # ── Button 1: Open Mini App (URL = GREEN) ──────────────────────────────
    if mini_app_url:
        builder.row(InlineKeyboardButton(
            text="🛍️  Open Mini App",
            url=mini_app_url          # URL button = GREEN color
        ))

    # ── Button 2: Buy button via bot deep link (URL = GREEN) ───────────────
    try:
        me = await bot.get_me()
        bot_username = me.username
    except Exception:
        bot_username = ""

    if bot_username:
        builder.row(InlineKeyboardButton(
            text=f"🤖  Buy {product_name}",
            url=f"https://t.me/{bot_username}"   # URL button = GREEN color
        ))

    return builder


async def broadcast_purchase(username: str, qty: int, product_name: str, product_id: int = 0):
    """Broadcast a real purchase to channel and group."""
    if not BOT_TOKEN or not (CHANNEL_ID or GROUP_ID):
        return

    bot = Bot(token=BOT_TOKEN)
    mini_app_url = os.getenv("MINI_APP_URL", "")

    text = (
        f"{E_CART} <b>Someone just bought {qty}×</b> 🤖 {product_name}!\n"
        f"<i>Be the next — tap below!</i>"
    )

    builder = await _get_buttons(bot, product_name, mini_app_url)
    kb = builder.as_markup()

    try:
        for chat_id in [CHANNEL_ID, GROUP_ID]:
            if chat_id:
                try:
                    await bot.send_message(chat_id, text, reply_markup=kb, parse_mode="HTML")
                except Exception as e:
                    log.warning("Broadcast failed to %s: %s", chat_id, e)
    finally:
        await bot.session.close()


async def broadcast_stock_update(stock: int):
    """Notify channel/group about stock refill."""
    if not BOT_TOKEN or not (CHANNEL_ID or GROUP_ID):
        return

    bot = Bot(token=BOT_TOKEN)
    mini_app_url = os.getenv("MINI_APP_URL", "")

    text = (
        f"📦 <b>Stock Refilled!</b>\n\n"
        f"<b>{stock}</b> new links available.\n"
        f"Get yours before they're gone! {E_STAR}"
    )

    builder = InlineKeyboardBuilder()
    if mini_app_url:
        builder.row(InlineKeyboardButton(text="🛍️  Shop Now", url=mini_app_url))

    try:
        for chat_id in [CHANNEL_ID, GROUP_ID]:
            if chat_id:
                try:
                    await bot.send_message(chat_id, text,
                                           reply_markup=builder.as_markup(),
                                           parse_mode="HTML")
                except Exception as e:
                    log.warning("Stock broadcast failed to %s: %s", chat_id, e)
    finally:
        await bot.session.close()
