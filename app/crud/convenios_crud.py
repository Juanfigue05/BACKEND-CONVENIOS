from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from datetime import datetime
import logging

from app.schemas.convenios_schema import CrearConvenio, EditarConvenio, RetornoConvenio

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# FUNCIONES DE VALIDACIÓN Y LIMPIEZA
# ============================================================================

def validar_fecha_formato(fecha_str: str) -> bool:
    """
    Valida que una fecha esté en formato ISO (YYYY-MM-DD) o sea "N/A".
    """
    if fecha_str == "N/A" or not fecha_str:
        return True
    
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def limpiar_texto_convenio(texto: str) -> str:
    """
    Limpia texto eliminando caracteres problemáticos.
    """
    if not texto or texto == "N/A":
        return texto
    
    # Eliminar tabulaciones y espacios múltiples
    import re
    texto = texto.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
    texto = texto.replace('\xa0', ' ')
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

# ============================================================================
# OPERACIONES CRUD - CREACIÓN
# ============================================================================

def crear_convenio(db: Session, convenio: CrearConvenio) -> Optional[bool]:
    """
    Crea un nuevo convenio en la base de datos con validación de datos.
    """
    try:
        dataconvenios = convenio.model_dump()
        
        # Validar fechas antes de insertar
        campos_fecha = [
            "fecha_firma", "fecha_inicio", "plazo_ejecucion",
            "prorroga", "plazo_prorroga", "fecha_publicacion_proceso"
        ]
        
        for campo in campos_fecha:
            if campo in dataconvenios and dataconvenios[campo]:
                if not validar_fecha_formato(dataconvenios[campo]):
                    logger.warning(f"Fecha inválida en {campo}: {dataconvenios[campo]}")
                    dataconvenios[campo] = "N/A"
        
        # Limpiar campos de texto
        campos_texto = [
            "num_convenio", "num_proceso", "objetivo_convenio", "duracion_convenio",
            "duracion_total", "enlace_secop", "supervisor", "tipo_convenio_sena",
            "persona_apoyo_fpi", "enlace_evidencias", "nombre_institucion"
        ]
        
        for campo in campos_texto:
            if campo in dataconvenios and dataconvenios[campo]:
                dataconvenios[campo] = limpiar_texto_convenio(dataconvenios[campo])
    
        query = text("""
            INSERT INTO convenios (
                tipo_convenio, num_convenio, nit_institucion, num_proceso, nombre_institucion,
                estado_convenio, objetivo_convenio, tipo_proceso, fecha_firma, fecha_inicio, 
                duracion_convenio, plazo_ejecucion, prorroga, plazo_prorroga, duracion_total, 
                fecha_publicacion_proceso, enlace_secop, supervisor, precio_estimado, 
                tipo_convenio_sena, persona_apoyo_fpi, enlace_evidencias
            ) VALUES (
                :tipo_convenio, :num_convenio, :nit_institucion, :num_proceso, :nombre_institucion,
                :estado_convenio, :objetivo_convenio, :tipo_proceso, :fecha_firma, :fecha_inicio, 
                :duracion_convenio, :plazo_ejecucion, :prorroga, :plazo_prorroga, :duracion_total, 
                :fecha_publicacion_proceso, :enlace_secop, :supervisor, :precio_estimado, 
                :tipo_convenio_sena, :persona_apoyo_fpi, :enlace_evidencias
            )
        """)
        
        db.execute(query, dataconvenios)
        db.commit()
        logger.info(f"Convenio creado exitosamente: {dataconvenios.get('num_convenio')}")
        return True
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error SQL al crear el convenio: {str(e)}")
        raise Exception(f"Error de base de datos al crear el convenio: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al crear el convenio: {str(e)}")
        raise Exception(f"Error al crear el convenio: {str(e)}")

# ============================================================================
# OPERACIONES CRUD - LECTURA
# ============================================================================

def obtener_todos_convenios(db: Session) -> List[RetornoConvenio]:
    """
    Obtiene todos los convenios ordenados por fecha de firma descendente.
    """
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            ORDER BY 
                CASE 
                    WHEN convenios.fecha_firma = 'N/A' THEN '9999-12-31'
                    ELSE convenios.fecha_firma
                END DESC
        """)
        result = db.execute(query).mappings().all()
        logger.info(f"Se obtuvieron {len(result)} convenios")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener todos los convenios: {str(e)}")
        raise Exception(f"Error de base de datos al obtener los convenios: {str(e)}")

def obtener_convenio_by_id(db: Session, id_convenio: int):
    """
    Obtiene un convenio específico por su ID.
    """
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.id_convenio = :id_conv
        """)
        result = db.execute(query, {"id_conv": id_convenio}).mappings().first()
        
        if result:
            logger.info(f"Convenio encontrado con ID: {id_convenio}")
        else:
            logger.warning(f"No se encontró convenio con ID: {id_convenio}")
            
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar el convenio por id: {str(e)}")
        raise Exception(f"Error de base de datos al buscar el convenio por id: {str(e)}")

