from fastapi import FastAPI
from fastapi.responses import Response
from src.routes.routes import api_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from src.config.database import Base, config, RESET_DB_ON_START, RESET_COOKIE_ON_START


async def reset_database(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def clear_all_cookies():
    response = Response()
    cookies_to_clear = ["access_token"]

    for cookie in cookies_to_clear:
        response.delete_cookie(
            key=cookie,
            httponly=True,
            secure=False,
            samesite="Lax",
        )


engine = create_async_engine(config.DATABASE_URL, echo=True)


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.on_event("startup")
    async def on_startup():
        if RESET_DB_ON_START:
            await reset_database(engine)

        if RESET_COOKIE_ON_START:
            await clear_all_cookies()

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)