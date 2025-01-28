from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from models.models import Users
from schemas.users_schemas import SingUpUser, UserResponse
from services.users_services import hash_password


async def get_user(session: AsyncSession):
    pass

async def sing_up_user(session: AsyncSession, data: SingUpUser):
    try:
        data_for_db = Users(
            email=data.email,
            phone=data.phone,
            password=hash_password(data.password).decode('utf-8'),
            first_name=data.first_name,
            second_name=data.second_name
            )
        session.add(data_for_db)
        await session.commit()
        await session.refresh(data_for_db)
        return data_for_db.user_id
    except:
        return False
    
async def get_user_by_email(session: AsyncSession, email: str):
    try:
        stmt = select(Users).where(Users.email == email)
        result: Result = await session.execute(stmt)
        return result.scalar_one_or_none()
    except:
        return None
    
async def get_user_without_pass(session: AsyncSession, user_id: int):
    try:
        stmt = select(Users).where(Users.user_id == user_id)
        result: Result = await session.execute(stmt)
        data = result.scalar_one_or_none()
        if data is None:
            return None
        return UserResponse(user_id = data.user_id, 
                            email = data.email,
                            first_name = data.first_name,
                            second_name = data.second_name,
                            phone = data.phone
                            )
    except:
        return None