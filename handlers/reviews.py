"""
Reviews handler.
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
from keyboards import review_stars_kb, back_kb
from locales import get as t

log = logging.getLogger(__name__)
router = Router()


class ReviewStates(StatesGroup):
    waiting_comment = State()


# ─────────────────────────────────────────────────────────────────────────────
# Reviews list
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "reviews")
async def cb_reviews(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    reviews = await db.get_reviews(limit=10)
    avg, count = await db.get_avg_rating()

    review_lines = ""
    for r in reviews:
        stars = "⭐" * r["rating"]
        uname = f"@{r['username'][:4]}****" if r["username"] else "User****"
        comment = r["comment"] or "<i>No comment</i>"
        review_lines += t(lang, "review_item", stars=stars, username=uname, comment=comment)

    if not review_lines:
        review_lines = "<i>No reviews yet. Be the first!</i>"

    avg_display = f"{'⭐' * round(avg)} ({avg})" if avg else "☆☆☆☆☆"
    text = t(lang, "reviews_header", avg_rating=avg_display, count=count, reviews=review_lines)

    await callback.message.edit_text(
        text,
        reply_markup=back_kb(lang, "main_menu"),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
# Start review flow
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("review_start:"))
async def cb_review_start(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    order_id = callback.data.split(":", 1)[1]

    # Check if already reviewed
    if await db.has_reviewed_order(order_id):
        await callback.answer("✅ You've already reviewed this order.", show_alert=True)
        return

    text = t(lang, "leave_review_prompt")
    await callback.message.edit_text(
        text,
        reply_markup=review_stars_kb(order_id),
        parse_mode="HTML"
    )
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
# Star rating selected
# ─────────────────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("review_rate:"))
async def cb_review_rate(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    parts = callback.data.split(":")
    order_id = parts[1]
    rating = int(parts[2])

    await state.update_data(order_id=order_id, rating=rating)

    await callback.message.edit_text(
        f"{'⭐' * rating} <b>{rating}/5 selected!</b>\n\n"
        "💬 <i>Optional: leave a comment (or type <code>skip</code>)</i>",
        reply_markup=back_kb(lang, "main_menu"),
        parse_mode="HTML"
    )
    await state.set_state(ReviewStates.waiting_comment)
    await callback.answer()


# ─────────────────────────────────────────────────────────────────────────────
# Comment received
# ─────────────────────────────────────────────────────────────────────────────

@router.message(ReviewStates.waiting_comment)
async def msg_review_comment(message: Message, state: FSMContext):
    user_id = message.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    data = await state.get_data()
    order_id = data.get("order_id")
    rating = data.get("rating", 5)
    comment = message.text.strip() if message.text.strip().lower() != "skip" else None

    await db.add_review(user_id, order_id, rating, comment)
    await state.clear()
    await message.answer(
        t(lang, "review_saved"),
        reply_markup=back_kb(lang, "main_menu"),
        parse_mode="HTML"
    )
