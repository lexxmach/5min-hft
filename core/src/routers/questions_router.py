from models.enums import QuestionType
import security
from cruds import crud_questions
from fastapi import Depends, APIRouter, HTTPException, status

from dependencies import get_db
from models.schemas import QuizQuestion, UserAnswer, QuestionRequest
from sqlalchemy.orm import Session

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=QuizQuestion)
def get_question_for_user(question_type: QuestionType = None, difficulty: int = None, category: str = None, db: Session = Depends(get_db), current_user_id: int = 1):
    # Fetch a question not yet answered by the user
    question, options = crud_questions.get_question_by_parameters(db, current_user_id, QuestionRequest(type=question_type, difficulty=difficulty, category=category))
    
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    
    return QuizQuestion(
        id=question.id,
        question=question.text,
        type=question.type,
        options=options,
        difficulty=question.difficulty,
        category=question.category,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_answer(user_answer: UserAnswer, db: Session = Depends(get_db), current_user_id: int = 1):
    history_entry = crud_questions.create_history_entry(db, current_user_id, user_answer)
    
    if history_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong with submitting the answer")

    return {"message": "Answer submitted successfully", "is_answer_correct": history_entry.correctly_answered}
