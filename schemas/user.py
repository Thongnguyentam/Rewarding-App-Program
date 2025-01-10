from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    username: str 
    balance: Optional[int] = 0

class AddPointRequest(BaseModel):
    payer: str
    points: int 
    timestamp: str
    
class UpdatePointRequest(BaseModel):
    user_id: int
    payer: str
    points: int 
    timestamp: str
    
class SpendPointRequest(BaseModel):
    points: int
    
class SpendPointResponse(BaseModel):
    payer: str
    points: int
    
class UpdatePointDTO(BaseModel):
    user_id: int
    payer_id: int
    points: int
    timestamp: datetime
    update_by: int