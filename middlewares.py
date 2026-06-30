"""
Alpha Bot — Middlewares
  - Anti-flood / anti-spam
  - Maintenance mode gate
  - Ban check
  - User auto-registration
"""
import logging
import time
from collections import defaultdict
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject, Update

import database as db
from config import (
    FLOOD_LIMIT_MESSAGES, FLOOD_LIMIT_WINDOW_SECONDS, FLOOD_BAN_SECONDS,
    is_admin
)

log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Anti-flood store  {user_id: [timestamps]}
# ─────────────────────────────────────────────────────────────────────────────
_flood_store: dict[int, list[float]] = defaultdict(list)
_flood_banned_until: dict[int, float] = {}


def _is_flooded(user_id: int) -> bool:
    now = time.time()

    # Check if currently flood-banned
    banned_until = _flood_banned_until.get(user_id, 0)
    if now < banned_until:
        return True

    # Prune old timestamps
    window = now - FLOOD_LIMIT_WINDOW_SECONDS
    _flood_store[user_id] = [t for t in _flood_store[user_id] if t > window]
    _flood_store[user_id].append(now)

    if len(_flood_store[user_id]) > FLOOD_LIMIT_MESSAGES:
        _flood_banned_until[user_id] = now + FLOOD_BAN_SECONDS
        return True

    return False


# ─────────────────────────────────────────────────────────────────────────────
# Main middleware
# ─────────────────────────────────────────────────────────────────────────────

class BotMiddleware(BaseMiddleware):
    """Single middleware that handles flood, bans, maintenance, and user registration."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        # Extract user from Message or CallbackQuery
        user = None
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user

        if user is None:
            return await handler(event, data)

        user_id = user.id

        # ── Admin bypass ──────────────────────────────────────────────────
        if is_admin(user_id):
            # Still register/update admin in DB
            await db.upsert_user(user_id, user.username, user.first_name or "")
            return await handler(event, data)

        # ── Anti-flood ────────────────────────────────────────────────────
        if _is_flooded(user_id):
            if isinstance(event, Message):
                await event.answer("⏳ You're sending messages too fast. Please slow down.")
            elif isinstance(event, CallbackQuery):
                await event.answer("⏳ Slow down!", show_alert=True)
            return  # drop the event

        # ── Register / update user ────────────────────────────────────────
        await db.upsert_user(user_id, user.username, user.first_name or "")

        # ── Ban check ─────────────────────────────────────────────────────
        db_user = await db.get_user(user_id)
        if db_user and db_user["is_banned"]:
            lang = db_user["language"]
            from locales import get as t
            if isinstance(event, Message):
                await event.answer(t(lang, "banned"))
            elif isinstance(event, CallbackQuery):
                await event.answer(t(lang, "banned"), show_alert=True)
            return

        # ── Maintenance mode ──────────────────────────────────────────────
        maintenance = await db.is_maintenance()
        if maintenance:
            lang = db_user["language"] if db_user else "en"
            from locales import get as t
            if isinstance(event, Message):
                await event.answer(t(lang, "maintenance"), parse_mode="HTML")
            elif isinstance(event, CallbackQuery):
                await event.answer(t(lang, "maintenance"), show_alert=True)
            return

        # ── Store lang in data for handlers ──────────────────────────────
        if db_user:
            data["lang"] = db_user["language"]
        else:
            data["lang"] = "en"

        return await handler(event, data)
