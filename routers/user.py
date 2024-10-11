from fastapi import APIRouter, Depends
from requests import Session

from constant import response_message
from database.database import get_db
from schemas.user import AddPointRequest, CreateUserDTO, SpendPointRequest
from services.user_service import add_points_service, create_user, get_balance_service, spend_points_service


router = APIRouter(tags=["user"])
current_user_id = None # hardcode this for now since there is only one user

@router.post("/add")
async def add_points(
    request: AddPointRequest,
    db: Session = Depends(get_db)
):
    user_payer = await add_points_service(request=request, current_user_id=current_user_id, db=db)
    return {
        "detail": response_message.USER_PAYER_CREATED_SUCCESS
    }

@router.post("/spend")
async def spend_points(
    request: SpendPointRequest,
    db: Session = Depends(get_db)
    
):
    return await spend_points_service(current_user_id=current_user_id,request=request,db=db)

@router.get("/balance")
async def get_user_balance(
    db: Session = Depends(get_db)
):
    return await get_balance_service(db=db, user_id=current_user_id)

@router.post("/new-user")
async def create_new_user(
    request : CreateUserDTO,
    db: Session = Depends(get_db)
):
    global current_user_id
    init_user = await create_user(db=db, request=request)
    current_user_id = init_user.id
    return init_user