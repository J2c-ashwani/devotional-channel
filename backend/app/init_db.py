import asyncio
from backend.app.database import init_db, engine
from backend.app.models import Base

async def main():
    print("Initializing Database tables...")
    await init_db()
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: sync_conn.dialect.get_table_names(sync_conn))
        print(f"Created {len(tables)} tables: {tables}")

if __name__ == "__main__":
    asyncio.run(main())
