import os
from datetime import datetime
import uuid
from fastapi import APIRouter, Form, HTTPException, Depends, UploadFile, status, Response
from app.funcs.check_token import get_current_user
from app.funcs.hash_password import HashPassword
from app.models import Users
from database import SessionLocal
from datetime import timedelta
from typing import Dict, Union
from dotenv import load_dotenv
load_dotenv()  # .env 파일을 활성화

router = APIRouter(
    prefix="/mypage",
    tags=["mypage"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_mypage(
    payload: Dict[str, Union[str, timedelta]] = Depends(get_current_user)
    ):
    db = SessionLocal()
    data = db.query(Users).filter(Users.email == payload["sub"]).first()
    db.close()
    return {"message": "마이페이지입니다.", "data": data}

@router.put("/", status_code=status.HTTP_200_OK)
async def change_myinfo(
    profile_image: UploadFile = Form(None),
    password: str = Form(None),
    hobby: str = Form(None),
    nickname: str = Form(None),
    payload: Dict[str, Union[str, timedelta]] = Depends(get_current_user)
    ):

    db = SessionLocal()
    user = db.query(Users).filter(Users.email == payload["sub"]).first()
    
    # 프로필 이미지 변경시 이미지 저장
    # 이전 이미지 삭제 코드 추가 필요!!
    if profile_image:
        current_directory = os.getcwd()
        content = await profile_image.read()
        filename = f"{str(uuid.uuid4())}.jpg"  # uuid로 유니크한 파일명으로 변경
        current_directory = os.path.join(current_directory, "images", filename)
        with open(current_directory, "wb") as fp:
            fp.write(content)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)
        setattr(user, "profile_image", current_directory)
    
    # 비밀번호 변경시
    if password:
        hashed_password = HashPassword.create_hash(password)
        setattr(user, "password", hashed_password)
    
    # 취미 변경시
    if hobby:
        setattr(user, "hobby", hobby)
    
    # 닉네임 변경시
    if nickname:
        setattr(user, "nickname", nickname)

    db.commit()
    db.refresh(user)
    db.close()
    return {"message": "고객 정보가 변경되었습니다"}