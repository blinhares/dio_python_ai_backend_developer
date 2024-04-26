from fastapi import APIRouter, Body, status
from workout_api.src.config.dependencies import DatabaseDependency
from workout_api.src.tabelas.atletas.schemas import AtletaIn

router = APIRouter()

@router.post(
        '/',
        summary='Criar novo atleta',
        status_code=status.HTTP_201_CREATED)

async def post(
    db_session:DatabaseDependency,
    atleta_in:AtletaIn = Body(...)):
    pass