from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class ConvenioBase(BaseModel):
    # CAMPOS OBLIGATORIOS
    tipo_convenio: str = Field(..., max_length=50, description="Tipo de convenio")
    num_convenio: str = Field(..., max_length=50, description="Número del convenio")
    nit_institucion: str = Field(..., max_length=20, description="NIT de la institución")
    nombre_institucion: str = Field(..., max_length=120, description="Nombre de la institución")
    estado_convenio: str = Field(..., max_length=50, description="Estado del convenio")
    
    # CAMPOS OPCIONALES
    num_proceso: Optional[str] = Field(None, max_length=50, description="Número de proceso")
    objetivo_convenio: Optional[str] = Field(None, description="Objetivo del convenio")
    tipo_proceso: Optional[str] = Field(None, max_length=50, description="Tipo de proceso")
    
    # FECHAS COMO STRING (OPCIONALES) - pueden contener texto o fechas
    fecha_firma: Optional[str] = Field(None, max_length=50, description="Fecha de firma (YYYY-MM-DD o texto)")
    fecha_inicio: Optional[str] = Field(None, max_length=50, description="Fecha de inicio (YYYY-MM-DD o texto)")
    duracion_convenio: Optional[str] = Field(None, max_length=20, description="Duración del convenio")
    plazo_ejecucion: Optional[str] = Field(None, max_length=50, description="Plazo de ejecución (YYYY-MM-DD o texto)")
    prorroga: Optional[str] = Field(None, max_length=50, description="Prórroga")
    plazo_prorroga: Optional[str] = Field(None, max_length=50, description="Plazo de prórroga")
    duracion_total: Optional[str] = Field(None, max_length=20, description="Duración total")
    fecha_publicacion_proceso: Optional[str] = Field(None, max_length=50, description="Fecha de publicación")
    
    # OTROS CAMPOS OPCIONALES
    enlace_secop: Optional[str] = Field(None, max_length=1500, description="Enlace SECOP")
    supervisor: Optional[str] = Field(None, max_length=400, description="Supervisor del convenio")
    precio_estimado: Optional[float] = Field(None, description="Precio estimado del convenio")
    tipo_convenio_sena: Optional[str] = Field(None, max_length=50, description="Tipo de convenio SENA")
    persona_apoyo_fpi: Optional[str] = Field(None, max_length=80, description="Persona de apoyo FPI")
    enlace_evidencias: Optional[str] = Field(None, description="Enlace a evidencias")
    
    @field_validator('num_convenio', 'tipo_convenio', 'nit_institucion', 'nombre_institucion', 'estado_convenio')
    @classmethod
    def validar_campos_obligatorios(cls, v, info):
        """Valida que los campos obligatorios no estén vacíos"""
        if not v or (isinstance(v, str) and v.strip() == ''):
            raise ValueError(f'El campo {info.field_name} es obligatorio y no puede estar vacío')
        return v.strip() if isinstance(v, str) else v
    
    @field_validator('precio_estimado')
    @classmethod
    def validar_precio(cls, v):
        """Valida que el precio sea positivo si se proporciona"""
        if v is not None and v < 0:
            raise ValueError('El precio estimado no puede ser negativo')
        return v
    
    class Config:
        from_attributes = True
        str_strip_whitespace = True
        json_schema_extra = {
            "example": {
                "tipo_convenio": "Interadministrativo",
                "num_convenio": "CONV-2024-001",
                "nit_institucion": "891480085-7",
                "nombre_institucion": "GOBERNACIÓN DE RISARALDA",
                "estado_convenio": "Convencional",
                "num_proceso": "PROC-2024-001",
                "objetivo_convenio": "Cooperación técnica y académica",
                "tipo_proceso": "Contratación directa",
                "fecha_firma": "2024-01-15",
                "fecha_inicio": "2024-02-01",
                "duracion_convenio": "12 meses",
                "plazo_ejecucion": "2025-01-31",
                "prorroga": "N/A",
                "plazo_prorroga": "N/A",
                "duracion_total": "12 meses",
                "fecha_publicacion_proceso": "2024-01-10",
                "enlace_secop": "https://www.colombiacompra.gov.co/secop",
                "supervisor": "Juan Pérez García",
                "precio_estimado": 50000000.00,
                "tipo_convenio_sena": "Docencia-Servicio",
                "persona_apoyo_fpi": "María López",
                "enlace_evidencias": "https://drive.google.com/convenio001"
            }
        }

