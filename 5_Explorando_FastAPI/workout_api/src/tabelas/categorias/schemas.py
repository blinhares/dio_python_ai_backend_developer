from pydantic import UUID4, Field
from typing import Annotated
from workout_api.src.contrib.schemas import BaseSchema


class Categoria(BaseSchema):
    nome:Annotated[str, Field(
        description='Nome da Categoria.',
        examples=['Scale'],
        max_length=10
    )]

class CategoriaIn(Categoria):
    pass
class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(
        description='Identificador da Categoria'
    )]
