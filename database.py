import aiosqlite


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def initialize(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    full_name TEXT,
                    phone_number TEXT,
                    register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    service_name TEXT,
                    amount REAL,
                    invoice_id INTEGER,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

    async def add_user(self, telegram_id: int, full_name: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR IGNORE INTO users (telegram_id, full_name)
                VALUES (?, ?)
            """, (telegram_id, full_name))
            await db.commit()

    async def add_order(self, telegram_id: int, service_name: str, amount: float, invoice_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO orders (telegram_id, service_name, amount, invoice_id, status)
                VALUES (?, ?, ?, ?, 'active')
            """, (telegram_id, service_name, amount, invoice_id))
            await db.commit()

    async def update_order_status(self, invoice_id: int, status: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE orders SET status = ? WHERE invoice_id = ?", (status, invoice_id))
            await db.commit()      