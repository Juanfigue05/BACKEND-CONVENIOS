from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.convenios_schema import ConvenioBase, RetornoConvenio, EditarConvenio
from sqlalchemy.orm import Session
from app.schemas.usuarios import RetornoUsuario
from app.router.dependencies import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import convenios_crud as crud_convenios
from typing import List, Optional
from datetime import datetime
import re

router = APIRouter()

# ============================================================================
# FUNCIONES AUXILIARES DE VALIDACIÓN
# ============================================================================

def validar_formato_fecha(fecha_str: str) -> bool:
    """
    Valida que una fecha esté en formato ISO (YYYY-MM-DD).
    """
    patron = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(patron, fecha_str))

def normalizar_fecha_entrada(fecha_str: str) -> str:
    """
    Normaliza entrada de fecha para búsquedas.
    Acepta varios formatos y los convierte a YYYY-MM-DD.
    """
    if not fecha_str or fecha_str.upper() == "N/A":
        return "N/A"
    
    # Si ya está en formato correcto
    if validar_formato_fecha(fecha_str):
        return fecha_str
    
    # Intentar parsear diferentes formatos
    formatos = ["%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"]
    for formato in formatos:
        try:
            fecha_obj = datetime.strptime(fecha_str, formato)
            return fecha_obj.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    raise ValueError(f"Formato de fecha inválido: {fecha_str}")

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def crear_convenio(
    convenio: ConvenioBase, 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para crear convenios"
            )
        
        creado = crud_convenios.crear_convenio(db, convenio)
        if creado:
            return {
                "mensaje": "Convenio creado correctamente",
                "exitoso": True
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El convenio no pudo ser creado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error al crear convenio: {str(e)}"
        )

