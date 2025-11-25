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