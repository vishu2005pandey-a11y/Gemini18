"""
Admin panel handler — full featured admin controls.
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, Document
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
from config import is_admin, LOW_STOCK_THRESHOLD, CHANNEL_ID, GROUP_ID
from keyboards import admin_kb, back_kb
from locales import get as t

log = logging.getLogger(__name__)
router = Router()


class AdminStates(StatesGroup):
    waiting_stock_file = State()
    waiting_price = State()
    waiting_broadcast = State()
    waiting_ban_id = State()
    waiting_unban_id = State()
    waiting_referral_reward = State()


def _admin_only(func):
    """Decorator to restrict handlers to admins."""
    async def wrapper(event, *args, **kwargs):
        if isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            user_id = event.from_user.id
        if not is_admin(user_id):
            if isinstance(event, CallbackQuery):
                await event.answer("⛔ Admin only.", show_alert=True)
            return
        return await func(event, *args, **kwargs)
    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
# Admin panel entry
# ─────────────────────────────────────────────────────────────────────────────

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        return

    db_user = await db.get_user(message.from_user.id)
    lang = db_user["language"] if db_user else "en"
    await _send_admin_panel(message, lang)


async def _send_admin_panel(event: Message | CallbackQuery, lang: str):
    total_users = await db.get_user_count()
    total_orders = await db.get_total_orders()
    total_revenue = await db.get_total_revenue()
    today_revenue = await db.get_today_revenue()
    links_sold = await db.get_total_links_sold()
    stock = await db.get_stock_count()

    text = t(
        lang, "admin_panel",
        total_users=total_users,
        total_orders=total_orders,
        total_revenue=f"{total_revenue:.2f}",
        today_revenue=f"{today_revenue:.2f}",
        links_sold=links_sold,
        stock=stock,
    )

    if isinstance(event, Message):
        await event.answer(text, reply_markup=admin_kb(lang), parse_mode="HTML")
    else:
        await event.message.edit_text(text, reply_markup=admin_kb(lang), parse_mode="HTML")


@router.callback_query(F.data == "admin:panel")
async def cb_admin_panel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"
    await _send_admin_panel(callback, lang)
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
# Upload stock
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:upload_stock")
async def cb_admin_upload(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"
    await callback.message.edit_text(
        t(lang, "upload_stock_prompt"),
        reply_markup=back_kb(lang, "admin:panel"),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_stock_file)
    await callback.answer()


@router.message(AdminStates.waiting_stock_file, F.document)
async def msg_stock_file(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    db_user = await db.get_user(message.from_user.id)
    lang = db_user["language"] if db_user else "en"

    doc: Document = message.document
    if not doc.file_name.endswith(".txt"):
        await message.answer("❌ Please send a .txt file.")
        return

    file = await message.bot.get_file(doc.file_id)
    file_bytes = await message.bot.download_file(file.file_path)
    content = file_bytes.read().decode("utf-8", errors="ignore")
    links = [l.strip() for l in content.splitlines() if l.strip()]

    added = await db.add_stock(links)
    total = await db.get_stock_count()

    await state.clear()
    await message.answer(
        t(lang, "stock_uploaded", count=added, total=total),
        reply_markup=admin_kb(lang),
        parse_mode="HTML"
    )

    # Low stock check — if we just went from low to restocked, skip alert
    if total <= LOW_STOCK_THRESHOLD:
        await message.answer(t(lang, "low_stock_alert", stock=total), parse_mode="HTML")

    log.info("Admin %s uploaded %d links (total: %d)", message.from_user.id, added, total)


@router.message(AdminStates.waiting_stock_file)
async def msg_stock_file_wrong(message: Message):
    await message.answer("❌ Please send a .txt file.")


# ─────────────────────────────────────────────────────────────────────────────
# Set price
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:set_price")
async def cb_set_price(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"
    current = await db.get_price()
    await callback.message.edit_text(
        t(lang, "set_price_prompt") + f"\n\n<i>Current price: <code>${current:.2f}</code></i>",
        reply_markup=back_kb(lang, "admin:panel"),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_price)
    await callback.answer()


@router.message(AdminStates.waiting_price)
async def msg_set_price(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    db_user = await db.get_user(message.from_user.id)
    lang = db_user["language"] if db_user else "en"

    try:
        price = float(message.text.strip())
        if price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Invalid price. Enter a positive number like 4.99")
        return

    await db.set_price(price)
    await state.clear()
    await message.answer(
        t(lang, "price_set", price=f"{price:.2f}"),
        reply_markup=admin_kb(lang),
        parse_mode="HTML"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Broadcast
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:broadcast")
async def cb_broadcast(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"
    await callback.message.edit_text(
        t(lang, "broadcast_prompt"),
        reply_markup=back_kb(lang, "admin:panel"),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_broadcast)
    await callback.answer()


@router.message(AdminStates.waiting_broadcast)
async def msg_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    db_user = await db.get_user(message.from_user.id)
    lang = db_user["language"] if db_user else "en"

    users = await db.get_all_users()
    sent = 0
    for user in users:
        try:
            await message.bot.send_message(
                user["user_id"], message.text or message.caption or "",
                parse_mode="HTML"
            )
            sent += 1
        except Exception:
            pass

    # Also post to channel and group
    for chat_id in [CHANNEL_ID, GROUP_ID]:
        if chat_id:
            try:
                await message.bot.send_message(chat_id, message.text or "", parse_mode="HTML")
            except Exception:
                pass

    await state.clear()
    await message.answer(
        t(lang, "broadcast_sent", count=sent),
        reply_markup=admin_kb(lang),
        parse_mode="HTML"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Ban / Unban
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:ban")
async def cb_ban(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"
    await callback.message.edit_text(
        t(lang, "ban_prompt"),
        reply_markup=back_kb(lang, "admin:panel"),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_ban_id)
    await callback.answer()


@router.message(AdminStates.waiting_ban_id)
async def msg_ban_id(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    db_user = await db.get_user(message.from_user.id)
    lang = db_user["language"] if db_user else "en"

    try:
        target_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid user ID.")
        return

    await db.ban_user(target_id)
    await state.clear()
    await message.answer(
        t(lang, "ban_success", user_id=target_id),
        reply_markup=admin_kb(lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin:unban")
async def cb_unban(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"
    await callback.message.edit_text(
        t(lang, "unban_prompt"),
        reply_markup=back_kb(lang, "admin:panel"),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_unban_id)
    await callback.answer()


@router.message(AdminStates.waiting_unban_id)
async def msg_unban_id(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    db_user = await db.get_user(message.from_user.id)
    lang = db_user["language"] if db_user else "en"

    try:
        target_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Invalid user ID.")
        return

    await db.unban_user(target_id)
    await state.clear()
    await message.answer(
        t(lang, "unban_success", user_id=target_id),
        reply_markup=admin_kb(lang),
        parse_mode="HTML"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Maintenance toggle
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:toggle_maintenance")
async def cb_toggle_maintenance(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"

    current = await db.is_maintenance()
    await db.set_maintenance(not current)
    new_state = not current
    msg = t(lang, "maintenance_on" if new_state else "maintenance_off")
    await callback.answer(msg, show_alert=True)
    await _send_admin_panel(callback, lang)


# ─────────────────────────────────────────────────────────────────────────────
# View users
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:users")
async def cb_admin_users(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"

    users = await db.get_all_users()
    total = len(users)

    lines = [
        f"👥 <b>Total Users:</b> {total}\n\n"
        f"<i>Last 10 registered:</i>\n"
    ]
    for u in users[-10:]:
        uname = f"@{u['username']}" if u["username"] else f"ID:{u['user_id']}"
        lines.append(f"• {uname} — <code>{u['user_id']}</code>")

    await callback.message.edit_text(
        "\n".join(lines),
        reply_markup=back_kb(lang, "admin:panel"),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
# View sales
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:sales")
async def cb_admin_sales(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"

    total_orders = await db.get_total_orders()
    total_links = await db.get_total_links_sold()
    total_revenue = await db.get_total_revenue()
    today_revenue = await db.get_today_revenue()
    stock = await db.get_stock_count()

    text = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>SALES REPORT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📦 <b>Total Orders:</b>    {total_orders}\n"
        f"🔗 <b>Total Links Sold:</b> {total_links}\n"
        f"💰 <b>Total Revenue:</b>   <code>${total_revenue:.2f}</code>\n"
        f"📈 <b>Today's Revenue:</b> <code>${today_revenue:.2f}</code>\n"
        f"📊 <b>Remaining Stock:</b> {stock} links\n"
    )
    await callback.message.edit_text(
        text,
        reply_markup=back_kb(lang, "admin:panel"),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
# Referral reward settings
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:referral_settings")
async def cb_referral_settings(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Admin only.", show_alert=True)
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"
    current = await db.get_referral_reward()
    await callback.message.edit_text(
        f"🎁 <b>Referral Reward Settings</b>\n\n"
        f"Current reward: <code>${current:.2f}</code> per referral\n\n"
        f"Enter new reward amount (USD):",
        reply_markup=back_kb(lang, "admin:panel"),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_referral_reward)
    await callback.answer()


@router.message(AdminStates.waiting_referral_reward)
async def msg_referral_reward(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    db_user = await db.get_user(message.from_user.id)
    lang = db_user["language"] if db_user else "en"

    try:
        reward = float(message.text.strip())
        if reward < 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Invalid amount.")
        return

    await db.set_setting("referral_reward", str(reward))
    await state.clear()
    await message.answer(
        f"✅ Referral reward updated to <code>${reward:.2f}</code>",
        reply_markup=admin_kb(lang),
        parse_mode="HTML"
    )
