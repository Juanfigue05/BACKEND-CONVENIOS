from pydantic import BaseModel, Field
from typing import Optional

class InstitucionBase(BaseModel):
	nit_institucion: int
	nombre_institucion: str = Field(min_length=3, max_length=100)
	direccion: str = Field(min_length=3, max_length=100)
	id_municipio: int

class RetornarInstitucion(InstitucionBase):
    cant_convenios: int

class EditarInstitucion(BaseModel):
    nit_institucion: Optional[int]
    nombre_institucion: Optional[str] = Field(default=None, min_length=3, max_length=100)
    direccion: Optional[str] = Field(default=None, min_length=3, max_length=100)