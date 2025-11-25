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