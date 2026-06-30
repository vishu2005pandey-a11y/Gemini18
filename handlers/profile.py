"""
Profile, Orders, Notifications, Language handlers.
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
from database import compute_badge
from config import ACHIEVEMENTS
from keyboards import (
    profile_kb, orders_kb, notifications_kb, language_kb, back_kb
)
from locales import get as t

log = logging.getLogger(__name__)
router = Router()


class SearchStates(StatesGroup):
    waiting_order_id = State()


# ─────────────────────────────────────────────────────────────────────────────
# Profile
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "profile")
@router.message(Command("profile"))
async def cb_profile(event: CallbackQuery | Message):
    if isinstance(event, CallbackQuery):
        user = event.from_user
    else:
        user = event.from_user

    db_user = await db.get_user(user.id)
    lang = db_user["language"] if db_user else "en"

    stats = await db.get_user_stats(user.id)
    badge = compute_badge(stats["links"])
    join_date = db_user["join_date"][:10] if db_user else "N/A"

    # Build achievements string
    unlocked = await db.get_unlocked_achievements(user.id)
    ach_lines = []
    for key, data in ACHIEVEMENTS.items():
        icon = "✅" if key in unlocked else "🔒"
        ach_lines.append(f"{icon} {data['label']}")
    achievements_str = "\n".join(ach_lines) if ach_lines else "No achievements yet."

    # Notifications status
    notif_on = "🔔 ON" if db_user and db_user["notif_stock"] else "🔕 OFF"

    text = t(
        lang, "profile",
        user_id=user.id,
        join_date=join_date,
        badge=badge,
        total_orders=stats["orders"],
        links_bought=stats["links"],
        total_spent=f"{stats['spent']:.2f}",
        referral_earnings=f"{db_user['referral_balance']:.2f}" if db_user else "0.00",
        achievements=achievements_str,
        notifications=notif_on,
    )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=profile_kb(lang), parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(text, reply_markup=profile_kb(lang), parse_mode="HTML")


# ─────────────────────────────────────────────────────────────────────────────
# Orders
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "orders")
@router.message(Command("orders"))
async def cb_orders(event: CallbackQuery | Message):
    if isinstance(event, CallbackQuery):
        user = event.from_user
    else:
        user = event.from_user

    db_user = await db.get_user(user.id)
    lang = db_user["language"] if db_user else "en"

    orders = await db.get_user_orders(user.id)
    if not orders:
        text = t(lang, "no_orders")
    else:
        text = t(lang, "orders_header", count=len(orders))
        for o in orders[:20]:  # show max 20 most recent
            paid_at = o["paid_at"][:10] if o["paid_at"] else "N/A"
            text += t(
                lang, "order_item",
                order_id=o["order_id"],
                date=paid_at,
                qty=o["quantity"],
                amount=f"{o['amount_usd']:.2f}",
            )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=orders_kb(lang), parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(text, reply_markup=orders_kb(lang), parse_mode="HTML")


# ─────────────────────────────────────────────────────────────────────────────
# Search order
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "search_order")
@router.message(Command("search"))
async def cb_search_order(event: CallbackQuery | Message, state: FSMContext):
    if isinstance(event, CallbackQuery):
        user = event.from_user
        db_user = await db.get_user(user.id)
        lang = db_user["language"] if db_user else "en"
        await event.message.edit_text(
            t(lang, "search_prompt"),
            reply_markup=back_kb(lang, "orders"),
            parse_mode="HTML"
        )
        await event.answer()
    else:
        user = event.from_user
        db_user = await db.get_user(user.id)
        lang = db_user["language"] if db_user else "en"
        await event.answer(t(lang, "search_prompt"), parse_mode="HTML")
    await state.set_state(SearchStates.waiting_order_id)


@router.message(SearchStates.waiting_order_id)
async def msg_search_order_id(message: Message, state: FSMContext):
    user_id = message.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    order_id = message.text.strip().upper()
    order = await db.get_order(order_id)

    if not order or order["user_id"] != user_id:
        await message.answer(
            t(lang, "order_not_found", order_id=order_id),
            reply_markup=back_kb(lang, "orders"),
            parse_mode="HTML"
        )
        await state.clear()
        return

    links = await db.get_order_links(order_id)
    links_text = "\n".join(f"<code>{i+1}. {l}</code>" for i, l in enumerate(links)) if links else "<i>No links</i>"
    paid_at = order["paid_at"][:19] if order["paid_at"] else "Pending"

    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔍 <b>ORDER DETAILS</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🆔 <b>Order ID:</b>  <code>{order_id}</code>\n"
        f"📦 <b>Quantity:</b>  {order['quantity']}× links\n"
        f"💰 <b>Amount:</b>    <code>${order['amount_usd']:.2f}</code>\n"
        f"📅 <b>Date:</b>      {paid_at}\n"
        f"✅ <b>Status:</b>    {order['status'].capitalize()}\n\n"
        f"🔗 <b>Links:</b>\n{links_text}"
    )
    await message.answer(text, reply_markup=back_kb(lang, "orders"), parse_mode="HTML")
    await state.clear()


# ─────────────────────────────────────────────────────────────────────────────
# Notifications
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "notifications")
async def cb_notifications(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    text = t(lang, "notifications_menu")
    await callback.message.edit_text(
        text,
        reply_markup=notifications_kb(
            lang,
            stock=bool(db_user["notif_stock"]),
            announce=bool(db_user["notif_announce"]),
            discount=bool(db_user["notif_discount"]),
        ),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("notif_toggle:"))
async def cb_notif_toggle(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    notif_type = callback.data.split(":")[1]
    new_state = await db.toggle_notification(user_id, notif_type)

    # Reload user and re-render
    db_user = await db.get_user(user_id)
    text = t(lang, "notifications_menu")
    await callback.message.edit_text(
        text,
        reply_markup=notifications_kb(
            lang,
            stock=bool(db_user["notif_stock"]),
            announce=bool(db_user["notif_announce"]),
            discount=bool(db_user["notif_discount"]),
        ),
        parse_mode="HTML"
    )
    await callback.answer("✅ Updated!")


# ─────────────────────────────────────────────────────────────────────────────
# Language
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "language")
async def cb_language(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    await callback.message.edit_text(
        t(lang, "language_menu"),
        reply_markup=language_kb(lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_lang:"))
async def cb_set_lang(callback: CallbackQuery):
    user_id = callback.from_user.id
    new_lang = callback.data.split(":")[1]
    await db.set_user_language(user_id, new_lang)
    await callback.answer("✅ Language updated!", show_alert=False)

    # Re-show profile in new language
    db_user = await db.get_user(user_id)
    stats = await db.get_user_stats(user_id)
    badge = compute_badge(stats["links"])
    join_date = db_user["join_date"][:10] if db_user else "N/A"
    unlocked = await db.get_unlocked_achievements(user_id)
    ach_lines = []
    for key, data in ACHIEVEMENTS.items():
        icon = "✅" if key in unlocked else "🔒"
        ach_lines.append(f"{icon} {data['label']}")

    text = t(
        new_lang, "profile",
        user_id=user_id,
        join_date=join_date,
        badge=badge,
        total_orders=stats["orders"],
        links_bought=stats["links"],
        total_spent=f"{stats['spent']:.2f}",
        referral_earnings=f"{db_user['referral_balance']:.2f}",
        achievements="\n".join(ach_lines),
        notifications="🔔 ON" if db_user["notif_stock"] else "🔕 OFF",
    )
    await callback.message.edit_text(text, reply_markup=profile_kb(new_lang), parse_mode="HTML")
