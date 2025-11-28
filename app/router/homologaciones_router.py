from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.homologaciones_schema import HomologacionBase, RetornoHomologacion, EditarHomologacion
from sqlalchemy.orm import Session
from app.schemas.usuarios import RetornoUsuario
from app.router.dependencies import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import homologaciones_crud as crud_homologacion

router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_institucion(homologacion: HomologacionBase, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        crear = crud_homologacion.crear_Homologacion(db, homologacion)
        if crear:
            return{"message": "homologacion creado correctamente"}
        else:
            return {"message": "La homologacion no puede ser creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-id", status_code=status.HTTP_200_OK, response_model=RetornoHomologacion)
def get_by_id(id_homologacion: int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        homologacion = crud_homologacion.obtener_homologacion_by_id(db, id_homologacion)
        if homologacion is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="homologacion no encontrada")
        return homologacion
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-nivel-programa", status_code=status.HTTP_200_OK, response_model=RetornoHomologacion)
def get_by_mivel_programa(nivel_program:str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        niv_prog = crud_homologacion.obtener_homologacion_by_nivel_programa(db, nivel_program)
        if niv_prog is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="homologacion no encontrada")
        return niv_prog
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-nombre-programa", status_code=status.HTTP_200_OK, response_model=RetornoHomologacion)
def get_by_nombre_programa_sena(nomb_program_sena:str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        nom_pro_sena = crud_homologacion.obtener_homologacion_by_nombre_programa_sena(db, nomb_program_sena)
        if nom_pro_sena is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="homologacion no encontrada")
        return nom_pro_sena
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/editar/{id_homologacion}")
def update_convenios(id_homologacion: int, homologacion: EditarHomologacion, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
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
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        user = crud_homologacion.eliminar_homologacion(db, id_homologacion)
        if user:
            return {"message": "Homologacion eliminada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))