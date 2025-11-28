from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class EstadisticaCategoriaBase(BaseModel):
    categoria: str = Field(max_length=50)
    nombre: str = Field(max_length=100)
    cantidad: int = Field(default=0)

class CrearEstadisticaCategoria(EstadisticaCategoriaBase):
    pass

class EditarEstadisticaCategoria(BaseModel):
    categoria: Optional[str] = Field(None, max_length=50)
    nombre: Optional[str] = Field(None, max_length=100)
    cantidad: Optional[int] = None

class RetornoEstadisticaCategoria(EstadisticaCategoriaBase):
    id_estadistica: int
    fecha_actualizacion: datetime