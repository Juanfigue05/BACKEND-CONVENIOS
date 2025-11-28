from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.institucion import InstitucionBase, RetornarInstitucion, EditarInstitucion
from app.schemas.usuarios import RetornoUsuario
from app.router.dependencies import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import institucion as crud_instituciones

router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_institucion(institucion: InstitucionBase, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        crear = crud_instituciones.create_institucion(db, institucion)
        if crear:
            return{"message": "Institución creada correctamente"}
        else:
            return {"message": "La institución no puede ser creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-nit", status_code=status.HTTP_200_OK, response_model=List[RetornarInstitucion])
def get_by_nit(nit_institucion: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        instituciones = crud_instituciones.get_institucion_by_nit(db, nit_institucion)
        if instituciones is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Institución no encontrada")
        return instituciones
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-nombre", status_code=status.HTTP_200_OK, response_model=List[RetornarInstitucion])
async def get_by_name(nombre_institucion:str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        institucion = crud_instituciones.get_institucion_by_name(db, nombre_institucion)
        if institucion is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Institución no encontrada")
        return institucion
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/editar/{nit_institucion}")
def update_institucion(nit_institucion: str, institucion: EditarInstitucion, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        success = crud_instituciones.institucion_update(db, nit_institucion, institucion)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar institución")
        return {"message": "Institución actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("eliminar-por-nit/{nit_institucion}")
def delete_institucion(nit_institucion: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
        institucion = crud_instituciones.institucion_delete(db, nit_institucion)
        if institucion:
            return {"message": "Institución eliminada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    