# ============================================================================
# BÚSQUEDAS POR IDENTIFICADORES
# ============================================================================

def obtener_convenios_by_num_convenio(db: Session, num_conv: str):
    """
    Busca convenios por número de convenio (búsqueda parcial).
    """
    try:
        filtro = f"%{num_conv}%"
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.num_convenio LIKE :num_convenio
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"num_convenio": filtro}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios con número: {num_conv}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar el convenio por número: {str(e)}")
        raise Exception(f"Error de base de datos al buscar el convenio por número: {str(e)}")

def obtener_convenios_by_num_proceso(db: Session, num_proc: str):
    """
    Busca convenios por número de proceso (búsqueda parcial).
    """
    try:
        filtro = f"%{num_proc}%"
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.num_proceso LIKE :num_proceso
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"num_proceso": filtro}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios con número de proceso: {num_proc}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por número de proceso: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por número de proceso: {str(e)}")

# ============================================================================
# BÚSQUEDAS POR INSTITUCIÓN
# ============================================================================

def obtener_convenios_by_nit_institucion(db: Session, nit_inst: str):
    """
    Busca convenios por NIT de institución (búsqueda exacta).
    """
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.nit_institucion = :nit_proveed
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"nit_proveed": nit_inst}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios para NIT: {nit_inst}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por nit de institución: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por NIT: {str(e)}")

def obtener_convenios_by_nombre_institucion(db: Session, nombre_inst: str):
    """
    Busca convenios por nombre de institución (búsqueda parcial).
    """
    try:
        filtro = f"%{nombre_inst}%"
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.nombre_institucion LIKE :nombre_inst
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"nombre_inst": filtro}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios para institución: {nombre_inst}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por nombre de institución: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por nombre: {str(e)}")

# ============================================================================
# BÚSQUEDAS POR ESTADO Y TIPO
# ============================================================================

def obtener_convenios_by_estado_convenio(db: Session, estado_conv: str):
    """
    Busca convenios por estado (búsqueda exacta).
    """
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.estado_convenio = :convenio_estado
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"convenio_estado": estado_conv}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios con estado: {estado_conv}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por estado: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por estado: {str(e)}")

def obtener_convenios_by_tipo_convenio(db: Session, tipo_conv: str):
    """
    Busca convenios por tipo de convenio (búsqueda exacta).
    """
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.tipo_convenio = :tipo_conve
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"tipo_conve": tipo_conv}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios de tipo: {tipo_conv}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por tipo de convenio: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por tipo: {str(e)}")

def obtener_convenios_by_tipo_proceso(db: Session, tipo_proc: str):
    """
    Busca convenios por tipo de proceso (búsqueda exacta).
    """
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.tipo_proceso = :tipo_proceso
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"tipo_proceso": tipo_proc}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios con tipo de proceso: {tipo_proc}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por tipo de proceso: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por tipo de proceso: {str(e)}")

def obtener_convenios_by_tipo_convenio_sena(db: Session, tipo_conv_sena: str):
    """
    Busca convenios por tipo de convenio SENA (búsqueda exacta).
    """
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.tipo_convenio_sena = :tipo_conv_sena
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"tipo_conv_sena": tipo_conv_sena}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios con tipo SENA: {tipo_conv_sena}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por tipo convenio SENA: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por tipo convenio SENA: {str(e)}")

# ============================================================================
# BÚSQUEDAS POR RESPONSABLES
# ============================================================================

def obtener_convenios_by_supervisor(db: Session, superv: str):
    """
    Busca convenios por supervisor (búsqueda parcial).
    """
    try:
        filtro = f"%{superv}%"
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.supervisor LIKE :supervisor
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"supervisor": filtro}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios supervisados por: {superv}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por supervisor: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por supervisor: {str(e)}")

def obtener_convenios_by_persona_apoyo(db: Session, persona_ap: str):
    """
    Busca convenios por persona de apoyo FPI (búsqueda parcial).
    """
    try:
        filtro = f"%{persona_ap}%"
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.persona_apoyo_fpi LIKE :persona_apoyo
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"persona_apoyo": filtro}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios con persona de apoyo: {persona_ap}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por persona de apoyo: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por persona de apoyo: {str(e)}")

# ============================================================================
# BÚSQUEDAS POR FECHAS
# ============================================================================

def obtener_convenios_by_rango_fechas_firma(db: Session, fecha_ini: str, fecha_fin: str):
    """
    Busca convenios por rango de fechas de firma.
    Maneja correctamente valores "N/A".
    """
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.fecha_firma != 'N/A' 
                AND convenios.fecha_firma BETWEEN :fecha_inicio AND :fecha_fin
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"fecha_inicio": fecha_ini, "fecha_fin": fecha_fin}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios firmados entre {fecha_ini} y {fecha_fin}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por rango de fechas de firma: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por rango de fechas: {str(e)}")

