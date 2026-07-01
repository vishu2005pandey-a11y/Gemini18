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

GEMINI_EMOJI = '<tg-emoji emoji-id="5206660927339924387">🤖</tg-emoji>'


async def _get_buttons(bot: Bot, product_name: str, mini_app_url: str, chat_id: int = 0) -> InlineKeyboardBuilder:
    """Build buttons for broadcast."""
    builder = InlineKeyboardBuilder()

    try:
        me = await bot.get_me()
        bot_username = me.username
    except Exception:
        bot_username = ""

    # Open Mini App — use t.me link with startapp param (opens Mini App inside Telegram)
    if mini_app_url and bot_username:
        builder.row(InlineKeyboardButton(
            text="🛍️  Open Mini App",
            url=f"https://t.me/{bot_username}/app"  # t.me/botname/app opens Mini App
        ))
    elif mini_app_url:
        builder.row(InlineKeyboardButton(
            text="🛍️  Open Mini App",
            url=mini_app_url
        ))

    if bot_username:
        builder.row(InlineKeyboardButton(
            text=f"🤖  Buy {product_name}",
            url=f"https://t.me/{bot_username}"
        ))

    return builder


async def _send_with_fallback(bot: Bot, chat_id: int, text: str, builder: InlineKeyboardBuilder):
    """Send message with buttons."""
    try:
        await bot.send_message(chat_id, text, reply_markup=builder.as_markup(), parse_mode="HTML")
    except Exception as e:
        log.warning("Broadcast failed to %s: %s", chat_id, e)


async def broadcast_purchase(username: str, qty: int, product_name: str, product_id: int = 0):
    """Broadcast a real purchase to channel and group."""
    if not BOT_TOKEN or not (CHANNEL_ID or GROUP_ID):
        return

    bot = Bot(token=BOT_TOKEN)
    mini_app_url = os.getenv("MINI_APP_URL", "")

    text = (
        f"{E_CART} <b>Someone just bought {qty}×</b> {GEMINI_EMOJI} {product_name}!\n"
        f"<i>Be the next — tap below!</i>"
    )

    builder = await _get_buttons(bot, product_name, mini_app_url)

    try:
        for chat_id in [CHANNEL_ID, GROUP_ID]:
            if chat_id:
                await _send_with_fallback(bot, chat_id, text, builder)
    finally:
        await bot.session.close()


async def broadcast_fake_purchase(qty: int, product_name: str, product_id: int = 0):
    """Broadcast a fake/simulated purchase to GROUP ONLY (not channel)."""
    if not BOT_TOKEN or not GROUP_ID:
        return

    bot = Bot(token=BOT_TOKEN)
    mini_app_url = os.getenv("MINI_APP_URL", "")

    text = (
        f"{E_CART} <b>Someone just bought {qty}×</b> {GEMINI_EMOJI} {product_name}!\n"
        f"<i>Be the next — tap below!</i>"
    )

    builder = await _get_buttons(bot, product_name, mini_app_url)

    try:
        await _send_with_fallback(bot, GROUP_ID, text, builder)
    except Exception as e:
        log.warning("Fake broadcast failed: %s", e)
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
        from aiogram.types import WebAppInfo
        builder.row(InlineKeyboardButton(text="🛍️  Shop Now", web_app=WebAppInfo(url=mini_app_url)))

    try:
        for chat_id in [CHANNEL_ID, GROUP_ID]:
            if chat_id:
                await _send_with_fallback(bot, chat_id, text, builder)
    finally:
        await bot.session.close()
