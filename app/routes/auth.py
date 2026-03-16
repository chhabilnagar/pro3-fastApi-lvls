from fastapi import APIRouter, HTTPException
from fastapi.params import Header
from app.core.config import Settings
from app.core.security import generate_access_token
from app.core.storage import load_json, save_json
from app.models.auth import LoginRequest, ValidateRequest, RegisterRequest, GoogleRegisterRequest, GoogleLoginRequest
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
@router.get('/config')
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



# google register
@router.post('/google/register')
def google_register(payload: GoogleRegisterRequest):
    

    # mock verification of google access token
    if not payload.access_token:
        raise HTTPException(status_code=400, detail='Invalid Google token')
    
    if alias_exists(payload.alias):
        raise HTTPException(status_code=400, detail='Alias already taken')
    

    user_data = RegisterRequest(
        email = f"{payload.access_token[:8]}@google.mock",
        name = "Google User",
        country=payload.country,
        division=None,
        city=payload.city,
        alias=payload.alias,
        trading_style=payload.trading_style,
        bio=payload.bio,
        public_profile=payload.public_profile,
        avatar=''
    )


    user = register_user(user_data)

    session = create_otp(user['email'])

    return APIResponse(
        message='Google account registered',
        data={
            'user':user,
            'otp': session['otp']
        }
    )



# google login

@router.post('/google/login')
def google_login(payload: GoogleLoginRequest):
    
    email = f"{payload.access_token[:8]}@google.mock"

    user = get_user_by_email(email)

    if not user:
        raise HTTPException(status_code=404, detail='Google user not registered')
    
    otp = create_otp(email)

    return APIResponse(
        message='Google login successful',
        data={
            'access_token': otp['otp'],

        }
    )


# token exchange 
# used after getting token from google to exh
@router.post('/token-exchange')
def token_exchange(authorization: str = Header(...)):

    token = authorization.replace('Bearer ','')

    session = {
        "access_token": generate_access_token(),
        "external_token" : token
    }

    tokens = load_json(Settings.TOKENS_FILE, {'otp_tokens' : [], 'access_tokens':[]})

    tokens['access_tokens'].append(session)

    save_json(Settings.TOKENS_FILE, tokens)
    

    return APIResponse(
        message='Token exchange successful',
        data={
            'access_token' : session['access_token']
        }
    )