def obtener_convenios_by_rango_fechas_inicio(db: Session, fecha_ini: str, fecha_fin: str):
    """
    Busca convenios por rango de fechas de inicio de ejecución.
    Maneja correctamente valores "N/A".
    """
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.fecha_inicio != 'N/A' 
                AND convenios.fecha_inicio BETWEEN :fecha_inicio AND :fecha_fin
            ORDER BY convenios.fecha_inicio DESC
        """)
        result = db.execute(query, {"fecha_inicio": fecha_ini, "fecha_fin": fecha_fin}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios iniciados entre {fecha_ini} y {fecha_fin}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por rango de fechas de inicio: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por rango de fechas de inicio: {str(e)}")

# ============================================================================
# BÚSQUEDA POR CONTENIDO
# ============================================================================

def buscar_convenios_by_objetivo(db: Session, palabra: str):
    """
    Busca convenios que contengan una palabra clave en el objetivo.
    """
    try:
        filtro = f"%{palabra}%"
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.objetivo_convenio LIKE :palabra_clave
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"palabra_clave": filtro}).mappings().all()
        logger.info(f"Se encontraron {len(result)} convenios con palabra clave: {palabra}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por objetivo: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por objetivo: {str(e)}")

# ============================================================================
# OPERACIONES CRUD - ACTUALIZACIÓN
# ============================================================================

def update_convenios(db: Session, id_conve: int, convenios_update: EditarConvenio) -> bool:
    """
    Actualiza un convenio existente con validación de datos.
    Solo actualiza los campos proporcionados.
    """
    try:
        fields = convenios_update.model_dump(exclude_unset=True)
        
        if not fields:
            logger.warning(f"No se proporcionaron campos para actualizar en convenio ID: {id_conve}")
            return False
        
        # Validar fechas si están presentes
        campos_fecha = [
            "fecha_firma", "fecha_inicio", "plazo_ejecucion",
            "prorroga", "plazo_prorroga", "fecha_publicacion_proceso"
        ]
        
        for campo in campos_fecha:
            if campo in fields and fields[campo]:
                if not validar_fecha_formato(fields[campo]):
                    logger.warning(f"Fecha inválida en {campo}: {fields[campo]}")
                    fields[campo] = "N/A"
        
        # Limpiar campos de texto
        campos_texto = [
            "num_convenio", "num_proceso", "objetivo_convenio", "duracion_convenio",
            "duracion_total", "enlace_secop", "supervisor", "tipo_convenio_sena",
            "persona_apoyo_fpi", "enlace_evidencias", "nombre_institucion"
        ]
        
        for campo in campos_texto:
            if campo in fields and fields[campo]:
                fields[campo] = limpiar_texto_convenio(fields[campo])
        
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["id_conven"] = id_conve

        query = text(f"""
            UPDATE convenios 
            SET {set_clause} 
            WHERE id_convenio = :id_conven
        """)
        
        result = db.execute(query, fields)
        db.commit()
        
        if result.rowcount > 0:
            logger.info(f"Convenio actualizado exitosamente: ID {id_conve}")
            return True
        else:
            logger.warning(f"No se encontró convenio con ID: {id_conve}")
            return False
            
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar el convenio: {str(e)}")
        raise Exception(f"Error de base de datos al actualizar el convenio: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al actualizar el convenio: {str(e)}")
        raise Exception(f"Error al actualizar el convenio: {str(e)}")

# ============================================================================
# OPERACIONES CRUD - ELIMINACIÓN
# ============================================================================

def eliminar_convenio(db: Session, id_convenio: int) -> bool:
    """
    Elimina un convenio de la base de datos.
    """
    try:
        query = text("""
            DELETE FROM convenios
            WHERE convenios.id_convenio = :id_eliminar
        """)
        result = db.execute(query, {"id_eliminar": id_convenio})
        db.commit()
        
        if result.rowcount > 0:
            logger.info(f"Convenio eliminado exitosamente: ID {id_convenio}")
            return True
        else:
            logger.warning(f"No se encontró convenio con ID: {id_convenio}")
            return False
            
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar convenio por id: {str(e)}")
        raise Exception(f"Error de base de datos al eliminar el convenio: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al eliminar convenio: {str(e)}")
        raise Exception(f"Error al eliminar el convenio: {str(e)}")

# ============================================================================
# FUNCIÓN DE SEGURIDAD (LEGACY)
# ============================================================================

def obtener_convenios_by_nit_security(db: Session, id_convenio_seguro: int):
    """
    Función de seguridad para obtener convenio por ID.
    Mantiene compatibilidad con código existente.
    """
    return obtener_convenio_by_id(db, id_convenio_seguro)