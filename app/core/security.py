import secrets
from datetime import datetime, timedelta, timezone


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def generate_otp() -> str:
    # 6-digit otp
    return str(secrets.randbelow(900000) + 100000)


def generate_access_token() -> str:
    return secrets.token_urlsafe(32)



def is_expired(expires_at: str) -> bool:
    expires_at = datetime.fromisoformat(expires_at)
    return now_utc() > expires_at


def expires_in_minutes(minutes: int) -> str:
    return (now_utc() + timedelta(minutes=minutes)).isoformat()


def expires_in_days(days:int) -> str:
    return (now_utc() + timedelta(days=days)).isoformat()

