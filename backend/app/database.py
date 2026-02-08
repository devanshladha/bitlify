import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()


PG_DB_USER = os.environ.get("DB_USER", "postgres")
PG_DB_PASSWORD = os.environ.get("DB_PASSWORD", "your_password")
PG_DB_HOST = os.environ.get("DB_HOST", "localhost")
PG_DB_PORT = os.environ.get("DB_PORT", "5432")
PG_DB_NAME = os.environ.get("DB_NAME", "your_database_name")

DATABASE_URL = f"postgresql+asyncpg://{PG_DB_USER}:{PG_DB_PASSWORD}@{PG_DB_HOST}:{PG_DB_PORT}/{PG_DB_NAME}"
Base = declarative_base()

engine = create_async_engine(DATABASE_URL)
Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db():
    async with Session() as session:
        try:
            yield session
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")
            raise e