
from fastapi import APIRouter
router = APIRouter()


@router.get('/test1')
def test():
    return {"Hello": "World"}


