"""
Alpha Bot — Crypto Payment Gateway
Supports:
  - USDT BEP20 (BSC)   verified via BSCScan API
  - USDT ERC20 (ETH)   verified via Etherscan API

No middleman. Zero fees. Direct on-chain verification.
"""
import uuid
import hashlib
import logging
import aiohttp
from decimal import Decimal, ROUND_UP
from config import (
    WALLET_ADDRESS_BSC, WALLET_ADDRESS_ETH,
    BSCSCAN_API_KEY, ETHERSCAN_API_KEY,
)

log = logging.getLogger(__name__)

# ── USDT contract addresses ───────────────────────────────────────────────────
USDT_BSC_CONTRACT  = "0x55d398326f99059fF775485246999027B3197955"  # BSC USDT
USDT_ETH_CONTRACT  = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # ETH USDT

# ── Networks ──────────────────────────────────────────────────────────────────
NETWORKS = {
    "USDT_BSC": {
        "label":    "USDT (BEP20 / BSC)",
        "symbol":   "USDT",
        "network":  "BSC",
        "address":  WALLET_ADDRESS_BSC,
        "contract": USDT_BSC_CONTRACT,
        "api_url":  "https://api.bscscan.com/api",
        "api_key":  BSCSCAN_API_KEY,
        "decimals": 18,
        "explorer": "https://bscscan.com/tx/",
    },
    "USDT_ETH": {
        "label":    "USDT (ERC20 / ETH)",
        "symbol":   "USDT",
        "network":  "ETH",
        "address":  WALLET_ADDRESS_ETH,
        "contract": USDT_ETH_CONTRACT,
        "api_url":  "https://api.etherscan.io/api",
        "api_key":  ETHERSCAN_API_KEY,
        "decimals": 6,
        "explorer": "https://etherscan.io/tx/",
    },
}


def generate_order_id() -> str:
    return uuid.uuid4().hex[:12].upper()


def get_network(network_key: str) -> dict:
    return NETWORKS.get(network_key, NETWORKS["USDT_BSC"])


def get_all_networks() -> dict:
    return NETWORKS


def usd_to_usdt(amount_usd: float) -> str:
    """Return USDT amount string (1:1 peg, rounded up to 2 decimals)."""
    return str(Decimal(str(amount_usd)).quantize(Decimal("0.01"), rounding=ROUND_UP))


async def get_token_transactions(network_key: str, wallet: str) -> list[dict]:
    """Fetch recent ERC20/BEP20 token transactions for a wallet."""
    net = get_network(network_key)
    params = {
        "module":          "account",
        "action":          "tokentx",
        "contractaddress": net["contract"],
        "address":         wallet,
        "sort":            "desc",
        "page":            "1",
        "offset":          "50",
        "apikey":          net["api_key"],
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                net["api_url"], params=params,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                data = await resp.json()
                if data.get("status") == "1":
                    return data.get("result", [])
                log.warning("%s API: %s", network_key, data.get("message", "unknown"))
                return []
    except Exception as e:
        log.error("get_token_transactions error (%s): %s", network_key, e)
        return []


async def verify_payment(
    network_key: str,
    wallet: str,
    expected_amount_usdt: str,
    order_id: str,
    created_at_ts: int,
) -> tuple[bool, str | None]:
    """
    Check if a payment of `expected_amount_usdt` USDT arrived at `wallet`
    after `created_at_ts` (unix timestamp).

    Returns (confirmed: bool, tx_hash: str | None)
    """
    net        = get_network(network_key)
    decimals   = net["decimals"]
    expected_raw = int(Decimal(expected_amount_usdt) * (10 ** decimals))

    txs = await get_token_transactions(network_key, wallet)
    for tx in txs:
        # Only incoming transfers to our wallet
        if tx.get("to", "").lower() != wallet.lower():
            continue
        # Must be after order creation
        tx_ts = int(tx.get("timeStamp", 0))
        if tx_ts < created_at_ts:
            continue
        # Check amount (allow up to 1% over — handles rounding)
        tx_value = int(tx.get("value", 0))
        if tx_value >= expected_raw * 0.99:
            return True, tx.get("hash")

    return False, None


def is_payment_confirmed(status: str) -> bool:
    return status == "confirmed"
