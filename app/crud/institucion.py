from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.institucion import InstitucionBase, EditarInstitucion

logger = logging.getLogger(__name__)

def create_institucion(db: Session, institucion: InstitucionBase) -> Optional[bool]:
    try:
        dataInstitucion = institucion.model_dump()
        # Log the payload for debugging
        try:
            logger.info("create_institucion data: %s", dataInstitucion)
        except Exception:
            logger.info("create_institucion data: <unserializable>")
        # Ensure id_municipio exists and is string (DB expects VARCHAR)
        if not dataInstitucion.get("id_municipio"):
            logger.warning("create_institucion: id_municipio is missing or empty")
        else:
            # cast to str to be safe
            dataInstitucion["id_municipio"] = str(dataInstitucion["id_municipio"]) if dataInstitucion.get("id_municipio") is not None else dataInstitucion.get("id_municipio")

        query = text("""
            INSERT INTO instituciones(nit_institucion, nombre_institucion,
            direccion, id_municipio, cant_convenios)
            VALUES (:nit_institucion, :nombre_institucion, :direccion, :id_municipio, :cant_convenios)
        """)
        db.execute(query, dataInstitucion)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear la institución: {e}")
        raise Exception("Error de base de datos al crear una institución")

def get_institucion_by_nit(db: Session, nit_institucion: str):
    try:
        ni_institucion = f"{nit_institucion}%"
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE UPPER(instituciones.nit_institucion) LIKE UPPER(:nit_intitu)
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query, {"nit_intitu": ni_institucion}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por nit: {e}")
        raise Exception("Error de la base de datos al buscar institución")
    
