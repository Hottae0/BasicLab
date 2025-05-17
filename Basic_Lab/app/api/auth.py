from django.db.models.sql import Query
from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import UserCreate, UserLogin
from app.db.database import db
from app.db.models import user_dict
from app.core.config import SECRET_KEY, ALGORITHM
from jose import jwt
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup")
async def signup(user: UserCreate):
    exists_email = await db.users.find_one({"email": user.email})
    if exists_email:
        raise HTTPException(status_code = 400, detail = "이미 가입된 이메일")

    nickname_taken = await db.users.find_one({"nickname": user.nickname})
    if nickname_taken:
        raise HTTPException(status_code = 400, detail = "이미 사용 중인 닉네임입니다.")

    hashed = pwd_context.hash(user.password)

    await db.users.insert_one(
        user_dict(user.email, hashed, user.name, user.nickname, user.plant_type)
    )

    return {"message": "회원가입 완료"}


@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})

    if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code = 401, detail = "로그인 실패")

    token = create_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}

@router.get("/check-nickname")
async def check_nickname(nickname: str = Query(...)):
    existing = await db.users.find_one({"nickname": nickname})
    return {"available": existing is None}