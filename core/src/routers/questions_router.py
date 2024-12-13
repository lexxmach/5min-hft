from cruds import crud_questions
from fastapi import Depends, APIRouter, HTTPException

from dependencies import get_db
from models.schemas import QuizQuestion, UserAnswer
from sqlalchemy.orm import Session

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=QuizQuestion)
def get_question_for_user(db: Session = Depends(get_db)):
    # Fetch a question not yet answered by the user
    question, options = crud_questions.get_question_by_user_id(db, 1)
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return QuizQuestion(
        id=question.id,
        question=question.text,
        type=question.type,
        options=options,
        difficulty=question.difficulty,
        category=question.category,
    )


@router.post("/", status_code=201)
def submit_answer(user_answer: UserAnswer, db: Session = Depends(get_db)):
    history_entry = crud_questions.create_history_entry(db, user_answer)
    
    if not history_entry:
        raise HTTPException(status_code=404, detail="Something went wrong with submitting the answerl")

    return {"message": "Answer submitted successfully", "is_answer_correct": history_entry.correctly_answered}