def get_institucion_by_name(db: Session, name_institucion: str):
    try:
        name_institucion = f"{name_institucion}%"
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE UPPER(instituciones.nombre_institucion) LIKE UPPER(:nom_institucion)
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query, {"nom_institucion": name_institucion}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por nombre: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def get_institucion_by_direccion(db: Session, direccion: str):
    try:
        direccion_pattern = f"{direccion}%"
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE UPPER(instituciones.direccion) LIKE UPPER(:direccion)
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query, {"direccion": direccion_pattern}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por dirección: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def get_institucion_by_municipio(db: Session, id_municipio: int):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE instituciones.id_municipio = :id_municipio
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query, {"id_municipio": id_municipio}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por municipio: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def get_institucion_by_convenios(db: Session, cant_convenios: int):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE instituciones.cant_convenios = :cant_convenios
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query, {"cant_convenios": cant_convenios}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por cantidad de convenios: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def get_institucion_by_rango_convenios(db: Session, min_convenios: int, max_convenios: int):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE instituciones.cant_convenios BETWEEN :min_convenios AND :max_convenios
            ORDER BY instituciones.cant_convenios DESC, instituciones.nombre_institucion
        """)
        result = db.execute(query, {"min_convenios": min_convenios, "max_convenios": max_convenios}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por rango de convenios: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def get_all_instituciones(db: Session):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener todas las instituciones: {e}")
        raise Exception("Error de la base de datos al obtener instituciones")

def busqueda_avanzada_instituciones(
    db: Session, 
    nit_institucion: Optional[str] = None,
    nombre_institucion: Optional[str] = None,
    direccion: Optional[str] = None,
    id_municipio: Optional[int] = None,
    min_convenios: Optional[int] = None,
    max_convenios: Optional[int] = None
):
    try:
        conditions = []
        params = {}
        
        if nit_institucion:
            conditions.append("UPPER(instituciones.nit_institucion) LIKE UPPER(:nit_institucion)")
            params["nit_institucion"] = f"{nit_institucion}%"
        
        if nombre_institucion:
            conditions.append("UPPER(instituciones.nombre_institucion) LIKE UPPER(:nombre_institucion)")
            params["nombre_institucion"] = f"{nombre_institucion}%"
        
        if direccion:
            conditions.append("UPPER(instituciones.direccion) LIKE UPPER(:direccion)")
            params["direccion"] = f"{direccion}%"
        
        if id_municipio is not None:
            conditions.append("instituciones.id_municipio = :id_municipio")
            params["id_municipio"] = id_municipio
        
        if min_convenios is not None and max_convenios is not None:
            conditions.append("instituciones.cant_convenios BETWEEN :min_convenios AND :max_convenios")
            params["min_convenios"] = min_convenios
            params["max_convenios"] = max_convenios
        elif min_convenios is not None:
            conditions.append("instituciones.cant_convenios >= :min_convenios")
            params["min_convenios"] = min_convenios
        elif max_convenios is not None:
            conditions.append("instituciones.cant_convenios <= :max_convenios")
            params["max_convenios"] = max_convenios
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = text(f"""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE {where_clause}
            ORDER BY instituciones.nombre_institucion
        """)
        
        result = db.execute(query, params).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error en búsqueda avanzada de instituciones: {e}")
        raise Exception("Error de la base de datos en búsqueda avanzada")

def institucion_update(db: Session, nit_institucion: str, update_institucion: EditarInstitucion) -> bool:
    try:
        fields = update_institucion.model_dump(exclude_unset=True)
        if not fields:
            return False
        # Log incoming update fields
        try:
            logger.info("institucion_update fields: %s", fields)
        except Exception:
            logger.info("institucion_update fields: <unserializable>")
        # ensure id_municipio is string if present
        if "id_municipio" in fields and fields["id_municipio"] is not None:
            fields["id_municipio"] = str(fields["id_municipio"])

        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["nit_institucion"] = nit_institucion
        
        query = text(f"UPDATE instituciones SET {set_clause} WHERE nit_institucion = :nit_institucion")
        result = db.execute(query, fields)
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        logger.error(f"Error al editar institución: {e}")
        db.rollback() 
        raise Exception("Error de base de datos al actualizar institución")

def get_institucion_by_direccion(db: Session, direccion: str):
    try:
        direccion_pattern = f"%{direccion}%"
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE UPPER(instituciones.direccion) LIKE UPPER(:direccion)
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query, {"direccion": direccion_pattern}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por dirección: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def get_institucion_by_municipio(db: Session, id_municipio: int):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE instituciones.id_municipio = :id_municipio
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query, {"id_municipio": id_municipio}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por municipio: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def get_institucion_by_convenios(db: Session, cant_convenios: int):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE instituciones.cant_convenios = :cant_convenios
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query, {"cant_convenios": cant_convenios}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por cantidad de convenios: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def get_institucion_by_rango_convenios(db: Session, min_convenios: int, max_convenios: int):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE instituciones.cant_convenios BETWEEN :min_convenios AND :max_convenios
            ORDER BY instituciones.cant_convenios DESC, instituciones.nombre_institucion
        """)
        result = db.execute(query, {"min_convenios": min_convenios, "max_convenios": max_convenios}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por rango de convenios: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def get_all_instituciones(db: Session):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            ORDER BY instituciones.nombre_institucion
        """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener todas las instituciones: {e}")
        raise Exception("Error de la base de datos al obtener instituciones")

def busqueda_avanzada_instituciones(
    db: Session, 
    nit_institucion: Optional[str] = None,
    nombre_institucion: Optional[str] = None,
    direccion: Optional[str] = None,
    id_municipio: Optional[int] = None,
    min_convenios: Optional[int] = None,
    max_convenios: Optional[int] = None
):
    try:
        conditions = []
        params = {}
        
        if nit_institucion:
            conditions.append("UPPER(instituciones.nit_institucion) LIKE UPPER(:nit_institucion)")
            params["nit_institucion"] = f"%{nit_institucion}%"
        
        if nombre_institucion:
            conditions.append("UPPER(instituciones.nombre_institucion) LIKE UPPER(:nombre_institucion)")
            params["nombre_institucion"] = f"%{nombre_institucion}%"
        
        if direccion:
            conditions.append("UPPER(instituciones.direccion) LIKE UPPER(:direccion)")
            params["direccion"] = f"%{direccion}%"
        
        if id_municipio is not None:
            conditions.append("instituciones.id_municipio = :id_municipio")
            params["id_municipio"] = id_municipio
        
        if min_convenios is not None and max_convenios is not None:
            conditions.append("instituciones.cant_convenios BETWEEN :min_convenios AND :max_convenios")
            params["min_convenios"] = min_convenios
            params["max_convenios"] = max_convenios
        elif min_convenios is not None:
            conditions.append("instituciones.cant_convenios >= :min_convenios")
            params["min_convenios"] = min_convenios
        elif max_convenios is not None:
            conditions.append("instituciones.cant_convenios <= :max_convenios")
            params["max_convenios"] = max_convenios
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        query = text(f"""
            SELECT instituciones.nit_institucion, 
                instituciones.nombre_institucion,
                instituciones.direccion, 
                instituciones.id_municipio, 
                instituciones.cant_convenios, 
                municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE {where_clause}
            ORDER BY instituciones.nombre_institucion
        """)
        
        result = db.execute(query, params).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error en búsqueda avanzada de instituciones: {e}")
        raise Exception("Error de la base de datos en búsqueda avanzada")

def institucion_delete(db: Session, nit: str):
    try:
        query = text("""
            DELETE FROM instituciones
            WHERE instituciones.nit_institucion = :el_nit
        """)
        result = db.execute(query, {"el_nit": nit})
        db.commit()
        return result.rowcount > 0
    except SQLAlchemyError as e:
        logger.error(f"Error al eliminar institución por nit: {e}")
        db.rollback()
        raise Exception("Error de base de datos al eliminar institución")