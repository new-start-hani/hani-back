import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sqlalchemy import TEXT, Column, INTEGER, String, Boolean, TIMESTAMP, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    hobby = Column(String(255), nullable=False)
    nickname = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    age = Column(INTEGER, nullable=False)
    profile_image = Column(TEXT)
    disabled = Column(Boolean, nullable=False, default=False)


class Posts(Base):
    __tablename__ = "posts"

    id = Column(INTEGER, primary_key=True)
    category = Column(String(255), nullable=False)
    content = Column(TEXT, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    user_id = Column(INTEGER, ForeignKey("users.id"), nullable=False)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(INTEGER, primary_key=True)
    content = Column(String, nullable=False)
    post_id = Column(INTEGER, ForeignKey("posts.id"), nullable=False)