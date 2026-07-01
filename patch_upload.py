import re

with open('handlers/admin.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_code = '''
@router.callback_query(F.data == "admin:upload_stock")
async def cb_admin_upload(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    products = await db.get_products()
    from aiogram.types import InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    for p in products:
        builder.row(InlineKeyboardButton(text=f"{p['name']} (Stock: {await db.get_stock_count(p['id'])})", callback_data=f"admin:upload_stock_prod:{p['id']}"))
    builder.row(InlineKeyboardButton(text="« Back", callback_data="admin:panel"))
    await callback.message.edit_text("<b>Select Product to Upload Stock:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("admin:upload_stock_prod:"))
async def cb_admin_upload_prod(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    prod_id = int(callback.data.split(":")[2])
    await state.update_data(upload_prod_id=prod_id)
    await callback.message.edit_text(
        f"?? <b>Upload Stock</b>\\n\\nSend a <b>.txt file</b> with one redemption link per line.",
        reply_markup=back_kb("en", "admin:upload_stock"),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_stock_file)
    await callback.answer()

async def _process_stock_file(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    db_user = await db.get_user(message.from_user.id)
    lang = db_user["language"] if db_user else "en"
    doc = message.document
    if not doc:
        await message.answer("? Please send a .txt file.")
        return
    import io
    try:
        file_bytes = io.BytesIO()
        await message.bot.download(doc, destination=file_bytes)
        file_bytes.seek(0)
        content = file_bytes.read().decode("utf-8", errors="ignore")
    except Exception as e:
        await message.answer(f"? Failed to read file: {e}")
        return
    links = [line.strip() for line in content.splitlines() if line.strip()]
    if not links:
        await message.answer("? File is empty.")
        return
    
    data = await state.get_data()
    prod_id = data.get("upload_prod_id", 1)
    added = await db.add_stock(prod_id, links)
    total = await db.get_stock_count(prod_id)
    
    await state.clear()
    await message.answer(
        f"? <b>Stock Uploaded!</b>\\n\\n?? New links added: <b>{added}</b>\\n?? Total stock now: <b>{total}</b>",
        reply_markup=admin_kb(lang),
        parse_mode="HTML"
    )
'''

# Find the block and replace
pattern = r'@router.callback_query\(F.data == "admin:upload_stock"\).*?(?=@router.message\(AdminStates.waiting_stock_file\))'
text = re.sub(pattern, new_code, text, flags=re.DOTALL)

with open('handlers/admin.py', 'w', encoding='utf-8') as f:
    f.write(text)
