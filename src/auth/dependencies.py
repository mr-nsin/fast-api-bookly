from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.utils import decode_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from src.auth.service import UserService

user_service = UserService()

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creds = await super().__call__(request)

        token = creds.credentials

        # Checking if token is valid
        if not self.token_valid(token):
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Invalid or expired token"
            )
    
        token_data = decode_token(token)

        # Checking if token is in blocklist
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = {"error": "This token is invalid or expired", "resolution": "Please get new token"}
            )
        

        # Checking if token is access or refresh token
        self.verify_token_data(token_data)
        
        return token_data
    
    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return token_data is not None

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError('Please Override this method in child classes')

        
class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'Please provide an access token'
            )

class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'Please provide an refresh token'
            )



async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)
    ):
    user_email = token_details['email']
    user = await user_service.get_user_by_email(user_email, session)
    return user