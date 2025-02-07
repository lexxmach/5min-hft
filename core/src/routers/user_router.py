from typing import Annotated
from common.repo.repository import DatabaseRepository
from cruds import crud_questions
from cruds import crud_credentials, crud_users
import security
from fastapi import Depends, APIRouter, HTTPException, status
from models.schemas import CredentialsAccept, CredentialsModel, UserModel, UserRegister, Token, UserStats
from dependencies import get_repo
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="", tags=["user"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=None)
def new_user(user_credentials: UserRegister, user_info: UserModel, repo: DatabaseRepository= Depends(get_repo)):
    db_user_id = crud_credentials.get_user_id_by_login(repo, user_credentials.login)
    if db_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login is already taken.")
    user_credentials.password = security.get_password_hash(user_credentials.password)
    user_id = crud_credentials.create_user(repo, user_info, CredentialsModel(login=user_credentials.login, password_hash=user_credentials.password))
    if user_id is None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect user data")
    return {}


@router.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], repo: DatabaseRepository = Depends(get_repo)):
    username, password = form_data.username, form_data.password
    db_credentials = crud_credentials.get_credentials_id_by_login(repo, username)

    if db_credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Incorrect username')

    if not security.authenticate_user(db_credentials, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Incorrect password',
                            headers={"WWW-Authenticate": "Bearer"})
    
    access_token = security.create_access_token(data={"sub": username})
    return Token(access_token=access_token, token_type="bearer")

# @router.post("/token", response_model=Token)
# def login(credentials: CredentialsAccept, repo: DatabaseRepository = Depends(get_repo)):
#     db_credentials = crud_credentials.get_credentials_id_by_login(repo, credentials.login)

#     if db_credentials is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                             detail='Incorrect username')

#     if not security.authenticate_user(db_credentials, credentials.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                             detail='Incorrect password',
#                             headers={"WWW-Authenticate": "Bearer"})
    
#     access_token = security.create_access_token(data={"sub": credentials.login})
#     return Token(access_token=access_token, token_type="bearer")


@router.get("/info", response_model=UserModel)
def get_user_info(repo: DatabaseRepository= Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    user = crud_users.get_user_by_user_id(repo, current_user_id)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserModel(name=user.name, surname=user.surname)


@router.get("/stats", response_model=UserStats)
def get_user_stats(repo: DatabaseRepository= Depends(get_repo), current_user_id: int = Depends(security.get_current_user_id)):
    solved_question_by_user = crud_questions.get_solved_question_by_user(repo, current_user_id)
    total_question_by_category = crud_questions.get_total_question_by_category(repo)
    
    if solved_question_by_user is None or total_question_by_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Something went wrong with getting the stats")

    return UserStats(user_id=current_user_id, 
                    solved_questions_by_category_count=solved_question_by_user,
                    total_questions_by_category_count=total_question_by_category)