from fastapi import Depends, APIRouter

from dependencies import get_db
from src.models.schemas import QuizQuestion
from sqlalchemy.orm import Session
import security

router = APIRouter(prefix="/questions", tags=["questions"],)


@router.get("/", response_model=QuizQuestion)
def get_question_for_user(db: Session = Depends(get_db), current_user_id: int = Depends(security.get_current_user_id)):
    return QuizQuestion(question="Какая сложность у сортировки пузырьком?", answer="O(n^2)")
