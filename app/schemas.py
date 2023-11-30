from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import Optional

class UserData(BaseModel):
    email: EmailStr
    password: str
    hobby: str
    nickname: str
    gender: str
    age: int