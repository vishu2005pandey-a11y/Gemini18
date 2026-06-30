"""
Alpha Bot — Cryptomus Payment Gateway Integration
Docs: https://doc.cryptomus.com/
"""
import hashlib
import hmac
import json
import logging
import uuid
import aiohttp
import base64
from config import CRYPTOMUS_API_KEY, CRYPTOMUS_MERCHANT_ID

log = logging.getLogger(__name__)

CRYPTOMUS_BASE = "https://api.cryptomus.com/v1"


def _sign(data: dict) -> str:
    """Cryptomus request signature."""
    body = json.dumps(data, separators=(",", ":"))
    encoded = base64.b64encode(body.encode()).decode()
    sig = hashlib.md5(f"{encoded}{CRYPTOMUS_API_KEY}".encode()).hexdigest()
    return sig


def _headers(data: dict) -> dict:
    return {
        "merchant": CRYPTOMUS_MERCHANT_ID,
        "sign": _sign(data),
        "Content-Type": "application/json",
    }


async def create_invoice(
    order_id: str,
    amount_usd: float,
    currency: str = "USDT",
    network: str = "TRON_TRC20",
    lifetime: int = 1800,   # seconds
) -> dict | None:
    """
    Create a Cryptomus payment invoice.
    Returns dict with keys: uuid, address, amount, currency, url, etc.
    Returns None on failure.
    """
    payload = {
        "amount": str(round(amount_usd, 2)),
        "currency": "USD",
        "to_currency": currency,
        "order_id": order_id,
        "lifetime": lifetime,
        "network": network,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{CRYPTOMUS_BASE}/payment",
                json=payload,
                headers=_headers(payload),
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                data = await resp.json()
                if data.get("state") == 0:
                    return data.get("result")
                log.error("Cryptomus invoice error: %s", data)
                return None
    except Exception as e:
        log.exception("Cryptomus create_invoice failed: %s", e)
        return None


async def check_payment(payment_uuid: str) -> dict | None:
    """
    Check payment status by Cryptomus payment UUID.
    Returns result dict with 'payment_status' field.
    Possible statuses: paid, paid_over, wrong_amount, process,
                       confirm_check, wrong_amount_waiting, cancel,
                       system_fail, refund_process, refund_fail, refund_paid
    """
    payload = {"uuid": payment_uuid}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{CRYPTOMUS_BASE}/payment/info",
                json=payload,
                headers=_headers(payload),
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                data = await resp.json()
                if data.get("state") == 0:
                    return data.get("result")
                log.error("Cryptomus check_payment error: %s", data)
                return None
    except Exception as e:
        log.exception("Cryptomus check_payment failed: %s", e)
        return None


def is_payment_confirmed(status: str) -> bool:
    return status in ("paid", "paid_over")


def generate_order_id() -> str:
    return uuid.uuid4().hex[:12].upper()
