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
        
        query = text("""
            INSERT INTO instituciones(nit_institucion, nombre_institucion,
            direccion, id_municipio)
            VALUES (:nit_institucion, :nombre_institucion, :direccion, :id_municipio)
        """)
        db.execute(query, dataInstitucion)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear la institucción :{e}")
        raise Exception("Error de base de datos al crear una institución")

def get_institucion_by_nit(db: Session, nit_institucion:int):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, instituciones.nombre_institucion,
                    instituciones.direccion, instituciones.id_municipio, instituciones.cant_convenios, municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE instituciones.nit_institucion = :registro_institucion
        """)
        result = db.execute(query, {"registro_institucion": nit_institucion}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por nit: {e}")
        raise Exception("Error de la base de datos al buscar institución")
    
def get_institucion_by_name(db: Session, name_institucion:str):
    try:
        query = text("""
            SELECT instituciones.nit_institucion, instituciones.nombre_institucion,
                    instituciones.direccion, instituciones.id_municipio, instituciones.cant_convenios, municipio.nom_municipio
            FROM instituciones
            INNER JOIN municipio ON instituciones.id_municipio = municipio.id_municipio
            WHERE instituciones.nit_institucion = :nom_institucion
        """)
        result = db.execute(query, {"nom_institucion": name_institucion}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar institución por nombre: {e}")
        raise Exception("Error de la base de datos al buscar institución")

def institucion_update(db: Session, nit_institucion:int, update_institucion: EditarInstitucion) -> bool:
    try:
        fields = update_institucion.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} =: {key}" for key in fields])
        fields["nit_institucion"] = nit_institucion
        
        query = text(f"UPDATE institucion SET {set_clause} WHERE nit_institucion = :nit_institucion")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error al editar institución: {e}")
        raise Exception("Error de base de datos al actualizar institución")

def institucion_delete(db: Session, nit:int):
    try:
        query = text("""
            DELETE FROM instituciones
            WHERE instituciones.nit_institucion = :el_nit
        """)
        db.execute(db, {"el_nit":nit})
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error al eliminar institución por nit {e}")
        raise Exception("Error de base de datos al eliminar institución")