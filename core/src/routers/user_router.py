from cruds import crud_credentials
import security
from fastapi import Depends, APIRouter, HTTPException, status
from models.schemas import CredentialsModel, UserRegister, Token
from dependencies import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=None)
def new_user(user: UserRegister, db: Session = Depends(get_db)):
    db_user_id = crud_credentials.get_user_id_by_login(db, user.login)
    if db_user_id:
        raise HTTPException(status_code=400, detail="Login is already taken.")
    user.password = security.get_password_hash(user.password)
    return crud_credentials.create_user(db, CredentialsModel(login=user.login, password_hash=user.password))


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_credentials = crud_credentials.get_credentials_id_by_login(db, form_data.username)

    if db_credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Incorrect username')

    if not security.authenticate_user(db_credentials, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Incorrect password',
                            headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")