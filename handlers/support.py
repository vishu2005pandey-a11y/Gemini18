"""
Support handler.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

import database as db
from keyboards import back_kb
from locales import get as t

router = Router()


@router.callback_query(F.data == "support")
@router.message(Command("support"))
async def cb_support(event: CallbackQuery | Message):
    if isinstance(event, CallbackQuery):
        user = event.from_user
    else:
        user = event.from_user

    db_user = await db.get_user(user.id)
    lang = db_user["language"] if db_user else "en"

    text = t(lang, "support")
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=back_kb(lang), parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(text, reply_markup=back_kb(lang), parse_mode="HTML")
