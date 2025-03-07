from src.auth.models import User
from src.auth.utils import gen_pass_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.auth.schemas import UserRequestModel
from src.auth.models import User

class UserService:
    async def get_user_by_email(
            self,
            email:str,
            session: AsyncSession
        ):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        return user if user is not None else None
    
    
    async def user_exists(
            self,
            email,
            session: AsyncSession
        ):
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False
    

    async def create_user(
            self,
            user_data: UserRequestModel,
            session: AsyncSession
        ):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)
    
        new_user.password = gen_pass_hash(user_data_dict['password'])
        new_user.role = 'user'

        session.add(new_user)
        await session.commit()
        return new_user
    