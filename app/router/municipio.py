from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.municipio import MunicipioBase
from app.router.dependencies import get_current_user
from app.schemas.usuarios import RetornoUsuario
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import municipio as crud_municipio

router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_municipio(municipio: MunicipioBase, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para registrar municipio")
        
        crear = crud_municipio.create_municipio(db, municipio)
        if crear:
            return {"message": "Municipio creado correctamente"}
        else:
            return {"message": "El municipio no puede ser creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

  
@router.get("/obtener-por-nombre", status_code=status.HTTP_200_OK, response_model=List[MunicipioBase])
async def get_by_name(nom_municipio:str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para buscar municipios")
        
        municipio = crud_municipio.get_municipios(db, nom_municipio)
        if municipio is None:
            raise HTTPException(status_code=404, detail="Municipio no encontrado")
        return municipio
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-todos", status_code=status.HTTP_200_OK, response_model=List[MunicipioBase])
async def get_all( db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para buscar municipios")
        
        municipio = crud_municipio.get_municipio_by_name(db)
        if municipio is None:
            raise HTTPException(status_code=404, detail="Municipio no encontrado")
        return municipio
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-id/{id_municipio}", status_code=status.HTTP_200_OK, response_model=MunicipioBase)
def get_by_id(id_municipio:int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para buscar municipios")
        
        municipio = crud_municipio.get_municipio_by_id(db, id_municipio)
        if municipio is None:
            raise HTTPException(status_code=404, detail="Municipio no encontrado")
        return municipio
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
    
@router.put("/editar/{id_municipio}")
def update_municipio(id_municipio: int, municipio: MunicipioBase, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para editar municipios")
        
        success = crud_municipio.update_municipio(db, id_municipio, municipio)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el municipio")
        return {"message": "Municipio actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/eliminar-por-id/{id_municipio}")
def delete_municipio(id_municipio: int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para borrar municipios")
        
        municipio = crud_municipio.municipio_delete(db, id_municipio)
        if municipio:
            return {"message": "Municipio eliminado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))