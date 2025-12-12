from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.convenios_schema import ConvenioBase, RetornoConvenio, EditarConvenio
from sqlalchemy.orm import Session
from app.schemas.usuarios import RetornoUsuario
from app.router.dependencies import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import convenios_crud as crud_convenios
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# ============================================================================
# ENDPOINT DE CREACIÓN
# ============================================================================

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_convenio(
    convenio: ConvenioBase, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Crea un nuevo convenio con validación de permisos.
    Solo usuarios con rol administrativo (id_rol = 1) pueden crear convenios.
    """
    try:
        if user_token.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para crear convenios"
            )
        
        crear = crud_convenios.crear_convenio(db, convenio)
        if crear:
            return {
                "message": "Convenio creado correctamente",
                "success": True
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

# ============================================================================
# ENDPOINTS DE CONSULTA GENERAL
# ============================================================================

@router.get(
    "/obtener-todos", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_all_convenios(
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Obtiene todos los convenios registrados en el sistema.
    Ordenados por fecha de firma de forma descendente.
    """
    try:
        if user_token.id_rol != 1:
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

@router.get(
    "/obtener-por-id/{id_convenio}", 
    status_code=status.HTTP_200_OK, 
    response_model=RetornoConvenio
)
def get_by_id(
    id_convenio: int, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Obtiene un convenio específico por su ID único.
    """
    try:
        if user_token.id_rol != 1:
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

# ============================================================================
# ENDPOINTS DE BÚSQUEDA POR IDENTIFICADORES
# ============================================================================

@router.get(
    "/obtener-por-numero-convenio", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_numero(
    num_convenio: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por número de convenio.
    Utiliza búsqueda parcial (LIKE) para mayor flexibilidad.
    """
    try:
        if user_token.id_rol != 1:
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

@router.get(
    "/obtener-por-numero-proceso", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_numero_proceso(
    num_proceso: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por número de proceso.
    Utiliza búsqueda parcial (LIKE) para mayor flexibilidad.
    """
    try:
        if user_token.id_rol != 1:
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

# ============================================================================
# ENDPOINTS DE BÚSQUEDA POR INSTITUCIÓN
# ============================================================================

@router.get(
    "/obtener-por-nit-institucion", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_nit_institucion(
    nit_institucion: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por NIT de la institución.
    Búsqueda exacta para garantizar precisión en identificación fiscal.
    """
    try:
        if user_token.id_rol != 1:
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

@router.get(
    "/obtener-por-nombre-institucion", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_nombre_institucion(
    nombre_institucion: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por nombre de la institución.
    Utiliza búsqueda parcial (LIKE) para permitir búsquedas flexibles.
    """
    try:
        if user_token.id_rol != 1:
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

# ============================================================================
# ENDPOINTS DE BÚSQUEDA POR ESTADO Y TIPO
# ============================================================================

@router.get(
    "/obtener-por-estado-convenio", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_estado_convenio(
    estado_conv: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por estado (ej: Activo, Finalizado, En ejecución).
    Útil para gestión y seguimiento administrativo.
    """
    try:
        if user_token.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        convenios = crud_convenios.obtener_convenios_by_estado_convenio(db, estado_conv)
        if not convenios:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No se encontraron convenios con estado: {estado_conv}"
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
    "/obtener-por-tipo-convenio", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_tipo_convenio(
    tipo_convenio: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por tipo general (ej: Compraventa, Prestación de servicios).
    """
    try:
        if user_token.id_rol != 1:
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
def get_by_tipo_proceso(
    tipo_proceso: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por tipo de proceso (ej: Licitación pública, Contratación directa).
    """
    try:
        if user_token.id_rol != 1:
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

@router.get(
    "/obtener-por-tipo-convenio-sena", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_tipo_convenio_sena(
    tipo_convenio_sena: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por clasificación específica del SENA.
    """
    try:
        if user_token.id_rol != 1:
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

# ============================================================================
# ENDPOINTS DE BÚSQUEDA POR RESPONSABLES
# ============================================================================

@router.get(
    "/obtener-por-supervisor", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_supervisor(
    supervisor: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por supervisor asignado.
    Utiliza búsqueda parcial para permitir búsqueda por nombre o apellido.
    """
    try:
        if user_token.id_rol != 1:
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

@router.get(
    "/obtener-por-persona-apoyo", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_persona_apoyo(
    persona_apoyo_fpi: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por persona de apoyo de FPI asignada.
    Utiliza búsqueda parcial para flexibilidad.
    """
    try:
        if user_token.id_rol != 1:
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

# ============================================================================
# ENDPOINTS DE BÚSQUEDA POR FECHAS
# ============================================================================

@router.get(
    "/obtener-por-rango-fechas-firma", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_rango_fechas_firma(
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por rango de fechas de firma.
    Formato esperado: YYYY-MM-DD
    Retorna convenios ordenados por fecha de firma descendente.
    """
    try:
        if user_token.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        # Validar formato de fechas
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de fecha inválido. Use YYYY-MM-DD"
            )
        
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
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.get(
    "/obtener-por-rango-fechas-inicio", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def get_by_rango_fechas_inicio(
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios por rango de fechas de inicio de ejecución.
    Formato esperado: YYYY-MM-DD
    Retorna convenios ordenados por fecha de inicio descendente.
    """
    try:
        if user_token.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para consultar convenios"
            )
        
        # Validar formato de fechas
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de fecha inválido. Use YYYY-MM-DD"
            )
        
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
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

# ============================================================================
# ENDPOINTS DE BÚSQUEDA POR CONTENIDO
# ============================================================================

@router.get(
    "/buscar-por-objetivo", 
    status_code=status.HTTP_200_OK, 
    response_model=List[RetornoConvenio]
)
def search_by_objetivo(
    palabra_clave: str, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Busca convenios que contengan la palabra clave en el objetivo.
    Búsqueda de texto completo para análisis de contenido.
    """
    try:
        if user_token.id_rol != 1:
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

# ============================================================================
# ENDPOINTS DE MODIFICACIÓN
# ============================================================================

@router.put("/editar/{id_convenio}", status_code=status.HTTP_200_OK)
def update_convenios(
    id_convenio: int, 
    convenio: EditarConvenio, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Actualiza los datos de un convenio existente.
    Solo actualiza los campos proporcionados (PATCH semántico).
    """
    try:
        if user_token.id_rol != 1:
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
        
        success = crud_convenios.update_convenios(db, id_convenio, convenio)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No se pudo actualizar el convenio. Verifique los datos"
            )
        
        return {
            "message": "Convenio actualizado correctamente",
            "id_convenio": id_convenio,
            "success": True
        }
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de base de datos: {str(e)}"
        )

@router.delete("/eliminar-por-id/{id_convenio}", status_code=status.HTTP_200_OK)
def delete_by_id(
    id_convenio: int, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Elimina un convenio del sistema.
    ADVERTENCIA: Esta operación es irreversible.
    """
    try:
        if user_token.id_rol != 1:
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
        
        success = crud_convenios.eliminar_convenio(db, id_convenio)
        if success:
            return {
                "message": "Convenio eliminado correctamente",
                "id_convenio": id_convenio,
                "success": True
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