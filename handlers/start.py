"""
Start / Force-Join handler.
"""
import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery

import database as db
from config import CHANNEL_ID, GROUP_ID, CHANNEL_LINK, GROUP_LINK, LINKS_SOLD_COUNTER_BASE, MINI_APP_URL
from keyboards import force_join_kb, main_menu_kb
from locales import get as t

log = logging.getLogger(__name__)
router = Router()


async def _is_member(bot, user_id: int) -> bool:
    """Return True if user is a member of both channel and group."""
    try:
        ch = await bot.get_chat_member(CHANNEL_ID, user_id)
        gr = await bot.get_chat_member(GROUP_ID, user_id)
        ok_statuses = ("member", "administrator", "creator")
        return ch.status in ok_statuses and gr.status in ok_statuses
    except Exception as e:
        log.warning("Membership check failed: %s", e)
        return False  # fail safe — require join


async def send_main_menu(message: Message | CallbackQuery, lang: str):
    """Send (or edit) the main menu message."""
    stock = await db.get_stock_count()
    links_sold_db = await db.get_total_links_sold()
    links_sold = LINKS_SOLD_COUNTER_BASE + links_sold_db

    if isinstance(message, Message):
        user = message.from_user
        name = user.first_name or "there"
        text = t(lang, "welcome", name=name, links_sold=f"{links_sold:,}", stock=stock)
        await message.answer(text, reply_markup=main_menu_kb(lang, MINI_APP_URL), parse_mode="HTML")
    else:
        # CallbackQuery — edit existing message
        user = message.from_user
        name = user.first_name or "there"
        text = t(lang, "welcome", name=name, links_sold=f"{links_sold:,}", stock=stock)
        await message.message.edit_text(text, reply_markup=main_menu_kb(lang, MINI_APP_URL), parse_mode="HTML")


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    user = message.from_user
    lang = "en"

    # Handle referral parameter: /start ref_<user_id>
    referrer_id = None
    if command.args and command.args.startswith("ref_"):
        try:
            referrer_id = int(command.args[4:])
            if referrer_id == user.id:
                referrer_id = None  # can't refer yourself
        except ValueError:
            pass

    # Register/update user
    is_new = await db.upsert_user(user.id, user.username, user.first_name or "", referrer_id)

    # Create referral record if applicable
    if is_new and referrer_id:
        await db.create_referral(referrer_id, user.id)

    # Load saved language
    db_user = await db.get_user(user.id)
    if db_user:
        lang = db_user["language"]

    # Force-join check
    member = await _is_member(message.bot, user.id)
    if not member:
        text = t(lang, "force_join_title", channel_link=CHANNEL_LINK, group_link=GROUP_LINK)
        await message.answer(text, reply_markup=force_join_kb(lang), parse_mode="HTML")
        return

    await send_main_menu(message, lang)


@router.callback_query(F.data == "check_join")
async def cb_check_join(callback: CallbackQuery):
    user = callback.from_user
    db_user = await db.get_user(user.id)
    lang = db_user["language"] if db_user else "en"

    member = await _is_member(callback.bot, user.id)
    if not member:
        await callback.answer(t(lang, "force_join_not_member"), show_alert=True)
        return

    await callback.answer("✅ Verified!", show_alert=False)
    await send_main_menu(callback, lang)


@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery):
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"
    await send_main_menu(callback, lang)
