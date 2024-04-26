from fastapi import APIRouter

from workout_api.src.tabelas.atletas.controller import router as atleta
from workout_api.src.tabelas.categorias.controller import router as categoria
from workout_api.src.tabelas.centro_treinamento.controller import router as centro_treinamento

api_router = APIRouter()
api_router.include_router(
    atleta,
    prefix='/atletas',
    tags=['Atletas'])

api_router.include_router(
    categoria,
    prefix='/categoria',
    tags=['Categorias'])

api_router.include_router(
    centro_treinamento,
    prefix='/centro_treinamento',
    tags=['Centros de Treinamento'])