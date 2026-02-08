from fastapi import APIRouter
from app.services.auth_services import alias_exists
from app.core.responses import APIResponse


router = APIRouter()

@router.get('/alias')
def check_alias(alias:str):
    return APIResponse(
        data={'available': not alias_exists(alias)}
    )
