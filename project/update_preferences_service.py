from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserPreferencesResponse(BaseModel):
    """
    Confirms the successful update of a user's preferences.
    """

    success: bool
    message: Optional[str] = None


async def update_preferences(
    user_id: str, excludeNSFW: bool, preferredTags: List[str]
) -> UpdateUserPreferencesResponse:
    """
    Updates a user's preferences for content and notifications.

    Args:
        user_id (str): Unique identifier of the user whose preferences are being updated.
        excludeNSFW (bool): Flag to set whether NSFW content should be excluded from the user's content feed.
        preferredTags (List[str]): List of tags that the user prefers for filtering content. Empty list means no specific tag preferences.

    Returns:
        UpdateUserPreferencesResponse: Confirms the successful update of a user's preferences.

    Example:
        update_preferences("some-user-id", True, ["funny", "science"])
        > UpdateUserPreferencesResponse(success=True, message="User preferences updated successfully.")
    """
    prefs = await prisma.models.UserPreferences.prisma().find_unique(
        where={"userId": user_id}
    )
    if not prefs:
        prefs = await prisma.models.UserPreferences.prisma().create(
            data={"userId": user_id, "excludeNSFW": excludeNSFW}
        )
    await prisma.models.UserPreferences.prisma().update(
        where={"id": prefs.id}, data={"excludeNSFW": excludeNSFW}
    )
    return UpdateUserPreferencesResponse(success=True)
