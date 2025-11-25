from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.convenios_schema import CrearConvenio, EditarConvenio, RetornoConvenio
from core.security import get_hashed_password, verify_password

logger = logging.getLogger(__name__)

def crear_convenio(db: Session, convenio: CrearConvenio) -> Optional[bool]:
    try:
        dataconvenios = convenio.model_dump() # convierte el esquema en diccionario
    
        query = text("""
            INSERT INTO convenios (
                tipo_convenio,num_convenio,nit_institucion,num_proceso,nombre_institucion,
                estado_convenio,objetivo_convenio, tipo_proceso,fecha_firma,fecha_inicio,duracion_convenio,
                     plazo_ejecucion, prorroga, plazo_prorroga, duracion_total, fecha_publicacion_proceso,enlace_secop,
                     supervisor, precio_estimado, tipo_convenio_sena, persona_apoyo_fpi, enlace_evidencias, fecha_vigencia
            ) VALUES (
                :tipo_convenio, :num_convenio, :nit_institucion, :num_proceso, :nombre_institucion,
                :estado_convenio, :objetivo_convenio, :tipo_proceso, :fecha_firma, :fecha_inicio, :duracion_convenio,
                     :plazo_ejecucion, :prorroga, :plazo_prorroga, :duracion_total, :fecha_publicacion_proceso, :enlace_secop,
                     :supervisor, :precio_estimado, :tipo_convenio_sena, :persona_apoyo_fpi, :enlace_evidencias, :fecha_vigencia
            )
        """)
        db.execute(query, dataconvenios)
        db.commit()

        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear el convenio: {e}")
        raise Exception("Error de base de datos al crear el convenio")

def obtener_convenios_by_id(db: Session, id_conv:int):
    try:
        query = text("""
            SELECT  convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                    convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                    convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                    convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, convenios.persona_apoyo_fpi, convenios.enlace_evidencias, convenios.fecha_vigencia
            FROM convenios
            WHERE convenios.id_convenio = :id_convenio
        """)

        result = db.execute(query, {"id_convenio": id_conv}).mappings().first()
        return result
    
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar el convenio por id: {e}")
        raise Exception("Error de base de datos al buscar el convenio por id")


def obtener_convenios_by_tipo_convenio(db: Session, tipo_conve:str):
    try:
        query = text("""
            SELECT  convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                    convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                    convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                    convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, convenios.persona_apoyo_fpi, convenios.enlace_evidencias, convenios.fecha_vigencia
            FROM convenios
            WHERE convenios.tipo_convenio = :tipo_conve
        """)

        result = db.execute(query, {"tipo_conve": tipo_conve}).mappings().first()
        return result
    
    except SQLAlchemyError as e:
        logger.error(f"Error al bucar los convenios por tipo de convenio: {e}")
        raise Exception("Error de base de datos al buscar los convenios por tipo")


def obtener_convenios_by_nit_institucion(db: Session, nit_provee:str):
    try:
        query = text("""
            SELECT  convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                    convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                    convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                    convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, convenios.persona_apoyo_fpi, convenios.enlace_evidencias, convenios.fecha_vigencia
            FROM convenios
            WHERE convenios.nit_institucion = :nit_proveed
        """)

        result = db.execute(query, {"nit_proveed": nit_provee}).mappings().first()
        return result
    
    except SQLAlchemyError as e:
        logger.error(f"Error al bucar los convenios por nit de institucion: {e}")
        raise Exception("Error de base de datos al buscar los convenios por tipo")


def obtener_convenios_by_estado_convenio(db: Session, estado_conve:str):
    try:
        query = text("""
            SELECT  convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                    convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                    convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                    convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, convenios.persona_apoyo_fpi, convenios.enlace_evidencias, convenios.fecha_vigencia
            FROM convenios
            WHERE convenios.estado_convenio = :convenio_estado
        """)

        result = db.execute(query, {"convenio_estado": estado_conve}).mappings().first()
        return result
    
    except SQLAlchemyError as e:
        logger.error(f"Error al bucar los convenios por estado: {e}")
        raise Exception("Error de base de datos al buscar los convenios por estado")

def eliminar_convenio(db: Session, id_convenio:int):
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
        raise Exception("Error de base de datos al eliminar el Convenio")


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

def obtener_convenios_by_nit_security(db: Session, id_convenio_seguro:int):
    try:
        query = text("""
            SELECT  convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                    convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                    convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                    convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, convenios.persona_apoyo_fpi, convenios.enlace_evidencias, convenios.fecha_vigencia
            FROM convenios
            WHERE convenios.id_convenio = :convenio_seguro
        """)

        result = db.execute(query, {"convenio_seguro": id_convenio_seguro}).mappings().first()
        return result
    
    except SQLAlchemyError as e:
        logger.error(f"Error al bucar el convenio por id: {e}")
        raise Exception("Error de base de datos al buscar el convenio por id")


