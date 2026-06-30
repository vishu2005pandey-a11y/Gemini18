"""
Referral & leaderboard handlers.
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

import database as db
from keyboards import leaderboard_kb, back_kb
from locales import get as t
from datetime import datetime

log = logging.getLogger(__name__)
router = Router()

RANK_ICONS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def _mask_username(username: str | None, first_name: str | None) -> str:
    if username:
        visible = username[:4] if len(username) > 4 else username
        return f"@{visible}****"
    if first_name:
        visible = first_name[:3] if len(first_name) > 3 else first_name
        return f"{visible}***"
    return "User****"


# ─────────────────────────────────────────────────────────────────────────────
# Referral dashboard
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "referral")
@router.message(Command("referral"))
async def cb_referral(event: CallbackQuery | Message):
    if isinstance(event, CallbackQuery):
        user = event.from_user
    else:
        user = event.from_user

    db_user = await db.get_user(user.id)
    lang = db_user["language"] if db_user else "en"

    stats = await db.get_referral_stats(user.id)
    reward = await db.get_referral_reward()

    # Build referral link using bot username
    try:
        if isinstance(event, CallbackQuery):
            bot_info = await event.bot.get_me()
        else:
            bot_info = await event.bot.get_me()
        bot_username = bot_info.username
    except Exception:
        bot_username = "AlphaShopBot"

    referral_link = f"https://t.me/{bot_username}?start=ref_{user.id}"

    text = t(
        lang, "referral_dashboard",
        reward=f"{reward:.2f}",
        total_invited=stats["total_invited"],
        successful=stats["successful"],
        pending=stats["pending"],
        total_earnings=f"{stats['total_earnings']:.2f}",
        available_balance=f"{stats['available_balance']:.2f}",
        referral_link=referral_link,
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=back_kb(lang), parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(text, reply_markup=back_kb(lang), parse_mode="HTML")


# ─────────────────────────────────────────────────────────────────────────────
# Leaderboard
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("leaderboard:"))
@router.message(Command("leaderboard"))
async def cb_leaderboard(event: CallbackQuery | Message):
    if isinstance(event, CallbackQuery):
        user = event.from_user
        period = event.data.split(":")[1] if ":" in event.data else "alltime"
    else:
        user = event.from_user
        period = "alltime"

    db_user = await db.get_user(user.id)
    lang = db_user["language"] if db_user else "en"

    entries_data = await db.get_leaderboard(period=period, limit=10)
    updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    if entries_data:
        lines = []
        for i, row in enumerate(entries_data):
            rank_icon = RANK_ICONS[i] if i < len(RANK_ICONS) else f"{i+1}."
            masked = _mask_username(row.get("username"), row.get("first_name"))
            lines.append(t(lang, "leaderboard_entry",
                           rank=rank_icon, username=masked, links=row["total_links"]))
        entries_str = "\n".join(lines)
    else:
        entries_str = "<i>No data yet. Make the first purchase!</i>"

    key_map = {
        "weekly": "leaderboard_weekly",
        "monthly": "leaderboard_monthly",
        "alltime": "leaderboard_alltime",
    }
    text = t(lang, key_map.get(period, "leaderboard_alltime"),
             entries=entries_str, updated=updated)

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(
            text,
            reply_markup=leaderboard_kb(lang, active=period),
            parse_mode="HTML"
        )
        await event.answer()
    else:
        await event.answer(
            text,
            reply_markup=leaderboard_kb(lang, active=period),
            parse_mode="HTML"
        )
