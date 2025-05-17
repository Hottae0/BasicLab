from pydantic import BaseModel
from typing import Optional

# 데이터를 어떻게 저장할 건지 나태는 칸! 필요한 거 미리미리 정해두자

class PlantCreate(BaseModel):
    name: str
    memo: Optional[str] = ""
    watering_cycle = int
