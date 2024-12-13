from pydantic import ValidationError
from sqlalchemy.orm import Session

from models.schemas import UserModel
from models.models import UserData


def create_user(db : Session, user_info: UserModel) -> int:
    try:
        db_user = UserData(name=user_info.name, surname=user_info.surname)
    except ValidationError:
        return None
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id

def get_user_by_user_id(db: Session, user_id: int) -> UserData:
    return db.query(UserData).filter(UserData.id == user_id).first()
