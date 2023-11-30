import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status, Response
from app.models import Comments, Posts, Users
from database import SessionLocal
from datetime import timedelta
from typing import Dict, Union
from dotenv import load_dotenv
load_dotenv()  # .env 파일을 활성화

from app.funcs.check_token import get_current_user

router = APIRouter(
    prefix="/feed",
    tags=["feed"]
)

# 해당 카테고리 모든 피드 확인
@router.get("/{hobby}", status_code=status.HTTP_200_OK)
def hobby_feed(
    hobby: str,
    payload: Dict[str, Union[str, timedelta]] = Depends(get_current_user)
    ):

    db = SessionLocal()
    feeds = db.query(Posts).filter(Posts.category == hobby).all()
    db.close()

    return {"message": f"This is {hobby} category page", "data": feeds}

# 포스트 하나 내용 확인
@router.get("/detail/{post_id}", status_code=status.HTTP_200_OK)
def get_post_detail(
    post_id: str,
    payload: Dict[str, Union[str, timedelta]] = Depends(get_current_user)
    ):

    db = SessionLocal()
    # 포스트 내용
    post_info = db.query(Posts).filter(Posts.id == post_id).first()
    if not post_info:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "없는 포스트입니다."
        )
    # 댓글 리스트
    comments_list = db.query(Comments).filter(Comments.post_id == post_info.id).all()
    db.close()
    return {"message": "Detailed post page", "data": post_info, "comments_list": comments_list}

# 코멘트 작성
@router.post("/detail/{post_id}", status_code=status.HTTP_200_OK)
def upload_comment(
    post_id: str,
    content: str,
    payload: Dict[str, Union[str, timedelta]] = Depends(get_current_user)
    ):

    db = SessionLocal()
    user_id = db.query(Users.id).filter(Users.email == payload["sub"]).first()
    new_comment = Comments(
        content=content,
        created_at=datetime.utcnow(),
        post_id=post_id,
        user_id=user_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    db.close()
    return {"message": "Comment Uploaded!"}