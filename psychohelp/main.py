from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine

from psychohelp.config.database import (
    Base,
    RESET_DB_ON_START,
    RESET_COOKIE_ON_START,
    config,
)
from psychohelp.routes import api_router

import uvicorn


async def reset_database(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


engine = create_async_engine(config.DATABASE_URL, echo=True)


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://psychohelp.example.com",
            "https://185.128.105.126",
            "http://localhost:3000",
            "http://localhost:8000",
            "http://localhost",
            "http://185.128.105.126:8000",
            "http://185.128.105.126:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.on_event("startup")
    async def on_startup():
        if RESET_DB_ON_START:
            await reset_database(engine)

    return application


app = get_application()


def main():
    uvicorn.run("psychohelp.main:app", host="0.0.0.0", reload=True)


if __name__ == "__main__":
    main()
