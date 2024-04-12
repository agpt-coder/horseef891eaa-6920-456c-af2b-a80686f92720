import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import project.authenticate_user_service
import project.fetch_random_comic_service
import project.register_user_service
import project.request_ai_explanation_service
import project.update_comic_metadata_service
import project.update_preferences_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="horse",
    lifespan=lifespan,
    description="To build a tool that returns a random xkcd comic and uses GPT-4-Vision to explain it, we would take the following approach using the specified tech stack: Python, FastAPI, PostgreSQL, and Prisma. Our solution comprises several components to meet the outlined requirements and preferences.\n\n1. **Fetching Random XKCD Comics:** Utilize the XKCD API endpoint ('https://xkcd.com/random/comic/') to fetch a random comic. This will involve sending a GET request to the URL, which will redirect to a random comic page from where we can parse the comic image URL and metadata.\n\n2. **Explaining Comics Using GPT-4-Vision:** Although a hypothetical scenario, assuming GPT-4-Vision's availability, integrate it by sending the comic image to the AI model via an API call. Using the response, which would include a description or explanation of the comic based on its visual content and themes, present this information to the user alongside the comic image.\n\n3. **Filtering and Safety Features:** Implement functionality allowing users to filter comics based on themes or tags and exclude explicit/NSFW content using metadata provided by XKCD or inferred by GPT-4-Vision analysis.\n\n4. **User Subscriptions and Recommendations:** Create a system where users can subscribe to notifications for new comics. Leveraging user interaction data and GPT-4-Vision's analysis of comic themes and visuals, develop a recommendation algorithm to suggest comics that align with individual tastes and previous likes.\n\n5. **Sharing and Community Engagement:** Enable direct sharing of comics from the generator to social media platforms or via email, fostering community interaction and engagement.\n\nThe backend service, built with FastAPI, will handle API requests and interactions, serving as the core of the tool. Data concerning user preferences, subscription details, and comic metadata will be stored in a PostgreSQL database, managed by Prisma ORM for efficient and simplified database operations.\n\nThis comprehensive approach ensures the tool is not only functional but also engaging and user-centered, aligning with the features and functionalities you've specified.",
)


@app.post(
    "/user/register", response_model=project.register_user_service.RegisterUserResponse
)
async def api_post_register_user(
    email: str,
    password: str,
    preferences: project.register_user_service.UserPreferences,
) -> project.register_user_service.RegisterUserResponse | Response:
    """
    Registers a new user in the system.
    """
    try:
        res = await project.register_user_service.register_user(
            email, password, preferences
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/comics/{id}/update",
    response_model=project.update_comic_metadata_service.UpdateComicMetadataResponse,
)
async def api_post_update_comic_metadata(
    id: str,
    title: Optional[str],
    imgUrl: Optional[str],
    pubDate: Optional[str],
    isNSFW: Optional[bool],
) -> project.update_comic_metadata_service.UpdateComicMetadataResponse | Response:
    """
    Updates the comic metadata in the database.
    """
    try:
        res = await project.update_comic_metadata_service.update_comic_metadata(
            id, title, imgUrl, pubDate, isNSFW
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/explanation/request",
    response_model=project.request_ai_explanation_service.AIExplanationResponse,
)
async def api_post_request_ai_explanation(
    comic_id: str, comic_url: str
) -> project.request_ai_explanation_service.AIExplanationResponse | Response:
    """
    Requests an AI-generated explanation for a specific comic.
    """
    try:
        res = await project.request_ai_explanation_service.request_ai_explanation(
            comic_id, comic_url
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/comics/random",
    response_model=project.fetch_random_comic_service.RandomComicResponse,
)
async def api_get_fetch_random_comic() -> project.fetch_random_comic_service.RandomComicResponse | Response:
    """
    Fetches a random XKCD comic for display to the user.
    """
    try:
        res = await project.fetch_random_comic_service.fetch_random_comic()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/preferences/update",
    response_model=project.update_preferences_service.UpdateUserPreferencesResponse,
)
async def api_put_update_preferences(
    user_id: str, excludeNSFW: bool, preferredTags: List[str]
) -> project.update_preferences_service.UpdateUserPreferencesResponse | Response:
    """
    Updates a user's preferences for content and notifications.
    """
    try:
        res = await project.update_preferences_service.update_preferences(
            user_id, excludeNSFW, preferredTags
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/authenticate",
    response_model=project.authenticate_user_service.AuthenticateUserOutput,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserOutput | Response:
    """
    Authenticates a user allowing them to log in.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
