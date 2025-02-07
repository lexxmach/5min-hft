from common.repo.repository import DatabaseRepository
from cruds import crud_credentials, crud_users
import security
from fastapi import Depends, APIRouter, HTTPException
import requests

from dependencies import get_repo, serializer, TELEGRAM_TOKEN, ADMIN_CHAT_ID


router = APIRouter(prefix="/admin", tags=["admin"])

def send_telegram_message(login: str, token: str):
    BOT_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": f"Requested an admin access for the username {login}",
        "reply_markup": {
            "inline_keyboard": [[{"text": "✅ Approve", "callback_data": token}]]
        },
    }
    requests.post(BOT_API_URL, json=payload)


@router.post("/request-access", response_model=None)
async def request_access(repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    user_login = crud_credentials.get_credentials_by_user_id(repo, current_user_id).login
    
    token = serializer.dumps(user_login)
    
    send_telegram_message(user_login, token)
    
    return {"message": "The message has been sent!"}
