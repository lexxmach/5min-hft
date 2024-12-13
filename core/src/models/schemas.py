from typing import Union
from pydantic import BaseModel, Field

from models.enums import QuestionType


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