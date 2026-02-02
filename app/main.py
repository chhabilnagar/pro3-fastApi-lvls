from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.data import router as data_router


app = FastAPI(
    title = settings.APP_NAME,
    version = '1.0.0',
    description='APIs for project 3 LVLS',
)


# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],

)

# static file hosting (avatar)
app.mount('/uploads', StaticFiles(directory = settings.UPLOAD_DIR),name='uploads')


# routes
app.include_router(auth_router, tags=['Auth'])
app.include_router(user_router, tags=['User'])
app.include_router(data_router, tags=['Data'])


@app.get('/working', tags=['Working'])
def health_check():
    return {'status':'working fine'}



