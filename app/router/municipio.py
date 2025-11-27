from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.municipio import MunicipioBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import municipio as crud_municipio

router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_municipio(municipio: MunicipioBase, db: Session = Depends(get_db)):
    try:
        crear = crud_municipio.create_municipio(db, municipio)
        if crear:
            return {"message": "Centro creado correctamente"}
        else:
            return {"message": "El municipio no puede ser creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   
    
@router.get("/obtener-por-id/{id_municipio}", status_code=status.HTTP_200_OK, response_model=MunicipioBase)
def get_by_id(id_municipio:int, db: Session = Depends(get_db)):
    try:
        municipio = crud_municipio.get_municipio_by_id(db, id_municipio)
        if municipio is None:
            raise HTTPException(status_code=404, detail="Municipio no encontrado")
        return municipio
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
    
@router.put("/editar/{id_municipio}")
def update_municipio(id_municipio: int, municipio: MunicipioBase, db: Session = Depends(get_db)):
    try:
        success = crud_municipio.update_municipio(db, id_municipio, municipio)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
        return {"message": "Usuario actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))