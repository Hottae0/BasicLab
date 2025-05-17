from fastapi import APIRouter, Depends, HTTPException, Header
from app.db.database import db
from app.db.models import plant_dict
from app.schemas.plant_schema import PlantCreate
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM

router = APIRouter()

#누가 요청한 데이터인지 확인하는 메소드. 후에 db에 들어있는 데이터를 꺼낼 때 이메일을 사용할 예정.
async def get_current_user(authorization: str = Header(...)): # 인증된 사용자만 사용 가능하게!
    try:
        scheme, token = authorization.split() # scheme와 토큰(JMT)으로 공백 기준으로 분리

        if scheme.lower() != "bearer": # scheme이 bearner가 아니라면 잘못된 요구
            raise ValueError

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # 암호화된 데이터를 복호화

        email = payload.get("sub") # 사용자의 이메일을 꺼냄.

        if not email:
            raise ValueError

        return email

    except (ValueError, JWTError):
        raise HTTPException(status_code = 401, detail = "유효하지 않은 토큰입니다.")



@router.post("/plants")
async def add_plant(plant: PlantCreate, user_email: str = Depends(get_current_user)):
    await db.plants.insert_one(plant_dict(user_email, plant.name, plant.memo))
    return {"message": "식물 저장 완료"}

@router.get("/plants")
async def get_plants(user_email: str = Depends(get_current_user)):
    plants = await db.plants.find({"user_id": user_email}).to_list(length=100)
    return plants
