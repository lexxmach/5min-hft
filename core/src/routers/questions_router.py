from common.repo.repository import DatabaseRepository
from cruds import crud_users
from models.enums import QuestionType
import security
from cruds import crud_questions
from fastapi import Depends, APIRouter, HTTPException, status

from dependencies import get_repo
from models.schemas import QuizQuestion, SubmitNewQuestion, UserAnswer, QuestionRequest, SubmitAnswerResponse

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=QuizQuestion)
def get_question_for_user(question_type: QuestionType = None, difficulty: int = None, category: str = None, room_id: int=None, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    # Fetch a question not yet answered by the user
    question, options = crud_questions.get_question_by_parameters(repo, current_user_id, QuestionRequest(type=question_type, difficulty=difficulty, category=category, room_id=room_id, session_id=None))
    
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

@router.get("/by-id", response_model=QuizQuestion)
def get_question_by_id(question_id: int, repo: DatabaseRepository = Depends(get_repo)):
    question, correct_answers, answers = crud_questions.get_question_by_id(repo, question_id)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question with this id does not exist")
    return QuizQuestion(
        id=question.id,
        question=question.text,
        type=question.type,
        options=answers,
        difficulty=question.difficulty,
        category=question.category,
    )
    

@router.post("/submit-answer", status_code=status.HTTP_201_CREATED, response_model=SubmitAnswerResponse)
def submit_answer(user_answer: UserAnswer, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    history_entry = crud_questions.create_history_entry(repo, current_user_id, user_answer)
    question, correct_answers, answers = crud_questions.get_question_by_id(repo, user_answer.question_id)
    
    if history_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong with submitting the answer")

    return SubmitAnswerResponse(is_answer_correct=history_entry.correctly_answered, 
                                hint=question.hint,
                                correct_answers=correct_answers)


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=int)
def create_new_question(new_question: SubmitNewQuestion, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    if not crud_users.is_user_root(repo, current_user_id):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not a root.")
    question = crud_questions.create_question(repo, new_question)
    return question.id
    

@router.delete("/")
def clear_history_for_user(repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    deleted_entries = crud_questions.clear_history_for_user(repo, current_user_id)
    return {"message": f"{deleted_entries} deleted successfully for the user id {current_user_id}"}
