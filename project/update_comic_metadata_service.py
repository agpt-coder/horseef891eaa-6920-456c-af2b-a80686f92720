import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateComicMetadataResponse(BaseModel):
    """
    Response model for confirming the update of a comic's metadata. Contains a success flag and optionally, an error message.
    """

    success: bool
    error: Optional[str] = None


async def update_comic_metadata(
    id: str,
    title: Optional[str],
    imgUrl: Optional[str],
    pubDate: Optional[str],
    isNSFW: Optional[bool],
) -> UpdateComicMetadataResponse:
    """
    Updates the comic metadata in the database.

    Args:
    id (str): The unique identifier of the comic to be updated.
    title (Optional[str]): The new title of the comic.
    imgUrl (Optional[str]): The new URL for the comic's image.
    pubDate (Optional[str]): The publication date of the comic.
    isNSFW (Optional[bool]): Flag to indicate if the comic is NSFW.

    Returns:
    UpdateComicMetadataResponse: Response model for confirming the update of a comic's metadata. Contains a success flag and optionally, an error message.
    """
    try:
        comic_data = {}
        if title is not None:
            comic_data["title"] = title
        if imgUrl is not None:
            comic_data["imgUrl"] = imgUrl
        if pubDate is not None:
            comic_data["pubDate"] = datetime.datetime.strptime(pubDate, "%Y-%m-%d")
        if isNSFW is not None:
            comic_data["isNSFW"] = isNSFW
        if not comic_data:
            return UpdateComicMetadataResponse(
                success=False, error="No data provided for update"
            )
        comic = await prisma.models.Comic.prisma().update(
            where={"id": id}, data=comic_data
        )
        if comic:
            return UpdateComicMetadataResponse(success=True)
        else:
            return UpdateComicMetadataResponse(success=False, error="Comic not found")
    except Exception as e:
        return UpdateComicMetadataResponse(success=False, error=str(e))
