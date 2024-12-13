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