import aiosqlite
from datetime import datetime

async def get_user(chat_id: int):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,)) as cursor:
            return await cursor.fetchone()

async def add_user(chat_id: int, username: str = None):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            "INSERT INTO users (chat_id, username) VALUES (?, ?)",
            (chat_id, username)
        )
        await db.commit()

async def update_username(chat_id: int, new_username: str):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            "UPDATE users SET username = ? WHERE chat_id = ?",
            (new_username, chat_id)
        )
        await db.commit()

async def get_user_balance(chat_id: int) -> float:
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT balance FROM users WHERE chat_id = ?", (chat_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0.0

async def add_user_balance(chat_id: int, amount: float):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("UPDATE users SET balance = balance + ? WHERE chat_id = ?", (amount, chat_id))
        await db.commit()

async def deduct_user_balance(chat_id: int, amount: float) -> bool:
    async with aiosqlite.connect("database.db") as db:
        balance = await get_user_balance(chat_id)
        if balance < amount:
            return False
        new_balance = balance - amount
        await db.execute("UPDATE users SET balance = ? WHERE chat_id = ?", (new_balance, chat_id))
        await db.commit()
        return True

async def record_purchase(user_chat_id: int, product_id: int, amount: float):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT id FROM users WHERE chat_id = ?", (user_chat_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return False
            user_id = row[0]

        await db.execute(
            "INSERT INTO payments (user_id, product_id, amount, status, invoice_id) VALUES (?, ?, ?, ?, ?)",
            (user_id, product_id, amount, "paid", "direct_purchase")
        )
        await db.commit()
        return True
    
async def add_product_to_db(name: str, description: str, price: float, file_path: str = None, link: str = None):
    created_at = datetime.now().isoformat()
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            INSERT INTO products (name, description, price, file_path, link, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, price, file_path, link, created_at))
        await db.commit()

async def get_all_products():
    async with aiosqlite.connect("database.db") as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM products")
        products = await cursor.fetchall()
    return [dict(row) for row in products]

async def get_product_by_id(product_id: int):
    async with aiosqlite.connect("database.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM products WHERE id = ?", (product_id,)) as cursor:
            product = await cursor.fetchone()
            if product:
                return dict(product)
            return None

async def get_user_purchases(chat_id: int):
    async with aiosqlite.connect("database.db") as db:
        return await (await db.execute("""
            SELECT products.name, payments.amount, payments.status, payments.created_at
            FROM payments
            JOIN products ON payments.product_id = products.id
            WHERE payments.chat_id = ?
            ORDER BY payments.created_at DESC
        """, (chat_id,))).fetchall()
    
async def delete_product_from_db(product_id: int):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        await db.commit()