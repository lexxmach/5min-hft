from common.repo.repository import DatabaseRepository
from cruds import crud_questions, crud_users
from fastapi import Depends, APIRouter, HTTPException, status
from models.schemas import CredentialsModel, Leaderboard, UserModel, UserRegister, Token, UserStats
from dependencies import get_repo
from sqlalchemy.orm import Session


router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/", response_model=Leaderboard)
def get_user_stats(repo: DatabaseRepository = Depends(get_repo)):
    sorted_users_by_category = crud_users.get_leaderboard_by_category(repo)
    total_question_by_category = crud_questions.get_total_question_by_category(repo)
    
    if sorted_users_by_category is None or total_question_by_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong with getting the stats")

    return Leaderboard(sorted_users_by_category=sorted_users_by_category,
                    total_questions_by_category_count=total_question_by_category)