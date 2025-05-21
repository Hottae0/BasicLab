from fastapi import APIRouter, Depends, HTTPException, Header
from app.db.database import db
from app.schemas.plant_schema import PlantCreate, PlantResponse
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM
from datetime import datetime
from bson import ObjectId

router = APIRouter()

# 토큰에서 이메일 추출
async def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise ValueError

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise ValueError

        return email

    except (ValueError, JWTError):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

# 식물 등록
@router.post("/plants", response_model=PlantResponse)
async def add_plant(plant: PlantCreate, email: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    plant_data = {
        "name": plant.name,
        "memo": plant.memo,
        "watering_cycle": plant.watering_cycle,
        "user_id": str(user["_id"]),
        "created_at": datetime.utcnow().isoformat()
    }

    result = await db.plants.insert_one(plant_data)
    plant_data["id"] = str(result.inserted_id)

    return plant_data

# 식물 조회
@router.get("/plants", response_model=list[PlantResponse])
async def get_plants(email: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    user_id = str(user["_id"])
    plants = await db.plants.find({"user_id": user_id}).to_list(100)

    return [
        {
            "id": str(p["_id"]),
            "name": p["name"],
            "memo": p.get("memo", ""),
            "watering_cycle": p["watering_cycle"],
            "user_id": p["user_id"],
            "created_at": p["created_at"]
        } for p in plants
    ]
