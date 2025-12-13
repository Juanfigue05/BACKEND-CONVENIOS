from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.homologaciones_schema import CrearHomologacion, RetornoHomologacion, EditarHomologacion
from sqlalchemy.orm import Session
from app.schemas.usuarios import RetornoUsuario
from app.router.dependencies import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import homologaciones_crud as crud_homologacion
from typing import List

router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_homologacion(homologacion: CrearHomologacion, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        crear = crud_homologacion.crear_Homologacion(db, homologacion)
        if crear:
            return{"message": "homologacion creada correctamente"}
        else:
            return {"message": "La homologacion no puede ser creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-todas-homologaciones/", status_code=status.HTTP_200_OK, response_model=List[RetornoHomologacion])
def get_all_homologaciones(
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        homologaciones = crud_homologacion.get_all_homologaciones(db)
        if homologaciones is None:
            raise HTTPException(status_code=404, detail="Homologaciones no encontrados")
        return homologaciones
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/obtener-por-id/{id_homologacion}", status_code=status.HTTP_200_OK, response_model=List[RetornoHomologacion])
def get_homologaciones_by_id(id_homologacion: int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        homologacion = crud_homologacion.obtener_homologacion_by_id(db, id_homologacion)
        if homologacion is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="homologacion no encontrada")
        return homologacion
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-nivel-programa/{nivel_programa}", status_code=status.HTTP_200_OK, response_model=List[RetornoHomologacion])
def get_by_nivel_programa(nivel_programa:str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        niv_prog = crud_homologacion.obtener_homologacion_by_nivel_programa(db, nivel_programa)
        if niv_prog is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="homologacion no encontrada")
        return niv_prog
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-nombre-programa/{nombre_programa_sena}", status_code=status.HTTP_200_OK, response_model=RetornoHomologacion)
def get_by_nombre_programa_sena(nombre_programa_sena:str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        nom_pro_sena = crud_homologacion.obtener_homologacion_by_nombre_programa_sena(db, nombre_programa_sena)
        if nom_pro_sena is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="homologacion no encontrada")
        return nom_pro_sena
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/editar/{id_homologacion}")
def update_homologacion(id_homologacion: int, homologacion: EditarHomologacion, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        success = crud_homologacion.homologacion_update(db, id_homologacion, homologacion)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la homologacion")
        return {"message": "Homologacion actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/eliminar-por-id/{id_homologacion}", status_code=status.HTTP_200_OK)
def delete_by_id(id_homologacion:int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        user = crud_homologacion.eliminar_homologacion(db, id_homologacion)
        if user:
            return {"message": "Homologacion eliminada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))