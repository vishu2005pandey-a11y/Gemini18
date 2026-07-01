"""English locale strings — with Telegram Premium Emoji (getmodpc pack)."""

# ── Premium Emoji helpers ─────────────────────────────────────────────────────
def _e(emoji_id: str, fallback: str) -> str:
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'

# ── getmodpc pack — real IDs ──────────────────────────────────────────────────
E_LIGHTNING  = _e("6053061091456457277", "⚡️")
E_FIRE       = _e("6053163053980063912", "🔥")
E_STAR       = _e("6053319588358133439", "⭐️")
E_SPARKLES   = _e("6053229479944264545", "✨")
E_DIAMOND    = _e("6053314026375485069", "💎")
E_CROWN      = _e("6052941558221642149", "👑")
E_TROPHY     = _e("6053023136830462029", "🥇")
E_ROCKET     = _e("6052879414339837562", "☄️")
E_MONEY      = _e("6338965051327650313", "💸")
E_CASH       = _e("6053104294532487625", "💵")
E_SHIELD     = _e("6052869252447215120", "🛡")
E_CHART      = _e("6062124099516243830", "📈")
E_CART       = _e("6053214005177095507", "🛍")
E_PACKAGE    = _e("6052991826518873591", "📌")
E_LOCK       = _e("6052921672523061549", "🔒")
E_CHECK      = _e("6053189188856059704", "✅")
E_WAVE       = _e("6339218531707525878", "👍")
E_GIFT       = _e("6053030296540946080", "🎉")
E_LINK       = _e("6052886672834566125", "🔗")
E_KEY        = _e("6052914628776697272", "🔖")
E_BELL       = _e("6053142399482339205", "🔔")
E_MEDAL      = _e("6053065150200552071", "🥈")
E_CLOCK      = _e("6053323501073341449", "⌛")
E_WARNING    = _e("6053315100117309042", "⚠️")
E_CROSS      = _e("6052869226677410910", "❌")
E_CARD       = _e("6053387526150823179", "💱")
E_REVIEW     = _e("6053319588358133439", "⭐️")
E_SUPPORT    = _e("6053367550257928793", "🚨")
E_ROBOT      = _e("6057669453926113105", "🤖")
E_CROWN2     = _e("6052941558221642149", "👑")
E_BRONZE     = _e("6053278382441896611", "🥉")
E_SILVER     = _e("6053065150200552071", "🥈")
E_GOLD       = _e("6053023136830462029", "🥇")
E_SEARCH     = _e("6053117952528493140", "🔍")
E_ANNOUNCE   = _e("6057650440105892655", "📢")
E_REFRESH    = _e("6339131232202267111", "🔄")
E_NEW        = _e("6339306810465327721", "🆕")
E_UP         = _e("6062124099516243830", "📈")
E_BROADCAST  = _e("6057650440105892655", "📢")
E_SETTINGS   = _e("6053063247530039664", "⚙️")
E_BAN        = _e("6052902989415324360", "🚫")
E_INFO       = _e("6053028307971085979", "ℹ️")
E_TARGET     = _e("6052854533594289999", "📍")
E_EXPLOSION  = _e("6052973985224728368", "💥")
E_HUNDRED    = _e("6053175754198358605", "💯")


