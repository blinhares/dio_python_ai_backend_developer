from pydantic import Field, PositiveFloat
from typing import Annotated
from workout_api.src.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome:Annotated[str, Field(
        description='Nome do Atleta.',
        examples=['Bruno', 'Carlos'],
        max_length=50
    )]

    cpf:Annotated[str, Field(
        description='CPF do Atleta.',
        examples=['12312312300', '22345443333'],
        max_length=11
    )]

    idade:Annotated[int, Field(
        description='Idade do Atleta.',
        examples=['21', '38']
    )]

    peso:Annotated[PositiveFloat, Field(
        description='Peso do Atleta.',
        examples=['56.2', '76']
    )]

    altura:Annotated[PositiveFloat, Field(
        description='Altura do Atleta.',
        examples=['1.73']
    )]

    sexo:Annotated[str, Field(
        description='Sexo do Atleta.',
        examples=['M','F'],
        max_length=1
    )]
class AtletaIn(Atleta):
    pass

class AtletaOut(AtletaIn, OutMixin):
    pass