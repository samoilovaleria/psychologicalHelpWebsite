from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# import os

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:pass@217.171.146.85:5432/polytech")
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://admin:pass@217.171.146.85:5432/polytech")

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/mydatabase"


engine = create_engine(DATABASE_URL, echo=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)



async_engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


# from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()