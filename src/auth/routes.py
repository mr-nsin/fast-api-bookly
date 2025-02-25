from fastapi import APIRouter, Depends, status, HTTPException
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from utils import create_access_token, decode_token, verify_pass
from fastapi.responses import JSONResponse

from datetime import timedelta

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2

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
    

@auth_router.post(
        '/login',
        status_code=status.HTTP_200_OK
    )
async def login_users(
        login_user: UserLoginModel,
        session: AsyncSession=Depends(get_session)
    ):    
    email = login_user.email
    password = login_user.password

    user = await user_service.get_user_by_email(email, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
    elif not verify_pass(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    else:
        access_token = create_access_token(user_data = {'email': user.email, 
                                                        'user_uid': str(user.uid)}, expiry=None)
        refresh_token = create_access_token(user_data = {'email': user.email, 
                                                        'user_uid': str(user.uid)}, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY), refresh=True)
        return JSONResponse(content={'message': 'Login successful', 'access_token': access_token, 'refresh_token': refresh_token, 'user': {'email': user.email, 'uid': str(user.uid)}})