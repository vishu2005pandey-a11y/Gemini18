"""
Shop / Purchase flow handler.
Payment: Direct on-chain USDT (BSC BEP20 or ETH ERC20)
Verified via BSCScan / Etherscan API — zero fees.
"""
import logging
import time
from datetime import datetime
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
import payments as pay
from config import PAYMENT_TIMEOUT_MINUTES, PRODUCT_NAME, ADMIN_LOG_GROUP_ID, MINI_APP_URL
from keyboards import shop_kb, terms_kb, after_purchase_kb, back_kb
from locales import get as t
from locales.en import (
    E_CHECK, E_CROSS, E_WARNING, E_FIRE, E_DIAMOND, E_TROPHY,
    E_LIGHTNING, E_MONEY, E_CART, E_PACKAGE, E_SHIELD, E_STAR,
    E_GIFT, E_CLOCK, E_CHART, E_KEY,
)

log = logging.getLogger(__name__)
router = Router()


class BuyStates(StatesGroup):
    waiting_custom_qty = State()


# ─────────────────────────────────────────────────────────────────────────────
# Shop menu
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "shop")
async def cb_shop(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    products = await db.get_products()
    stock_map = await db.get_stock_map()
    
    from keyboards import shop_product_list_kb
    text = t(lang, "shop_header") + t(lang, "shop_list_header")
    
    await callback.message.edit_text(
        text,
        reply_markup=shop_product_list_kb(lang, products, stock_map),
        parse_mode="HTML"
    )
    await callback.answer()

async def send_product_card(message: Message | CallbackQuery, lang: str, prod_id: int):
    product = await db.get_product(prod_id)
    if not product:
        if isinstance(message, CallbackQuery):
            await message.answer("Product not found.", show_alert=True)
        else:
            await message.answer("Product not found.")
        return

    stock_map = await db.get_stock_map()
    stock = stock_map.get(prod_id, 0)
    
    total_sold = await db.get_total_links_sold()
    avg_rating, review_count = await db.get_avg_rating()

    stars = "⭐" * round(avg_rating) if avg_rating else "☆☆☆☆☆"
    text = t(lang, "shop_header") + t(
        lang, "product_card",
        name=product["name"],
        price=f"{product['price']:.2f}",
        stock=stock,
        sold=f"{total_sold:,}",
        rating=stars,
        review_count=review_count,
        description=product["description"] or ""
    )
    from keyboards import product_detail_kb
    kb = product_detail_kb(lang, prod_id, product["price"], in_stock=stock > 0)
    
    if isinstance(message, CallbackQuery):
        await message.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        await message.answer()
    else:
        await message.answer(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("view_prod:"))
async def cb_view_prod(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    prod_id = int(callback.data.split(":")[1])
    await send_product_card(callback, lang, prod_id)

# ─────────────────────────────────────────────────────────────────────────────
# Buy — quantity selection
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("buy:"))
async def cb_buy(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    parts = callback.data.split(":")
    if len(parts) == 3:
        # Multi-product format: buy:prod_id:qty
        prod_id = int(parts[1])
        qty_str = parts[2]
    else:
        # Legacy format: buy:qty
        prod_id = 1
        qty_str = parts[1]

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
    prod_id = data.get("buy_prod_id", 1)

    try:
        qty = int(message.text.strip())
        if not 1 <= qty <= 100:
            raise ValueError
    except ValueError:
        await message.answer(t(lang, "invalid_qty"), parse_mode="HTML")
        return

    await state.clear()
    stock_map = await db.get_stock_map()
    stock = stock_map.get(prod_id, 0)
    
    if qty > stock:
        await message.answer(t(lang, "insufficient_stock", stock=stock), parse_mode="HTML")
        return
    
    product = await db.get_product(prod_id)
    if not product:
        return
        
    await message.answer(
        t(lang, "terms"),
        reply_markup=terms_kb(lang, f"{prod_id}:{qty}"),
        parse_mode="HTML"
    )


async def _show_terms(callback: CallbackQuery, lang: str, prod_id: int, qty: int):
    stock_map = await db.get_stock_map()
    stock = stock_map.get(prod_id, 0)
    if qty > stock:
        await callback.message.edit_text(
            t(lang, "insufficient_stock", stock=stock),
            reply_markup=back_kb(lang, f"view_prod:{prod_id}"),
            parse_mode="HTML"
        )
        return
    
    # Send custom payload to agree callback containing prod_id and qty
    # Using keyboards.py terms_kb which takes qty string, so we'll pass prod_id:qty as the 'qty' param
    await callback.message.edit_text(
        t(lang, "terms"),
        reply_markup=terms_kb(lang, f"{prod_id}:{qty}"),
        parse_mode="HTML"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Terms agreed — network selection
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("agree:"))
async def cb_agree(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    parts = callback.data.split(":")
    qty = int(parts[-1])

    price = await db.get_price()
    total = round(price * qty, 2)
    usdt_amount = pay.usd_to_usdt(total)

    # Premium animated emojis for networks (message text only)
    TRON_E    = '<tg-emoji emoji-id="5413589900450625318">🔴</tg-emoji>'
    TRX_E     = '<tg-emoji emoji-id="5391239186994967770">🔥</tg-emoji>'
    BNB_E     = '<tg-emoji emoji-id="5388622778817589921">🟡</tg-emoji>'
    BNB_E2    = '<tg-emoji emoji-id="5397895634684490738">💛</tg-emoji>'
    ETH_E     = E_DIAMOND
    GEMINI_E  = '<tg-emoji emoji-id="5206660927339924387">🤖</tg-emoji>'

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text=f"Binance Pay — ${total:.2f}",
        callback_data=f"pay_network:BINANCE_PAY:{qty}"
    ))
    builder.row(InlineKeyboardButton(
        text=f"USDT BEP20 (BSC) — ${total:.2f}",
        callback_data=f"pay_network:USDT_BSC:{qty}"
    ))
    builder.row(InlineKeyboardButton(
        text=f"USDT TRC20 (Tron) — ${total:.2f}",
        callback_data=f"pay_network:USDT_TRC20:{qty}"
    ))
    builder.row(InlineKeyboardButton(
        text=f"USDT ERC20 (ETH) — ${total:.2f}",
        callback_data=f"pay_network:USDT_ETH:{qty}"
    ))
    builder.row(InlineKeyboardButton(
        text=t(lang, "btn_back"), callback_data="shop"
    ))

    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CART} <b>SELECT PAYMENT NETWORK</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_PACKAGE} <b>Product:</b> {PRODUCT_NAME}\n"
        f"🔢 <b>Quantity:</b> {qty}× code(s)\n"
        f"{E_MONEY} <b>Total:</b>  <code>{usdt_amount} USDT</code>\n\n"
        f"Choose network 👇\n\n"
        f"{BNB_E} Binance Pay  •  {TRX_E} Tron TRC20  •  {ETH_E} ETH ERC20\n"
        f"{BNB_E2} BSC BEP20"
    )

    try:
        await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    except Exception:
        pass  # message not modified — ignore
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
# Network selected — show payment address
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("pay_network:"))
async def cb_pay_network(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    parts = callback.data.split(":")
    network_key = parts[1]
    qty = int(parts[-1])   # always last element

    price = await db.get_price()
    total = round(price * qty, 2)
    usdt_amount = pay.usd_to_usdt(total)

    # Check for existing pending order
    existing = await db.get_pending_order_for_user(user_id)
    if existing:
        await callback.answer(
            "⏳ You have a pending order. Please complete or cancel it first.",
            show_alert=True
        )
        return

    # Check stock
    stock = await db.get_stock_count()
    if qty > stock:
        try:
            await callback.message.edit_text(
                t(lang, "insufficient_stock", stock=stock),
                reply_markup=back_kb(lang, "shop"),
                parse_mode="HTML"
            )
        except Exception:
            pass
        await callback.answer()
        return

    # Get network info
    net = pay.get_network(network_key)
    wallet = net.get("address", "")
    order_id = pay.generate_order_id()
    created_ts = int(time.time())

    if not wallet:
        await callback.answer(
            f"⚠️ {net['label']} wallet not configured. Contact admin.",
            show_alert=True
        )
        return

    # Save order
    await db.create_order(
        order_id=order_id,
        user_id=user_id,
        qty=qty,
        amount_usd=total,
        payment_id=str(created_ts),
        address=wallet,
        crypto_amount=float(usdt_amount),
        currency=network_key,
        product_id=prod_id,
    )
    # The order schema actually uses product_id if available, let's just make sure it creates.
    # Note: create_order needs updating if it doesn't take product_id yet, but for now it defaults to 1.

    # Build invoice message
    network_icon = "🟡" if network_key == "USDT_BSC" else "🔷"
    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_MONEY} <b>PAYMENT INVOICE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_CART} <b>Product:</b>  {PRODUCT_NAME}\n"
        f"🔢 <b>Quantity:</b> {qty}× link(s)\n"
        f"{E_MONEY} <b>Total:</b>   <code>{usdt_amount} USDT</code>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{network_icon} <b>Network:</b>  {net['label']}\n\n"
        f"{E_KEY} <b>Send EXACTLY:</b>\n"
        f"<code>{usdt_amount} USDT</code>\n\n"
        f"📋 <b>To Address:</b>\n"
        f"<code>{wallet}</code>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CLOCK} <b>Expires in:</b> {PAYMENT_TIMEOUT_MINUTES} minutes\n"
        f"🆔 <b>Order ID:</b> <code>{order_id}</code>\n\n"
        f"{E_WARNING} Send EXACT amount. Wrong amount = not detected.\n"
        f"{E_LIGHTNING} After sending, tap <b>Check Payment</b>."
    )

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🔄  Check Payment",
            callback_data=f"check_pay:{order_id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="❌  Cancel Order",
            callback_data=f"cancel_pay:{order_id}"
        )
    )

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
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

    # Verify on-chain
    network_key   = order["currency"]
    usdt_amount   = str(order["crypto_amount"])
    created_ts    = int(order["payment_id"]) if order["payment_id"].isdigit() else 0
    wallet        = order["payment_address"]

    await callback.answer("🔍 Checking blockchain...", show_alert=False)

    confirmed, tx_hash = await pay.verify_payment(
        network_key=network_key,
        wallet=wallet,
        expected_amount_usdt=usdt_amount,
        order_id=order_id,
        created_at_ts=created_ts,
    )

    if confirmed:
        await _deliver_order(callback, order, lang, tx_hash)
    else:
        net = pay.get_network(network_key)
        await callback.answer(
            f"⏳ Payment not found on {net['label']} yet.\n"
            f"Please wait for blockchain confirmation and try again.",
            show_alert=True
        )


