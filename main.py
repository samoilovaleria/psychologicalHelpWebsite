from fastapi import FastAPI
from fastapi.responses import Response
from src.routes.routes import api_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from src.config.database import Base, config, RESET_DB_ON_START, RESET_COOKIE_ON_START

# # Определяем базу для моделей
# Base = declarative_base()

# Функция для сброса и пересоздания таблиц
async def reset_database(engine: AsyncEngine):
    async with engine.begin() as conn:
        # Удаление всех таблиц
        # print("Удаление всех таблиц...")
        await conn.run_sync(Base.metadata.drop_all)
        
        # Создание новых таблиц
        # print("Создание таблиц...")
        await conn.run_sync(Base.metadata.create_all)

    # print("Таблицы успешно пересозданы.")


async def clear_all_cookies():
    # Здесь устанавливаем пустые cookie с истекшим временем
    response = Response()
    cookies_to_clear = ["access_token"]  # Добавьте имена cookie, которые хотите очистить

    for cookie in cookies_to_clear:
        response.delete_cookie(
            key=cookie,
            httponly=True,
            secure=False,  # Установите в False для локального тестирования
            samesite="Lax",  # Используем "Lax" для лучшей совместимости
        )

    # print("Все cookie успешно очищены при запуске приложения.")


# Создаем асинхронный движок подключения
engine = create_async_engine(config.DATABASE_URL, echo=True)


def get_application() -> FastAPI:
    # TODO:
    # application = FastAPI(
    #     title=settings.PROJECT_NAME,
    #     debug=settings.DEBUG,
    #     version=settings.VERSION
    # )
    application = FastAPI()
    application.include_router(api_router)

    application.add_middleware(
        CORSMiddleware,
        # TODO:
        # allow_origins=settings.CORS_ALLOWED_ORIGINS.split(" "),
        allow_origins=["*"],  # Разрешить все домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Добавляем обработчик события startup
    @application.on_event("startup")
    async def on_startup():
        # Вызов функции сброса и создания таблиц
        if RESET_DB_ON_START:
            await reset_database(engine)

        # Очищаем все cookie
        if RESET_COOKIE_ON_START:
            await clear_all_cookies()

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)