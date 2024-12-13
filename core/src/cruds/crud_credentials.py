from pydantic import ValidationError
from sqlalchemy.orm import Session

from models.schemas import CredentialsModel
from models.models import Credentials

def get_credentials_by_credentials_id(db: Session, credentials_id: int) -> Credentials:
    return None


def get_credentials_by_user_id(db: Session, user_id: int) -> Credentials:
    return None


def get_credentials_id_by_login(db: Session, login : str) -> Credentials:
    return None


def get_user_id_by_login(db: Session, login : str) -> int:
    return None


def create_user(db: Session, credentials: CredentialsModel) -> int:
    return 0


def delete_credentials(db: Session, credentials_id: int) -> Credentials:
    return Credentials()