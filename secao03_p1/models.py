from typing import Optional

from pydantic import BaseModel,validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator('aulas')
    def validar_aulas(cls,value):
        if value ==0:
                raise ValueError('O numero de aulas deve ser maior que zero')


