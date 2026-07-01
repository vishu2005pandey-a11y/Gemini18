"""
Alpha Bot — Database Layer (aiosqlite)
All database interactions are centralised here.
"""
import asyncio
import aiosqlite
import logging
import shutil
import os
from datetime import datetime, date, timedelta
from pathlib import Path
from config import DB_PATH, BADGE_THRESHOLDS, ACHIEVEMENTS

log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Schema
# ─────────────────────────────────────────────────────────────────────────────

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS users (
    user_id         INTEGER PRIMARY KEY,
    username        TEXT,
    first_name      TEXT,
    language        TEXT    DEFAULT 'en',
    join_date       TEXT    NOT NULL,
    is_banned       INTEGER DEFAULT 0,
    is_admin        INTEGER DEFAULT 0,
    referrer_id     INTEGER,
    referral_balance REAL   DEFAULT 0.0,
    notif_stock     INTEGER DEFAULT 1,
    notif_announce  INTEGER DEFAULT 1,
    notif_discount  INTEGER DEFAULT 1,
    FOREIGN KEY (referrer_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT,
    price       REAL NOT NULL,
    image_url   TEXT,
    is_active   INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS stock (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER NOT NULL DEFAULT 1,
    link        TEXT    UNIQUE NOT NULL,
    is_sold     INTEGER DEFAULT 0,
    added_at    TEXT    NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id        TEXT    PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    product_id      INTEGER NOT NULL DEFAULT 1,
    quantity        INTEGER NOT NULL,
    amount_usd      REAL    NOT NULL,
    payment_id      TEXT,
    payment_address TEXT,
    crypto_amount   REAL,
    currency        TEXT,
    status          TEXT    DEFAULT 'pending',   -- pending | paid | expired | cancelled
    created_at      TEXT    NOT NULL,
    paid_at         TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    TEXT    NOT NULL,
    product_id  INTEGER NOT NULL DEFAULT 1,
    link        TEXT    NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS referrals (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    referrer_id     INTEGER NOT NULL,
    referred_id     INTEGER NOT NULL UNIQUE,
    rewarded        INTEGER DEFAULT 0,
    created_at      TEXT    NOT NULL,
    rewarded_at     TEXT,
    FOREIGN KEY (referrer_id) REFERENCES users(user_id),
    FOREIGN KEY (referred_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS achievements (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    achievement TEXT    NOT NULL,
    unlocked_at TEXT    NOT NULL,
    UNIQUE(user_id, achievement),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    order_id    TEXT    NOT NULL,
    rating      INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    comment     TEXT,
    created_at  TEXT    NOT NULL,
    UNIQUE(order_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS settings (
    key     TEXT PRIMARY KEY,
    value   TEXT NOT NULL
);

-- Default settings
INSERT OR IGNORE INTO settings (key, value) VALUES ('price', '4.99');
INSERT OR IGNORE INTO settings (key, value) VALUES ('maintenance', 'false');
INSERT OR IGNORE INTO settings (key, value) VALUES ('referral_reward', '0.50');
INSERT OR IGNORE INTO settings (key, value) VALUES ('links_sold_base', '69987');
INSERT OR IGNORE INTO settings (key, value) VALUES ('product_image_url', '');
INSERT OR IGNORE INTO settings (key, value) VALUES ('product_description', 'Premium Gemini AI Pro access for 18 months. Instant delivery via redemption link.');

CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_stock_sold ON stock(is_sold);
CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);
"""

# ─────────────────────────────────────────────────────────────────────────────
# Connection helper
# ─────────────────────────────────────────────────────────────────────────────

_db: aiosqlite.Connection | None = None

async def get_db() -> aiosqlite.Connection:
    global _db
    if _db is None:
        Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
        _db = await aiosqlite.connect(DB_PATH)
        _db.row_factory = aiosqlite.Row
        await _db.executescript(SCHEMA)
        await _db.commit()
        log.info("Database connected: %s", DB_PATH)
    return _db

async def close_db():
    global _db
    if _db:
        await _db.close()
        _db = None

# ─────────────────────────────────────────────────────────────────────────────
# Users
# ─────────────────────────────────────────────────────────────────────────────

async def upsert_user(user_id: int, username: str | None, first_name: str,
                      referrer_id: int | None = None) -> bool:
    """Insert or update user. Returns True if this is a new user."""
    db = await get_db()
    now = datetime.utcnow().isoformat()
    cursor = await db.execute(
        "SELECT user_id FROM users WHERE user_id=?", (user_id,)
    )
    existing = await cursor.fetchone()
    if existing:
        await db.execute(
            "UPDATE users SET username=?, first_name=? WHERE user_id=?",
            (username, first_name, user_id)
        )
        await db.commit()
        return False
    else:
        await db.execute(
            "INSERT INTO users (user_id, username, first_name, join_date, referrer_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, username, first_name, now, referrer_id)
        )
        await db.commit()
        return True

async def get_user(user_id: int) -> aiosqlite.Row | None:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return await cursor.fetchone()

async def get_all_users() -> list[aiosqlite.Row]:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM users WHERE is_banned=0")
    return await cursor.fetchall()

async def get_user_count() -> int:
    db = await get_db()
    cursor = await db.execute("SELECT COUNT(*) FROM users")
    row = await cursor.fetchone()
    return row[0]

async def ban_user(user_id: int):
    db = await get_db()
    await db.execute("UPDATE users SET is_banned=1 WHERE user_id=?", (user_id,))
    await db.commit()

async def unban_user(user_id: int):
    db = await get_db()
    await db.execute("UPDATE users SET is_banned=0 WHERE user_id=?", (user_id,))
    await db.commit()

async def set_user_language(user_id: int, lang: str):
    db = await get_db()
    await db.execute("UPDATE users SET language=? WHERE user_id=?", (lang, user_id))
    await db.commit()

async def toggle_notification(user_id: int, notif_type: str) -> bool:
    """Toggle a notification setting. Returns new state."""
    db = await get_db()
    col_map = {"stock": "notif_stock", "announce": "notif_announce", "discount": "notif_discount"}
    col = col_map.get(notif_type, "notif_stock")
    cursor = await db.execute(f"SELECT {col} FROM users WHERE user_id=?", (user_id,))
    row = await cursor.fetchone()
    new_val = 0 if row[0] else 1
    await db.execute(f"UPDATE users SET {col}=? WHERE user_id=?", (new_val, user_id))
    await db.commit()
    return bool(new_val)

# ─────────────────────────────────────────────────────────────────────────────
# Stock
# ─────────────────────────────────────────────────────────────────────────────

async def add_stock(links: list[str]) -> int:
    """Add links to stock. Returns number of NEW (non-duplicate) links added."""
    db = await get_db()
    now = datetime.utcnow().isoformat()
    added = 0
    for link in links:
        link = link.strip()
        if not link:
            continue
        try:
            await db.execute(
                "INSERT INTO stock (link, added_at) VALUES (?, ?)", (link, now)
            )
            added += 1
        except aiosqlite.IntegrityError:
            pass  # duplicate
    await db.commit()
    return added

async def get_stock_count(product_id: int | None = None) -> int:
    db = await get_db()
    if product_id is not None:
        cursor = await db.execute("SELECT COUNT(*) FROM stock WHERE is_sold=0 AND product_id=?", (product_id,))
    else:
        cursor = await db.execute("SELECT COUNT(*) FROM stock WHERE is_sold=0")
    row = await cursor.fetchone()
    return row[0]

async def get_stock_map() -> dict:
    db = await get_db()
    cursor = await db.execute("SELECT product_id, COUNT(*) FROM stock WHERE is_sold=0 GROUP BY product_id")
    rows = await cursor.fetchall()
    return {r["product_id"]: r[1] for r in rows}

async def pop_links(qty: int, product_id: int = 1) -> list[str]:
    """Atomically fetch and mark `qty` unsold links as sold. Returns the links."""
    db = await get_db()
    cursor = await db.execute(
        "SELECT id, link FROM stock WHERE is_sold=0 AND product_id=? LIMIT ?", (product_id, qty)
    )
    rows = await cursor.fetchall()
    if len(rows) < qty:
        return []
    ids = [r["id"] for r in rows]
    links = [r["link"] for r in rows]
    placeholders = ",".join("?" * len(ids))
    await db.execute(f"UPDATE stock SET is_sold=1 WHERE id IN ({placeholders})", ids)
    await db.commit()
    return links

async def delete_all_stock():
    db = await get_db()
    await db.execute("DELETE FROM stock WHERE is_sold=0")
    await db.commit()

# ─────────────────────────────────────────────────────────────────────────────
# Orders
# ─────────────────────────────────────────────────────────────────────────────

async def create_order(order_id: str, user_id: int, qty: int, amount_usd: float,
                       payment_id: str, address: str, crypto_amount: float,
                       currency: str, product_id: int = 1) -> None:
    db = await get_db()
    now = datetime.utcnow().isoformat()
    await db.execute(
        "INSERT INTO orders (order_id, user_id, product_id, quantity, amount_usd, payment_id, "
        "payment_address, crypto_amount, currency, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (order_id, user_id, product_id, qty, amount_usd, payment_id, address, crypto_amount, currency, now)
    )
    await db.commit()

async def get_order(order_id: str) -> aiosqlite.Row | None:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM orders WHERE order_id=?", (order_id,))
    return await cursor.fetchone()

async def mark_order_paid(order_id: str, links: list[str]) -> None:
    db = await get_db()
    now = datetime.utcnow().isoformat()
    await db.execute(
        "UPDATE orders SET status='paid', paid_at=? WHERE order_id=?", (now, order_id)
    )
    for link in links:
        await db.execute(
            "INSERT INTO order_items (order_id, link) VALUES (?,?)", (order_id, link)
        )
    await db.commit()

async def mark_order_expired(order_id: str):
    db = await get_db()
    await db.execute(
        "UPDATE orders SET status='expired' WHERE order_id=?", (order_id,)
    )
    await db.commit()

async def mark_order_cancelled(order_id: str):
    db = await get_db()
    await db.execute(
        "UPDATE orders SET status='cancelled' WHERE order_id=?", (order_id,)
    )
    await db.commit()

async def get_user_orders(user_id: int) -> list[aiosqlite.Row]:
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM orders WHERE user_id=? AND status='paid' ORDER BY paid_at DESC",
        (user_id,)
    )
    return await cursor.fetchall()

async def get_order_links(order_id: str) -> list[str]:
    db = await get_db()
    cursor = await db.execute(
        "SELECT link FROM order_items WHERE order_id=?", (order_id,)
    )
    rows = await cursor.fetchall()
    return [r["link"] for r in rows]

async def get_total_orders() -> int:
    db = await get_db()
    cursor = await db.execute("SELECT COUNT(*) FROM orders WHERE status='paid'")
    row = await cursor.fetchone()
    return row[0]

async def get_total_links_sold() -> int:
    db = await get_db()
    cursor = await db.execute("SELECT COALESCE(SUM(quantity),0) FROM orders WHERE status='paid'")
    row = await cursor.fetchone()
    return row[0]

async def get_total_revenue() -> float:
    db = await get_db()
    cursor = await db.execute(
        "SELECT COALESCE(SUM(amount_usd),0.0) FROM orders WHERE status='paid'"
    )
    row = await cursor.fetchone()
    return row[0]

async def get_today_revenue() -> float:
    db = await get_db()
    today = date.today().isoformat()
    cursor = await db.execute(
        "SELECT COALESCE(SUM(amount_usd),0.0) FROM orders WHERE status='paid' AND paid_at LIKE ?",
        (f"{today}%",)
    )
    row = await cursor.fetchone()
    return row[0]

async def get_user_stats(user_id: int) -> dict:
    db = await get_db()
    cursor = await db.execute(
        "SELECT COUNT(*) as orders, COALESCE(SUM(quantity),0) as links, "
        "COALESCE(SUM(amount_usd),0.0) as spent "
        "FROM orders WHERE user_id=? AND status='paid'",
        (user_id,)
    )
    row = await cursor.fetchone()
    return dict(row)

async def get_pending_orders_older_than(minutes: int) -> list[aiosqlite.Row]:
    db = await get_db()
    cutoff = (datetime.utcnow() - timedelta(minutes=minutes)).isoformat()
    cursor = await db.execute(
        "SELECT * FROM orders WHERE status='pending' AND created_at < ?", (cutoff,)
    )
    return await cursor.fetchall()

async def get_pending_order_for_user(user_id: int) -> aiosqlite.Row | None:
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM orders WHERE user_id=? AND status='pending' ORDER BY created_at DESC LIMIT 1",
        (user_id,)
    )
    return await cursor.fetchone()

# ─────────────────────────────────────────────────────────────────────────────
# Leaderboard
# ─────────────────────────────────────────────────────────────────────────────

async def get_leaderboard(period: str = "alltime", limit: int = 10) -> list[dict]:
    db = await get_db()
    if period == "weekly":
        start = (datetime.utcnow() - timedelta(days=7)).isoformat()
        where = f"AND o.paid_at >= '{start}'"
    elif period == "monthly":
        start = (datetime.utcnow() - timedelta(days=30)).isoformat()
        where = f"AND o.paid_at >= '{start}'"
    else:
        where = ""
    cursor = await db.execute(f"""
        SELECT u.username, u.first_name, SUM(o.quantity) as total_links
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        WHERE o.status='paid' {where}
        GROUP BY o.user_id
        ORDER BY total_links DESC
        LIMIT ?
    """, (limit,))
    rows = await cursor.fetchall()
    return [dict(r) for r in rows]

# ─────────────────────────────────────────────────────────────────────────────
# Referrals
# ─────────────────────────────────────────────────────────────────────────────

async def create_referral(referrer_id: int, referred_id: int):
    db = await get_db()
    now = datetime.utcnow().isoformat()
    try:
        await db.execute(
            "INSERT INTO referrals (referrer_id, referred_id, created_at) VALUES (?,?,?)",
            (referrer_id, referred_id, now)
        )
        await db.commit()
    except aiosqlite.IntegrityError:
        pass  # already exists

async def reward_referral(referred_id: int, reward_amount: float) -> int | None:
    """Credit referral reward. Returns referrer_id if rewarded, else None."""
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM referrals WHERE referred_id=? AND rewarded=0", (referred_id,)
    )
    row = await cursor.fetchone()
    if not row:
        return None
    referrer_id = row["referrer_id"]
    now = datetime.utcnow().isoformat()
    await db.execute(
        "UPDATE referrals SET rewarded=1, rewarded_at=? WHERE referred_id=?",
        (now, referred_id)
    )
    await db.execute(
        "UPDATE users SET referral_balance = referral_balance + ? WHERE user_id=?",
        (reward_amount, referrer_id)
    )
    await db.commit()
    return referrer_id

async def get_referral_stats(user_id: int) -> dict:
    db = await get_db()
    cursor = await db.execute(
        "SELECT COUNT(*) as total FROM referrals WHERE referrer_id=?", (user_id,)
    )
    total = (await cursor.fetchone())[0]
    cursor = await db.execute(
        "SELECT COUNT(*) as rewarded FROM referrals WHERE referrer_id=? AND rewarded=1",
        (user_id,)
    )
    rewarded = (await cursor.fetchone())[0]
    cursor = await db.execute(
        "SELECT referral_balance FROM users WHERE user_id=?", (user_id,)
    )
    balance_row = await cursor.fetchone()
    balance = balance_row["referral_balance"] if balance_row else 0.0
    return {
        "total_invited": total,
        "successful": rewarded,
        "pending": total - rewarded,
        "total_earnings": balance,
        "available_balance": balance,
    }

# ─────────────────────────────────────────────────────────────────────────────
# Achievements
# ─────────────────────────────────────────────────────────────────────────────

async def get_unlocked_achievements(user_id: int) -> list[str]:
    db = await get_db()
    cursor = await db.execute(
        "SELECT achievement FROM achievements WHERE user_id=?", (user_id,)
    )
    rows = await cursor.fetchall()
    return [r["achievement"] for r in rows]

async def unlock_achievement(user_id: int, achievement: str) -> bool:
    """Returns True if newly unlocked."""
    db = await get_db()
    now = datetime.utcnow().isoformat()
    try:
        await db.execute(
            "INSERT INTO achievements (user_id, achievement, unlocked_at) VALUES (?,?,?)",
            (user_id, achievement, now)
        )
        await db.commit()
        return True
    except aiosqlite.IntegrityError:
        return False

async def check_and_unlock_achievements(user_id: int, links_count: int) -> list[str]:
    """Check all achievement thresholds and unlock new ones. Returns newly unlocked keys."""
    newly_unlocked = []
    for key, data in ACHIEVEMENTS.items():
        if links_count >= data["threshold"]:
            unlocked = await unlock_achievement(user_id, key)
            if unlocked:
                newly_unlocked.append(key)
    return newly_unlocked

# ─────────────────────────────────────────────────────────────────────────────
# Reviews
# ─────────────────────────────────────────────────────────────────────────────

async def add_review(user_id: int, order_id: str, rating: int, comment: str):
    db = await get_db()
    now = datetime.utcnow().isoformat()
    try:
        await db.execute(
            "INSERT INTO reviews (user_id, order_id, rating, comment, created_at) VALUES (?,?,?,?,?)",
            (user_id, order_id, rating, comment, now)
        )
        await db.commit()
    except aiosqlite.IntegrityError:
        pass

async def get_reviews(limit: int = 10) -> list[aiosqlite.Row]:
    db = await get_db()
    cursor = await db.execute(
        "SELECT r.*, u.username FROM reviews r JOIN users u ON r.user_id=u.user_id "
        "ORDER BY r.created_at DESC LIMIT ?", (limit,)
    )
    return await cursor.fetchall()

async def get_avg_rating() -> tuple[float, int]:
    db = await get_db()
    cursor = await db.execute("SELECT AVG(rating), COUNT(*) FROM reviews")
    row = await cursor.fetchone()
    return (round(row[0], 1) if row[0] else 0.0, row[1] or 0)

async def has_reviewed_order(order_id: str) -> bool:
    db = await get_db()
    cursor = await db.execute("SELECT id FROM reviews WHERE order_id=?", (order_id,))
    return bool(await cursor.fetchone())

# ─────────────────────────────────────────────────────────────────────────────
# Settings
# ─────────────────────────────────────────────────────────────────────────────

async def get_setting(key: str) -> str | None:
    db = await get_db()
    cursor = await db.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = await cursor.fetchone()
    return row["value"] if row else None

async def set_setting(key: str, value: str):
    db = await get_db()
    await db.execute(
        "INSERT INTO settings (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value)
    )
    await db.commit()

async def get_price() -> float:
    val = await get_setting("price")
    return float(val) if val else 4.99

async def set_price(price: float):
    await set_setting("price", str(price))

async def is_maintenance() -> bool:
    val = await get_setting("maintenance")
    return val == "true"

async def set_maintenance(enabled: bool):
    await set_setting("maintenance", "true" if enabled else "false")

async def get_referral_reward() -> float:
    val = await get_setting("referral_reward")
    return float(val) if val else 0.50


async def get_product_info() -> dict:
    """Returns product info dict with name, price, stock, sold, rating, reviews, image_url, description."""
    from config import PRODUCT_NAME, LINKS_SOLD_COUNTER_BASE
    price = await get_price()
    stock = await get_stock_count()
    sold_db = await get_total_links_sold()
    sold = LINKS_SOLD_COUNTER_BASE + sold_db
    avg_rating, review_count = await get_avg_rating()
    image_url = await get_setting("product_image_url") or ""
    description = await get_setting("product_description") or "Premium Gemini AI Pro access for 18 months. Instant delivery via redemption link."
    return {
        "name": PRODUCT_NAME,
        "price": price,
        "stock": stock,
        "sold": sold,
        "rating": avg_rating if avg_rating else 4.8,
        "reviews": review_count,
        "image_url": image_url,
        "description": description,
    }


async def set_product_info(image_url: str, description: str):
    """Saves product image_url and description to settings table."""
    await set_setting("product_image_url", image_url)
    await set_setting("product_description", description)


async def migrate_db():
    """Run migrations to ensure new settings rows exist in older databases."""
    db = await get_db()
    
    # Run multi-product schema changes on existing DB
    try:
        await db.execute("ALTER TABLE stock ADD COLUMN product_id INTEGER DEFAULT 1")
    except Exception: pass
    try:
        await db.execute("ALTER TABLE orders ADD COLUMN product_id INTEGER DEFAULT 1")
    except Exception: pass
    try:
        await db.execute("ALTER TABLE order_items ADD COLUMN product_id INTEGER DEFAULT 1")
    except Exception: pass
    try:
        await db.execute("""CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT,
            price       REAL NOT NULL,
            image_url   TEXT,
            is_active   INTEGER DEFAULT 1
        )""")
    except Exception: pass
    try:
        await db.execute("INSERT OR IGNORE INTO products (id, name, description, price, image_url) VALUES (1, 'Premium Gemini AI Pro', 'Premium Gemini AI Pro access for 18 months. Instant delivery via redemption link.', 4.99, '')")
    except Exception: pass
    
    await db.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('product_image_url', '')")
    await db.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('product_description', 'Premium Gemini AI Pro access for 18 months. Instant delivery via redemption link.')")
    await db.commit()

# ─────────────────────────────────────────────────────────────────────────────
# Badge helper
# ─────────────────────────────────────────────────────────────────────────────

def compute_badge(links_count: int) -> str:
    badge = "🆕 New Member"
    for label, threshold in BADGE_THRESHOLDS.items():
        if links_count >= threshold:
            badge = label
    return badge

# ─────────────────────────────────────────────────────────────────────────────
# Backup
# ─────────────────────────────────────────────────────────────────────────────

async def backup_database():
    """Copy the database file to the backups directory with a timestamp."""
    src = Path(DB_PATH)
    if not src.exists():
        return
    backup_dir = Path("data/backups")
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    dest = backup_dir / f"alpha_bot_{ts}.db"
    shutil.copy2(src, dest)
    log.info("Database backed up to %s", dest)
    # Keep only last 10 backups
    backups = sorted(backup_dir.glob("*.db"))
    for old in backups[:-10]:
        old.unlink()
import aiosqlite

async def add_product(name: str, description: str, price: float, image_url: str = '') -> int:
    db = await get_db()
    cursor = await db.execute(
        "INSERT INTO products (name, description, price, image_url, is_active) VALUES (?,?,?,?, 1)",
        (name, description, price, image_url)
    )
    await db.commit()
    return cursor.lastrowid

async def get_products() -> list[aiosqlite.Row]:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM products WHERE is_active=1")
    return await cursor.fetchall()

async def get_product(product_id: int) -> aiosqlite.Row | None:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM products WHERE id=? AND is_active=1", (product_id,))
    return await cursor.fetchone()

async def update_product(product_id: int, name: str, description: str, price: float, image_url: str):
    db = await get_db()
    await db.execute(
        "UPDATE products SET name = ?, description = ?, price = ?, image_url = ? WHERE id = ?",
        (name, description, price, image_url, product_id)
    )
    await db.commit()

async def delete_product(product_id: int):
    db = await get_db()
    await db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    await db.execute("DELETE FROM stock WHERE product_id = ?", (product_id,))
    await db.commit()
