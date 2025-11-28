from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from datetime import datetime
import logging

from app.schemas.convenios_schema import CrearConvenio, EditarConvenio, RetornoConvenio

logger = logging.getLogger(__name__)

def crear_convenio(db: Session, convenio: CrearConvenio) -> Optional[bool]:
    try:
        dataconvenios = convenio.model_dump()
    
        query = text("""
            INSERT INTO convenios (
                tipo_convenio, num_convenio, nit_institucion, num_proceso, nombre_institucion,
                estado_convenio, objetivo_convenio, tipo_proceso, fecha_firma, fecha_inicio, duracion_convenio,
                plazo_ejecucion, prorroga, plazo_prorroga, duracion_total, fecha_publicacion_proceso, enlace_secop,
                supervisor, precio_estimado, tipo_convenio_sena, persona_apoyo_fpi, enlace_evidencias
            ) VALUES (
                :tipo_convenio, :num_convenio, :nit_institucion, :num_proceso, :nombre_institucion,
                :estado_convenio, :objetivo_convenio, :tipo_proceso, :fecha_firma, :fecha_inicio, :duracion_convenio,
                :plazo_ejecucion, :prorroga, :plazo_prorroga, :duracion_total, :fecha_publicacion_proceso, :enlace_secop,
                :supervisor, :precio_estimado, :tipo_convenio_sena, :persona_apoyo_fpi, :enlace_evidencias
            )
        """)
        db.execute(query, dataconvenios)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear el convenio: {e}")
        raise Exception("Error de base de datos al crear el convenio")

def obtener_todos_convenios(db: Session) -> List[RetornoConvenio]:
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
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener todos los convenios: {e}")
        raise Exception("Error de base de datos al obtener los convenios")

def obtener_convenio_by_id(db: Session, id_convenio: int):
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
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar el convenio por id: {e}")
        raise Exception("Error de base de datos al buscar el convenio por id")

def obtener_convenios_by_num_convenio(db: Session, num_conv: str):
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
        """)
        result = db.execute(query, {"num_convenio": filtro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar el convenio por número: {e}")
        raise Exception("Error de base de datos al buscar el convenio por número")

def obtener_convenios_by_tipo_convenio(db: Session, tipo_conv: str):
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
        """)
        result = db.execute(query, {"tipo_conve": tipo_conv}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por tipo de convenio: {e}")
        raise Exception("Error de base de datos al buscar los convenios por tipo")

def obtener_convenios_by_nit_institucion(db: Session, nit_inst: str):
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
        """)
        result = db.execute(query, {"nit_proveed": nit_inst}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por nit de institución: {e}")
        raise Exception("Error de base de datos al buscar los convenios por NIT")

def obtener_convenios_by_nombre_institucion(db: Session, nombre_inst: str):
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
        """)
        result = db.execute(query, {"nombre_inst": filtro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por nombre de institución: {e}")
        raise Exception("Error de base de datos al buscar los convenios por nombre")

def obtener_convenios_by_estado_convenio(db: Session, estado_conv: str):
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
        """)
        result = db.execute(query, {"convenio_estado": estado_conv}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por estado: {e}")
        raise Exception("Error de base de datos al buscar los convenios por estado")

def obtener_convenios_by_tipo_proceso(db: Session, tipo_proc: str):
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
        """)
        result = db.execute(query, {"tipo_proceso": tipo_proc}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por tipo de proceso: {e}")
        raise Exception("Error de base de datos al buscar los convenios por tipo de proceso")

def obtener_convenios_by_supervisor(db: Session, superv: str):
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
        """)
        result = db.execute(query, {"supervisor": filtro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por supervisor: {e}")
        raise Exception("Error de base de datos al buscar los convenios por supervisor")

def obtener_convenios_by_tipo_convenio_sena(db: Session, tipo_conv_sena: str):
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
        """)
        result = db.execute(query, {"tipo_conv_sena": tipo_conv_sena}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por tipo convenio SENA: {e}")
        raise Exception("Error de base de datos al buscar los convenios por tipo convenio SENA")

def obtener_convenios_by_persona_apoyo(db: Session, persona_ap: str):
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
        """)
        result = db.execute(query, {"persona_apoyo": filtro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por persona de apoyo: {e}")
        raise Exception("Error de base de datos al buscar los convenios por persona de apoyo")

def obtener_convenios_by_rango_fechas_firma(db: Session, fecha_ini: datetime, fecha_fin: datetime):
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
            WHERE convenios.fecha_firma BETWEEN :fecha_inicio AND :fecha_fin
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"fecha_inicio": fecha_ini, "fecha_fin": fecha_fin}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por rango de fechas de firma: {e}")
        raise Exception("Error de base de datos al buscar los convenios por rango de fechas")

def obtener_convenios_by_rango_fechas_inicio(db: Session, fecha_ini: datetime, fecha_fin: datetime):
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
            WHERE convenios.fecha_inicio BETWEEN :fecha_inicio AND :fecha_fin
            ORDER BY convenios.fecha_inicio DESC
        """)
        result = db.execute(query, {"fecha_inicio": fecha_ini, "fecha_fin": fecha_fin}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por rango de fechas de inicio: {e}")
        raise Exception("Error de base de datos al buscar los convenios por rango de fechas de inicio")

def obtener_convenios_by_num_proceso(db: Session, num_proc: str):
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
        """)
        result = db.execute(query, {"num_proceso": filtro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por número de proceso: {e}")
        raise Exception("Error de base de datos al buscar los convenios por número de proceso")

def buscar_convenios_by_objetivo(db: Session, palabra: str):
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
        """)
        result = db.execute(query, {"palabra_clave": filtro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar los convenios por objetivo: {e}")
        raise Exception("Error de base de datos al buscar los convenios por objetivo")

def eliminar_convenio(db: Session, id_convenio: int):
    try:
        query = text("""
            DELETE FROM convenios
            WHERE convenios.id_convenio = :id_eliminar
        """)
        db.execute(query, {"id_eliminar": id_convenio})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar convenio por id: {e}")
        raise Exception("Error de base de datos al eliminar el convenio")

def update_convenios(db: Session, id_conve: int, convenios_update: EditarConvenio) -> bool:
    try:
        fields = convenios_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["id_conven"] = id_conve

        query = text(f"UPDATE convenios SET {set_clause} WHERE id_convenio = :id_conven")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar el convenio: {e}")
        raise Exception("Error de base de datos al actualizar el convenio")

def obtener_convenios_by_nit_security(db: Session, id_convenio_seguro: int):
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
            WHERE convenios.id_convenio = :convenio_seguro
        """)
        result = db.execute(query, {"convenio_seguro": id_convenio_seguro}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar el convenio por id: {e}")
        raise Exception("Error de base de datos al buscar el convenio por id")