from fastapi import HTTPException, status
from sqlalchemy.orm import Session 
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
import logging

from app.schemas.homologaciones_schema import HomologacionBase, EditarHomologacion

logger = logging.getLogger(__name__)

def crear_Homologacion(db: Session, homologacion: HomologacionBase) -> Optional[bool]:
    try:
        dataHomologacion = homologacion.model_dump()
        
        query = text("""
            INSERT INTO homologacion(id_homologacion, nit_institucion_destino,
            nombre_programa_sena, cod_programa_sena, version_programa, titulo, programa_ies, nivel_programa,
            snies, creditos_homologados, creditos_totales, creditos_pendientes, modalidad, semestres, regional, enlace)
            VALUES ( :id_homologacion, :nit_institucion_destino,
            :nombre_programa_sena, :cod_programa_sena, :version_programa, :titulo, :programa_ies, :nivel_programa,
            :snies, :creditos_homologados, :creditos_totales, :creditos_pendientes, :modalidad, :semestres, :regional, :enlace)
        """)
        db.execute(db, dataHomologacion)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear la homologacion :{e}")
        raise Exception("Error de base de datos al crear una homologacion")

def obtener_homologacion_by_id(db: Session, id_homologacion:int):
    try:
        query = text("""
            SELECT homologacion.id_homologacion, homologacion.nit_institucion_destino, homologacion.nombre_programa_sena,
                      homologacion.cod_programa_sena, homologacion.version_programa, municipio.titulo, homologacion.programa_ies,
                        homologacion.nivel_programa, homologacion.snies, homologacion.creditos_homologados, homologacion.creditos_totales,
                        homologacion.creditos_pendientes, homologacion.modalidad, homologacion.semestres, homologacion.regional, homologacion.enlace
            FROM homologacion
            WHERE homologacion.id_homologacion = :id_homolog
        """)
        result = db.execute(query, {"id_homolog": id_homologacion}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar homologacion por id: {e}")
        raise Exception("Error de la base de datos al buscar homologacion por id")
    
def obtener_homologacion_by_nombre_programa_sena(db: Session, programa_sena:str):
    try:
        query = text("""
            SELECT homologacion.id_homologacion, homologacion.nit_institucion_destino, homologacion.nombre_programa_sena,
                      homologacion.cod_programa_sena, homologacion.version_programa, municipio.titulo, homologacion.programa_ies,
                        homologacion.nivel_programa, homologacion.snies, homologacion.creditos_homologados, homologacion.creditos_totales,
                        homologacion.creditos_pendientes, homologacion.modalidad, homologacion.semestres, homologacion.regional, homologacion.enlace
            FROM homologacion
            WHERE homologacion.nombre_programa_sena LIKE nom_programa_sena
            """)
        result = db.execute(query, {"nom_programa_sena": programa_sena}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar homologacion por programa sena: {e}")
        raise Exception("Error de la base de datos al buscar homologacion por programa sena")
    
def obtener_homologacion_by_nivel_programa(db: Session, nivel_program:str):
    try:
        query = text("""
            SELECT homologacion.id_homologacion, homologacion.nit_institucion_destino, homologacion.nombre_programa_sena,
                      homologacion.cod_programa_sena, homologacion.version_programa, municipio.titulo, homologacion.programa_ies,
                        homologacion.nivel_programa, homologacion.snies, homologacion.creditos_homologados, homologacion.creditos_totales,
                        homologacion.creditos_pendientes, homologacion.modalidad, homologacion.semestres, homologacion.regional, homologacion.enlace
            FROM homologacion
            WHERE homologacion.nivel_programa = :niv_prog
            """)
        result = db.execute(query, {"niv_prog": nivel_program}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar homologacion por nivel de programa: {e}")
        raise Exception("Error de la base de datos al buscar homologacion por nivel de programa")

def homologacion_update(db: Session, id_homologacion:int, homologacion_update: EditarHomologacion) -> bool:
    try:
        fields = homologacion_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} =: {key}" for key in fields])
        fields["id_homolg"] = id_homologacion
        
        query = text(f"UPDATE homologacion SET {set_clause} WHERE id_homologacion = :id_homolg")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error al editar institución: {e}")
        raise Exception("Error de base de datos al actualizar institución")

def eliminar_homologacion(db: Session, id_homolog:int):
    try:
        query = text("""
            DELETE FROM homologacion
            WHERE homologacion.id_homologacion = :homologacion
        """)
        db.execute(db, {"homologacion":id_homolog})
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error al eliminar homologacion por id {e}")
        raise Exception("Error de base de datos al eliminar homologacion")