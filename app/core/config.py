from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = 'Project 3 LVLS'
    API_PREFIX: str = ''
    BASE_URL: str = 'http://localhost:8000'

    DATA_DIR: str = 'data'
    USERS_FILE: str = 'data/users.json'
    TOKENS_FILE: str = 'data/tokens.json'

    UPLOAD_DIR: str = 'uploads'
    AVATAR_DIR: str = 'data/tokens.json'

    OTP_EXP_MINUTES: int = 10
    ACCESS_TOKEN_EXP_DAYS: int = 7

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
