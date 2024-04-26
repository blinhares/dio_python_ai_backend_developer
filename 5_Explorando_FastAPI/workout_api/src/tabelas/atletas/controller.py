from fastapi import APIRouter

router = APIRouter()

@router.post('/',
             summary='Criar novo atleta')
async def post():
    pass