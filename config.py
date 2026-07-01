"""
Alpha Bot — Central Configuration
Loads all settings from .env and exposes them as typed constants.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Telegram ────────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_IDS: list[int] = [
    int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
]
ADMIN_LOG_GROUP_ID: int = int(os.getenv("ADMIN_LOG_GROUP_ID", "0"))
CHANNEL_ID: int = int(os.getenv("CHANNEL_ID", "0"))
CHANNEL_LINK: str = os.getenv("CHANNEL_LINK", "https://t.me/channel")
GROUP_ID: int = int(os.getenv("GROUP_ID", "0"))
GROUP_LINK: str = os.getenv("GROUP_LINK", "https://t.me/group")

# ── Payment ─────────────────────────────────────────────────
# BSC (BEP20 USDT)
WALLET_ADDRESS_BSC:  str = os.getenv("WALLET_ADDRESS_BSC", "")
BSCSCAN_API_KEY:     str = os.getenv("BSCSCAN_API_KEY", "")
# ETH (ERC20 USDT)
WALLET_ADDRESS_ETH:  str = os.getenv("WALLET_ADDRESS_ETH", "")
ETHERSCAN_API_KEY:   str = os.getenv("ETHERSCAN_API_KEY", "")

PAYMENT_TIMEOUT_MINUTES: int = int(os.getenv("PAYMENT_TIMEOUT_MINUTES", "30"))
PAYMENT_CURRENCY: str = os.getenv("PAYMENT_CURRENCY", "USDT_BSC")  # USDT_BSC or USDT_ETH

# ── Product ──────────────────────────────────────────────────
PRODUCT_NAME: str = os.getenv("PRODUCT_NAME", "Gemini Pro 18-Month Subscription")
PRODUCT_PRICE: float = float(os.getenv("PRODUCT_PRICE", "4.99"))
LOW_STOCK_THRESHOLD: int = int(os.getenv("LOW_STOCK_THRESHOLD", "10"))

# ── Referral ─────────────────────────────────────────────────
REFERRAL_REWARD_USD: float = float(os.getenv("REFERRAL_REWARD_USD", "0.50"))

# ── Database ─────────────────────────────────────────────────
DB_PATH: str = os.getenv("DB_PATH", "data/alpha_bot.db")
BACKUP_INTERVAL_HOURS: int = int(os.getenv("BACKUP_INTERVAL_HOURS", "6"))

# ── Bot Settings ─────────────────────────────────────────────
BOT_LANGUAGE: str = os.getenv("BOT_LANGUAGE", "en")
MAINTENANCE_MODE: bool = os.getenv("MAINTENANCE_MODE", "false").lower() == "true"
LINKS_SOLD_COUNTER_BASE: int = int(os.getenv("LINKS_SOLD_COUNTER_BASE", "69987"))
MINI_APP_URL: str = os.getenv("MINI_APP_URL", "")

# ── Buyer Badge Thresholds ───────────────────────────────────
BADGE_THRESHOLDS = {
    "🥉 Bronze Buyer":  1,
    "🥈 Silver Buyer":  10,
    "🥇 Gold Buyer":    25,
    "💎 VIP Buyer":     50,
    "👑 Top Buyer":     100,
}

# ── Achievement Thresholds ───────────────────────────────────
ACHIEVEMENTS = {
    "first_purchase":   {"label": "🎯 First Purchase",       "threshold": 1},
    "links_10":         {"label": "🔥 10 Links Purchased",   "threshold": 10},
    "links_50":         {"label": "💫 50 Links Purchased",   "threshold": 50},
    "links_100":        {"label": "🏆 100 Links Purchased",  "threshold": 100},
}

# ── Anti-flood ───────────────────────────────────────────────
FLOOD_LIMIT_MESSAGES: int = 5       # max messages per window
FLOOD_LIMIT_WINDOW_SECONDS: int = 5 # window size in seconds
FLOOD_BAN_SECONDS: int = 30         # cooldown after flood

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
