from typing import Annotated
from cruds import crud_questions
from cruds import crud_credentials
import security
from fastapi import Depends, APIRouter, HTTPException, status
from models.schemas import CredentialsModel, UserModel, UserRegister, Token, UserStats
from dependencies import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="", tags=["user"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=None)
def new_user(user_credentials: UserRegister, user_info: UserModel, db: Session = Depends(get_db)):
    db_user_id = crud_credentials.get_user_id_by_login(db, user_credentials.login)
    if db_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login is already taken.")
    user_credentials.password = security.get_password_hash(user_credentials.password)
    user_id = crud_credentials.create_user(db, user_info, CredentialsModel(login=user_credentials.login, password_hash=user_credentials.password))
    if user_id is None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect user data")
    return {}


@router.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_credentials = crud_credentials.get_credentials_id_by_login(db, form_data.username)

    if db_credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Incorrect username')

    if not security.authenticate_user(db_credentials, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Incorrect password',
                            headers={"WWW-Authenticate": "Bearer"})
    
    access_token = security.create_access_token(data={"sub": form_data.username})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/stats", response_model=UserStats)
def get_user_stats(db: Session = Depends(get_db), current_user_id: int = 1):
    solved_question_by_user = crud_questions.get_solved_question_by_user(db, current_user_id)
    total_question_by_category = crud_questions.get_total_question_by_category(db)
    
    if solved_question_by_user is None or total_question_by_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong with getting the stats")

    return UserStats(user_id=current_user_id, 
                    solved_questions_by_category_count=solved_question_by_user,
                    total_questions_by_category_count=total_question_by_category)