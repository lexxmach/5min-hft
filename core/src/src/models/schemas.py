from typing import Union
from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    login : str
    password : str


class CredentialsModel(BaseModel):
    login : str
    password_hash : str
 
    
class UserModel(BaseModel):
    name : str = Field(default=None)
    surname : str = Field(default=None)


class QuizQuestion(BaseModel):
    question : str
    answer : str


class Token(BaseModel):
    access_token: str
    token_type: str
   
    
class TokenData(BaseModel):
    username: Union[str, None] = None