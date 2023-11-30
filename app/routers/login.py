import os
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from app.jwt_utils import create_access_token
from database import SessionLocal
from datetime import timedelta
from typing import Dict
from dotenv import load_dotenv
load_dotenv()  # .env 파일을 활성화

from app.models import Users
from app.funcs.hash_password import HashPassword

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

SECRET_KEY = os.getenv("SECRET_KEY")
manager = LoginManager(SECRET_KEY, '/login', use_cookie=True)
ACCESS_TOKEN_EXPIRE_MINUTES = 6000
hash_password = HashPassword()

@router.post("/", status_code=status.HTTP_200_OK)
def login(
    response: Response,
    user_input: OAuth2PasswordRequestForm = Depends()
    ):

    # 이메일이 DB에 존재하는지 확인 -> 비밀번호 매칭 확인 -> access_token 발급
    db = SessionLocal()
    # 이메일이 DB에 존재하는지 확인
    user_exist = db.query(Users).filter(Users.email == user_input.username).first()
    if not user_exist:
        db.close()
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "이메일이나 비밀번호가 잘못되었습니다."
        )

    # 비밀번호 매칭 확인
    if hash_password.verify_hash(user_input.password, user_exist.password):
        db.close()
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_input.username}, expires_delta=access_token_expires
        )
        # cookie: access_token 발급
        response.set_cookie(key="access_token", value=access_token)

        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    db.close()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="이메일이나 비밀번호가 잘못되었습니다.",
        headers={"WWW-Authenticate": "Bearer"}
    )