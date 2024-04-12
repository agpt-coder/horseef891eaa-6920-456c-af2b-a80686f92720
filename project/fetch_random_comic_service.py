from datetime import datetime

import httpx
from pydantic import BaseModel


class RandomComicResponse(BaseModel):
    """
    The response model for the fetch_random_comic endpoint, providing details of the random comic fetched from XKCD.
    """

    comic_id: int
    title: str
    img_url: str
    alt_text: str
    date_published: str


async def fetch_random_comic() -> RandomComicResponse:
    """
    Fetches a random XKCD comic for display to the user.

    Args:


    Returns:
    RandomComicResponse: The response model for the fetch_random_comic endpoint, providing details of the random comic fetched from XKCD.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://xkcd.com/info.0.json")
        if response.status_code != 200:
            raise Exception("Error fetching the current XKCD comic.")
        current_comic_data = response.json()
        max_comic_num = current_comic_data["num"]
        import random

        random_comic_num = random.randint(1, max_comic_num)
        comic_response = await client.get(
            f"https://xkcd.com/{random_comic_num}/info.0.json"
        )
        if comic_response.status_code != 200:
            raise Exception(f"Error fetching XKCD comic number {random_comic_num}.")
        comic_data = comic_response.json()
        return RandomComicResponse(
            comic_id=comic_data["num"],
            title=comic_data["title"],
            img_url=comic_data["img"],
            alt_text=comic_data["alt"],
            date_published=datetime(
                year=int(comic_data["year"]),
                month=int(comic_data["month"]),
                day=int(comic_data["day"]),
            ).strftime("%Y-%m-%d"),
        )
