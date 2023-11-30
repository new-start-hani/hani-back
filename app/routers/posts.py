import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status, Response
from database import SessionLocal
from datetime import timedelta
from typing import Dict, Union
from dotenv import load_dotenv
load_dotenv()  # .env 파일을 활성화

from app.models import Posts, Users
from app.funcs.check_token import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_post(payload: Dict[str, Union[str, timedelta]] = Depends(get_current_user)):
    return {"message": "포스트 작성 페이지입니다."}

@router.post("/", status_code=status.HTTP_200_OK)
def update_post(
    category: str,
    content: str,
    payload: Dict[str, Union[str, timedelta]] = Depends(get_current_user)
    ):

    db = SessionLocal()
    user_id = db.query(Users.id).filter(Users.email == payload['sub']).first()
    new_post = Posts(
        category=category,
        content=content,
        created_at=datetime.utcnow(),
        user_id=user_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    post_id = db.query(Posts.id).filter(Posts.user_id == user_id)[-1]
    db.close()
    return {"message": "포스트가 업로드되었습니다.", "post_id": post_id}