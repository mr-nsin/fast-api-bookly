from fastapi import APIRouter, Depends, status, HTTPException
from src.auth.schemas import UserCreateModel, UserModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession


auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
        '/signup',
        response_model=UserModel,
        status_code=status.HTTP_201_CREATED
    )
async def create_user_account(
        user: UserCreateModel,
        session: AsyncSession=Depends(get_session)
    ):
    email = user.email
    if await user_service.user_exists(email, session):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {email} already exists"
        )
    else:
        new_user = await user_service.create_user(user, session)
        return new_user