from pydantic import BaseModel
from typing import Optional

# 응답이랑 전송 해는 거 구분하기.

class PlantCreate(BaseModel):
    name: str
    memo: Optional[str] = ""
    watering_cycle: int

class PlantResponse(BaseModel):
    id: str
    name: str
    memo: Optional[str]
    watering_cycle: int
    user_id: str
    created_at: str
