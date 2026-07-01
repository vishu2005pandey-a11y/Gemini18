import re

with open('handlers/shop.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add imports for new keyboards
text = text.replace('shop_kb, terms_kb', 'shop_product_list_kb, product_detail_kb, terms_kb')

new_shop_flow = '''
@router.callback_query(F.data == "shop")
async def cb_shop(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    products = await db.get_products()
    stock_map = {}
    for p in products:
        stock_map[p["id"]] = await db.get_stock_count(p["id"])
    
    text = f"{E_CART} <b>Catálogo de productos</b>\\n\\n{E_CHECK} Entrega automática al instante\\n\\n?? Elige tu producto:"
    await callback.message.edit_text(
        text,
        reply_markup=shop_product_list_kb(lang, products, stock_map),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("view_prod:"))
async def cb_view_prod(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"
    
    prod_id = int(callback.data.split(":")[1])
    p = await db.get_product(prod_id)
    if not p: return await callback.answer("Product not found.", show_alert=True)
    
    stock = await db.get_stock_count(prod_id)
    sold = p['id'] * 123  # just a dummy logic or skip
    
    text = t(lang, "shop_header") + t(
        lang, "product_card",
        name=p['name'],
        price=f"{p['price']:.2f}",
        stock=stock,
        sold=f"{sold:,}",
        rating="?????",
        review_count=12,
    )
    # replace description inside text if needed, for simplicity we just use default translation
    text = text.replace("Premium Gemini AI Pro access for 18 months.", p['description'] or "")
    
    await callback.message.edit_text(
        text,
        reply_markup=product_detail_kb(lang, prod_id, p['price'], stock > 0),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("buy:"))
async def cb_buy(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    parts = callback.data.split(":")
    prod_id = int(parts[1])
    qty_str = parts[2]

    if qty_str == "custom":
        await callback.message.edit_text(
            t(lang, "custom_qty_prompt"),
            reply_markup=back_kb(lang, f"view_prod:{prod_id}"),
            parse_mode="HTML"
        )
        await state.update_data(buy_prod_id=prod_id)
        await state.set_state(BuyStates.waiting_custom_qty)
        await callback.answer()
        return

    qty = int(qty_str)
    await _show_terms(callback, lang, prod_id, qty)
    await callback.answer()

@router.message(BuyStates.waiting_custom_qty)
async def msg_custom_qty(message: Message, state: FSMContext):
    user_id = message.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    data = await state.get_data()
    prod_id = data.get("buy_prod_id")
    if not prod_id: return
    
    try:
        qty = int(message.text.strip())
        if not 1 <= qty <= 100:
            raise ValueError
    except ValueError:
        await message.answer(t(lang, "invalid_qty"), parse_mode="HTML")
        return

    await state.clear()
    stock = await db.get_stock_count(prod_id)
    if qty > stock:
        await message.answer(t(lang, "insufficient_stock", stock=stock), parse_mode="HTML")
        return

    text = t(lang, "terms")
    await message.answer(text, reply_markup=terms_kb(lang, prod_id, qty), parse_mode="HTML")

async def _show_terms(callback: CallbackQuery, lang: str, prod_id: int, qty: int):
    stock = await db.get_stock_count(prod_id)
    if qty > stock:
        await callback.message.edit_text(
            t(lang, "insufficient_stock", stock=stock),
            reply_markup=back_kb(lang, f"view_prod:{prod_id}"),
            parse_mode="HTML"
        )
        return
    text = t(lang, "terms")
    await callback.message.edit_text(text, reply_markup=terms_kb(lang, prod_id, qty), parse_mode="HTML")
'''

pattern = r'@router.callback_query\(F.data == "shop"\).*?async def _show_terms\(callback: CallbackQuery, lang: str, qty: int\):.*?await callback\.message\.edit_text\(text, reply_markup=terms_kb\(lang, qty\), parse_mode="HTML"\)'
text = re.sub(pattern, new_shop_flow, text, flags=re.DOTALL)

# update agree
old_agree = '''@router.callback_query(F.data.startswith("agree:"))
async def cb_agree(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    qty = int(callback.data.split(":")[1])
    price = await db.get_price()
    total = round(price * qty, 2)'''

new_agree = '''@router.callback_query(F.data.startswith("agree:"))
async def cb_agree(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_user = await db.get_user(user_id)
    lang = db_user["language"] if db_user else "en"

    parts = callback.data.split(":")
    prod_id = int(parts[1])
    qty = int(parts[2])
    
    p = await db.get_product(prod_id)
    price = p['price']
    total = round(price * qty, 2)'''
text = text.replace(old_agree, new_agree)

old_stock_check = '''    stock = await db.get_stock_count()
    if qty > stock:'''
new_stock_check = '''    stock = await db.get_stock_count(prod_id)
    if qty > stock:'''
text = text.replace(old_stock_check, new_stock_check, 1) # Only replace the one in cb_agree

old_invoice_text = '''    text = t(
        lang, "payment_invoice",
        product=PRODUCT_NAME,
        qty=qty,'''
new_invoice_text = '''    text = t(
        lang, "payment_invoice",
        product=p['name'],
        qty=qty,'''
text = text.replace(old_invoice_text, new_invoice_text)

with open('handlers/shop.py', 'w', encoding='utf-8') as f:
    f.write(text)