async def _deliver_order(callback: CallbackQuery, order, lang: str, tx_hash: str | None = None):
    """Deliver links and complete the order."""
    order_id = order["order_id"]
    user_id  = order["user_id"]
    qty      = order["quantity"]
    prod_id  = dict(order).get("product_id", 1)

    links = await db.pop_links(qty, prod_id)
    if not links:
        await callback.answer(f"{E_CROSS} Out of stock! Contact support.", show_alert=True)
        return

    await db.mark_order_paid(order_id, links)

    formatted_links = "\n".join(f"<code>{i+1}. {link}</code>" for i, link in enumerate(links))
    net = pay.get_network(order["currency"])
    tx_line = f"\n🔗 <b>TX:</b> <a href='{net['explorer']}{tx_hash}'>View on Explorer</a>" if tx_hash else ""

    text = t(lang, "delivery_success", links=formatted_links, order_id=order_id) + tx_line

    from stickers import send_sticker
    await send_sticker(callback.bot, callback.message.chat.id, "success")
    await callback.message.edit_text(
        text,
        reply_markup=after_purchase_kb(lang, order_id),
        parse_mode="HTML"
    )
    await callback.answer(f"{E_CHECK} Payment confirmed!")

    # Post-purchase processing
    user     = await db.get_user(user_id)
    username = (user["username"] or "unknown") if user else "unknown"
    stats    = await db.get_user_stats(user_id)

    # Achievements
    new_ach = await db.check_and_unlock_achievements(user_id, stats["links"])
    for ach_key in new_ach:
        from config import ACHIEVEMENTS
        label = ACHIEVEMENTS[ach_key]["label"]
        try:
            await callback.message.answer(
                t(lang, "achievement_unlocked", label=label), parse_mode="HTML"
            )
        except Exception:
            pass

    # Badge
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
    reward      = await db.get_referral_reward()
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
    await _send_purchase_log(
        callback.bot, user_id, username, order_id, qty,
        order["amount_usd"], net["label"], tx_hash
    )

    # Broadcast to channel/group using broadcaster module
    import broadcaster
    await broadcaster.broadcast_purchase(username, qty, PRODUCT_NAME)


async def _send_purchase_log(bot, user_id: int, username: str, order_id: str,
                              qty: int, amount: float, method: str, tx_hash: str | None):
    if not ADMIN_LOG_GROUP_ID:
        return
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    net_key = method
    tx_line = f"\n🔗 TX: <code>{tx_hash}</code>" if tx_hash else ""
    text = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CART} <b>NEW PURCHASE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>User:</b>     @{username} (<code>{user_id}</code>)\n"
        f"🆔 <b>Order ID:</b>  <code>{order_id}</code>\n"
        f"🔢 <b>Quantity:</b>  {qty}× link(s)\n"
        f"{E_MONEY} <b>Amount:</b>    <code>${amount:.2f}</code>\n"
        f"💱 <b>Method:</b>    {method}\n"
        f"📅 <b>Date:</b>      {now}"
        f"{tx_line}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    try:
        await bot.send_message(ADMIN_LOG_GROUP_ID, text, parse_mode="HTML")
    except Exception as e:
        log.warning("Failed to send purchase log: %s", e)


async def _broadcast_purchase(bot, username: str, qty: int, product_name: str, product_id: int):
    import broadcaster
    await broadcaster.broadcast_purchase(username, qty, product_name, product_id)


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
