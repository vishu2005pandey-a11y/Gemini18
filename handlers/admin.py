"""
Admin panel handler — full featured admin controls.
"""
import io
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
from locales.en import E_CHECK, E_CROSS, E_WARNING, E_FIRE, E_DIAMOND, E_TROPHY, E_LIGHTNING, E_MONEY, E_CART, E_PACKAGE, E_SHIELD, E_CHART, E_GIFT, E_STAR, E_BELL, E_CROWN, E_ANNOUNCE, E_SEARCH, E_SETTINGS, E_BAN, E_REFRESH
from locales.en import (
    E_CHECK, E_CROSS, E_WARNING, E_FIRE, E_DIAMOND, E_TROPHY,
    E_LIGHTNING, E_MONEY, E_CART, E_PACKAGE, E_SHIELD, E_CHART,
    E_GIFT, E_STAR, E_BELL, E_CROWN, E_SEARCH, E_ANNOUNCE,
)

log = logging.getLogger(__name__)
router = Router()


class AdminStates(StatesGroup):
    waiting_stock_file = State()
    waiting_price = State()
    waiting_broadcast = State()
    waiting_ban_id = State()
    waiting_unban_id = State()
    waiting_referral_reward = State()
    waiting_product_image = State()
    waiting_product_description = State()


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
    if not is_admin(callback.from_user.id): return
    products = await db.get_products()
    from aiogram.types import InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    for p in products:
        stock = await db.get_stock_count(p['id'])
        builder.row(InlineKeyboardButton(text=f"{p['name']} (Stock: {stock})", callback_data=f"admin:upstock:{p['id']}"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:panel"))
    await callback.message.edit_text("<b>Select Product to Upload Stock:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("admin:upstock:"))
async def cb_admin_upstock(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    prod_id = int(callback.data.split(":")[2])
    await state.update_data(upload_prod_id=prod_id)
    await callback.message.edit_text(
        f"📦 <b>Upload Stock</b>\n\nSend a <b>.txt file</b> with one redemption link per line.",
        reply_markup=back_kb("en", "admin:upload_stock"),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_stock_file)
    await callback.answer()

async def _process_stock_file(message: Message, state: FSMContext):
    """Core logic to process uploaded stock file."""
    if not is_admin(message.from_user.id):
        return

    db_user = await db.get_user(message.from_user.id)
    lang = db_user["language"] if db_user else "en"

    doc = message.document
    if not doc:
        await message.answer(f"{E_CROSS} Please send a .txt file.")
        return

    try:
        file_bytes = io.BytesIO()
        await message.bot.download(doc, destination=file_bytes)
        file_bytes.seek(0)
        content = file_bytes.read().decode("utf-8", errors="ignore")
    except Exception as e:
        log.error("Stock file download error: %s", e)
        await message.answer(f"{E_CROSS} Failed to read file: {e}")
        return

    links = [line.strip() for line in content.splitlines() if line.strip()]

    if not links:
        await message.answer(f"{E_CROSS} File is empty — no links found.")
        return

    data = await state.get_data()
    prod_id = data.get("upload_prod_id", 1)
    added = await db.add_stock(prod_id, links)
    total = await db.get_stock_count(prod_id)

    await state.clear()
    await message.answer(
        f"{E_CHECK} <b>Stock Uploaded!</b>\n\n"
        f"📥 New links added: <b>{added}</b>\n"
        f"📊 Total stock now: <b>{total}</b>",
        reply_markup=admin_kb(lang),
        parse_mode="HTML"
    )

    if 0 < total <= LOW_STOCK_THRESHOLD:
        await message.answer(t(lang, "low_stock_alert", stock=total), parse_mode="HTML")

    log.info("Admin %s uploaded %d links (total: %d)", message.from_user.id, added, total)


@router.message(AdminStates.waiting_stock_file)
async def msg_stock_file(message: Message, state: FSMContext):
    """Handle any message while waiting for stock file."""
    if not is_admin(message.from_user.id):
        return
    if message.document:
        await _process_stock_file(message, state)
    else:
        await message.answer(
            f"{E_WARNING} Please send a <b>.txt file</b> with one link per line.",
            parse_mode="HTML"
        )


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
        await message.answer(f"{E_CROSS} Invalid price. Enter a positive number like 4.99")
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
        await message.answer(f"{E_CROSS} Invalid user ID.")
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
        await message.answer(f"{E_CROSS} Invalid user ID.")
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
        lines.append(f"{E_CHECK} {uname} — <code>{u['user_id']}</code>")

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
        f"{E_CHART} <b>SALES REPORT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_PACKAGE} <b>Total Orders:</b>    {total_orders}\n"
        f"🔗 <b>Total Links Sold:</b> {total_links}\n"
        f"{E_MONEY} <b>Total Revenue:</b>   <code>${total_revenue:.2f}</code>\n"
        f"{E_FIRE} <b>Today's Revenue:</b> <code>${today_revenue:.2f}</code>\n"
        f"{E_CHART} <b>Remaining Stock:</b> {stock} links\n"
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
        await message.answer(f"{E_CROSS} Invalid amount.")
        return

    await db.set_setting("referral_reward", str(reward))
    await state.clear()
    await message.answer(
        f"{E_CHECK} Referral reward updated to <code>${reward:.2f}</code>",
        reply_markup=admin_kb(lang),
        parse_mode="HTML"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Manage Products
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:manage_products")
async def cb_manage_products(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.fromuser_id if hasattr(callback, "fromuser_id") else callback.from_user.id):
        return
    db_user = await db.get_user(callback.from_user.id)
    lang = db_user["language"] if db_user else "en"
    
    products = await db.get_products()
    from aiogram.types import InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    
    for p in products:
        builder.row(InlineKeyboardButton(text=f"{p['name']} - ${p['price']}", callback_data=f"admin:edit_prod:{p['id']}"))
    
    builder.row(InlineKeyboardButton(text="➕ Add Product", callback_data="admin:add_product"))
    builder.row(InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="admin:panel"))
    
    await callback.message.edit_text("<b>Manage Products</b>", reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "admin:add_product")
async def cb_add_product(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    await callback.message.edit_text("Send product name:", reply_markup=back_kb("en", "admin:manage_products"))
    await state.set_state(AdminStates.waiting_product_description)
    await state.update_data(add_step="name")

@router.message(AdminStates.waiting_product_description)
async def msg_product_add_step(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    data = await state.get_data()
    step = data.get("add_step")
    prod_id = data.get("edit_prod_id")
    
    if step == "name":
        await state.update_data(name=message.text)
        await message.answer("Send product price:")
        await state.update_data(add_step="price")
    elif step == "price":
        try:
            price = float(message.text)
            await state.update_data(price=price)
            await message.answer("Send product description:")
            await state.update_data(add_step="desc")
        except ValueError:
            await message.answer("Invalid price.")
    elif step == "desc":
        await state.update_data(desc=message.text)
        await message.answer("Send product image URL (or 'skip' to use none/current, or send a photo):")
        await state.update_data(add_step="image")
    elif step == "image":
        image_url = ""
        text_val = message.text.strip().lower() if message.text else ""
        if message.photo:
            photo = message.photo[-1]
            file = await message.bot.get_file(photo.file_id)
            image_url = f"https://api.telegram.org/file/bot{message.bot.token}/{file.file_path}"
        elif text_val != "skip":
            image_url = message.text

        data = await state.get_data()
        if prod_id:
            if text_val == "skip":
                old_p = await db.get_product(prod_id)
                image_url = old_p['image_url'] if old_p else ""
            await db.update_product(prod_id, data["name"], data["desc"], data["price"], image_url)
            await message.answer("✅ Product updated!", reply_markup=back_kb("en", "admin:manage_products"))
        else:
            await db.add_product(data["name"], data["desc"], data["price"], image_url)
            await message.answer("✅ Product added successfully!", reply_markup=back_kb("en", "admin:manage_products"))
        await state.clear()

@router.callback_query(F.data.startswith("admin:edit_prod:"))
async def cb_edit_prod(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    prod_id = int(callback.data.split(":")[2])
    p = await db.get_product(prod_id)
    if not p: return await callback.answer("Not found", show_alert=True)
    
    from aiogram.types import InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✏️ Edit", callback_data=f"admin:do_edit_prod:{prod_id}"))
    builder.row(InlineKeyboardButton(text="🗑️ Delete", callback_data=f"admin:del_prod:{prod_id}"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:manage_products"))
    
    await callback.message.edit_text(f"<b>{p['name']}</b>\nPrice: ${p['price']}\nDesc: {p['description']}", reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("admin:do_edit_prod:"))
async def cb_do_edit_prod(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    prod_id = int(callback.data.split(":")[2])
    await callback.message.edit_text("Send new product name:", reply_markup=back_kb("en", f"admin:edit_prod:{prod_id}"))
    await state.set_state(AdminStates.waiting_product_description)
    await state.update_data(add_step="name", edit_prod_id=prod_id)
    await callback.answer()

@router.callback_query(F.data.startswith("admin:del_prod:"))
async def cb_del_prod(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    prod_id = int(callback.data.split(":")[2])
    await db.delete_product(prod_id)
    await callback.answer("Product deleted!", show_alert=True)
    
    products = await db.get_products()
    from aiogram.types import InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    for p in products:
        builder.row(InlineKeyboardButton(text=f"{p['name']} - ${p['price']}", callback_data=f"admin:edit_prod:{p['id']}"))
    builder.row(InlineKeyboardButton(text="➕ Add Product", callback_data="admin:add_product"))
    builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="admin:panel"))
    await callback.message.edit_text("<b>Manage Products</b>", reply_markup=builder.as_markup(), parse_mode="HTML")
