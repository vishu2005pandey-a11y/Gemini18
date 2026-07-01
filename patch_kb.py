import re

with open('keyboards.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_kb = '''
def shop_product_list_kb(lang: str, products: list, stock_map: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in products:
        pid = p["id"]
        stock = stock_map.get(pid, 0)
        btn_style = "success" if stock > 0 else "danger"
        status_icon = "??" if stock > 0 else "??"
        status_text = f"{stock} disponibles" if stock > 0 else "Sin stock" # or english
        
        btn_text = f"{p['name']} |  | {status_icon} {status_text}"
        builder.row(InlineKeyboardButton(text=btn_text, callback_data=f"view_prod:{pid}", style=btn_style))
        
    builder.row(InlineKeyboardButton(text="?? Refresh Stock", callback_data="shop"))
    builder.row(InlineKeyboardButton(text="?? Main Menu", callback_data="main_menu"))
    return builder.as_markup()

def product_detail_kb(lang: str, product_id: int, price: float, in_stock: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if in_stock:
        builder.row(
            InlineKeyboardButton(
                text=t(lang, "btn_buy_1", price=f"{price:.2f}"),
                callback_data=f"buy:{product_id}:1"
            )
        )
        builder.row(
            InlineKeyboardButton(
                text=t(lang, "btn_buy_3", price=f"{price * 3:.2f}"),
                callback_data=f"buy:{product_id}:3"
            ),
            InlineKeyboardButton(
                text=t(lang, "btn_buy_5", price=f"{price * 5:.2f}"),
                callback_data=f"buy:{product_id}:5"
            ),
        )
        builder.row(
            InlineKeyboardButton(
                text=t(lang, "btn_buy_10", price=f"{price * 10:.2f}"),
                callback_data=f"buy:{product_id}:10"
            ),
            InlineKeyboardButton(
                text=t(lang, "btn_custom_qty"),
                callback_data=f"buy:{product_id}:custom"
            ),
        )
    builder.row(
        InlineKeyboardButton(text=t(lang, "btn_back"), callback_data="shop")
    )
    return builder.as_markup()
'''

pattern = r'def shop_kb.*?(?=\n# \S*# Terms\n)'
text = re.sub(pattern, new_kb, text, flags=re.DOTALL)

# update terms_kb
old_terms = 'def terms_kb(lang: str = "en", qty: int = 1) -> InlineKeyboardMarkup:\n    builder = InlineKeyboardBuilder()\n    builder.row(\n        InlineKeyboardButton(text=t(lang, "btn_agree"), callback_data=f"agree:{qty}"),'
new_terms = 'def terms_kb(lang: str = "en", prod_id: int = 1, qty: int = 1) -> InlineKeyboardMarkup:\n    builder = InlineKeyboardBuilder()\n    builder.row(\n        InlineKeyboardButton(text=t(lang, "btn_agree"), callback_data=f"agree:{prod_id}:{qty}"),'
text = text.replace(old_terms, new_terms)

with open('keyboards.py', 'w', encoding='utf-8') as f:
    f.write(text)
