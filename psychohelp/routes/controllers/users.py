from fastapi import HTTPException, APIRouter, Request, Response

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from psychohelp.services.users import (
    get_user_by_id,
    get_user_by_email,
    get_user_by_token,
    login_user,
    register_user,
    UUID,
)
from psychohelp.schemas.users import (
    UserBase,
    LoginRequest,
    UserCreateRequest,
    TokenResponse,
    UserResponse,
    EmailStr,
)
from . import set_token_in_cookie


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/user", response_model=UserResponse)
async def user_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован"
        )
    user = await get_user_by_token(token)

    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )

    return user


@router.get("/user/{id}", response_model=UserResponse)
async def user(id: EmailStr | UUID):
    user = None

    if isinstance(id, UUID):
        user = await get_user_by_id(id)
    else:
        user = await get_user_by_email(id)

    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )

    return user


@router.post("/register", response_model=UserResponse)
async def register_users(user_data: UserCreateRequest, response: Response):
    try:
        user, token = await register_user(**user_data.model_dump())
        set_token_in_cookie(response, token)
        response.status_code = HTTP_201_CREATED
    except ValueError as e:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    return user


@router.post("/login", response_model=UserResponse)
async def login(data: LoginRequest, response: Response):
    user, token = await login_user(data.email, data.password)
    if token is None or not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль"
        )

    set_token_in_cookie(response, token)
    response.status_code = HTTP_200_OK

    return user


@router.post("/logout")
async def logout(request: Request, response: Response):
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован"
        )

    response.delete_cookie("access_token")
    response.status_code = HTTP_200_OK
