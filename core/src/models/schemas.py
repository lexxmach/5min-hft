import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field

from models.enums import QuestionStatusType, QuestionType


class UserRegister(BaseModel):
    login : str
    password : str
    
    
class UserModel(BaseModel):
    name : str = Field(default=None)
    surname : str = Field(default=None)


class CredentialsModel(BaseModel):
    login : str
    password_hash : str
 
 
class CredentialsAccept(BaseModel):
    login : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str
   
    
class TokenData(BaseModel):
    username: Union[str, None] = None
    
    
class QuizQuestion(BaseModel):
    id: int
    question: str
    type: QuestionType
    options: Union[list[str], None]  # List of option texts
    difficulty: int
    category: str


class UserAnswer(BaseModel):
    question_id: int
    users_answer: list[str]

class QuestionRequest(BaseModel):
    type: Union[QuestionType, None]
    difficulty: Union[int, None]
    category: Union[str, None]
    room_id: Union[int, None]
    session_id: Union[int, None]

class SubmitAnswerResponse(BaseModel):
    is_answer_correct: bool
    hint: str
    correct_answers: list[str]


class UserStats(BaseModel):
    user_id: int
    solved_questions_by_category_count: dict[str, int]
    total_questions_by_category_count: dict[str, int]


class UserStatWithInCategory(BaseModel):
    user_id: int
    name: str
    surname: str
    tasks_solved: int

class Leaderboard(BaseModel):
    sorted_users_by_category: dict[str, list[UserStatWithInCategory]]
    total_questions_by_category_count: dict[str, int]

class AnswerBase(BaseModel):
    answer_text: str

class AnswerMultipleOptionsBase(BaseModel):
    option_text: str
    is_correct: bool


class SubmitNewQuestion(BaseModel):
    question_text: str
    type: QuestionType
    difficulty: int
    category: str
    hint: str
    room_id: Union[int, None]

    answer: Optional[AnswerBase] = None
    answers_multiple_options: Optional[list[AnswerMultipleOptionsBase]] = None

class RoomCreate(BaseModel):
    name: str
    duration_seconds: int
    min_start_time: datetime.datetime
    max_start_time: datetime.datetime

class RoomResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    duration: datetime.timedelta 
    min_start_time: datetime.datetime
    max_start_time: datetime.datetime


class QuestionsToRoomAdd(BaseModel):
    question_ids: list[int]


class ExamSessionResponse(BaseModel):
    session_id: int
    user_id: int
    room_id: int
    start_time: datetime.datetime
    duration: datetime.timedelta


class QuestionStatusInSessionResult(BaseModel):
    question_id: int
    question_status: QuestionStatusType
    user_id: int
    user_name: str
    user_surname: str

class SessionResult(BaseModel):
    questions: list[QuestionStatusInSessionResult]