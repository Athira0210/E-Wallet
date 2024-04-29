# build a schema using pydantic
from pydantic import BaseModel,Field

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
 
 
class UserAuth(BaseModel):
    username : str
    password: str =Field(..., min_length=5, max_length=24, description="user password")
    email: str = Field(..., description="user email")
    phone : str
    
 
class UserResponse(BaseModel):
    id : int
    email: str
    amount : int
    
class TransactionResponse(BaseModel):
    id : int
    transfer_type: str
    description : str