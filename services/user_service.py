from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database.models.user import UserPayer
from database.query.db_user import add_user_payer, get_user_payer_points_by_payer_id, update_user_payer, get_user_payers
from database.query.db_payer import get_payer_by_name, add_payer, get_payer_list_by_user_id, get_spent_payers_by_user_id
from schemas.user import AddPointRequest, SpendPointRequest, SpendPointResponse
from schemas.payer import NewPayerDTO
from constant import response_message
from sqlalchemy.exc import SQLAlchemyError

async def add_points_service(request: AddPointRequest, current_user_id: int, db: Session):
    # check the format of the request
    payer_name = request.payer
    added_points = request.points
    try:
        added_timestamp = request.timestamp
        added_timestamp = datetime.strptime(added_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail= response_message.INVALID_TIMESTAMP
        )
    # add payer if it does not exit
    payer = await get_payer_by_name(db, payer_name)
    if not payer:
        payer_dto = NewPayerDTO(name=payer_name)
        payer = await add_payer(db=db, new_payer_dto=payer_dto)
    
    # check if adding points to current amount of point of user from a payer (since added points can be negative) 
    points_from_payer = await get_user_payer_points_by_payer_id(db, current_user_id, payer.id)
    if ((not points_from_payer and added_points < 0) or 
        (points_from_payer and (points_from_payer + added_points) < 0)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=response_message.NOT_ENOUGH_POINTS_ERROR
        )
        
    # add new transaction 
    user_payer = UserPayer(
        user_id=current_user_id,
        payer_id=payer.id,
        points=added_points,
        created_at=added_timestamp,
        updated_at=added_timestamp
    )
    return await add_user_payer(db, user_payer)

async def spend_points_service(request: SpendPointRequest, current_user_id: int, db: Session):
    try:
        payer_user_list, pts_by_payer_list, last_row_not_used_pts = await get_spent_payers_by_user_id(
            db=db, 
            user_id=current_user_id,
            spent_points= request.points
        )
        # update spent points
        curr_spent = 0
        for ind in range(len(payer_user_list)):
            # the last row may not be used all points
            if ind == len(payer_user_list)-1:
                spent_point = request.points - curr_spent
            else:
                spent_point =  payer_user_list[ind].points
            curr_spent += spent_point
            
            #update the points spent by the user from the payer 
            await update_user_payer(
                db=db, 
                payer_user_id =payer_user_list[ind].id, 
                spent_point = spent_point
            )
        db.commit()
        
        # format the response
        spent_points = []
        for payer, points, payer_id in pts_by_payer_list:
            if payer_id == payer_user_list[-1].payer_id:
                points = points - last_row_not_used_pts
            response = SpendPointResponse(payer=payer, points=-points) 
            spent_points.append(response)
            
        return spent_points
    
    # rollback all changes in database if there is exception
    except HTTPException as http_exception:
        db.rollback()
        raise http_exception
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= str(e)
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= str(exc)
        )    
        
async def get_balance_service(
    db: Session,
    user_id: int
):
    payer_list = await get_payer_list_by_user_id(db=db, user_id=user_id)
    balance = {}
    for points, payer in payer_list:
        balance[payer] = points
    return balance
