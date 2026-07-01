import re

with open('database.py', 'r', encoding='utf-8') as f:
    code = f.read()

products_table = '''
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT,
    price       REAL NOT NULL,
    image_url   TEXT,
    is_active   INTEGER DEFAULT 1
);
'''
code = code.replace('CREATE TABLE IF NOT EXISTS stock (', products_table + '\nCREATE TABLE IF NOT EXISTS stock (')

migrate_ext = '''
    # Multi-product migration
    try:
        await db.execute('ALTER TABLE stock ADD COLUMN product_id INTEGER DEFAULT 1')
    except Exception:
        pass
    try:
        await db.execute('ALTER TABLE orders ADD COLUMN product_id INTEGER DEFAULT 1')
    except Exception:
        pass
    try:
        await db.execute('ALTER TABLE order_items ADD COLUMN product_id INTEGER DEFAULT 1')
    except Exception:
        pass
    try:
        await db.execute('''CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT,
            price       REAL NOT NULL,
            image_url   TEXT,
            is_active   INTEGER DEFAULT 1
        )''')
    except Exception:
        pass

    # Ensure a default product exists
    await db.execute('''
        INSERT OR IGNORE INTO products (id, name, description, price, image_url) 
        VALUES (1, 'Premium Gemini AI Pro', 'Premium Gemini AI Pro access for 18 months.', 4.99, '')
    ''')
'''
code = code.replace('await db.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (''product_image_url'', '''')")', migrate_ext + '\n    await db.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (''product_image_url'', '''')")')

with open('database_new.py', 'w', encoding='utf-8') as f:
    f.write(code)
