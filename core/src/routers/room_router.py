from common.repo.repository import DatabaseRepository
import security
from cruds import crud_users, crud_rooms
from fastapi import APIRouter, Depends, HTTPException, status
from models.schemas import QuestionsToRoomAdd, RoomCreate, RoomResponse
from typing import List
from dependencies import get_repo


router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/", response_model=int)
def create_room(room_info: RoomCreate, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    if not crud_users.is_user_root(repo, current_user_id):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуются права администратора для создания новой комнаты. Перейдите по ссылке, чтобы запросить административные права: admin/request-access.")
    return crud_rooms.create_room(repo, room_info, current_user_id)


@router.get("/", response_model=List[RoomResponse])
def get_rooms(repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    rooms = crud_rooms.get_rooms_by_owner_id(repo, current_user_id)
    return [RoomResponse(id=room.id, name=room.name, owner_id=room.owner_id, duration=room.duration, 
                         min_start_time=room.min_start_time, max_start_time=room.max_start_time) for room in rooms]

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, repo: DatabaseRepository = Depends(get_repo)):
    room = crud_rooms.get_room_by_id(repo, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена. Пожалуйста, проверьте ID комнаты и попробуйте снова.")
    
    return RoomResponse(id=room.id, name=room.name, owner_id=room.owner_id, duration=room.duration, 
                         min_start_time=room.min_start_time, max_start_time=room.max_start_time)
    
@router.delete("/{room_id}")
def delete_room(room_id: int, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    room = crud_rooms.get_room_by_id(repo, room_id)
    
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена. Пожалуйста, проверьте ID комнаты и попробуйте снова.")
    
    if room.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Для удаления комнаты нужно быть её создателем. Пожалуйста, войдите в аккаунт, с которого Вы создавали комнату.')
    
    crud_rooms.delete_room(repo, room_id)
    
    return {"message": "Room deleted"}


@router.post("/{room_id}/questions")
def add_questions_to_room(room_id: int, questions: QuestionsToRoomAdd, repo: DatabaseRepository = Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    room = crud_rooms.get_room_by_id(repo, room_id)
    
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена. Пожалуйста, проверьте ID комнаты и попробуйте снова.")
    if room.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Для добавления вопросов в комнату нужно быть её создателем. Пожалуйста, войдите в аккаунт, с которого Вы создавали комнату.')
    
    crud_rooms.add_questions_to_room(repo, questions, room_id)
    return {"message": "Questions added"}