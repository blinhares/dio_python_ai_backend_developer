from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.src.config.dependencies import DatabaseDependency
from workout_api.src.tabelas.centro_treinamento.models import CentroTreinamentoModel
from workout_api.src.tabelas.centro_treinamento.schemas import CentroTreinamentoIn,\
        CentroTreinamentoOut
from sqlalchemy.future import select

router = APIRouter()

@router.post(
        '/',
        summary='Criar novo Centro Treinamento ',
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut)

async def post(
    db_session:DatabaseDependency,
    centro_treinamento_in:CentroTreinamentoIn = Body(...)
    ) -> CentroTreinamentoOut:

    centro_treinamento_out = CentroTreinamentoOut(
        id=uuid4(),
        **centro_treinamento_in.model_dump()
        )
    centro_treinamento_model = CentroTreinamentoModel(
        **centro_treinamento_out.model_dump())
    
    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get(
        '/',
        summary='Consultar Todas os Centros de Treinamento',
        status_code=status.HTTP_200_OK,
        response_model=list[CentroTreinamentoOut])

async def query( # type: ignore
    db_session:DatabaseDependency,
    ) -> list[CentroTreinamentoOut]:

    centros_de_treinamento:list[CentroTreinamentoOut] = (
        await db_session.execute(
            select(CentroTreinamentoModel
        ))).scalars().all() # type: ignore
    
    return centros_de_treinamento

@router.get(
        '/{id}',
        summary='Consultar Centro de Treinamento por ID',
        status_code=status.HTTP_200_OK,
        response_model=CentroTreinamentoOut)

async def query(
    id:UUID4,
    db_session:DatabaseDependency,
    ) -> CentroTreinamentoOut:

    centro_de_treinamento:CentroTreinamentoOut = (
        await db_session.execute(
            
            select(CentroTreinamentoModel).\
                filter_by(id=id)

                )
                ).scalars().first() # type: ignore

    if not centro_de_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Centro de Treinamento de id: {id} não encontrada!'
            )

    return centro_de_treinamento