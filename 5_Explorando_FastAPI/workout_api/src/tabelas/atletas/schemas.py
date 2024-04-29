from pydantic import Field, PositiveFloat
from typing import Annotated, Optional
from workout_api.src.contrib.schemas import BaseSchema, OutMixin
from workout_api.src.tabelas.categorias.schemas import CategoriaIn
from workout_api.src.tabelas.centro_treinamento.schemas import CentroTreinamentoIn

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
    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta')]
    centro_treinamento: Annotated[
        CentroTreinamentoIn,
        Field(description='Cento de Treinamento do Atleta')]
    

class AtletaOut(AtletaIn, OutMixin):
    pass
class AtletaOut_all(BaseSchema, OutMixin):
    nome:Annotated[str, Field(
        description='Nome do Atleta.',
        examples=['Bruno', 'Carlos'],
        max_length=50
    )]

    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta')]
    centro_treinamento: Annotated[
        CentroTreinamentoIn,
        Field(description='Cento de Treinamento do Atleta')]
    


class AtletaUpdate(BaseSchema):
    nome: Annotated[
        Optional[str],
            Field(
                None,
                description='Nome do atleta',
                examples=['Joao'],
                max_length=50
                )
            ]
    
    idade: Annotated[
        Optional[int],
        Field(
            None,
            description='Idade do atleta',
            examples=[25]
            )
            ]