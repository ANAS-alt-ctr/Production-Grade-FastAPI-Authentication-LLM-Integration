import requests
from fastapi import APIRouter, Depends
from routes.protected_routes import get_current_user

router = APIRouter()

from core.config import GEMINI_API_KEY

@router.post("/ask-llm")
def ask_llm(prompt: str, user = Depends(get_current_user)):

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}",
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
    )

    data = response.json()

    if "error" in data:
        error_msg = data.get("error", {}).get("message", "LLM request failed")
        from fastapi import HTTPException
        raise HTTPException(status_code=502, detail=error_msg)

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        from fastapi import HTTPException
        raise HTTPException(status_code=502, detail="Invalid LLM response shape")

    return {
        "response": text
    }