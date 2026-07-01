"""
Alpha Bot — Scheduled Tasks
  - Expire old invoices
  - Post leaderboard to channel/group
  - Database backup
  - Low stock alerts
"""
import logging
from datetime import datetime
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import database as db
from config import (
    PAYMENT_TIMEOUT_MINUTES, CHANNEL_ID, GROUP_ID, ADMIN_IDS,
    LOW_STOCK_THRESHOLD, BACKUP_INTERVAL_HOURS
)

log = logging.getLogger(__name__)

RANK_ICONS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def _mask(username, first_name):
    if username:
        v = username[:4] if len(username) > 4 else username
        return f"@{v}****"
    if first_name:
        v = first_name[:3] if len(first_name) > 3 else first_name
        return f"{v}***"
    return "User****"


async def expire_pending_orders(bot=None):
    """Mark orders as expired if they exceed the payment timeout."""
    orders = await db.get_pending_orders_older_than(PAYMENT_TIMEOUT_MINUTES)
    for order in orders:
        await db.mark_order_expired(order["order_id"])
        if bot:
            try:
                user = await db.get_user(order["user_id"])
                lang = user["language"] if user else "en"
                from locales import get as t
                await bot.send_message(
                    order["user_id"],
                    t(lang, "payment_expired"),
                    parse_mode="HTML"
                )
            except Exception:
                pass
    if orders:
        log.info("Expired %d pending orders", len(orders))


async def post_leaderboard(bot, period: str = "weekly"):
    """Build and post the leaderboard to channel and group."""
    entries = await db.get_leaderboard(period=period, limit=10)
    if not entries:
        return

    updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    for i, row in enumerate(entries):
        rank_icon = RANK_ICONS[i] if i < len(RANK_ICONS) else f"{i+1}."
        masked = _mask(row.get("username"), row.get("first_name"))
        lines.append(f"{rank_icon}  {masked}   🔗 {row['total_links']} links")

    title_map = {
        "weekly": "🏆 <b>WEEKLY TOP BUYERS</b>",
        "monthly": "📅 <b>MONTHLY TOP BUYERS</b>",
        "alltime": "👑 <b>ALL-TIME TOP BUYERS</b>",
    }
    title = title_map.get(period, "🏆 <b>TOP BUYERS</b>")

    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{title}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        + "\n".join(lines) +
        f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🕐 Updated: {updated}"
    )

    for chat_id in [CHANNEL_ID, GROUP_ID]:
        if chat_id:
            try:
                await bot.send_message(chat_id, text, parse_mode="HTML")
            except Exception as e:
                log.warning("Failed to post leaderboard to %s: %s", chat_id, e)


async def check_low_stock(bot):
    """Alert admins if stock is running low."""
    stock = await db.get_stock_count()
    if stock <= LOW_STOCK_THRESHOLD:
        text = (
            f"⚠️ <b>LOW STOCK ALERT</b>\n\n"
            f"Only <b>{stock}</b> links remaining!\n"
            f"Please upload more stock."
        )
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(admin_id, text, parse_mode="HTML")
            except Exception:
                pass
        log.warning("Low stock alert sent: %d remaining", stock)


async def database_backup():
    """Back up the database file."""
    await db.backup_database()


async def send_fake_purchase():
    """Send a fake purchase broadcast to the group to build FOMO."""
    log.info("[fake_purchase] Triggered — checking products...")
    try:
        products = await db.get_products()
        if not products:
            log.warning("[fake_purchase] No products found in DB — skipping.")
            return
        
        prod = random.choice(products)
        qty = random.randint(1, 3)
        
        import broadcaster
        from config import GROUP_ID
        log.info("[fake_purchase] GROUP_ID=%s | Sending %sx '%s'", GROUP_ID, qty, prod['name'])
        await broadcaster.broadcast_fake_purchase(qty, prod["name"], prod["id"])
        log.info("[fake_purchase] Done — sent to group.")
    except Exception as e:
        log.error("[fake_purchase] Error: %s", e, exc_info=True)


def setup_scheduler(bot) -> AsyncIOScheduler:
    """Create and configure the APScheduler instance."""
    scheduler = AsyncIOScheduler(timezone="UTC")

    # Expire old invoices — every 2 minutes
    scheduler.add_job(
        expire_pending_orders,
        "interval",
        minutes=2,
        kwargs={"bot": bot},
        id="expire_orders",
    )

    # Post weekly leaderboard — every Monday at 12:00 UTC
    scheduler.add_job(
        post_leaderboard,
        "cron",
        day_of_week="mon",
        hour=12,
        minute=0,
        kwargs={"bot": bot, "period": "weekly"},
        id="leaderboard_weekly",
    )

    # Post monthly leaderboard — 1st of every month at 12:00 UTC
    scheduler.add_job(
        post_leaderboard,
        "cron",
        day=1,
        hour=12,
        minute=0,
        kwargs={"bot": bot, "period": "monthly"},
        id="leaderboard_monthly",
    )

    # Check low stock — every 30 minutes
    scheduler.add_job(
        check_low_stock,
        "interval",
        minutes=30,
        kwargs={"bot": bot},
        id="low_stock_check",
    )

    # Database backup — configurable interval
    scheduler.add_job(
        database_backup,
        "interval",
        hours=BACKUP_INTERVAL_HOURS,
        id="db_backup",
    )

    # Fake purchase broadcast — every 5 minutes (only to group)
    scheduler.add_job(
        send_fake_purchase,
        "interval",
        minutes=5,
        next_run_time=datetime.utcnow(),  # trigger immediately on start
        id="fake_purchase",
    )

    return scheduler
