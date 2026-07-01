with open('database.py', 'r', encoding='utf-8') as f:
    text = f.read()

if 'async def delete_product' not in text:
    text += '''
async def update_product(product_id: int, name: str, description: str, price: float, image_url: str):
    async with get_db() as db:
        await db.execute(
            "UPDATE products SET name = ?, description = ?, price = ?, image_url = ? WHERE id = ?",
            (name, description, price, image_url, product_id)
        )
        await db.commit()

async def delete_product(product_id: int):
    async with get_db() as db:
        await db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        await db.execute("DELETE FROM stock WHERE product_id = ?", (product_id,))
        await db.commit()
'''
    with open('database.py', 'w', encoding='utf-8') as f:
        f.write(text)
