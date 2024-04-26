from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.src.config.dependencies import DatabaseDependency
from workout_api.src.tabelas.categorias.models import CategoriaModel
from workout_api.src.tabelas.categorias.schemas import CategoriaIn,\
        CategoriaOut
from sqlalchemy.future import select

router = APIRouter()

@router.post(
        '/',
        summary='Criar nova Categoria',
        status_code=status.HTTP_201_CREATED,
        response_model=CategoriaOut)

async def post(
    db_session:DatabaseDependency,
    categoria_in:CategoriaIn = Body(...)
    ) -> CategoriaOut:

    categoria_out = CategoriaOut(
        id=uuid4(),
        **categoria_in.model_dump()
        )
    categoria_model = CategoriaModel(
        **categoria_out.model_dump())
    
    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out


@router.get(
        '/',
        summary='Consultar Todas as Categorias',
        status_code=status.HTTP_200_OK,
        response_model=list[CategoriaOut])

async def query( # type: ignore
    db_session:DatabaseDependency,
    ) -> list[CategoriaOut]:

    categorias:list[CategoriaOut] = (
        await db_session.execute(
            select(CategoriaModel
        ))).scalars().all() # type: ignore
    
    return categorias

@router.get(
        '/{id}',
        summary='Consultar Categoria por ID',
        status_code=status.HTTP_200_OK,
        response_model=CategoriaOut)

async def query(
    id:UUID4,
    db_session:DatabaseDependency,
    ) -> CategoriaOut:

    categoria:CategoriaOut = (
        await db_session.execute(
            
            select(CategoriaModel).\
                filter_by(id=id)

                )
                ).scalars().first() # type: ignore

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria de id: {id} não encontrado!'
            )

    return categoria