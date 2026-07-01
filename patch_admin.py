import re

with open('handlers/admin.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_msg_step = '''
@router.message(AdminStates.waiting_product_description)
async def msg_product_add_step(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    data = await state.get_data()
    step = data.get("add_step")
    prod_id = data.get("edit_prod_id")
    
    if step == "name":
        await state.update_data(name=message.text)
        await message.answer("Send product price:")
        await state.update_data(add_step="price")
    elif step == "price":
        try:
            price = float(message.text)
            await state.update_data(price=price)
            await message.answer("Send product description:")
            await state.update_data(add_step="desc")
        except ValueError:
            await message.answer("Invalid price.")
    elif step == "desc":
        await state.update_data(desc=message.text)
        await message.answer("Send product image URL (or 'skip' to use none/current, or send a photo):")
        await state.update_data(add_step="image")
    elif step == "image":
        image_url = ""
        text_val = message.text.strip().lower() if message.text else ""
        if message.photo:
            photo = message.photo[-1]
            file = await message.bot.get_file(photo.file_id)
            image_url = f"https://api.telegram.org/file/bot{message.bot.token}/{file.file_path}"
        elif text_val != "skip":
            image_url = message.text

        data = await state.get_data()
        if prod_id:
            if text_val == "skip":
                # preserve old image
                old_p = await db.get_product(prod_id)
                image_url = old_p['image_url'] if old_p else ""
            await db.update_product(prod_id, data["name"], data["desc"], data["price"], image_url)
            await message.answer("? Product updated!", reply_markup=back_kb("en", "admin:manage_products"))
        else:
            await db.add_product(data["name"], data["desc"], data["price"], image_url)
            await message.answer("? Product added successfully!", reply_markup=back_kb("en", "admin:manage_products"))
        await state.clear()

@router.callback_query(F.data.startswith("admin:edit_prod:"))
async def cb_edit_prod(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    prod_id = int(callback.data.split(":")[2])
    p = await db.get_product(prod_id)
    if not p: return await callback.answer("Not found", show_alert=True)
    
    from aiogram.types import InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="?? Edit", callback_data=f"admin:do_edit_prod:{prod_id}"))
    builder.row(InlineKeyboardButton(text="??? Delete", callback_data=f"admin:del_prod:{prod_id}"))
    builder.row(InlineKeyboardButton(text="« Back", callback_data="admin:manage_products"))
    
    await callback.message.edit_text(f"<b>{p['name']}</b>\\nPrice: \\nDesc: {p['description']}", reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("admin:do_edit_prod:"))
async def cb_do_edit_prod(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    prod_id = int(callback.data.split(":")[2])
    await callback.message.edit_text("Send new product name:", reply_markup=back_kb("en", f"admin:edit_prod:{prod_id}"))
    await state.set_state(AdminStates.waiting_product_description)
    await state.update_data(add_step="name", edit_prod_id=prod_id)
    await callback.answer()

@router.callback_query(F.data.startswith("admin:del_prod:"))
async def cb_del_prod(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id): return
    prod_id = int(callback.data.split(":")[2])
    await db.delete_product(prod_id)
    await callback.answer("Product deleted!", show_alert=True)
    # Redirect to manage_products
    # To keep it simple, just call cb_manage_products (simulate)
    await callback.message.edit_text("Deleted. Use /admin to go back.")
'''

# We want to replace the old msg_product_add_step
pattern = r'@router.message\(AdminStates.waiting_product_description\)\s*async def msg_product_add_step.*?await message.answer\("Product added!", reply_markup=back_kb\("en", "admin:manage_products"\)\)'
text = re.sub(pattern, new_msg_step, text, flags=re.DOTALL)

with open('handlers/admin.py', 'w', encoding='utf-8') as f:
    f.write(text)
