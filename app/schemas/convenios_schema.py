
from typing import Optional
from pydantic import BaseModel,Field
from datetime import datetime

class ConvenioBase(BaseModel):
    tipo_convenio: str = Field(max_length=50)
    num_convenio: str = Field(max_length=50)
    nit_institucion: str = Field(max_length=20)
    num_proceso: str = Field(max_length=20)
    nombre_institucion: str = Field(max_length=100)
    estado_convenio: str= Field(max_length=20)
    objetivo_convenio: str = Field(max_length=255)
    tipo_proceso: str	= Field(max_length=50)
    fecha_firma: datetime 
    fecha_inicio: datetime
    duracion_convenio: str = Field(max_length=20)	
    plazo_ejecucion: datetime
    prorroga: datetime
    plazo_prorroga: datetime
    duracion_total: str	= Field(max_length=20)
    fecha_publicacion_proceso: datetime
    enlace_secop: str = Field(max_length=100)
    supervisor: str	= Field(max_length=80)
    precio_estimado: float 
    tipo_convenio_sena: str	= Field(max_length=50)
    persona_apoyo_fpi: str= Field(max_length=80)
    enlace_evidencias: str= Field(max_length=100)

class CrearConvenio(ConvenioBase):
    pass

class EditarConvenio(BaseModel):
    tipo_convenio: Optional[str] = None
    num_convenio: Optional[str] = None
    nit_institucion: Optional[str] = None
    num_proceso:  Optional[str] = None
    nombre_institucion: Optional[str] = None
    estado_convenio: Optional[str] = None
    objetivo_convenio: Optional[str] = None
    tipo_proceso: Optional[str]	= None
    fecha_firma: Optional[datetime]  = None
    fecha_inicio: Optional[datetime] = None
    duracion_convenio: Optional[str]	= None
    plazo_ejecucion: Optional[datetime] = None
    prorroga: Optional[datetime] = None
    plazo_prorroga: Optional[datetime] = None
    duracion_total: Optional[str]	= None
    fecha_publicacion_proceso: Optional[datetime] = None
    enlace_secop: Optional[str] = None
    supervisor: Optional[str]	= None
    precio_estimado: Optional[float]  = None
    tipo_convenio_sena: Optional[str]	= None
    persona_apoyo_fpi: Optional[str]= None
    enlace_evidencias: Optional[str]= None

class RetornoConvenio(ConvenioBase):
    id_convenio: int
