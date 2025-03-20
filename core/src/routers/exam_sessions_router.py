import security
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from dependencies import get_repo
from common.repo.repository import DatabaseRepository
from cruds import crud_exam_sessions, crud_rooms, crud_questions
from models.schemas import ExamSessionResponse, QuestionStatusInSessionResult, SessionResult, SubmitAnswerResponse, UserAnswer

router = APIRouter(prefix="/exam_sessions", tags=["exam sessions"])


@router.post("/start/{rood_id}", response_model=ExamSessionResponse)
def start_exam(room_id: int, duration_seconds: int = 10 * 60, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    room = crud_rooms.get_room_by_id(repo, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found.")

    session = crud_exam_sessions.get_active_session(repo, current_user_id)
    if session is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is already an active session.")   
    
    session = crud_exam_sessions.create_exam_session(repo, user_id=current_user_id, room_id=room_id, duration_seconds=duration_seconds)

    if session is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to start the exam session.")

    return ExamSessionResponse(session_id=session.id, room_id=session.room_id, user_id=session.user_id,
                               start_time=session.start_time, duration=session.duration)


@router.get("/question")
def get_question(repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    session = crud_exam_sessions.get_active_session(repo, current_user_id)

    if session is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active exam session found.")

    time_left = crud_exam_sessions.get_time_left(repo, session.id)
    if time_left == 0:
        crud_exam_sessions.mark_session_completed(repo, session.id)
        return RedirectResponse(f"/exam_sessions/results/{session.id}")
    
    return RedirectResponse(f"/questions/?room_id={session.room_id}")


@router.post("/submit-answer/{session_id}", status_code=status.HTTP_201_CREATED, response_model=SubmitAnswerResponse)
def submit_answer(user_answer: UserAnswer, session_id: int, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    session = crud_exam_sessions.get_active_session(repo, current_user_id)
    if session is None or session.id != session_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active exam session found: check the session id.")
    time_left = crud_exam_sessions.get_time_left(repo, session.id)
    if time_left == 0:
        crud_exam_sessions.mark_session_completed(repo, session.id)
        return RedirectResponse(f"/exam_sessions/results/{session.id}")
    
    history_entry = crud_questions.create_history_entry(repo, current_user_id, user_answer, session_id)
    question, correct_answers, answers = crud_questions.get_question_by_id(repo, user_answer.question_id)
    
    if history_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong with submitting the answer")

    return SubmitAnswerResponse(is_answer_correct=history_entry.correctly_answered, 
                                hint=question.hint,
                                correct_answers=correct_answers)

@router.get("/timer_left")
def timer_left(repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    session = crud_exam_sessions.get_active_session(repo, current_user_id)

    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active exam session found.")

    return {"time_left": crud_exam_sessions.get_time_left(repo, session.id)}


@router.get("/results/{session_id}", response_model=SessionResult)
def get_exam_results(session_id: int, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    session = crud_exam_sessions.get_session_by_id(repo, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No exam session found.")
    if not session.completed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exam session is not completed.")

    results = crud_exam_sessions.get_results_for_session(repo, session_id)
    if results is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No exam session found.")
    questions, statuses = results
    
    return SessionResult(questions=[QuestionStatusInSessionResult(question_id=question.id, question_status=q_status) for question, q_status in zip(questions, statuses)])