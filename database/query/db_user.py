from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from constant import response_message
from database.models.user import SysUser, UserPayer
from schemas.user import CreateUserDTO, UpdatePointDTO

async def add_user(db:Session, new_user:CreateUserDTO):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def add_user_payer(db: Session, user_payer: UserPayer):
    db.add(user_payer)
    db.commit()
    db.refresh(user_payer)
    return user_payer

async def get_user_payer_points_by_payer_id(db: Session, user_id: int, payer_id: int):
    return db.query(func.sum(UserPayer.points)).filter(
        UserPayer.user_id == user_id,
        UserPayer.payer_id == payer_id
    ).scalar()

async def update_user_payer(db: Session, payer_user_id: int, spent_point: int):
    payer_user = db.query(UserPayer).filter(UserPayer.id == payer_user_id).first()
    payer_user.points -= spent_point
    payer_user.updated_at = datetime.now()
    db.flush()

async def get_user_payers(db: Session, user_id: int):
    return db.query(UserPayer).filter(UserPayer.user_id == user_id).all()

async def update_user_points(db: Session, update_dto: UpdatePointDTO):
    user_payer = (db.query(UserPayer)
                  .filter(
                      UserPayer.user_id == update_dto.user_id, 
                      UserPayer.payer_id == update_dto.payer_id, 
                      UserPayer.created_at == update_dto.timestamp
                      ).first()
                  )
    if not user_payer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= response_message.USER_PAYER_NOT_FOUND)
        
    user_payer.points = update_dto.points
    user_payer.updated_at = datetime.now()
    
    db.commit()