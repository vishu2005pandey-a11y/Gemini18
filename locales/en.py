"""English locale strings."""

STRINGS = {
    # ── Welcome / Force Join ──────────────────────────────────────────────
    "force_join_title": (
        "👋 <b>Welcome to Alpha Shop!</b>\n\n"
        "🔐 <b>Please join our community to continue:</b>\n\n"
        "📢 <b>Channel:</b> <a href='{channel_link}'>Alpha Official</a>\n"
        "💬 <b>Group:</b> <a href='{group_link}'>Alpha Community</a>\n\n"
        "✅ <i>After joining, tap <b>\"I Joined\"</b> below.</i>"
    ),
    "force_join_not_member": (
        "⚠️ <b>Access Denied</b>\n\n"
        "You haven't joined our channel and group yet.\n"
        "Please join both and try again."
    ),
    "btn_join_channel": "📢 Join Channel",
    "btn_join_group": "💬 Join Group",
    "btn_i_joined": "✅ I Joined — Continue",

    # ── Main Menu ─────────────────────────────────────────────────────────
    "welcome": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ <b>ALPHA SHOP</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Hey {name}! 👋\n\n"
        "✨ <b>Premium digital products — lowest prices.</b>\n"
        "Fast • Secure • Fully Automated\n\n"
        "┌──────────────────────────\n"
        "│ 🛍️  <b>Shop</b> — Browse & buy products\n"
        "│ 👤  <b>Profile</b> — Your stats & history\n"
        "│ 🔗  <b>Referral</b> — Invite & earn rewards\n"
        "│ 🆘  <b>Support</b> — Get help\n"
        "└──────────────────────────\n\n"
        "📊 <b>{links_sold}+</b> links sold  •  <b>{stock}</b> in stock\n\n"
        "Choose an option below 👇"
    ),
    "btn_shop": "🛍️  Shop",
    "btn_profile": "👤  My Profile",
    "btn_orders": "📦  My Orders",
    "btn_referral": "🔗  Refer & Earn",
    "btn_support": "🆘  Support",
    "btn_leaderboard": "🏆  Leaderboard",
    "btn_reviews": "⭐  Reviews",
    "btn_back": "◀️  Back",
    "btn_main_menu": "🏠  Main Menu",

    # ── Shop / Product ────────────────────────────────────────────────────
    "shop_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🛍️ <b>ALPHA SHOP</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌟 <b>Featured Product</b>\n\n"
    ),
    "product_card": (
        "╔══════════════════════════╗\n"
        "  🤖 <b>{name}</b>\n"
        "╚══════════════════════════╝\n\n"
        "📋 <b>Description:</b>\n"
        "  Premium Gemini AI Pro access for 18 months.\n"
        "  Instant delivery via redemption link.\n\n"
        "💰 <b>Price:</b>  <code>${price}</code> per link\n"
        "📦 <b>Stock:</b>  <code>{stock}</code> available\n"
        "📊 <b>Sold:</b>   <code>{sold}+</code> links\n\n"
        "⭐ <b>Rating:</b> {rating} ({review_count} reviews)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Select quantity 👇"
    ),
    "out_of_stock": "❌ <b>Out of Stock</b>\n\nWe're restocking soon. Enable stock alerts in your profile to get notified!",
    "btn_buy_1": "1× Link — ${price}",
    "btn_buy_3": "3× Links — ${price}",
    "btn_buy_5": "5× Links — ${price}",
    "btn_buy_10": "10× Links — ${price}",
    "btn_custom_qty": "✏️  Custom Quantity",

    # ── Terms & Conditions ────────────────────────────────────────────────
    "terms": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📜 <b>TERMS & CONDITIONS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚠️ <b>Important — Please Read Carefully</b>\n\n"
        "✅ This warranty is <b>strictly for the Gemini links</b> themselves and is valid for <b>24 hours only</b> from the time of delivery.\n\n"
        "📌 This warranty covers <b>link activation only</b>, not the subscription duration after it has been successfully redeemed.\n\n"
        "🚫 <b>No replacements</b> will be provided after the 24-hour window.\n\n"
        "⏰ Kindly check and activate your links <b>within the time frame</b>.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "By proceeding you agree to these terms."
    ),
    "btn_agree": "✅  Agree & Continue",
    "btn_decline": "❌  Decline",

    # ── Payment ───────────────────────────────────────────────────────────
    "payment_invoice": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💳 <b>PAYMENT INVOICE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🛒 <b>Order Summary</b>\n"
        "  📦 Product:   {product}\n"
        "  🔢 Quantity:  {qty}× link(s)\n"
        "  💰 Total:     <code>${total}</code>\n\n"
        "💳 <b>Payment Details</b>\n"
        "  💱 Currency:  {currency}\n"
        "  🔑 Amount:    <code>{crypto_amount} {currency}</code>\n"
        "  📋 Address:   <code>{address}</code>\n\n"
        "⏳ <b>Expires in:</b> {timeout} minutes\n"
        "🆔 <b>Order ID:</b>  <code>{order_id}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ Send exact amount to the address above.\n"
        "Delivery is instant after confirmation."
    ),
    "btn_check_payment": "🔄  Check Payment",
    "btn_cancel_payment": "❌  Cancel Order",
    "payment_pending": "⏳ Payment not confirmed yet. Please send the exact amount and check again.",
    "payment_expired": "⌛ <b>Payment Expired</b>\n\nYour invoice has expired. Please place a new order.",
    "payment_cancelled": "❌ Order cancelled.",

    # ── Delivery ──────────────────────────────────────────────────────────
    "delivery_success": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ <b>PAYMENT CONFIRMED!</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎉 Thank you for your purchase!\n\n"
        "📦 <b>Your Gemini Pro Links:</b>\n\n"
        "{links}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⏰ <b>Warranty:</b> 24 hours from now\n"
        "🆔 <b>Order ID:</b> <code>{order_id}</code>\n\n"
        "⚠️ Activate your links within 24 hours!\n"
        "💬 Issues? Use /support"
    ),

    # ── Profile ───────────────────────────────────────────────────────────
    "profile": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👤 <b>MY PROFILE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🪪 <b>User ID:</b>       <code>{user_id}</code>\n"
        "📅 <b>Member Since:</b>  {join_date}\n"
        "🏅 <b>Badge:</b>         {badge}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>Statistics</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📦 <b>Total Orders:</b>   {total_orders}\n"
        "🔗 <b>Links Bought:</b>   {links_bought}\n"
        "💰 <b>Total Spent:</b>    <code>${total_spent}</code>\n"
        "🎁 <b>Referral Earn:</b>  <code>${referral_earnings}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏆 <b>Achievements</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "{achievements}\n\n"
        "🔔 <b>Notifications:</b>  {notifications}"
    ),
    "btn_toggle_notifications": "🔔  Notifications",
    "btn_change_language": "🌐  Language",

    # ── Orders ────────────────────────────────────────────────────────────
    "orders_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📦 <b>ORDER HISTORY</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "You have <b>{count}</b> order(s).\n\n"
    ),
    "order_item": (
        "🆔 <code>{order_id}</code>\n"
        "📅 {date}  •  🔢 {qty}×  •  💰 ${amount}\n"
        "─────────────────────────\n"
    ),
    "no_orders": "📭 You haven't made any purchases yet.\n\nHead to 🛍️ Shop to get started!",
    "btn_search_order": "🔍  Search Order",

    # ── Referral ──────────────────────────────────────────────────────────
    "referral_dashboard": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔗 <b>REFER & EARN</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💸 Earn <b>${reward}</b> for every friend who makes their first purchase!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 <b>Your Stats</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👥 <b>Total Invited:</b>      {total_invited}\n"
        "✅ <b>Successful:</b>         {successful}\n"
        "⏳ <b>Pending:</b>            {pending}\n"
        "💰 <b>Total Earnings:</b>     <code>${total_earnings}</code>\n"
        "💵 <b>Available Balance:</b>  <code>${available_balance}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔗 <b>Your Invite Link:</b>\n"
        "<code>{referral_link}</code>\n\n"
        "<i>⚡ Rewards are credited only after your friend's first purchase.</i>"
    ),
    "btn_copy_link": "📋  Copy Link",
    "btn_withdraw": "💸  Withdraw Earnings",

    # ── Leaderboard ───────────────────────────────────────────────────────
    "leaderboard_weekly": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏆 <b>WEEKLY TOP BUYERS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🕐 Updated: {updated}"
    ),
    "leaderboard_monthly": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📅 <b>MONTHLY TOP BUYERS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🕐 Updated: {updated}"
    ),
    "leaderboard_alltime": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👑 <b>ALL-TIME TOP BUYERS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🕐 Updated: {updated}"
    ),
    "leaderboard_entry": "{rank}  {username}   🔗 {links} links",
    "btn_weekly": "📅  Weekly",
    "btn_monthly": "🗓️  Monthly",
    "btn_alltime": "👑  All-Time",

    # ── Reviews ───────────────────────────────────────────────────────────
    "reviews_header": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⭐ <b>REVIEWS</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Average: <b>{avg_rating}</b>/5  ({count} reviews)\n\n"
        "{reviews}"
    ),
    "review_item": "⭐ {stars}  •  {username}\n<i>{comment}</i>\n─────────────────\n",
    "leave_review_prompt": "⭐ <b>Leave a Review</b>\n\nRate your purchase from 1 to 5 stars:",
    "btn_leave_review": "⭐  Leave a Review",
    "review_saved": "✅ Thank you for your review!",

    # ── Support ───────────────────────────────────────────────────────────
    "support": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🆘 <b>SUPPORT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Need help? We're here for you.\n\n"
        "📋 <b>Order issue?</b>  Use /search to find your order.\n"
        "💬 <b>Live support:</b> Contact an admin in the group.\n\n"
        "<i>Please include your Order ID when contacting support.</i>"
    ),

    # ── Maintenance ───────────────────────────────────────────────────────
    "maintenance": (
        "🔧 <b>Maintenance Mode</b>\n\n"
        "We're currently updating the bot.\n"
        "Please check back shortly.\n\n"
        "<i>We apologize for the inconvenience.</i>"
    ),

    # ── Notifications ─────────────────────────────────────────────────────
    "notifications_menu": (
        "🔔 <b>Notification Settings</b>\n\n"
        "Toggle notifications below:"
    ),
    "notif_stock": "📦 Stock Alerts",
    "notif_announcements": "📢 Announcements",
    "notif_discounts": "🏷️ Discount Alerts",

    # ── Admin ─────────────────────────────────────────────────────────────
    "admin_panel": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ <b>ADMIN PANEL</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👥 <b>Users:</b>         {total_users}\n"
        "📦 <b>Orders:</b>        {total_orders}\n"
        "💰 <b>Revenue:</b>       <code>${total_revenue}</code>\n"
        "📈 <b>Today:</b>         <code>${today_revenue}</code>\n"
        "🔗 <b>Links Sold:</b>    {links_sold}\n"
        "📊 <b>Stock:</b>         {stock} remaining\n\n"
        "Choose an action 👇"
    ),
    "btn_upload_stock": "📤  Upload Stock",
    "btn_set_price": "💲  Set Price",
    "btn_broadcast": "📢  Broadcast",
    "btn_ban_user": "🚫  Ban User",
    "btn_unban_user": "✅  Unban User",
    "btn_view_users": "👥  View Users",
    "btn_view_sales": "📊  View Sales",
    "btn_maintenance": "🔧  Maintenance",
    "btn_referral_settings": "🎁  Referral Settings",

    # ── Purchase Log (sent to admin group) ────────────────────────────────
    "purchase_log": (
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🛒 <b>NEW PURCHASE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👤 <b>User:</b>     @{username} (<code>{user_id}</code>)\n"
        "🆔 <b>Order ID:</b>  <code>{order_id}</code>\n"
        "🔢 <b>Quantity:</b>  {qty}× link(s)\n"
        "💰 <b>Amount:</b>    <code>${amount}</code>\n"
        "💱 <b>Method:</b>    {method}\n"
        "📅 <b>Date:</b>      {date}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),

    # ── Low stock alert ───────────────────────────────────────────────────
    "low_stock_alert": (
        "⚠️ <b>LOW STOCK ALERT</b>\n\n"
        "Only <b>{stock}</b> links remaining!\n"
        "Please upload more stock."
    ),

    # ── Misc ──────────────────────────────────────────────────────────────
    "error_generic": "❌ Something went wrong. Please try again.",
    "banned": "🚫 You have been banned from using this bot.",
    "custom_qty_prompt": "✏️ Enter the quantity you want to buy (1–100):",
    "invalid_qty": "❌ Invalid quantity. Please enter a number between 1 and 100.",
    "insufficient_stock": "❌ Not enough stock. Only {stock} link(s) available.",
    "language_menu": "🌐 <b>Select Language</b>",
    "btn_lang_en": "🇬🇧 English",
    "btn_lang_es": "🇪🇸 Español",
    "search_prompt": "🔍 Enter your Order ID to search:",
    "order_not_found": "❌ Order <code>{order_id}</code> not found.",
    "upload_stock_prompt": "📤 Send a .txt file with one redemption link per line.",
    "stock_uploaded": "✅ Uploaded <b>{count}</b> new links.\n📊 Total stock: <b>{total}</b>",
    "price_set": "✅ Price updated to <code>${price}</code> per link.",
    "broadcast_prompt": "📢 Type your broadcast message:",
    "broadcast_sent": "✅ Broadcast sent to <b>{count}</b> users.",
    "ban_prompt": "🚫 Enter the User ID to ban:",
    "ban_success": "✅ User <code>{user_id}</code> has been banned.",
    "unban_prompt": "✅ Enter the User ID to unban:",
    "unban_success": "✅ User <code>{user_id}</code> has been unbanned.",
    "maintenance_on": "🔧 Maintenance mode <b>enabled</b>.",
    "maintenance_off": "✅ Maintenance mode <b>disabled</b>.",
    "achievement_unlocked": "🏆 <b>Achievement Unlocked!</b>\n\n{label}",
    "new_badge": "🎖️ <b>New Badge!</b>\n\nYou've earned: {badge}",
    "set_price_prompt": "💲 Enter new price per link (USD):",
}
