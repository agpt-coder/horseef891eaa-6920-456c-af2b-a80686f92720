from enum import Enum
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class User(BaseModel):
    """
    This type represents the user's public profile information, excluding sensitive data like passwords.
    """

    id: str
    email: str
    username: str
    avatarUrl: Optional[str] = None
    role: prisma.enums.UserRole


class AuthenticateUserOutput(BaseModel):
    """
    The response model for the authentication process, indicating whether the authentication was successful, and including user data or error messages as appropriate.
    """

    success: bool
    message: str
    user: Optional[User] = None


async def get_user_by_email(email: str) -> Optional[prisma.models.User]:
    """
    Retrieve a user from the database by their email address.

    This function uses Prisma Client to query the database for a user by their email.
    It will return the user object if found, otherwise, it will return None.
    This is useful in operations where identifying a user by their email is crucial,
    such as authentication, sending emails, or user profile management.

    Args:
        email (str): The email address of the user to retrieve.

    Returns:
        Optional[prisma.models.User]: The user if found, else None.

    Example:
        user = await get_user_by_email('jane.doe@example.com')
        if user:
            print(f"User found: {user.email}")
        else:
            print("No user found with that email.")
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    return user


class UserRole(Enum):
    ADMIN: str = "ADMIN"
    SUBSCRIBER: str = "SUBSCRIBER"
    GUEST: str = "GUEST"


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if input plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, else False.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: str, password: str) -> AuthenticateUserOutput:
    """
    Authenticates a user allowing them to log in.

    Args:
    email (str): The email address of the user attempting to authenticate. Used as the primary identification credential in the authentication process.
    password (str): The password input by the user for the authentication process. It will be validated against the hashed password stored in the database.

    Returns:
    AuthenticateUserOutput: The response model for the authentication process, indicating whether the authentication was successful, and including user data or error messages as appropriate.
    """
    user = await get_user_by_email(email)
    if not user:
        return AuthenticateUserOutput(success=False, message="User not found.")
    user_data = user.dict()
    if not await verify_password(password, user_data["hashedPassword"]):
        return AuthenticateUserOutput(success=False, message="Incorrect password.")
    user_data.pop("hashedPassword", None)
    safe_user = User(**user_data)
    return AuthenticateUserOutput(
        success=True, message="Authentication successful.", user=safe_user
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
