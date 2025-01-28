from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users_schemas import SingUpUser, SingInUser
from app.databases.postgresdb import get_session
from app.cruds import users_crud
from app.services.users_services import validate_password, sign_jwt, dependencies, get_user_id_from_token



router = APIRouter(prefix="/users")


@router.post("/sing_up")
async def sing_up(
    data: SingUpUser,
    session: AsyncSession = Depends(get_session),
):
    user_id = await users_crud.sing_up_user(session=session, data=data)
    if user_id:
        token = sign_jwt(data={'user_id': user_id})
        return JSONResponse(status_code=200, content={
            'message': "Успешная регистрация",
            'token': f"Bearer {token}",
            })
    raise HTTPException(status_code=500, detail="Ошибка при регистрации")


@router.post_("/sing_in")
async def sing_in(
    data: SingInUser,
    session: AsyncSession = Depends(get_session),
):
    user = await users_crud.get_user_by_email(session=session, email=data.email)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if not validate_password(data.password, user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    return JSONResponse(status_code=200, content="Успешный вход")

@router.get("/me", dependencies=dependencies)
async def get_user_me(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    me = await users_crud.get_user_without_pass(session=session, user_id=get_user_id_from_token(request))
    if me:
        return JSONResponse(
            status_code=200,
            content=me,
        )
    raise HTTPException(status_code=404, detail="Пользователь не найден (невалидный токен)")