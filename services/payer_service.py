from database.query.db_payer import add_payer
from schemas.payer import NewPayerDTO
from sqlalchemy.orm import Session

async def create_payer(payer_name: str, db: Session):
    payer_dto = NewPayerDTO(name=payer_name)
    payer = await add_payer(db=db, new_payer_dto=payer_dto)
    return payer
    