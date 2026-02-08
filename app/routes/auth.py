from fastapi import APIRouter, HTTPException
from app.models.auth import LoginRequest, ValidateRequest, RegisterRequest
from app.services.auth_services import (
    alias_exists,
    get_user_by_email,
    create_otp,
    validate_otp,
    register_user
)

from app.core.responses import APIResponse



router = APIRouter(prefix='/auth')


# login 

@router.post('/login')
def login(payload: LoginRequest):
    user = get_user_by_email(payload.email.lower())
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    otp_record = create_otp(payload.email.lower())

    return APIResponse(
        message='OTP generated',
        data={
            'otp': otp_record['otp'],
            'expires_at': otp_record['expires_at']
        },
    )


# validate

@router.post('/validate')
def validate(payload: ValidateRequest):
    session = validate_otp(payload.email.lower(),payload.token)
    if not session:
        raise HTTPException(status_code=400, detail='Invalid OTP')
    
    return APIResponse(
        message='Login successful',
        data={
            'access_token': session['access_token'],
            'token_type': 'Bearer',
        }
    )


# Auth config
@router.get('')
def auth_config():
    return APIResponse(
        data={
            'basic_enabled':True,
            'google_enabled':False,
        }
    )


# register user
@router.post('/register')
def register(payload: RegisterRequest):
    if alias_exists(payload.alias):
        raise HTTPException(status_code=400, detail='Alias already exists')
    
    user = register_user(payload)

    return APIResponse(
        message='User registered successfully',
        data = user
    )


    
