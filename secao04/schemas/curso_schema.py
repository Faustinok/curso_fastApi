from typing import Optional
from pydantic import BaseModel as SCBaseModel

class CursoSchema(SCBaseModel):
    __tablename__ = 'cursos'
    id: Optional[int]
    titulo: int
    aulas: int
    horas: int
    class Config:
        orm_mode = True