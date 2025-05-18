from datetime import datetime
from typing import List

def user_dict(email: str, hashed_pw: str, name: str, nickname: str, plant_type: List[str]):
    return {
        "email": email,
        "hashed_password": hashed_pw,
        "name": name,
        "nickname": nickname,
        "plant_type": plant_type,
    }

def plant_dict(user_id: str, name: str, memo: str = ""):
    return {
        "user_id": user_id,
        "name": name,
        "memo": memo,
        "created_at": datetime.utcnow(),
    }