class CrearConvenio(ConvenioBase):
    """Schema para crear un nuevo convenio"""
    pass

class EditarConvenio(BaseModel):
    """Schema para editar un convenio existente - todos los campos son opcionales"""
    tipo_convenio: Optional[str] = Field(None, max_length=50)
    num_convenio: Optional[str] = Field(None, max_length=50)
    nit_institucion: Optional[str] = Field(None, max_length=20)
    num_proceso: Optional[str] = Field(None, max_length=50)
    nombre_institucion: Optional[str] = Field(None, max_length=120)
    estado_convenio: Optional[str] = Field(None, max_length=50)
    objetivo_convenio: Optional[str] = None
    tipo_proceso: Optional[str] = Field(None, max_length=50)
    
    # FECHAS COMO STRING (OPCIONALES)
    fecha_firma: Optional[str] = Field(None, max_length=50)
    fecha_inicio: Optional[str] = Field(None, max_length=50)
    duracion_convenio: Optional[str] = Field(None, max_length=20)
    plazo_ejecucion: Optional[str] = Field(None, max_length=50)
    prorroga: Optional[str] = Field(None, max_length=50)
    plazo_prorroga: Optional[str] = Field(None, max_length=50)
    duracion_total: Optional[str] = Field(None, max_length=20)
    fecha_publicacion_proceso: Optional[str] = Field(None, max_length=50)

    enlace_secop: Optional[str] = Field(None, max_length=1500)
    supervisor: Optional[str] = Field(None, max_length=400)
    precio_estimado: Optional[float] = None
    tipo_convenio_sena: Optional[str] = Field(None, max_length=50)
    persona_apoyo_fpi: Optional[str] = Field(None, max_length=80)
    enlace_evidencias: Optional[str] = None
    
    @field_validator('precio_estimado')
    @classmethod
    def validar_precio(cls, v):
        """Valida que el precio sea positivo si se proporciona"""
        if v is not None and v < 0:
            raise ValueError('El precio estimado no puede ser negativo')
        return v
    
    class Config:
        from_attributes = True
        str_strip_whitespace = True

class RetornoConvenio(BaseModel):
    """Schema para retornar un convenio"""
    id_convenio: int
    tipo_convenio: Optional[str] = None
    num_convenio: Optional[str] = None
    nit_institucion: Optional[str] = None
    num_proceso: Optional[str] = None
    nombre_institucion: Optional[str] = None
    estado_convenio: Optional[str] = None
    objetivo_convenio: Optional[str] = None
    tipo_proceso: Optional[str] = None
    
    # FECHAS
    fecha_firma: Optional[str] = None
    fecha_inicio: Optional[str] = None
    duracion_convenio: Optional[str] = None
    plazo_ejecucion: Optional[str] = None
    prorroga: Optional[str] = None
    plazo_prorroga: Optional[str] = None
    duracion_total: Optional[str] = None
    fecha_publicacion_proceso: Optional[str] = None
    
    # OTROS
    enlace_secop: Optional[str] = None
    supervisor: Optional[str] = None
    precio_estimado: Optional[float] = None
    tipo_convenio_sena: Optional[str] = None
    persona_apoyo_fpi: Optional[str] = None
    enlace_evidencias: Optional[str] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_convenio": 1,
                "tipo_convenio": "Interadministrativo",
                "num_convenio": "CONV-2024-001",
                "nit_institucion": "891480085-7",
                "nombre_institucion": "GOBERNACIÓN DE RISARALDA",
                "estado_convenio": "Convencional",
                "num_proceso": "PROC-2024-001",
                "objetivo_convenio": "Cooperación técnica y académica",
                "tipo_proceso": "Contratación directa",
                "fecha_firma": "2024-01-15",
                "fecha_inicio": "2024-02-01",
                "duracion_convenio": "12 meses",
                "plazo_ejecucion": "2025-01-31",
                "prorroga": "N/A",
                "plazo_prorroga": "N/A",
                "duracion_total": "12 meses",
                "fecha_publicacion_proceso": "2024-01-10",
                "enlace_secop": "https://www.colombiacompra.gov.co/secop",
                "supervisor": "Juan Pérez García",
                "precio_estimado": 50000000.00,
                "tipo_convenio_sena": "Docencia-Servicio",
                "persona_apoyo_fpi": "María López",
                "enlace_evidencias": "https://drive.google.com/convenio001"
            }
        }