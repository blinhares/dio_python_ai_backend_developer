from pydantic import UUID4, Field
from typing import Annotated
from workout_api.src.contrib.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
    nome:Annotated[str, Field(
        description='Nome do Centro Treinamento.',
        examples=['CT King'],
        max_length=20
    )]

    endereco:Annotated[str, Field(
        description='Endereço do Centro Treinamento.',
        examples=['Av H, 324'],
        max_length=60
    )]

    proprietario:Annotated[str, Field(
        description='Proprietario da Centro Treinamento.',
        examples=['Marcos Belutti'],
        max_length=30
    )]
class CentroTreinamentoIn(CentroTreinamento):
    pass

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(
        description='Identificador da Centro de Treinamento'
    )]
    