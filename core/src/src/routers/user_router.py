from fastapi import Depends, APIRouter
from src.models.schemas import UserRegister, Token
from dependencies import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=None)
def new_user(user: UserRegister, db: Session = Depends(get_db)):
    return None


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    return None