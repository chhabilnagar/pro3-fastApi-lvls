import uuid
from app.core.storage import load_json, save_json
from app.core.security import (
    generate_otp,
    generate_access_token,
    expires_in_minutes,
    expires_in_days
)
from app.core.config import settings


def get_user_by_email(email: str):
    user = load_json(settings.USERS_FILE,[])
    for u in user:
        if u['email'] == email:
            return u
    return None


def alias_exists(alias: str) -> bool:
    users = load_json(settings.USERS_FILE,[])
    return any(u['alias'] == alias for u in users)


def create_otp(email:str):
    tokens = load_json(settings.TOKENS_FILE,{'otp_tokens': [], 'access_tokens':[]})

    otp = generate_otp()
    record = {
        'email': email,
        'otp': otp,
        'expires_at': expires_in_minutes(settings.OTP_EXP_MINUTES),
    }

    tokens['otp_tokens'].append(record)
    save_json(settings.TOKENS_FILE,tokens)

    return record




def validate_otp(email:str, otp:str):
    tokens = load_json(settings.TOKENS_FILE, {'otp_tokens' :[], 'access_tokens': []})

    for t in tokens['otp_tokens']:
        if t['email'] == email and t['otp'] == otp:
            access_token = generate_access_token()
            session = {
                'email': email,
                'access_token': access_token,
                'expires_at': expires_in_days(settings.ACCESS_TOKEN_EXP_DAYS)
            }

            tokens['access_tokens'].append(session)

            save_json(settings.TOKENS_FILE,tokens)
            return session
        
    return None


def register_user(data):
    users = load_json(settings.USERS_FILE,[])

    user = {
        'id' : str(uuid.uuid4()),
        'email' : data.email.lower(),
        'name' : data.name,
        'country' : data.country,
        'division' :data.division,
        'city' : data.city,
        'alias' : data.alias,
        'trading_style' : data.trading_style,
        'bio' : data.bio,
        'public_profile': data.public_profile,
        'avatar': data.avatar,
    }

    users.append(user)
    save_json(settings.USERS_FILE,users)
    return user

