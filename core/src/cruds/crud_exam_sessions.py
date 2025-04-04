from datetime import datetime, timedelta
from typing import Optional
from common.repo.repository import DatabaseRepository
from models.enums import QuestionStatusType
from models.models import ExamSession, History, Questions, QuestionsInRoom
from pydantic import ValidationError
from sqlalchemy import and_


def create_exam_session(repo: DatabaseRepository, user_id: int, room_id: int) -> Optional[ExamSession]:
    try:
        db_session = {
            "user_id": user_id,
            "room_id": room_id,
            "start_time": datetime.now(),
            "completed": False,
        }
    except ValidationError:
        return None

    created_session = repo.create(db_session, model=ExamSession)
    return created_session


def get_active_session(repo: DatabaseRepository, user_id: int) -> Optional[ExamSession]:
    session = repo.filter(and_(
        ExamSession.user_id == user_id, ExamSession.completed == False),
        model=ExamSession,
    )

    if not session:
        return None

    return session[0]


def get_session_by_id(repo: DatabaseRepository, session_id: int) -> Optional[ExamSession]:
    session = repo.filter(
        ExamSession.id == session_id,
        model=ExamSession,
    )

    if session is None:
        return None

    return session[0]

def get_session_by_room_id(repo: DatabaseRepository, room_id: int, user_id: int) -> Optional[ExamSession]:
    session = repo.filter(and_(ExamSession.user_id == user_id, 
                               ExamSession.room_id == room_id),
        model=ExamSession,
    )

    if not session:
        return None

    return session[0]

def get_all_sessions_by_room_id(repo: DatabaseRepository, room_id: int) -> Optional[list[ExamSession]]:
    sessions = repo.filter(ExamSession.room_id == room_id,
        model=ExamSession)

    if not sessions:
        return None

    return sessions

def mark_session_completed(repo: DatabaseRepository, session_id: int) -> bool:
    session = get_session_by_id(repo, session_id)
    if session is None:
        return False

    repo.update(ExamSession.id == session_id, data={"completed": True}, model=ExamSession)
    return True


def get_time_left(repo: DatabaseRepository, session_id: int, room_duration: timedelta) -> Optional[int]:
    session = get_session_by_id(repo, session_id)
    if session is None:
        return None

    time_left = max(0, (session.start_time + room_duration - datetime.now()).total_seconds())
    return int(time_left)


def get_results_for_session(repo: DatabaseRepository, session_id: int) -> Optional[tuple[list[Questions], list[QuestionStatusType]]]:
    session = get_session_by_id(repo, session_id)
    if session is None:
        return None
    room_subquery = repo.session.query(QuestionsInRoom.question_id).filter(QuestionsInRoom.room_id == session.room_id).subquery()
    questions = repo.filter(Questions.id.in_(room_subquery), model=Questions)

    statuses = []
    for question in questions:
        history_entry = repo.filter(and_(History.user_id == session.user_id, History.question_id == question.id, History.session_id == session_id), model=History)
        if not history_entry:
            statuses.append(QuestionStatusType.NOT_ANSWERED)
        else:
            statuses.append(QuestionStatusType.CORRECT if history_entry[0].correctly_answered else QuestionStatusType.INCORRECT)
            
    return questions, statuses