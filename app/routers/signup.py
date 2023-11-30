import os
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from database import SessionLocal
from datetime import timedelta
from typing import Dict
from dotenv import load_dotenv
load_dotenv()  # .env 파일을 활성화

from app.models import Users
from app.schemas import UserData
from app.funcs.hash_password import HashPassword

router = APIRouter(
    prefix="/signup",
    tags=["signup"]
)

hash_password = HashPassword()

@router.post("/", status_code=status.HTTP_200_OK)
def signup(data: UserData):
    # DB에서 이메일 존재 여부 확인
    db = SessionLocal()
    id_exist = db.query(Users).filter(Users.email == data.email).first()
    
    # 이미 등록된 이메일인 경우
    if id_exist:
        db.close()
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    
    # 등록되지 않은 이메일인 경우 -> 회원가입 진행
    else:
        hashed_password = hash_password.create_hash(data.password)
        new_user = Users(
            email=data.email,
            password=hashed_password,
            hobby=data.hobby,
            nickname=data.nickname,
            gender=data.gender,
            age=data.age
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
    
    return {"message": "회원가입 완료!"}