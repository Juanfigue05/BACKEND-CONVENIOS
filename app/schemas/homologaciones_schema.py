
from typing import Optional
from pydantic import BaseModel,Field
from datetime import datetime

class HomologacionBase(BaseModel):
    id_homologacion: int
    nit_institucion_destino: str = Field(max_length=20)
    nombre_programa_sena: str = Field(max_length=100)
    cod_programa_sena: str = Field(max_length=50)
    version_programa: int
    titulo: str = Field(max_length=100)
    programa_ies: str = Field(max_length=50)
    nivel_programa: str = Field(max_length=10)
    snies :int 
    creditos_homologados: int
    creditos_totales: int
    creditos_pendientes: int
    modalidad: str = Field(max_length=10)
    semestres: str = Field(max_length=5)
    regional: str = Field(max_length=20)
    enlace: str = Field(max_length=100)

class CrearHomologacion(HomologacionBase):
    pass

class EditarHomologacion(BaseModel):
    nit_institucion_destino: Optional[str] = None
    nombre_programa_sena: Optional[str] = None
    cod_programa_sena: Optional[str] = None
    version_programa: Optional[int] = None
    titulo: Optional[str] = None
    programa_ies: Optional[str] = None
    nivel_programa: Optional[str] = None
    snies :Optional[int]  = None
    creditos_homologados: Optional[int] = None
    creditos_totales: Optional[int] = None
    creditos_pendientes: Optional[int] = None
    modalidad: Optional[str] = None
    semestres: Optional[str] = None
    regional: Optional[str] = None
    enlace: Optional[str] = None

class RetornoHomologacion(HomologacionBase):
    id_convenio: int
