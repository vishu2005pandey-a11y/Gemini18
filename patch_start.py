import re

with open('keyboards.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_kb = '''def start_language_kb(lang: str = "en") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="???? English", callback_data="start_lang:en"),
        InlineKeyboardButton(text="???? Español", callback_data="start_lang:es"),
    )
    return builder.as_markup()

def language_kb'''

text = text.replace('def language_kb', new_kb)

with open('keyboards.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('handlers/start.py', 'r', encoding='utf-8') as f:
    start_text = f.read()

start_text = start_text.replace('from keyboards import force_join_kb, main_menu_kb', 'from keyboards import force_join_kb, main_menu_kb, start_language_kb')

old_start = '''    # Force-join check
    member = await _is_member(message.bot, user.id)
    if not member:
        text = t(lang, "force_join_title", channel_link=CHANNEL_LINK, group_link=GROUP_LINK)
        await message.answer(text, reply_markup=force_join_kb(lang), parse_mode="HTML")
        return

    await send_main_menu(message, lang, show_sticker=True)'''

new_start = '''    # Show language selection on /start
    text = "Please select your language: / Por favor, selecciona tu idioma:"
    await message.answer(text, reply_markup=start_language_kb(lang), parse_mode="HTML")'''

start_text = start_text.replace(old_start, new_start)

# Add callback handler for start_lang
new_handler = '''@router.callback_query(F.data.startswith("start_lang:"))
async def cb_start_lang(callback: CallbackQuery):
    user_id = callback.from_user.id
    new_lang = callback.data.split(":")[1]
    await db.set_user_language(user_id, new_lang)
    await callback.answer("Language updated! / ¡Idioma actualizado!", show_alert=False)

    lang = new_lang
    member = await _is_member(callback.bot, user_id)
    if not member:
        text = t(lang, "force_join_title", channel_link=CHANNEL_LINK, group_link=GROUP_LINK)
        await callback.message.edit_text(text, reply_markup=force_join_kb(lang), parse_mode="HTML")
        return

    await send_main_menu(callback, lang, show_sticker=True)
'''

start_text += "\n" + new_handler

with open('handlers/start.py', 'w', encoding='utf-8') as f:
    f.write(start_text)
