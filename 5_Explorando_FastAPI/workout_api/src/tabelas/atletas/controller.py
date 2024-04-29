from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.src.config.dependencies import DatabaseDependency
from workout_api.src.tabelas.atletas.schemas import AtletaIn,\
      AtletaOut, AtletaUpdate
from workout_api.src.tabelas.atletas.models import AtletaModel
from workout_api.src.tabelas.categorias.models import CategoriaModel
from workout_api.src.tabelas.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.exc import IntegrityError


router = APIRouter()

@router.post(
        '/',
        summary='Criar novo atleta',
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut
        )
async def post(
    db_session:DatabaseDependency,
    atleta_in:AtletaIn = Body(...)):

    categoria = (
        await db_session.execute(
            select(CategoriaModel
                ).\
                filter_by(
                    nome=(categoria_nome :=atleta_in.categoria.nome)
                    )
            )).scalars().first() # type: ignore
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Categoria {categoria_nome} não encontrada!'
            )
    
    centro_treinamento = (
        await db_session.execute(
            select(CentroTreinamentoModel
                ).\
                filter_by(
                    nome=(ct_nome :=atleta_in.centro_treinamento.nome)
                    )
            )).scalars().first() # type: ignore
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Centro de Treinamento {ct_nome} não encontrado!'
            )
    
    try:

        atleta_out = AtletaOut(
            id=uuid4(),
            create_at=datetime.now(timezone.utc).replace(tzinfo=None), #utcnow()deprecated
            **atleta_in.model_dump()
            )

        atleta_model = AtletaModel(
            **atleta_out.model_dump(
                exclude={'categoria','centro_treinamento'}
                ))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

    except IntegrityError :
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Erro! CPF: {atleta_out.cpf} já existe.'
        )

    return atleta_out

#consultar todos atletas
@router.get(
        '/',
        summary='Consultar Todos as Atletas',
        status_code=status.HTTP_200_OK,
        response_model=list[AtletaOut]
        )
async def query( # type: ignore
    db_session:DatabaseDependency,
    ) -> list[AtletaOut]:

    atletas:list[AtletaOut] = (
        await db_session.execute(
            select(AtletaModel
        ))).scalars().all() # type: ignore
    
    return [AtletaOut.model_validate(atleta) for atleta in atletas]
    
#colsultar por ID
@router.get(
        '/{id}',
        summary='Consultar Atleta por ID',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut
        )
async def get(
    id:UUID4,
    db_session:DatabaseDependency,
    ) -> AtletaOut:

    atleta:AtletaOut = (
        await db_session.execute(
            
            select(AtletaModel).\
                filter_by(id=id)

                )
                ).scalars().first() # type: ignore

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta de id: {id} não encontrado!'
            )

    return atleta

###nome
@router.get(
        '/nome/',
        summary='Consultar Atleta por Nome',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut
        )
async def get_by_name(
    nome:str,
    db_session:DatabaseDependency,
)-> AtletaOut:
    

    atleta:AtletaOut = (
        await db_session.execute(
            
            select(AtletaModel).\
                filter_by(nome = nome)

                )
                ).scalars().first() # type: ignore
  
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta de nome: {nome} não encontrado!'
            )

    return atleta

# get by cpf
@router.get(
        '/cpf/',
        summary='Consultar Atleta por CPF',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut
        )
async def get_by_cpf(
    cpf:str,
    db_session:DatabaseDependency,
)-> AtletaOut:
    
    atleta:AtletaOut = (
        await db_session.execute(
            
            select(AtletaModel).\
                filter_by(cpf = cpf)

                )
                ).scalars().first() # type: ignore
  
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta de cpf: {cpf} não encontrado!'
            )

    return atleta

#edit by ID
@router.patch(
        '/{id}',
        summary='Editar Atleta por ID',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut
        )
async def patch(
    id:UUID4,
    db_session:DatabaseDependency,
    atleta_up:AtletaUpdate = Body(...)
    ) -> AtletaOut:

    atleta:AtletaOut = (
        await db_session.execute(
            
            select(AtletaModel).\
                filter_by(id=id)

                )
                ).scalars().first() # type: ignore

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta de id: {id} não encontrado!'
            )
    atleta_update = atleta_up.model_dump(
        exclude_unset=True
        )
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta

#delete by ID
@router.delete(
        '/{id}',
        summary='Deletar Atleta por ID',
        status_code=status.HTTP_204_NO_CONTENT
    )
async def delete(
    id:UUID4,
    db_session:DatabaseDependency
    ) -> None:

    atleta:AtletaOut = (
        await db_session.execute(
            
            select(AtletaModel).\
                filter_by(id=id)

                )
                ).scalars().first() # type: ignore

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta de id: {id} não encontrado!'
            )
    
    await db_session.delete(atleta)
    await db_session.commit()
