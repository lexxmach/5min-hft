from pydantic import ValidationError
from common.repo.repository import DatabaseRepository
from sqlalchemy import func


from models.schemas import UserModel, UserStatWithInCategory
from models.models import History, Questions, UserData


def create_user(repo: DatabaseRepository, user_info: UserModel) -> int:
    try:
        db_user = {"name": user_info.name, "surname": user_info.surname, "is_root": False}
    except ValidationError:
        return None
    created_user = repo.create(db_user, model=UserData)
    return created_user.id


def get_user_by_user_id(repo: DatabaseRepository, user_id: int) -> UserData:
    user = repo.filter(UserData.id == user_id, model=UserData)
    if not user:
        return None
    return user[0]


def get_leaderboard_by_category(repo: DatabaseRepository):
    raw_leaderboard = (
        repo.session.query(
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

def is_user_root(repo: DatabaseRepository, user_id: int):
    user = get_user_by_user_id(repo, user_id)
    return user.is_root


def make_user_root(repo: DatabaseRepository, user_id: int):
    repo.update(UserData.id == user_id, data={"is_root": True}, model=UserData)