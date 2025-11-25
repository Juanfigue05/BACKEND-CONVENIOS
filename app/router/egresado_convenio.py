from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.egresado_convenio import Egresado_convenioBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import egresado_convenio as crud_egresado_convenio

router = APIRouter()

@router.post("/registrar convenio-egresado", status_code=status.HTTP_201_CREATED)
def create_egresadoConvenio(egresado_convenio: Egresado_convenioBase, db: Session = Depends(get_db)):
    try:
        crear = crud_egresado_convenio.create_egresado_convenio(db, egresado_convenio)
        if crear: 
            return {"message": "Conexion egresado convenio creada exitosamente"}
        else:
            return {"message": "La conexion no pudo ser creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))