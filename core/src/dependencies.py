import os
from typing import Callable
from common.repo.repository import DatabaseRepository
from common.repo.session import get_repository_callable
from models import database
from sqlalchemy.orm import Session
from itsdangerous import URLSafeSerializer
from dotenv import load_dotenv



get_repo: Callable[[Session], DatabaseRepository] = get_repository_callable(database.engine)

serializer = URLSafeSerializer("supersecretkey")

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID'))