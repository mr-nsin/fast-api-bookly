from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.utils import decode_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from src.auth.service import UserService
from typing import List, Any
from src.auth.models import User

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


class RoleChecker:
    """
    A dependency class for FastAPI to check if the current user has one of the allowed roles.
    Attributes:
        allowed_roles (List[str]): A list of roles that are allowed to access the endpoint.
    Methods:
        __init__(allowed_roles: List[str]):
            Initializes the RoleChecker with the allowed roles.
        __call__(user: User = Depends(get_current_user)) -> Any:
            Checks if the current user's role is in the list of allowed roles.
            Raises an HTTPException with status code 403 if the user does not have permission.
    """

    def __init__(self, allowed_roles: List[str]):
        """
        Initialize the dependency with a list of allowed roles.

        Args:
            allowed_roles (List[str]): A list of roles that are allowed to access certain resources.
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, user : User = Depends(get_current_user)) -> Any:
        """
        Checks if the current user has the required role to perform an action.

        Args:
            user (User): The current user, obtained from the dependency injection.

        Raises:
            HTTPException: If the user's role is not in the allowed roles, a 403 Forbidden error is raised.

        Returns:
            Any: Returns True if the user has the required role.
        """
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'You do not have permission to perform this action'
            )
        return True