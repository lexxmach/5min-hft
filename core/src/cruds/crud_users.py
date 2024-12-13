from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import func


from models.schemas import UserModel, UserStatWithInCategory
from models.models import History, Questions, UserData


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

def get_leaderboard_by_category(db: Session):
    raw_leaderboard = (
        db.query(
            Questions.category,
            UserData.id.label('user_id'),
            UserData.name,
            UserData.surname,
            func.count(History.id).label('tasks_solved')
        )
        .join(History, History.question_id == Questions.id)
        .join(UserData, History.user_id == UserData.id)
        .filter(History.correctly_answered == True)
        .group_by(Questions.category, UserData.id, UserData.name, UserData.surname)
        .order_by(Questions.category, func.count(History.id).desc())
        .all()
    )
    
    leaderboard = {}
    for entry in raw_leaderboard:
        category = entry.category
        user_data = UserStatWithInCategory(user_id=entry.user_id,
            name=entry.name,
            surname=entry.surname,
            tasks_solved=entry.tasks_solved)
        if category not in leaderboard:
            leaderboard[category] = []
        leaderboard[category].append(user_data)

    return leaderboard