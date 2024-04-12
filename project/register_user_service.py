from typing import List

import prisma
import prisma.enums
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class UserPreferences(BaseModel):
    """
    Represents user-defined settings and preferences.
    """

    excludeNSFW: bool
    preferredTags: List[str]


class RegisterUserResponse(BaseModel):
    """
    Response model indicating the result of the user registration process.
    """

    userId: str
    message: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_user(
    email: str, password: str, preferences: UserPreferences
) -> RegisterUserResponse:
    """
    Registers a new user in the system.

    Args:
        email (str): Email address for the user, used as a unique identifier.
        password (str): Password for the user account. Should be securely hashed before storage.
        preferences (UserPreferences): Optional preferences the user can set at the time of registration.

    Returns:
        RegisterUserResponse: Response model indicating the result of the user registration process.
    """
    hashed_password = pwd_context.hash(password)
    user = await prisma.models.User.prisma().create(
        data={
            "email": email,
            "hashedPassword": hashed_password,
            "role": prisma.enums.UserRole.SUBSCRIBER,
            "preferences": {
                "create": {
                    "excludeNSFW": preferences.excludeNSFW,
                    "preferredTags": {
                        "connectOrCreate": [
                            {"where": {"name": tag}, "create": {"name": tag}}
                            for tag in preferences.preferredTags
                        ]
                    },
                }
            },
        }
    )
    return RegisterUserResponse(userId=user.id, message="User registered successfully.")
