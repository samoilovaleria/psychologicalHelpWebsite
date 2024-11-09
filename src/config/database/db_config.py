from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class Config:
    DATABASE_URL = ""

class LocalDevConfig(Config):
    DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/mydatabase"

class DevConfig(Config):
    DATABASE_URL = "postgresql+asyncpg://a_admin:superStrongPassword@185.128.105.126:5432/psychological"

configurations = {
    "local-dev": LocalDevConfig,
    "dev": DevConfig,
}

# Заменить на dev, чтобы работало с удаленным сервером
profile = "local-dev"
config = configurations[profile]

engine = create_engine(config.DATABASE_URL, echo=True)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async_engine = create_async_engine(config.DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


# from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()