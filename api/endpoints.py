import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Request,status
from fastapi.security import OAuth2PasswordBearer
from fastapi_sqlalchemy import db
from schema import  TokenSchema, TransactionResponse, UserAuth, UserResponse
from uitls import ALGORITHM, JWT_SECRET_KEY, create_access_token, create_refresh_token, get_hashed_password, verify_password
import models
from jose import jwt

router = APIRouter()

aouth2_schema = OAuth2PasswordBearer(tokenUrl="token")
 
 
async def decode_jwt_token(token: Annotated[str, Depends(aouth2_schema)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        print(payload,"ttt")
        return dict(status=200, message=payload)
    except:
        raise credential_exception

@router.get("/me")
async def root():
    return {"message": "hello world"}

#################################### user ##########################################

@router.post("/signup", response_model=UserResponse)
async def create_user(data: UserAuth):
    user = db.session.query(models.User).filter(models.User.email == data.email).first()
    if user is not None:
        raise HTTPException(status_code=400, detail="username or email already exist")
    new_user = models.User(
        username=data.username,
        password=get_hashed_password(data.password),
        email=data.email,
        phone=data.phone,
    )
    db.session.add(new_user)
    db.session.commit()
    if new_user:
        user_id = new_user.id
        user_account = models.UserAccount(user_id=user_id, username=new_user.username)
        db.session.add(user_account)
        db.session.commit()
 
        return new_user
    
@router.post('/login', response_model=TokenSchema)
async def login(request:Request):
    data = await request.json()
    email=data.get("email")
    password=data.get("password")
    user = db.session.query(models.User).filter(models.User.email ==email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }
    
async def log_activity(sender_id: int, receiver_id: int, transfer_type: str, amount: int):
    sender = db.session.query(models.User).filter(models.User.id == sender_id).first()
    receiver = db.session.query(models.User).filter(models.User.id == receiver_id).first()
    activity_entry = models.ActivityTracker(
        transfer_type=transfer_type,
        description=f"{sender.email} {transfer_type} of {amount} to {receiver.email}",
        sender_to=sender_id,
        received_by=receiver_id,
    )
    db.session.add(activity_entry)
    db.session.commit()
    
    
@router.get('/user/{user_id}', response_model=UserResponse)
async def get_user_details(user_id: int):
    user = db.session.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user_dict = {
        "id": user.id,
        "email": user.email,
        "amount": user.amount
    }
    return user_dict

    
###################################### deposit ###############################################
    
@router.post('/deposit',response_model=UserResponse)
async def deposit_money(request:Request,token: dict = Depends(decode_jwt_token)):
    
    data = await request.json()
    # user_id=data.get("user_id")
    amount=data.get("amount")
    sender_id = token["message"]["sub"]
    user = db.session.query(models.User).filter(models.User.email == sender_id).first()
    # sender = db.session.query(models.User).filter(models.User.email == sender_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.amount += amount
    db.session.commit()
    await log_activity(user.id, user.id, "Deposit", amount)

    user_dict = {
        "id": user.id,
        "email": user.email,
        "amount": user.amount
    }
    return user_dict
    # return {"message": f"Successfully deposited {amount} into user's account"}

################################# withdraw #####################################################

@router.post('/withdraw')
async def withdraw_money(request:Request,token: dict = Depends(decode_jwt_token)):
    data = await request.json()
    # user_id=data.get("user_id")
    amount=data.get("amount")
    sender_id = token["message"]["sub"]
    user = db.session.query(models.User).filter(models.User.email == sender_id).first()
    # sender = db.session.query(models.User).filter(models.User.email == sender_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.amount < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )

    user.amount -= amount
    db.session.commit()
    await log_activity(user.id, user.id, "Withdrawal", amount)
    user_dict = {
        "id": user.id,
        "email": user.email,
        "amount": user.amount
    }
    return user_dict


####################################### transaction ################################################################

@router.post('/transfer')
async def transfer_money(request:Request,token: dict = Depends(decode_jwt_token)):
    data = await request.json()
    transfer_type = data.get("transfer_type")
    transfer_to = data.get("transfer_to")
    amount = data.get("amount")
    sender_id = token["message"]["sub"]
    
    transfer_user_obj=db.session.query(models.User).filter(models.User.email == transfer_to).first()
    sender_user_obj=db.session.query(models.User).filter(models.User.email == sender_id).first()
    
    if transfer_user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found for the user"
        )
    new_transaction = models.Wallet(
        transfer_to=transfer_to,
        amount=amount,
        sender_id=sender_user_obj.id,
        receiver_id=transfer_user_obj.id
    )
    db.session.add(new_transaction)
    
    activity_entry = models.ActivityTracker(
        transfer_type="Transfer",
        description=f"{sender_id} transfer of {amount} to {transfer_to}",
        sender_to=sender_user_obj.id,
        received_by=transfer_user_obj.id
    )
    db.session.add(activity_entry)
    db.session.commit()
    
    return {"message": "Transaction successful"}


# @router.get('/transfer_details', response_model=TransactionResponse)
# async def get_transaction_details():
#     activity_tracker = db.session.query(models.ActivityTracker).all()
#     print(activity_tracker,"aaaa")
#     user_dict = {
#         "id": activity_tracker.id,
#         "transfer_type": activity_tracker.transfer_type,
#         "description": activity_tracker.description
#     }
#     return user_dict


@router.get('/activity')
async def get_activity_by_date_range(request:Request,token: dict = Depends(decode_jwt_token)):
    data = await request.json()
    account_owner = token["message"]["sub"]
    start_date = data.get("start_date")
    owner = db.session.query(models.User).filter(models.User.email==account_owner).first()
    activities = db.session.query(models.ActivityTracker).filter(
        models.ActivityTracker.transaction_time >= start_date,models.ActivityTracker.sender_to==owner.id).all()
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities found in the given date range"
        )

    activity_list = []
    for activity in activities:
        activity_dict = {
            "id": activity.id,
            "transfer_type": activity.transfer_type,
            "description": activity.description,
            "sender": activity.sender.email,
            "receiver": activity.receiver.email,
            "transaction_time": activity.transaction_time
        }
        activity_list.append(activity_dict)

    return activity_list






