from pydantic import ValidationError
from cruds import crud_users

from models.schemas import CredentialsModel, UserModel
from models.models import Credentials
from common.repo.repository import DatabaseRepository


def get_credentials_by_user_id(repo: DatabaseRepository, user_id: int) -> Credentials:
    credentials = repo.filter(Credentials.user_id == user_id, model=Credentials)
    if not credentials:
        return None
    return credentials[0]


def get_credentials_id_by_login(repo: DatabaseRepository, login: str) -> Credentials:
    credentials = repo.filter(Credentials.login == login, model=Credentials)
    if not credentials:
        return None
    return credentials[0]


def get_user_id_by_login(repo: DatabaseRepository, login: str) -> int:
    credentials = repo.filter(Credentials.login == login, model=Credentials)
    if not credentials:
        return None
    return credentials[0].user_id


def create_user(
    repo: DatabaseRepository, user_info: UserModel, credentials: CredentialsModel
) -> int:
    user_id = crud_users.create_user(repo, user_info)
    if user_id is None:
        return None
    try:
        db_cred = {
            "user_id": user_id,
            "login": credentials.login,
            "password_hash": credentials.password_hash}
        
    except ValidationError:
        return None
    new_cred = repo.create(db_cred, model=Credentials)
    return new_cred.user_id