@router.get("/obtener-todos", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_todos_los_convenios(
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_todos_convenios(db)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No se encontraron convenios registrados"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-id/{id_convenio}",status_code=status.HTTP_200_OK, response_model=RetornoConvenio
)
def obtener_convenio_por_id(
    id_convenio: int, 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    """
    Obtiene un convenio específico por su ID único.
    """
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenio = crud_convenios.obtener_convenio_by_id(db, id_convenio)
        if convenio is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Convenio con ID {id_convenio} no encontrado"
            )
        return convenio
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-numero-convenio", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_numero_convenio(
    num_convenio: str = Query(..., description="Número del convenio a buscar"), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_num_convenio(db, num_convenio)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios con número: {num_convenio}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-numero-proceso", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_numero_proceso(
    num_proceso: str = Query(..., description="Número del proceso a buscar"), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_num_proceso(db, num_proceso)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios con número de proceso: {num_proceso}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-nit-institucion", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_nit_institucion(
    nit_institucion: str = Query(..., description="NIT de la institución (20 caracteres)", max_length=20), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_nit_institucion(db, nit_institucion)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios para el NIT: {nit_institucion}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-nombre-institucion", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_nombre_institucion(
    nombre_institucion: str = Query(..., description="Nombre de la institución (completo o parcial)"), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_nombre_institucion(db, nombre_institucion)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios para la institución: {nombre_institucion}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-estado-convenio",  status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_estado_convenio(
    estado_convenio: str = Query(..., description="Estado del convenio", max_length=50), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_estado_convenio(db, estado_convenio)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios con estado: {estado_convenio}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-tipo-convenio", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_tipo_convenio(
    tipo_convenio: str = Query(..., description="Tipo de convenio", max_length=50), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_tipo_convenio(db, tipo_convenio)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios de tipo: {tipo_convenio}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get(
    "/obtener-por-tipo-proceso", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def obtener_por_tipo_proceso(
    tipo_proceso: str = Query(..., description="Tipo de proceso", max_length=50), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_tipo_proceso(db, tipo_proceso)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios con tipo de proceso: {tipo_proceso}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get( "/obtener-por-tipo-convenio-sena",  status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_tipo_convenio_sena(
    tipo_convenio_sena: str = Query(..., description="Tipo de convenio SENA", max_length=50), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_tipo_convenio_sena(db, tipo_convenio_sena)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios con tipo SENA: {tipo_convenio_sena}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )
    
@router.get("/obtener-por-supervisor", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_supervisor(
    supervisor: str = Query(..., description="Nombre del supervisor (completo o parcial)"), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_supervisor(db, supervisor)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios supervisados por: {supervisor}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-persona-apoyo", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_persona_apoyo(
    persona_apoyo_fpi: str = Query(..., description="Nombre de la persona de apoyo FPI"), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_persona_apoyo(db, persona_apoyo_fpi)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios con persona de apoyo: {persona_apoyo_fpi}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-rango-fechas-firma", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_rango_fechas_firma(
    fecha_inicio: str = Query(..., description="Fecha de inicio (YYYY-MM-DD)", regex=r'^\d{4}-\d{2}-\d{2}$'),
    fecha_fin: str = Query(..., description="Fecha fin (YYYY-MM-DD)", regex=r'^\d{4}-\d{2}-\d{2}$'),
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        # Validar que fecha_inicio <= fecha_fin
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        
        if fecha_inicio_dt > fecha_fin_dt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio no puede ser mayor que la fecha final"
            )
        
        convenios = crud_convenios.obtener_convenios_by_rango_fechas_firma(
            db, fecha_inicio, fecha_fin
        )
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios firmados entre {fecha_inicio} y {fecha_fin}"
            )
        return convenios
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato de fecha inválido: {str(e)}"
        )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/obtener-por-rango-fechas-inicio", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def obtener_por_rango_fechas_inicio(
    fecha_inicio: str = Query(..., description="Fecha de inicio (YYYY-MM-DD)", regex=r'^\d{4}-\d{2}-\d{2}$'),
    fecha_fin: str = Query(..., description="Fecha fin (YYYY-MM-DD)", regex=r'^\d{4}-\d{2}-\d{2}$'),
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        # Validar que fecha_inicio <= fecha_fin
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        
        if fecha_inicio_dt > fecha_fin_dt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio no puede ser mayor que la fecha final"
            )
        
        convenios = crud_convenios.obtener_convenios_by_rango_fechas_inicio(
            db, fecha_inicio, fecha_fin
        )
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios iniciados entre {fecha_inicio} y {fecha_fin}"
            )
        return convenios
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato de fecha inválido: {str(e)}"
        )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get("/buscar-por-objetivo", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio]
)
def buscar_por_objetivo(
    palabra_clave: str = Query(..., description="Palabra clave para buscar en objetivos"), 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.buscar_convenios_by_objetivo(db, palabra_clave)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios con la palabra clave: {palabra_clave}"
            )
        return convenios
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.put("/editar/{id_convenio}", status_code=status.HTTP_200_OK)
def actualizar_convenio(
    id_convenio: int, 
    convenio: EditarConvenio, 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para editar convenios"
            )
        
        # Verificar que el convenio existe
        convenio_existente = crud_convenios.obtener_convenio_by_id(db, id_convenio)
        if not convenio_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Convenio con ID {id_convenio} no encontrado"
            )
        
        exitoso = crud_convenios.actualizar_convenio(db, id_convenio, convenio)
        if not exitoso:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No se pudo actualizar el convenio. Verifique los datos"
            )
        
        return {
            "mensaje": "Convenio actualizado correctamente",
            "id_convenio": id_convenio,
            "exitoso": True
        }
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.delete("/eliminar-por-id/{id_convenio}", status_code=status.HTTP_200_OK)
def eliminar_convenio_por_id(
    id_convenio: int, 
    db: Session = Depends(get_db),
    usuario_actual: RetornoUsuario = Depends(get_current_user)
):
    try:
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para eliminar convenios"
            )
        
        # Verificar que el convenio existe
        convenio_existente = crud_convenios.obtener_convenio_by_id(db, id_convenio)
        if not convenio_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Convenio con ID {id_convenio} no encontrado"
            )
        
        exitoso = crud_convenios.eliminar_convenio(db, id_convenio)
        if exitoso:
            return {
                "mensaje": "Convenio eliminado correctamente",
                "id_convenio": id_convenio,
                "exitoso": True
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No se pudo eliminar el convenio"
            )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )