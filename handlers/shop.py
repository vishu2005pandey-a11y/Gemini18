"""
Shop / Purchase flow handler.
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
import payments as pay
from config import PAYMENT_TIMEOUT_MINUTES, PRODUCT_NAME, ADMIN_IDS, ADMIN_LOG_GROUP_ID
from keyboards import shop_product_list_kb, product_detail_kb, terms_kb, payment_kb, after_purchase_kb, back_kb
from locales import get as t
from locales.en import (
    E_CHECK, E_CROSS, E_WARNING, E_FIRE, E_DIAMOND, E_TROPHY,
    E_LIGHTNING, E_MONEY, E_CART, E_PACKAGE, E_SHIELD, E_CHART,
    E_GIFT, E_STAR, E_BELL, E_CROWN, E_SEARCH, E_ANNOUNCE,
)
from datetime import datetime

log = logging.getLogger(__name__)
router = Router()


class BuyStates(StatesGroup):
    waiting_custom_qty = State()
    waiting_review_comment = State()


# ─────────────────────────────────────────────────────────────────────────────
# Shop menu
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "shop")
async def cb_shop(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    products = await db.get_products()
    stock_map = {}
    for p in products:
        stock_map[p["id"]] = await db.get_stock_count(p["id"])
    
    text = f"{E_CART} <b>Catálogo de productos</b>\n\n{E_CHECK} Entrega automática al instante\n\n⬇️ Elige tu producto:"
    await callback.message.edit_text(
        text,
        reply_markup=shop_product_list_kb(lang, products, stock_map),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("view_prod:"))
async def cb_view_prod(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"
    
    prod_id = int(callback.data.split(":")[1])
    p = await db.get_product(prod_id)
    if not p: return await callback.answer("Product not found.", show_alert=True)
    
    stock = await db.get_stock_count(prod_id)
    sold = p['sold_count'] if 'sold_count' in p.keys() else 123
    
    text = t(lang, "shop_header") + t(
        lang, "product_card",
        name=p['name'],
        price=f"{p['price']:.2f}",
        stock=stock,
        sold=f"{sold:,}",
        rating="⭐⭐⭐⭐⭐",
        review_count=12,
    )
    text = text.replace("Premium Gemini AI Pro access for 18 months.", p['description'] or "")
    
    await callback.message.edit_text(
        text,
        reply_markup=product_detail_kb(lang, prod_id, p['price'], stock > 0),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("buy:"))
async def cb_buy(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    parts = callback.data.split(":")
    prod_id = int(parts[1])
    qty_str = parts[2]

    if qty_str == "custom":
        await callback.message.edit_text(
            t(lang, "custom_qty_prompt"),
            reply_markup=back_kb(lang, f"view_prod:{prod_id}"),
            parse_mode="HTML"
        )
        await state.update_data(buy_prod_id=prod_id)
        await state.set_state(BuyStates.waiting_custom_qty)
        await callback.answer()
        return

    qty = int(qty_str)
    await _show_terms(callback, lang, prod_id, qty)
    await callback.answer()

@router.message(BuyStates.waiting_custom_qty)
async def msg_custom_qty(message: Message, state: FSMContext):
    user_id = message.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    data = await state.get_data()
    prod_id = data.get("buy_prod_id")
    if not prod_id: return
    
    try:
        qty = int(message.text.strip())
        if not 1 <= qty <= 100:
            raise ValueError
    except ValueError:
        await message.answer(t(lang, "invalid_qty"), parse_mode="HTML")
        return

    await state.clear()
    stock = await db.get_stock_count(prod_id)
    if qty > stock:
        await message.answer(t(lang, "insufficient_stock", stock=stock), parse_mode="HTML")
        return

    text = t(lang, "terms")
    await message.answer(text, reply_markup=terms_kb(lang, prod_id, qty), parse_mode="HTML")

async def _show_terms(callback: CallbackQuery, lang: str, prod_id: int, qty: int):
    stock = await db.get_stock_count(prod_id)
    if qty > stock:
        await callback.message.edit_text(
            t(lang, "insufficient_stock", stock=stock),
            reply_markup=back_kb(lang, f"view_prod:{prod_id}"),
            parse_mode="HTML"
        )
        return
    text = t(lang, "terms")
    await callback.message.edit_text(text, reply_markup=terms_kb(lang, prod_id, qty), parse_mode="HTML")


# ─────────────────────────────────────────────────────────────────────────────
# Terms agreed — create invoice
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("agree:"))
async def cb_agree(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    parts = callback.data.split(":")
    prod_id = int(parts[1])
    qty = int(parts[2])

    p = await db.get_product(prod_id)
    price = p['price']
    total = round(price * qty, 2)

    # Check if user has a pending order already
    existing = await db.get_pending_order_for_user(user_id)
    if existing:
        await callback.answer("⏳ You have a pending order. Please complete or cancel it first.", show_alert=True)
        return

    # Check stock
    stock = await db.get_stock_count(prod_id)
    if qty > stock:
        await callback.message.edit_text(
            t(lang, "insufficient_stock", stock=stock),
            reply_markup=back_kb(lang, f"view_prod:{prod_id}"),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    # Create Cryptomus invoice
    order_id = pay.generate_order_id()
    invoice = await pay.create_invoice(
        order_id=order_id,
        amount_usd=total,
        lifetime=PAYMENT_TIMEOUT_MINUTES * 60,
    )

    if not invoice:
        await callback.message.edit_text(
            t(lang, "error_generic"),
            reply_markup=back_kb(lang, "shop"),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    payment_uuid = invoice.get("uuid", "")
    address = invoice.get("address", "N/A")
    crypto_amount = float(invoice.get("payer_amount") or invoice.get("amount") or total)
    currency = invoice.get("payer_currency") or invoice.get("to_currency") or "USDT"
    pay_url = invoice.get("url", "")

    await db.create_order(
        order_id=order_id,
        user_id=user_id,
        product_id=prod_id,
        qty=qty,
        amount_usd=total,
        payment_id=payment_uuid,
        address=address,
        crypto_amount=crypto_amount,
        currency=currency,
    )

    text = t(
        lang, "payment_invoice",
        product=p['name'],
        qty=qty,
        total=f"{total:.2f}",
        currency=currency,
        crypto_amount=crypto_amount,
        address=address,
        timeout=PAYMENT_TIMEOUT_MINUTES,
        order_id=order_id,
    )
    await callback.message.edit_text(
        text,
        reply_markup=payment_kb(lang, order_id, pay_url),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
# Check payment
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("check_pay:"))
async def cb_check_pay(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    order_id = callback.data.split(":", 1)[1]
    order = await db.get_order(order_id)

    if not order:
        await callback.answer(t(lang, "error_generic"), show_alert=True)
        return

    if order["status"] == "paid":
        await callback.answer(f"{E_CHECK} Already delivered!", show_alert=True)
        return

    if order["status"] in ("expired", "cancelled"):
        await callback.message.edit_text(
            t(lang, "payment_expired"),
            reply_markup=back_kb(lang, "shop"),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    # Query Cryptomus
    payment_info = await pay.check_payment(order["payment_id"])
    if not payment_info:
        await callback.answer(t(lang, "payment_pending"), show_alert=True)
        return

    status = payment_info.get("payment_status", "")
    if pay.is_payment_confirmed(status):
        await _deliver_order(callback, order, lang)
    else:
        await callback.answer(t(lang, "payment_pending"), show_alert=True)


async def _deliver_order(callback: CallbackQuery, order, lang: str):
    """Deliver links and complete the order."""
    order_id = order["order_id"]
    user_id = order["user_id"]
    qty = order["quantity"]

    # Pop links atomically
    links = await db.pop_links(qty)
    if not links:
        await callback.answer(f"{E_CROSS} Out of stock! Contact support.", show_alert=True)
        return

    # Mark order paid
    await db.mark_order_paid(order_id, links)

    # Format links for delivery
    formatted_links = "\n".join(f"<code>{i+1}. {link}</code>" for i, link in enumerate(links))

    text = t(lang, "delivery_success", links=formatted_links, order_id=order_id)
    # Send animated sticker before delivery
    from stickers import send_sticker
    await send_sticker(callback.bot, callback.message.chat.id, "success")
    await callback.message.edit_text(
        text,
        reply_markup=after_purchase_kb(lang, order_id),
        parse_mode="HTML"
    )
    await callback.answer(f"{E_CHECK} Payment confirmed!")

    # Post-purchase processing
    user = await db.get_user(user_id)
    username = user["username"] or "unknown" if user else "unknown"
    stats = await db.get_user_stats(user_id)

    # Check and unlock achievements
    new_achievements = await db.check_and_unlock_achievements(user_id, stats["links"])
    for ach_key in new_achievements:
        from config import ACHIEVEMENTS
        label = ACHIEVEMENTS[ach_key]["label"]
        try:
            await callback.message.answer(
                t(lang, "achievement_unlocked", label=label), parse_mode="HTML"
            )
        except Exception:
            pass

    # Badge update notification
    from database import compute_badge
    new_badge = compute_badge(stats["links"])
    old_badge = compute_badge(stats["links"] - qty)
    if new_badge != old_badge:
        try:
            await callback.message.answer(
                t(lang, "new_badge", badge=new_badge), parse_mode="HTML"
            )
        except Exception:
            pass

    # Referral reward
    reward = await db.get_referral_reward()
    referrer_id = await db.reward_referral(user_id, reward)
    if referrer_id:
        try:
            await callback.bot.send_message(
                referrer_id,
                f"{E_GIFT} <b>Referral Reward!</b>\n\n"
                f"Your friend @{username} just made their first purchase.\n"
                f"You earned <code>${reward:.2f}</code>! {E_MONEY}",
                parse_mode="HTML"
            )
        except Exception:
            pass

    # Admin purchase log
    await _send_purchase_log(callback.bot, user_id, username, order_id, qty,
                              order["amount_usd"], order["currency"])

    # Auto-post to channel/group
    await _broadcast_purchase(callback.bot, username, qty)


async def _send_purchase_log(bot, user_id: int, username: str, order_id: str,
                              qty: int, amount: float, method: str):
    from config import ADMIN_LOG_GROUP_ID
    if not ADMIN_LOG_GROUP_ID:
        return
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    text = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CART} <b>NEW PURCHASE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>User:</b>     @{username} (<code>{user_id}</code>)\n"
        f"🆔 <b>Order ID:</b>  <code>{order_id}</code>\n"
        f"🔢 <b>Quantity:</b>  {qty}× link(s)\n"
        f"{E_MONEY} <b>Amount:</b>    <code>${amount:.2f}</code>\n"
        f"💱 <b>Method:</b>    {method}\n"
        f"📅 <b>Date:</b>      {now}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    try:
        await bot.send_message(ADMIN_LOG_GROUP_ID, text, parse_mode="HTML")
    except Exception as e:
        log.warning("Failed to send purchase log: %s", e)


async def _broadcast_purchase(bot, username: str, qty: int):
    from config import CHANNEL_ID, GROUP_ID, PRODUCT_NAME
    import os
    mini_app_url = os.getenv("MINI_APP_URL", "")

    text = (
        f"{E_CART} Someone just bought <b>{qty}×</b> {E_STAR} {PRODUCT_NAME}!\n"
        f"<i>Be the next — tap below!</i>"
    )

    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    from aiogram.utils.keyboard import InlineKeyboardBuilder

    builder = InlineKeyboardBuilder()
    if mini_app_url:
        builder.row(InlineKeyboardButton(
            text="🛍️ Open Mini App",
            web_app={"url": mini_app_url}
        ))
    builder.row(InlineKeyboardButton(
        text=f"🤖 Buy {PRODUCT_NAME}",
        callback_data="shop"
    ))
    kb = builder.as_markup()

    for chat_id in [CHANNEL_ID, GROUP_ID]:
        if chat_id:
            try:
                await bot.send_message(chat_id, text, reply_markup=kb, parse_mode="HTML")
            except Exception as e:
                log.warning("Failed to broadcast purchase to %s: %s", chat_id, e)


# ─────────────────────────────────────────────────────────────────────────────
# Cancel payment
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("cancel_pay:"))
async def cb_cancel_pay(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    order_id = callback.data.split(":", 1)[1]
    await db.mark_order_cancelled(order_id)
    await callback.message.edit_text(
        t(lang, "payment_cancelled"),
        reply_markup=back_kb(lang, "shop"),
        parse_mode="HTML"
    )
    await callback.answer()
