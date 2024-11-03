from pydantic import ValidationError
from sqlalchemy.orm import Session

from models.schemas import CredentialsModel
from models.models import Credentials
from cruds import crud_users

def get_credentials_by_credentials_id(db: Session, credentials_id: int) -> Credentials:
    return db.query(Credentials).filter(Credentials.credentials_id == credentials_id).first()


def get_credentials_by_user_id(db: Session, user_id: int) -> Credentials:
    return db.query(Credentials).filter(Credentials.user_id == user_id).first()


def get_credentials_id_by_login(db: Session, login : str) -> Credentials:
    return db.query(Credentials).filter(Credentials.login == login).first()


def get_user_id_by_login(db: Session, login : str) -> int:
    credentials = db.query(Credentials).filter(Credentials.login == login).first()
    if credentials is not None:
        return credentials.user_id
    return None


def create_user(db: Session, credentials: CredentialsModel) -> int:
    user_id = crud_users.create_user(db)
    try:
        db_cred = Credentials(user_id=user_id, login=credentials.login, 
                                password_hash=credentials.password_hash)
    except ValidationError:
        return None
    db.add(db_cred)
    db.commit()
    db.refresh(db_cred)
    return db_cred.user_id


def delete_credentials(db: Session, credentials_id: int) -> Credentials:
    credentials = get_credentials_by_credentials_id(credentials_id)
    db.delete(credentials)
    db.commit()
    db.close()
    return credentials