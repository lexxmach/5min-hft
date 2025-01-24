from typing import Callable
from common.repo.repository import DatabaseRepository
from common.repo.session import get_repository_callable
from models import database
from sqlalchemy.orm import Session


get_repo: Callable[[Session], DatabaseRepository] = get_repository_callable(database.engine)