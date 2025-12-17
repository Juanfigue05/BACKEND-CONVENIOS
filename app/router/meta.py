from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from core.database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get('/ultima-actualizacion', status_code=200)
def ultima_actualizacion(db: Session = Depends(get_db)):
    try:
        # Agrupar las últimas fechas de actualización de tablas relevantes y devolver la máxima
        query = text("""
            SELECT MAX(ultima) AS ultima FROM (
                SELECT MAX(fecha_actualizacion) AS ultima FROM instituciones
                UNION ALL
                SELECT MAX(fecha_actualizacion) FROM convenios
                UNION ALL
                SELECT MAX(fecha_actualizacion) FROM homologacion
                UNION ALL
                SELECT MAX(fecha_actualizacion) FROM municipio
                UNION ALL
                SELECT MAX(fecha_actualizacion) FROM usuarios
            ) t
        """)
        result = db.execute(query).scalar()
        logger.info("ultima_actualizacion consulta retornó: %s", result)
        if result is None:
            return {"ultima_actualizacion": None}
        # Si es un objeto datetime, devolver en ISO; si es string, devolver tal cual
        try:
            return {"ultima_actualizacion": result.isoformat()}
        except Exception:
            return {"ultima_actualizacion": str(result)}
    except SQLAlchemyError as e:
        logger.error("Error al obtener ultima_actualizacion: %s", e)
        raise HTTPException(status_code=500, detail=str(e))