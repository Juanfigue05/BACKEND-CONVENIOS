from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from datetime import datetime
import logging

from app.schemas.estadistica_schema import CrearEstadisticaCategoria, EditarEstadisticaCategoria, RetornoEstadisticaCategoria

logger = logging.getLogger(__name__)

def crear_estadistica_categoria(db: Session, estadistica: CrearEstadisticaCategoria) -> Optional[bool]:
    try:
        data_estadistica = estadistica.model_dump()
    
        query = text("""
            INSERT INTO estadistica_categoria (
                categoria, nombre, cantidad
            ) VALUES (
                :categoria, :nombre, :cantidad
            )
        """)
        db.execute(query, data_estadistica)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear la estadística de categoría: {e}")
        raise Exception("Error de base de datos al crear la estadística de categoría")

def obtener_todas_estadisticas(db: Session) -> List[RetornoEstadisticaCategoria]:
    try:
        query = text("""
            SELECT  
                id_estadistica, categoria, nombre, cantidad, fecha_actualizacion
            FROM estadistica_categoria
            ORDER BY categoria, nombre
        """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener todas las estadísticas: {e}")
        raise Exception("Error de base de datos al obtener las estadísticas")

def obtener_estadistica_by_id(db: Session, id_estadistica: int):
    try:
        query = text("""
            SELECT  
                id_estadistica, categoria, nombre, cantidad, fecha_actualizacion
            FROM estadistica_categoria
            WHERE id_estadistica = :id_est
        """)
        result = db.execute(query, {"id_est": id_estadistica}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar la estadística por id: {e}")
        raise Exception("Error de base de datos al buscar la estadística por id")

def obtener_estadisticas_by_categoria(db: Session, categoria: str):
    try:
        filtro = f"%{categoria}%"
        query = text("""
            SELECT  
                id_estadistica, categoria, nombre, cantidad, fecha_actualizacion
            FROM estadistica_categoria
            WHERE categoria LIKE :categoria
            ORDER BY nombre
        """)
        result = db.execute(query, {"categoria": filtro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar las estadísticas por categoría: {e}")
        raise Exception("Error de base de datos al buscar las estadísticas por categoría")

def obtener_estadisticas_by_nombre(db: Session, nombre: str):
    try:
        filtro = f"%{nombre}%"
        query = text("""
            SELECT  
                id_estadistica, categoria, nombre, cantidad, fecha_actualizacion
            FROM estadistica_categoria
            WHERE nombre LIKE :nombre
            ORDER BY categoria
        """)
        result = db.execute(query, {"nombre": filtro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar las estadísticas por nombre: {e}")
        raise Exception("Error de base de datos al buscar las estadísticas por nombre")

def obtener_estadisticas_by_categoria_exacta(db: Session, categoria: str):
    try:
        query = text("""
            SELECT  
                id_estadistica, categoria, nombre, cantidad, fecha_actualizacion
            FROM estadistica_categoria
            WHERE categoria = :categoria
            ORDER BY nombre
        """)
        result = db.execute(query, {"categoria": categoria}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar las estadísticas por categoría exacta: {e}")
        raise Exception("Error de base de datos al buscar las estadísticas por categoría exacta")

def eliminar_estadistica(db: Session, id_estadistica: int):
    try:
        query = text("""
            DELETE FROM estadistica_categoria
            WHERE id_estadistica = :id_eliminar
        """)
        db.execute(query, {"id_eliminar": id_estadistica})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar estadística por id: {e}")
        raise Exception("Error de base de datos al eliminar la estadística")

def update_estadistica(db: Session, id_est: int, estadistica_update: EditarEstadisticaCategoria) -> bool:
    try:
        fields = estadistica_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["id_estadist"] = id_est

        query = text(f"UPDATE estadistica_categoria SET {set_clause} WHERE id_estadistica = :id_estadist")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar la estadística: {e}")
        raise Exception("Error de base de datos al actualizar la estadística")