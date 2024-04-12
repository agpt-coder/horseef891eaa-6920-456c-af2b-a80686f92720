from typing import Optional

import httpx
import prisma
import prisma.models
from pydantic import BaseModel


class AIExplanationResponse(BaseModel):
    """
    Encapsulates the AI-generated explanation for the requested comic.
    """

    comic_id: str
    explanation: str
    additional_info: Optional[str] = None


async def request_ai_explanation(
    comic_id: str, comic_url: str
) -> AIExplanationResponse:
    """
    Requests an AI-generated explanation for a specific comic.

    Args:
    comic_id (str): The unique identifier of the comic for which an explanation is requested.
    comic_url (str): The URL link to the comic image, required by GPT-4-Vision for analysis.

    Returns:
    AIExplanationResponse: Encapsulates the AI-generated explanation for the requested comic.
    """
    gpt_4_vision_api_url = "https://gpt-4-vision-api-url.com/analyze"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            gpt_4_vision_api_url, json={"image_url": comic_url}
        )
        response.raise_for_status()
        analysis = response.json()
    explanation = analysis.get("explanation", "Explanation unavailable.")
    additional_info = analysis.get("additional_info", None)
    ai_explanation_request = await prisma.models.AIExplanationRequest.prisma().create(
        data={
            "comicId": comic_id,
            "requestId": response.headers["x-request-id"],
            "response": explanation,
        }
    )
    return AIExplanationResponse(
        comic_id=comic_id, explanation=explanation, additional_info=additional_info
    )
