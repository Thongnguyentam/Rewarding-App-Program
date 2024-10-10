from datetime import datetime
from pydantic import BaseModel


class AddPointRequest(BaseModel):
    payer: str
    points: int 
    timestamp: str
    
class SpendPointRequest(BaseModel):
    points: int
    
class SpendPointResponse(BaseModel):
    payer: str
    points: int
    