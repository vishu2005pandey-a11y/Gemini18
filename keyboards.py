"""
Alpha Bot — All inline keyboard builders.
Every keyboard function accepts a `lang` parameter for i18n.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from locales import get as t
from config import CHANNEL_LINK, GROUP_LINK


# ─────────────────────────────────────────────────────────────────────────────
# Force Join
# ─────────────────────────────────────────────────────────────────────────────

def force_join_kb(lang: str = "en") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_join_channel"), url=CHANNEL_LINK, style="primary"),
        InlineKeyboardButton(text=t(lang, "btn_join_group"), url=GROUP_LINK, style="primary"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_i_joined"), callback_data="check_join", style="success")
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Main Menu
# ─────────────────────────────────────────────────────────────────────────────

def main_menu_kb(lang: str = "en", mini_app_url: str = "") -> InlineKeyboardMarkup:
    from aiogram.types import WebAppInfo
    builder = InlineKeyboardBuilder()

    # ── Mini App button (green — WebApp type) ──────────────────────────
    if mini_app_url:
        builder.row(
            InlineKeyboardButton(
                text="📱  Open Mini App",
                web_app=WebAppInfo(url=mini_app_url),
                style="primary"
            )
        )

    # 🟢 Shop button GREEN 🟢
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_shop"), callback_data="shop", style="success")
    )

    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_profile"), callback_data="profile"),
        InlineKeyboardButton(text=t(lang, "btn_orders"), callback_data="orders"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_referral"), callback_data="referral"),
        InlineKeyboardButton(text=t(lang, "btn_support"), callback_data="support"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_leaderboard"), callback_data="leaderboard:alltime"),
        InlineKeyboardButton(text=t(lang, "btn_reviews"), callback_data="reviews"),
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Shop
# ─────────────────────────────────────────────────────────────────────────────

def shop_product_list_kb(lang: str, products: list, stock_map: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in products:
        pid = p["id"]
        stock = stock_map.get(pid, 0)
        btn_style = "success" if stock > 0 else "danger"
        status_icon = "🟢" if stock > 0 else "🔴"
        status_text = f"{stock} disponibles" if stock > 0 else "Sin stock" # or english
        
        btn_text = f"{p['name']} | ${p['price']:.2f} | {status_icon} {status_text}"
        builder.row(InlineKeyboardButton(text=btn_text, callback_data=f"view_prod:{pid}", style=btn_style))
        
    builder.row(InlineKeyboardButton(text="🔄 Refresh Stock", callback_data="shop"))
    builder.row(InlineKeyboardButton(text="◀️ Main Menu", callback_data="main_menu"))
    return builder.as_markup()

def product_detail_kb(lang: str, product_id: int, price: float, in_stock: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if in_stock:
        builder.row(
            InlineKeyboardButton(
                text=t(lang, "btn_buy_1", price=f"{price:.2f}"),
                callback_data=f"buy:{product_id}:1"
            )
        )
        builder.row(
            InlineKeyboardButton(
                text=t(lang, "btn_buy_3", price=f"{price * 3:.2f}"),
                callback_data=f"buy:{product_id}:3"
            ),
            InlineKeyboardButton(
                text=t(lang, "btn_buy_5", price=f"{price * 5:.2f}"),
                callback_data=f"buy:{product_id}:5"
            ),
        )
        builder.row(
            InlineKeyboardButton(
                text=t(lang, "btn_buy_10", price=f"{price * 10:.2f}"),
                callback_data=f"buy:{product_id}:10"
            ),
            InlineKeyboardButton(
                text=t(lang, "btn_custom_qty"),
                callback_data=f"buy:{product_id}:custom"
            ),
        )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="shop")
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Terms
# ─────────────────────────────────────────────────────────────────────────────

def terms_kb(lang: str = "en", prod_id: int = 1, qty: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_agree"), callback_data=f"agree:{prod_id}:{qty}"),
        InlineKeyboardButton(text=t(lang, "btn_decline"), callback_data="main_menu"),
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Payment
# ─────────────────────────────────────────────────────────────────────────────

def payment_kb(lang: str = "en", order_id: str = "", payment_url: str = "") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if payment_url:
        builder.row(
            InlineKeyboardButton(text="💳  Pay Now", url=payment_url)
        )
    builder.row(
        InlineKeyboardButton(
            text=t(lang, "btn_check_payment"),
            callback_data=f"check_pay:{order_id}"
        ),
        InlineKeyboardButton(
            text=t(lang, "btn_cancel_payment"),
            callback_data=f"cancel_pay:{order_id}"
        ),
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# After purchase
# ─────────────────────────────────────────────────────────────────────────────

def after_purchase_kb(lang: str = "en", order_id: str = "") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=t(lang, "btn_leave_review"),
            callback_data=f"review_start:{order_id}"
        )
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_main_menu"), callback_data="main_menu")
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Profile
# ─────────────────────────────────────────────────────────────────────────────

def profile_kb(lang: str = "en") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=t(lang, "btn_toggle_notifications"),
            callback_data="notifications"
        ),
        InlineKeyboardButton(
            text=t(lang, "btn_change_language"),
            callback_data="language"
        ),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_orders"), callback_data="orders")
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="main_menu")
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Orders
# ─────────────────────────────────────────────────────────────────────────────

def orders_kb(lang: str = "en") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_search_order"), callback_data="search_order")
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="profile")
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Leaderboard
# ─────────────────────────────────────────────────────────────────────────────

def leaderboard_kb(lang: str = "en", active: str = "alltime") -> InlineKeyboardMarkup:
    def _btn(label_key: str, period: str):
        prefix = "▶ " if active == period else ""
        return InlineKeyboardButton(
            text=prefix + t(lang, label_key),
            callback_data=f"leaderboard:{period}"
        )
    builder = InlineKeyboardBuilder()
    builder.row(
        _btn("btn_weekly", "weekly"),
        _btn("btn_monthly", "monthly"),
        _btn("btn_alltime", "alltime"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="main_menu")
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Reviews — star rating
# ─────────────────────────────────────────────────────────────────────────────

def review_stars_kb(order_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(*[
        InlineKeyboardButton(text=f"{'⭐' * i}", callback_data=f"review_rate:{order_id}:{i}")
        for i in range(1, 6)
    ])
    builder.row(
        InlineKeyboardButton(text="❌  Skip", callback_data="main_menu")
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Notifications
# ─────────────────────────────────────────────────────────────────────────────

def notifications_kb(lang: str, stock: bool, announce: bool, discount: bool) -> InlineKeyboardMarkup:
    def _state(val: bool) -> str:
        return "✅" if val else "❌"

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"{_state(stock)} {t(lang, 'notif_stock')}",
            callback_data="notif_toggle:stock"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"{_state(announce)} {t(lang, 'notif_announcements')}",
            callback_data="notif_toggle:announce"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"{_state(discount)} {t(lang, 'notif_discounts')}",
            callback_data="notif_toggle:discount"
        )
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="profile")
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Language selector
# ─────────────────────────────────────────────────────────────────────────────

def start_language_kb(lang: str = "en") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇬🇧 English", callback_data="start_lang:en"),
        InlineKeyboardButton(text="🇪🇸 Español", callback_data="start_lang:es"),
    )
    return builder.as_markup()

def language_kb(lang: str = "en") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_lang_en"), callback_data="set_lang:en"),
        InlineKeyboardButton(text=t(lang, "btn_lang_es"), callback_data="set_lang:es"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="profile")
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Admin panel
# ─────────────────────────────────────────────────────────────────────────────

def admin_kb(lang: str = "en") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_upload_stock"), callback_data="admin:upload_stock"),
        InlineKeyboardButton(text=t(lang, "btn_set_price"), callback_data="admin:set_price"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_broadcast"), callback_data="admin:broadcast"),
        InlineKeyboardButton(text=t(lang, "btn_maintenance"), callback_data="admin:toggle_maintenance"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_ban_user"), callback_data="admin:ban"),
        InlineKeyboardButton(text=t(lang, "btn_unban_user"), callback_data="admin:unban"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_view_users"), callback_data="admin:users"),
        InlineKeyboardButton(text=t(lang, "btn_view_sales"), callback_data="admin:sales"),
    )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_referral_settings"), callback_data="admin:referral_settings"),
    )
    builder.row(
        InlineKeyboardButton(text="Manage Products", callback_data="admin:manage_products"),
    )
    return builder.as_markup()


# ─────────────────────────────────────────────────────────────────────────────
# Generic back button
# ─────────────────────────────────────────────────────────────────────────────

def back_kb(lang: str, target: str = "main_menu") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data=target)
    )
    return builder.as_markup()
