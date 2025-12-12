from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
import logging

from app.schemas.homologaciones_schema import CrearHomologacion, EditarHomologacion, RetornoHomologacion

logger = logging.getLogger(__name__)

def crear_Homologacion(db: Session, homologacion: CrearHomologacion) -> Optional[bool]:
    try:
        dataHomologacion = homologacion.model_dump()
        query = text("""
            INSERT INTO homologacion(nit_institucion_destino,
            nombre_programa_sena, cod_programa_sena, version_programa, titulo, programa_ies, nivel_programa,
            snies, creditos_homologados, creditos_totales, creditos_pendientes, modalidad, semestres, regional, enlace)
            VALUES (:nit_institucion_destino,
            :nombre_programa_sena, :cod_programa_sena, :version_programa, :titulo, :programa_ies, :nivel_programa,
            :snies, :creditos_homologados, :creditos_totales, :creditos_pendientes, :modalidad, :semestres, :regional, :enlace)
        """)
        db.execute(query, dataHomologacion)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear la homologación: {e}")
        raise Exception("Error de base de datos al crear una homologación")

def get_all_homologaciones(db: Session) -> List[RetornoHomologacion]:
    try:
        query = text("""
            SELECT homologacion.id_homologacion, homologacion.nit_institucion_destino,
            homologacion.nombre_programa_sena, homologacion.cod_programa_sena, homologacion.version_programa, 
            homologacion.titulo, homologacion.programa_ies, homologacion.nivel_programa,
            homologacion.snies, homologacion.creditos_homologados, homologacion.creditos_totales, 
            homologacion.creditos_pendientes, homologacion.modalidad, homologacion.semestres, homologacion.regional, homologacion.enlace
            FROM homologacion
        """)

        result = db.execute(query).mappings().all()
        return result

    except SQLAlchemyError as e:
        logger.error(f"Error al buscar homologaciones: {e}")
        raise Exception("Error de base de datos al buscar las homologaciones")
    
def obtener_homologacion_by_id(db: Session, id_homologacion: int):
    try:
        query = text("""
            SELECT id_homologacion, nit_institucion_destino, nombre_programa_sena,
            cod_programa_sena, version_programa, titulo, programa_ies,
            nivel_programa, snies, creditos_homologados, creditos_totales,
            creditos_pendientes, modalidad, semestres, regional, enlace
            FROM homologacion
            WHERE id_homologacion = :id_homolog
        """)
        result = db.execute(query, {"id_homolog": id_homologacion}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar homologación por id: {e}")
        raise Exception("Error de la base de datos al buscar homologación por id")
    
def obtener_homologacion_by_nombre_programa_sena(db: Session, programa_sena: str):
    try:
        query = text("""
            SELECT id_homologacion, nit_institucion_destino, nombre_programa_sena,
            cod_programa_sena, version_programa, titulo, programa_ies,
            nivel_programa, snies, creditos_homologados, creditos_totales,
            creditos_pendientes, modalidad, semestres, regional, enlace
            FROM homologacion
            WHERE nombre_programa_sena LIKE :nom_programa_sena
        """)
        result = db.execute(query, {"nom_programa_sena": f"%{programa_sena}%"}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar homologación por programa sena: {e}")
        raise Exception("Error de la base de datos al buscar homologación por programa sena")
    
def obtener_homologacion_by_nivel_programa(db: Session, nivel_program: str):
    try:
        # SOLUCIÓN: Agregado id_convenio a la query
        query = text("""
            SELECT id_homologacion, nit_institucion_destino, nombre_programa_sena,
            cod_programa_sena, version_programa, titulo, programa_ies,
            nivel_programa, snies, creditos_homologados, creditos_totales,
            creditos_pendientes, modalidad, semestres, regional, enlace
            FROM homologacion
            WHERE nivel_programa = :niv_prog
        """)
        result = db.execute(query, {"niv_prog": nivel_program}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar homologación por nivel de programa: {e}")
        raise Exception("Error de la base de datos al buscar homologación por nivel de programa")

def homologacion_update(db: Session, id_homologacion: int, homologacion_update: EditarHomologacion) -> bool:
    try:
        # Validar que la homologación existe antes de actualizar
        existe = obtener_homologacion_by_id(db, id_homologacion)
        if not existe:
            raise HTTPException(status_code=404, detail="Homologación no encontrada")
        
        fields = homologacion_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["id_homologacion"] = id_homologacion

        query = text(f"UPDATE homologacion SET {set_clause} WHERE id_homologacion = :id_homologacion")
        result = db.execute(query, fields)
        db.commit()
        
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al editar homologación: {e}")
        raise Exception("Error de base de datos al actualizar homologación")

def eliminar_homologacion(db: Session, id_homolog: int):
    try:
        # Validar que la homologación existe antes de eliminar
        existe = obtener_homologacion_by_id(db, id_homolog)
        if not existe:
            raise HTTPException(status_code=404, detail="Homologación no encontrada")
        
        query = text("""
            DELETE FROM homologacion
            WHERE id_homologacion = :homologacion
        """)
        result = db.execute(query, {"homologacion": id_homolog})
        db.commit()
        
        return result.rowcount > 0
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar homologación por id {e}")
        raise Exception("Error de base de datos al eliminar homologación")