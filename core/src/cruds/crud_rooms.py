from datetime import timedelta
from typing import List
from pydantic import ValidationError
from common.repo.repository import DatabaseRepository


from models.schemas import RoomCreate, QuestionsToRoomAdd
from models.models import Rooms, QuestionsInRoom

def create_room(repo: DatabaseRepository, room_info: RoomCreate, user_id: int) -> int:
    try:
        db_room = {"name": room_info.name, "owner_id": user_id, 
            "duration": timedelta(seconds=room_info.duration_seconds),
            "min_start_time": room_info.min_start_time, 
            "max_start_time": room_info.max_start_time}
    except ValidationError:
        return None
    created_room = repo.create(db_room, model=Rooms)
    return created_room.id


def add_questions_to_room(repo: DatabaseRepository, new_questions: QuestionsToRoomAdd, room_id: int) -> int:
    db_questions = []
    try:
        for question_id in new_questions.question_ids:
            db_question = {"question_id": question_id, "room_id": room_id}
            db_questions.append(db_question)
    except ValidationError:
        return None
    for db_question in db_questions:
        _ = repo.create(db_question, model=QuestionsInRoom)
    return 


def get_rooms_by_owner_id(repo: DatabaseRepository, user_id: int) -> List[Rooms]:
    return repo.filter(Rooms.owner_id == user_id, model=Rooms)


def get_room_by_id(repo: DatabaseRepository, room_id: int) -> Rooms:
    room = repo.filter(Rooms.id == room_id, model=Rooms)
    if not room:
        return None
    return room[0]

def delete_room(repo: DatabaseRepository, room_id: int) -> None:
    repo.delete(Rooms.id == room_id, model=Rooms)

def get_questions_in_room(repo: DatabaseRepository, room_id: int) -> List[int]:
    questions = repo.filter(QuestionsInRoom.room_id == room_id, model=QuestionsInRoom)
    return [q.question_id for q in questions]

def remove_question_from_room(repo: DatabaseRepository, room_id: int, question_id: int) -> None:
    repo.delete(QuestionsInRoom.room_id == room_id, QuestionsInRoom.question_id == question_id, model=QuestionsInRoom)
