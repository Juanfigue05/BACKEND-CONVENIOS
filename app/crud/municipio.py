from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.municipio import MunicipioBase

logger = logging.getLogger(__name__)

def create_municipio(db: Session, municipio: MunicipioBase) -> bool:
    try:
        dataMunicipio = municipio.model_dump()
        
        query = text("""
            INSERT INTO municipio(
                id_municipio, nom_municipio
            ) VALUES (
                :id_municipio, :nom_municipio
            )
        """)
        db.execute(query, dataMunicipio)
        db.commit()
        
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear el municipio: {e}")
        raise Exception("Error de base de datos al crear municipio")
    
def get_municipio_by_id(db: Session, id_municipio:int):
    try:
        query = text("""
            SELECT id_municipio, nom_municipio
            FROM municipio
            WHERE id_municipio = :id_municipio
        """)

        result = db.execute(query, {"id_municipio": id_municipio}).mappings().first()
        return result
    
    except SQLAlchemyError as e:
        logger.error(f"Error al bucar municipio por id: {e}")
        raise Exception("Error de base de datos al buscar el municipio")
    
def get_municipio_by_name(db: Session, nom_municipio:str):
    try:
        # buscar por patrón (ej. una letra) usando LIKE, se añade el % alrededor del parámetro
        nom_municipio = f"%{nom_municipio}%"
        query = text("""
            SELECT id_municipio, nom_municipio
            FROM municipio
            WHERE UPPER(nom_municipio) LIKE UPPER(:nom_municipio)
        """)
        result = db.execute(query, {"nom_municipio": nom_municipio}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar municipio por nombre: {e}")
        raise Exception("Error de la base de datos al buscar municipio")
    
def update_municipio(db: Session, id_municipio: int, municipio_update: MunicipioBase) -> bool:
    try:
        fields = municipio_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["id_municipio"] = id_municipio
        query = text(f"UPDATE municipio SET {set_clause} WHERE id_municipio = :id_municipio")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar municipio: {e}")
        raise Exception("Error de base de datos al actualizar el municipio")
    
def municipio_delete(db: Session, id_municipio: int) -> bool:
    try:
        query = text("""
            DELETE FROM municipio
            WHERE id_municipio = :id_municipio
        """)
        db.execute(query, {"id_municipio": id_municipio})
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error al eliminar municipio por id {e}")
        raise Exception("Error de base de datos al eliminar municipio")