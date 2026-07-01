import aiosqlite

async def add_product(name: str, description: str, price: float, image_url: str = '') -> int:
    db = await get_db()
    cursor = await db.execute(
        "INSERT INTO products (name, description, price, image_url, is_active) VALUES (?,?,?,?, 1)",
        (name, description, price, image_url)
    )
    await db.commit()
    return cursor.lastrowid

async def get_products() -> list[aiosqlite.Row]:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM products WHERE is_active=1")
    return await cursor.fetchall()

async def get_product(product_id: int) -> aiosqlite.Row | None:
    db = await get_db()
    cursor = await db.execute("SELECT * FROM products WHERE id=? AND is_active=1", (product_id,))
    return await cursor.fetchone()
