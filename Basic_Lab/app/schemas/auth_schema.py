from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str[8:20]
    name: str[:20]        # 이름
    nickname: str[:20]    # 닉네임
    plant_type: List[str]   # 키우려는 식물 종류

class UserLogin(BaseModel):
    email: EmailStr
    password: str
