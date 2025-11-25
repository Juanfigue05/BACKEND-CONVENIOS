from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.egresado_convenio import Egresado_convenioBase

logger = logging.getLogger(__name__)

def create_egresado_convenio(db: Session, egresado_convenio: Egresado_convenioBase) -> bool:
    try:
        dataEgresado_convenio = egresado_convenio.model_dump()
        
        query = text("""
            INSERT INTO egresado_convenio(documento, num_proceso)
            VALUES (:documento, :num_proceso)
        """)
        db.execute(db, dataEgresado_convenio)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear conexion egresado-convenio: {e}")
        raise Exception ("Error en la base de datos al crear vinculo egresado-convenio")