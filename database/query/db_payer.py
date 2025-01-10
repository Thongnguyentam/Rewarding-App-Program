from sqlalchemy.orm import Session
from sqlalchemy import func, select
from database.models.payer import SysPayer
from database.models.user import UserPayer
from constant import response_message
from fastapi import HTTPException, status

async def get_payer_by_name(db: Session, name: str):
    return db.query(SysPayer).filter(SysPayer.name == name).first()

async def add_payer(db: Session, new_payer_dto):
    payer = SysPayer(name=new_payer_dto.name)
    db.add(payer)
    db.commit()
    db.refresh(payer)
    return payer

async def get_spent_payers_by_user_id(db: Session, user_id: int, spent_points: int):
    # get the cumulative sum and row number for each row
    cte = (
        db.query(
            UserPayer,
            func.row_number().over(order_by=[UserPayer.created_at, UserPayer.id]).label("row_number"),
            func.sum(UserPayer.points).over(order_by=[UserPayer.created_at, UserPayer.id]).label("total_points")
        )
        .filter(UserPayer.user_id == user_id, UserPayer.points != 0)
        .cte("cumulative_pts_cte")
    )
    
    # min row number subquery
    min_row_number_subquery = (
        select(func.min(cte.c.row_number))
        .where(cte.c.total_points >= spent_points)
        .scalar_subquery()
    )

    payer_user_list = (
        db.query(cte.c.id, cte.c.points, cte.c.total_points, cte.c.payer_id)
        .filter(cte.c.row_number <= min_row_number_subquery)
        .all()
    )

    # not enough point
    if not payer_user_list or payer_user_list[-1].total_points < spent_points:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=response_message.NOT_ENOUGH_POINTS_ERROR
        )
    
    # get the the list of payers that have to pay for the user' points
    points_by_payer_list = (
        db.query(SysPayer.name, func.sum(cte.c.points).label("points"), cte.c.payer_id)
        .join(SysPayer, cte.c.payer_id == SysPayer.id)
        .filter(cte.c.row_number <= min_row_number_subquery)
        .group_by(SysPayer.name, cte.c.payer_id)
        .all()
    )
    
    # last row's point might not be fully used
    last_row_not_used_pts = payer_user_list[-1].total_points - spent_points
    return payer_user_list, points_by_payer_list, last_row_not_used_pts

async def get_payer_list_by_user_id(db: Session, user_id: int):
    return (
        db.query(func.sum(UserPayer.points), SysPayer.name)
        .join(SysPayer, SysPayer.id == UserPayer.payer_id)
        .filter(UserPayer.user_id == user_id)
        .group_by(UserPayer.payer_id, SysPayer.name)
        .all()
    )