STRINGS = {
    # ── Welcome / Force Join ─────────────────────────────────────────────
    "force_join_title": (
        f"{E_WAVE} <b>Welcome to Alpha Shop!</b>\n\n"
        f"{E_LOCK} <b>Please join our community to continue:</b>\n\n"
        "📢 <b>Channel:</b> <a href='{channel_link}'>Alpha Official</a>\n"
        "💬 <b>Group:</b> <a href='{group_link}'>Alpha Community</a>\n\n"
        f"{E_CHECK} <i>After joining, tap <b>\"I Joined\"</b> below.</i>"
    ),
    "force_join_not_member": (
        f"{E_WARNING} <b>Access Denied</b>\n\n"
        "You haven't joined our channel and group yet.\n"
        "Please join both and try again."
    ),
    "btn_join_channel": "📢 Join Channel",
    "btn_join_group": "💬 Join Group",
    "btn_i_joined": "✅ I Joined — Continue",

    # ── Main Menu ────────────────────────────────────────────────────────
    "welcome": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_LIGHTNING} <b>ALPHA SHOP</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Hey {{name}}! {E_WAVE}\n\n"
        f"{E_SPARKLES} <b>Premium digital products — lowest prices.</b>\n"
        f"{E_ROCKET} Fast  {E_SHIELD} Secure  {E_CHECK} Fully Automated\n\n"
        "┌──────────────────────────\n"
        f"│ {E_CART}  <b>Shop</b> — Browse & buy products\n"
        f"│ {E_DIAMOND}  <b>Profile</b> — Your stats & history\n"
        f"│ {E_GIFT}  <b>Referral</b> — Invite & earn rewards\n"
        f"│ {E_SUPPORT}  <b>Support</b> — Get help\n"
        "└──────────────────────────\n\n"
        f"{E_CHART} <b>{{links_sold}}+</b> links sold  •  <b>{{stock}}</b> in stock\n\n"
        f"Choose an option below {E_FIRE}"
    ),
    "btn_shop":        "🛍️  Shop",
    "btn_profile":     "👤  My Profile",
    "btn_orders":      "📦  My Orders",
    "btn_referral":    "🔗  Refer & Earn",
    "btn_support":     "🆘  Support",
    "btn_leaderboard": "🏆  Leaderboard",
    "btn_reviews":     "⭐  Reviews",
    "btn_back":        "◀️  Back",
    "btn_main_menu":   "🏠  Main Menu",

    # ── Shop / Product ───────────────────────────────────────────────────
    "shop_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CART} <b>ALPHA SHOP</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_STAR} <b>Featured Product</b>\n\n"
    ),
    "product_card": (
        "╔══════════════════════════╗\n"
        f"  {E_ROBOT} <b>{{name}}</b>\n"
        "╚══════════════════════════╝\n\n"
        f"{E_PACKAGE} <b>Description:</b>\n"
        "  Premium Gemini AI Pro access for 18 months.\n"
        "  Instant delivery via redemption link.\n\n"
        f"{E_MONEY} <b>Price:</b>  <code>${{price}}</code> per link\n"
        f"{E_PACKAGE} <b>Stock:</b>  <code>{{stock}}</code> available\n"
        f"{E_CHART} <b>Sold:</b>   <code>{{sold}}+</code> links\n\n"
        f"{E_STAR} <b>Rating:</b> {{rating}} ({{review_count}} reviews)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Select quantity {E_FIRE}"
    ),
    "out_of_stock": (
        f"{E_CROSS} <b>Out of Stock</b>\n\n"
        "We're restocking soon. Enable stock alerts in your profile!"
    ),
    "btn_buy_1":      "1× Link — ${price}",
    "btn_buy_3":      "3× Links — ${price}",
    "btn_buy_5":      "5× Links — ${price}",
    "btn_buy_10":     "10× Links — ${price}",
    "btn_custom_qty": "✏️  Custom Quantity",

    # ── Terms ────────────────────────────────────────────────────────────
    "terms": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_SHIELD} <b>TERMS & CONDITIONS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_WARNING} <b>Important — Please Read Carefully</b>\n\n"
        f"{E_CHECK} Warranty is <b>strictly for the Gemini links</b> — valid <b>24 hours only</b> from delivery.\n\n"
        f"{E_KEY} Covers <b>link activation only</b>, not subscription duration after redemption.\n\n"
        f"{E_CROSS} <b>No replacements</b> after the 24-hour window.\n\n"
        f"{E_CLOCK} Activate your links <b>within the time frame</b>.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "By proceeding you agree to these terms."
    ),
    "btn_agree":   "✅  Agree & Continue",
    "btn_decline": "❌  Decline",

    # ── Payment ──────────────────────────────────────────────────────────
    "payment_invoice": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CARD} <b>PAYMENT INVOICE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_CART} <b>Order Summary</b>\n"
        "  📦 Product:   {product}\n"
        "  🔢 Quantity:  {qty}× link(s)\n"
        f"  {E_MONEY} Total:     <code>${{total}}</code>\n\n"
        f"{E_CARD} <b>Payment Details</b>\n"
        "  💱 Currency:  {currency}\n"
        f"  {E_KEY} Amount:    <code>{{crypto_amount}} {{currency}}</code>\n"
        "  📋 Address:   <code>{address}</code>\n\n"
        f"{E_CLOCK} <b>Expires in:</b> {{timeout}} minutes\n"
        "🆔 <b>Order ID:</b>  <code>{order_id}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_LIGHTNING} Send exact amount to the address above.\n"
        "Delivery is instant after confirmation."
    ),
    "btn_check_payment":  "🔄  Check Payment",
    "btn_cancel_payment": "❌  Cancel Order",
    "payment_pending":    f"{E_CLOCK} Payment not confirmed yet. Please send exact amount and check again.",
    "payment_expired":    f"{E_CLOCK} <b>Payment Expired</b>\n\nYour invoice has expired. Please place a new order.",
    "payment_cancelled":  f"{E_CROSS} Order cancelled.",

    # ── Delivery ─────────────────────────────────────────────────────────
    "delivery_success": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CHECK} <b>PAYMENT CONFIRMED!</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_SPARKLES} Thank you for your purchase!\n\n"
        f"{E_PACKAGE} <b>Your Gemini Pro Links:</b>\n\n"
        "{links}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CLOCK} <b>Warranty:</b> 24 hours from now\n"
        "🆔 <b>Order ID:</b> <code>{order_id}</code>\n\n"
        f"{E_WARNING} Activate your links within 24 hours!\n"
        f"{E_SUPPORT} Issues? Use /support"
    ),

    # ── Profile ──────────────────────────────────────────────────────────
    "profile": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_DIAMOND} <b>MY PROFILE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🪪 <b>User ID:</b>       <code>{user_id}</code>\n"
        "📅 <b>Member Since:</b>  {join_date}\n"
        f"{E_MEDAL} <b>Badge:</b>         {{badge}}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CHART} <b>Statistics</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_PACKAGE} <b>Total Orders:</b>   {{total_orders}}\n"
        f"{E_LINK} <b>Links Bought:</b>   {{links_bought}}\n"
        f"{E_MONEY} <b>Total Spent:</b>    <code>${{total_spent}}</code>\n"
        f"{E_GIFT} <b>Referral Earn:</b>  <code>${{referral_earnings}}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_TROPHY} <b>Achievements</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "{achievements}\n\n"
        f"{E_BELL} <b>Notifications:</b>  {{notifications}}"
    ),
    "btn_toggle_notifications": "🔔  Notifications",
    "btn_change_language":      "🌐  Language",

    # ── Orders ───────────────────────────────────────────────────────────
    "orders_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_PACKAGE} <b>ORDER HISTORY</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "You have <b>{count}</b> order(s).\n\n"
    ),
    "order_item": (
        "🆔 <code>{order_id}</code>\n"
        "📅 {date}  •  🔢 {qty}×  •  💰 ${amount}\n"
        "─────────────────────────\n"
    ),
    "no_orders": (
        f"{E_PACKAGE} You haven't made any purchases yet.\n\n"
        f"Head to {E_CART} Shop to get started!"
    ),
    "btn_search_order": "🔍  Search Order",

    # ── Referral ─────────────────────────────────────────────────────────
    "referral_dashboard": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_GIFT} <b>REFER & EARN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_MONEY} Earn <b>${{reward}}</b> for every friend who makes their first purchase!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CHART} <b>Your Stats</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👥 <b>Total Invited:</b>      {total_invited}\n"
        f"{E_CHECK} <b>Successful:</b>         {{successful}}\n"
        f"{E_CLOCK} <b>Pending:</b>            {{pending}}\n"
        f"{E_MONEY} <b>Total Earnings:</b>     <code>${{total_earnings}}</code>\n"
        f"{E_DIAMOND} <b>Available Balance:</b> <code>${{available_balance}}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_LINK} <b>Your Invite Link:</b>\n"
        "<code>{referral_link}</code>\n\n"
        f"<i>{E_LIGHTNING} Rewards credited only after friend's first purchase.</i>"
    ),
    "btn_copy_link": "📋  Copy Link",
    "btn_withdraw":  "💸  Withdraw Earnings",

    # ── Leaderboard ──────────────────────────────────────────────────────
    "leaderboard_weekly": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_TROPHY} <b>WEEKLY TOP BUYERS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{{entries}}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CLOCK} Updated: {{updated}}"
    ),
    "leaderboard_monthly": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_STAR} <b>MONTHLY TOP BUYERS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{{entries}}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CLOCK} Updated: {{updated}}"
    ),
    "leaderboard_alltime": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CROWN} <b>ALL-TIME TOP BUYERS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{{entries}}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CLOCK} Updated: {{updated}}"
    ),
    "leaderboard_entry": "{{rank}}  {{username}}   {E_LINK} {{links}} links",
    "btn_weekly":  "📅  Weekly",
    "btn_monthly": "🗓️  Monthly",
    "btn_alltime": "👑  All-Time",

    # ── Reviews ──────────────────────────────────────────────────────────
    "reviews_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_STAR} <b>REVIEWS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Average: <b>{avg_rating}</b>/5  ({count} reviews)\n\n"
        "{reviews}"
    ),
    "review_item":        f"{E_STAR} {{stars}}  •  {{username}}\n<i>{{comment}}</i>\n─────────────────\n",
    "leave_review_prompt": f"{E_STAR} <b>Leave a Review</b>\n\nRate your purchase from 1 to 5 stars:",
    "btn_leave_review":   "⭐  Leave a Review",
    "review_saved":       f"{E_CHECK} Thank you for your review!",

    # ── Support ──────────────────────────────────────────────────────────
    "support": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_SUPPORT} <b>SUPPORT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{E_SHIELD} Need help? We're here for you.\n\n"
        f"{E_PACKAGE} <b>Order issue?</b>  Use /search to find your order.\n"
        "💬 <b>Live support:</b> Contact an admin in the group.\n\n"
        "<i>Please include your Order ID when contacting support.</i>"
    ),

    # ── Maintenance ──────────────────────────────────────────────────────
    "maintenance": (
        f"{E_WARNING} <b>Maintenance Mode</b>\n\n"
        "We're currently updating the bot.\n"
        f"Please check back shortly. {E_CLOCK}\n\n"
        "<i>We apologize for the inconvenience.</i>"
    ),

    # ── Notifications ────────────────────────────────────────────────────
    "notifications_menu": (
        f"{E_BELL} <b>Notification Settings</b>\n\n"
        "Toggle notifications below:"
    ),
    "notif_stock":         "📦 Stock Alerts",
    "notif_announcements": "📢 Announcements",
    "notif_discounts":     "🏷️ Discount Alerts",

    # ── Admin ────────────────────────────────────────────────────────────
    "admin_panel": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ <b>ADMIN PANEL</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 <b>Users:</b>         {{total_users}}\n"
        f"{E_PACKAGE} <b>Orders:</b>        {{total_orders}}\n"
        f"{E_MONEY} <b>Revenue:</b>       <code>${{total_revenue}}</code>\n"
        f"{E_CHART} <b>Today:</b>         <code>${{today_revenue}}</code>\n"
        f"{E_LINK} <b>Links Sold:</b>    {{links_sold}}\n"
        f"{E_CHART} <b>Stock:</b>         {{stock}} remaining\n\n"
        "Choose an action 👇"
    ),
    "btn_upload_stock":     "📤  Upload Stock",
    "btn_set_price":        "💲  Set Price",
    "btn_broadcast":        "📢  Broadcast",
    "btn_ban_user":         "🚫  Ban User",
    "btn_unban_user":       "✅  Unban User",
    "btn_view_users":       "👥  View Users",
    "btn_view_sales":       "📊  View Sales",
    "btn_maintenance":      "🔧  Maintenance",
    "btn_referral_settings":"🎁  Referral Settings",

    # ── Purchase Log ─────────────────────────────────────────────────────
    "purchase_log": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{E_CART} <b>NEW PURCHASE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👤 <b>User:</b>     @{username} (<code>{user_id}</code>)\n"
        "🆔 <b>Order ID:</b>  <code>{order_id}</code>\n"
        f"🔢 <b>Quantity:</b>  {{qty}}× link(s)\n"
        f"{E_MONEY} <b>Amount:</b>    <code>${{amount}}</code>\n"
        "💱 <b>Method:</b>    {method}\n"
        "📅 <b>Date:</b>      {date}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),

    # ── Low stock ────────────────────────────────────────────────────────
    "low_stock_alert": (
        f"{E_WARNING} <b>LOW STOCK ALERT</b>\n\n"
        f"Only <b>{{stock}}</b> links remaining! {E_FIRE}\n"
        "Please upload more stock."
    ),

    # ── Achievements ─────────────────────────────────────────────────────
    "achievement_unlocked": f"{E_TROPHY} <b>Achievement Unlocked!</b>\n\n{{label}}",
    "new_badge":            f"{E_MEDAL} <b>New Badge!</b>\n\nYou've earned: {{badge}}",

    # ── Misc ─────────────────────────────────────────────────────────────
    "error_generic":       f"{E_CROSS} Something went wrong. Please try again.",
    "banned":              "🚫 You have been banned from using this bot.",
    "custom_qty_prompt":   "✏️ Enter the quantity you want to buy (1–100):",
    "invalid_qty":         f"{E_CROSS} Invalid quantity. Please enter a number between 1 and 100.",
    "insufficient_stock":  f"{E_CROSS} Not enough stock. Only {{stock}} link(s) available.",
    "language_menu":       "🌐 <b>Select Language</b>",
    "btn_lang_en":         "🇬🇧 English",
    "btn_lang_es":         "🇪🇸 Español",
    "search_prompt":       "🔍 Enter your Order ID to search:",
    "order_not_found":     f"{E_CROSS} Order <code>{{order_id}}</code> not found.",
    "upload_stock_prompt": f"{E_PACKAGE} Send a .txt file with one redemption link per line.",
    "stock_uploaded":      f"{E_CHECK} Uploaded <b>{{count}}</b> new links.\n{E_CHART} Total stock: <b>{{total}}</b>",
    "price_set":           f"{E_CHECK} Price updated to <code>${{price}}</code> per link.",
    "broadcast_prompt":    "📢 Type your broadcast message:",
    "broadcast_sent":      f"{E_CHECK} Broadcast sent to <b>{{count}}</b> users.",
    "ban_prompt":          "🚫 Enter the User ID to ban:",
    "ban_success":         f"{E_CHECK} User <code>{{user_id}}</code> has been banned.",
    "unban_prompt":        "✅ Enter the User ID to unban:",
    "unban_success":       f"{E_CHECK} User <code>{{user_id}}</code> has been unbanned.",
    "maintenance_on":      f"🔧 Maintenance mode <b>enabled</b>.",
    "maintenance_off":     f"{E_CHECK} Maintenance mode <b>disabled</b>.",
    "set_price_prompt":    f"{E_MONEY} Enter new price per link (USD):",
}
