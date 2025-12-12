from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class ConvenioBase(BaseModel):
    tipo_convenio: str = Field(max_length=50)
    num_convenio: str = Field(max_length=50)
    nit_institucion: str = Field(max_length=20)
    num_proceso: str = Field(max_length=50)
    nombre_institucion: str = Field(max_length=100)
    estado_convenio: str = Field(max_length=50)
    objetivo_convenio: str 
    tipo_proceso: str = Field(max_length=50)
    
    fecha_firma: str = Field(max_length=50)
    fecha_inicio: str = Field(max_length=50)
    duracion_convenio: str = Field(max_length=20)
    plazo_ejecucion: str = Field(max_length=50)
    prorroga: str = Field(max_length=50)
    plazo_prorroga: str = Field(max_length=50)
    duracion_total: str = Field(max_length=20)
    fecha_publicacion_proceso: str = Field(max_length=50)
    
    enlace_secop: str = Field(max_length=1500)
    supervisor: str  
    precio_estimado: float
    tipo_convenio_sena: str = Field(max_length=50)
    persona_apoyo_fpi: str = Field(max_length=80)
    enlace_evidencias: str  
    
class CrearConvenio(ConvenioBase):
    pass

class EditarConvenio(BaseModel):
    tipo_convenio: Optional[str] = Field(None, max_length=50)
    num_convenio: Optional[str] = Field(None, max_length=50)
    nit_institucion: Optional[str] = Field(None, max_length=20)
    num_proceso: Optional[str] = Field(None, max_length=50)
    nombre_institucion: Optional[str] = Field(None, max_length=100)
    estado_convenio: Optional[str] = Field(None, max_length=50)
    objetivo_convenio: Optional[str] = None  
    tipo_proceso: Optional[str] = Field(None, max_length=50)
    
    # FECHAS COMO STRING
    fecha_firma: Optional[str] = Field(None, max_length=50)
    fecha_inicio: Optional[str] = Field(None, max_length=50)
    duracion_convenio: Optional[str] = Field(None, max_length=20)
    plazo_ejecucion: Optional[str] = Field(None, max_length=50)
    prorroga: Optional[str] = Field(None, max_length=50)
    plazo_prorroga: Optional[str] = Field(None, max_length=50)
    duracion_total: Optional[str] = Field(None, max_length=20)
    fecha_publicacion_proceso: Optional[str] = Field(None, max_length=50)
    
    enlace_secop: Optional[str] = Field(None, max_length=1500)
    supervisor: Optional[str] = None  
    precio_estimado: Optional[float] = None
    tipo_convenio_sena: Optional[str] = Field(None, max_length=50)
    persona_apoyo_fpi: Optional[str] = Field(None, max_length=80)
    enlace_evidencias: Optional[str] = None 

class RetornoConvenio(ConvenioBase):
    id_convenio: int
