
from typing import Optional
from pydantic import BaseModel,Field
from datetime import datetime

class HomologacionBase(BaseModel):
    # Hacer campos opcionales con valores por defecto para aceptar payloads parciales
    nit_institucion_destino: Optional[str] = Field(default="NA", max_length=30)
    nombre_programa_sena: Optional[str] = Field(default="NA", max_length=100)
    cod_programa_sena: Optional[str] = Field(default="NA", max_length=50)
    version_programa: Optional[int] = Field(default=0)
    titulo: Optional[str] = Field(default="NA", max_length=150)
    programa_ies: Optional[str] = Field(default="NA", max_length=80)
    nivel_programa: Optional[str] = Field(default="NA", max_length=50)
    snies: Optional[int] = Field(default=0)
    creditos_homologados: Optional[int] = Field(default=0)
    creditos_totales: Optional[int] = Field(default=0)
    creditos_pendientes: Optional[int] = Field(default=0)
    modalidad: Optional[str] = Field(default="NA", max_length=20)
    semestres: Optional[str] = Field(default="NA", max_length=5)
    regional: Optional[str] = Field(default="NA", max_length=30)
    enlace: Optional[str] = Field(default="NA", max_length=255)
    
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
    id_homologacion: int
