from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr


class ValidateRequest(BaseModel):
    email: EmailStr
    token: str



class RegisterRequest(BaseModel):
    country: str
    division: Optional[str] = None
    city: Optional[str] = ''
    alias: str
    trading_style: Optional[str] = ''
    bio: Optional[str] = ''
    public_profile: bool = False
    email: EmailStr
    name: str
    avatar: Optional[str] = ''
    referrer_token: Optional[str] = None

    
# google register request flow
class GoogleRegisterRequest(BaseModel):
    access_token: str
    invite_uuid: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    alias: Optional[str] = None
    trading_style: Optional[str] = ""
    bio: Optional[str] = ""
    public_profile: Optional[bool] = False


# google login request 
class GoogleLoginRequest(BaseModel):
    access_token: str

