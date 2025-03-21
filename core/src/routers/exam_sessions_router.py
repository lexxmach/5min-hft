from datetime import datetime
import security
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from dependencies import get_repo
from common.repo.repository import DatabaseRepository
from cruds import crud_exam_sessions, crud_rooms, crud_questions
from models.schemas import ExamSessionResponse, QuestionRequest, QuestionStatusInSessionResult, QuizQuestion, SessionResult, SubmitAnswerResponse, UserAnswer
import pytz

router = APIRouter(prefix="/exam_sessions", tags=["exam sessions"])


@router.post("/start/{room_id}", response_model=ExamSessionResponse)
def start_exam(room_id: int, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    room = crud_rooms.get_room_by_id(repo, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена. Пожалуйста, проверьте ID комнаты и попробуйте снова.")

    session = crud_exam_sessions.get_active_session(repo, current_user_id)
    if session is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Активная экзаменационная сессия в данной комнате уже существует. Пожалуйста, завершите текущий экзамен перед началом нового.")   
    session = crud_exam_sessions.get_session_by_room_id(repo, room_id, current_user_id)
    if session is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вы уже проходили этот экзамен. Каждый экзамен можно пройти только один раз. Пожалуйста, выберите другую комнату.")   
    
    if datetime.now() > room.max_start_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Время для начала экзамена истекло. Этот экзамен больше недоступен. Пожалуйста, обратитесь к преподавателю за дополнительной информацией.") 
    if datetime.now() < room.min_start_time:
        room_min_time = room.min_start_time.astimezone(pytz.timezone("Europe/Moscow")).strftime('%d.%m.%Y %H:%M')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Экзамен еще не начался. Пожалуйста, подождите до {room_min_time}, чтобы начать этот экзамен.")
    
    session = crud_exam_sessions.create_exam_session(repo, user_id=current_user_id, room_id=room_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка в запуске экзаменационной сессии.")

    return ExamSessionResponse(session_id=session.id, room_id=session.room_id, user_id=session.user_id,
                               start_time=session.start_time, duration=room.duration)


@router.get("/question/{room_id}")
def get_question(room_id: int, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    session = crud_exam_sessions.get_session_by_room_id(repo, room_id, current_user_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не найдена экзаменационная сессия для данной комнаты.")
    if session.completed is True:
        return RedirectResponse(f"/exam_sessions/results/{room_id}")
    
    room = crud_rooms.get_room_by_id(repo, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена. Пожалуйста, проверьте ID комнаты и попробуйте снова.")

    time_left = crud_exam_sessions.get_time_left(repo, session.id, room.duration)
    question, options = crud_questions.get_question_by_parameters(repo, current_user_id, QuestionRequest(room_id=session.room_id, session_id=session.id, type=None, difficulty=None, category=None))
    if time_left == 0 or not question:
        crud_exam_sessions.mark_session_completed(repo, session.id)
        return RedirectResponse(f"/exam_sessions/results/{room_id}")
    
    # return RedirectResponse(f"/questions/?room_id={session.room_id}")
    return QuizQuestion(
        id=question.id,
        question=question.text,
        type=question.type,
        options=options,
        difficulty=question.difficulty,
        category=question.category,
    )



@router.post("/submit-answer/{room_id}", status_code=status.HTTP_201_CREATED, response_model=SubmitAnswerResponse)
def submit_answer(room_id: int, user_answer: UserAnswer, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    session = crud_exam_sessions.get_session_by_room_id(repo, room_id, current_user_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не найдена экзаменационная сессия для данной комнаты. ")
    if session.completed is True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Экзамен завершен. Пожалуйста, перейдите /exam_sessions/results/, чтобы узнать результаты.")
    
    room = crud_rooms.get_room_by_id(repo, session.room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена. Пожалуйста, проверьте ID комнаты и попробуйте снова.")

    time_left = crud_exam_sessions.get_time_left(repo, session.id, room.duration)
    if time_left == 0:
        crud_exam_sessions.mark_session_completed(repo, session.id)
        return RedirectResponse(f"/exam_sessions/results/{room_id}")
    
    history_entry = crud_questions.create_history_entry(repo, current_user_id, user_answer, session.id)
    question, correct_answers, answers = crud_questions.get_question_by_id(repo, user_answer.question_id)
    
    if history_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Что-то пошло не так при отправке ответа. Попробуйте ещё раз или, если ошибка повторилась, обратитесь в техническую поддержку.")

    return SubmitAnswerResponse(is_answer_correct=history_entry.correctly_answered, 
                                hint=question.hint,
                                correct_answers=correct_answers)

@router.get("/timer_left/{room_id}")
def timer_left(room_id: int, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    session = crud_exam_sessions.get_active_session(repo, current_user_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдено активной экзаменационной сессии для залогиненного пользователя.")
    
    room = crud_rooms.get_room_by_id(repo, session.room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена. Пожалуйста, проверьте ID комнаты и попробуйте снова.")

    return {"time_left": crud_exam_sessions.get_time_left(repo, session.id, room.duration)}


@router.get("/results/{room_id}", response_model=SessionResult)
def get_exam_results(room_id: int, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    session = crud_exam_sessions.get_session_by_room_id(repo, room_id, current_user_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдена экзаменационная сессия для данной комнаты.")
    if not session.completed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Экзаменационная сессия ещё не завершена.")

    results = crud_exam_sessions.get_results_for_session(repo, session.id)
    if results is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдена экзаменационная сессия для данной комнаты.")
    questions, statuses = results
    
    return SessionResult(questions=[QuestionStatusInSessionResult(user_id=current_user_id, question_id=question.id, question_status=q_status) for question, q_status in zip(questions, statuses)])


@router.get("/complete/{room_id}")
def manually_complete_session(room_id: int, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    session = crud_exam_sessions.get_session_by_room_id(repo, room_id, current_user_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдена экзаменационная сессия для данной комнаты.")
    
    if not crud_exam_sessions.mark_session_completed(repo, session.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдена экзаменационная сессия для данной комнаты.")
    
    return {"message": "Session completed."}


@router.get("/results/all/{room_id}", response_model=list[SessionResult])
def get_all_exam_results(room_id: int, repo: DatabaseRepository = Depends(get_repo)):
    sessions = crud_exam_sessions.get_all_sessions_by_room_id(repo, room_id)
    if sessions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдена экзаменационная сессия для данной комнаты.")

    results = []
    for session in sessions:
        result = crud_exam_sessions.get_results_for_session(repo, session.id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не выгрузились результаты. Попробуйте позже.")   
        questions, statuses = result
        results.append(SessionResult(questions=[QuestionStatusInSessionResult(user_id=session.user_id, question_id=question.id, question_status=q_status) for question, q_status in zip(questions, statuses)]))
    return results
