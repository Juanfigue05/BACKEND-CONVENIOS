from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.convenios_schema import ConvenioBase, RetornoConvenio, EditarConvenio
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import convenios_crud as crud_convenios

router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_convenio(convenio: ConvenioBase, db: Session = Depends(get_db)):
    try:
        crear = crud_convenios.crear_convenio(db, convenio)
        if crear:
            return{"message": "Convenio creado correctamente"}
        else:
            return {"message": "El convenio no puedo ser creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-numero-convenio", status_code=status.HTTP_200_OK, response_model=RetornoConvenio)
def get_by_id(num_convenio: str, db: Session = Depends(get_db)):
    try:
        convenios = crud_convenios.obtener_convenios_by_num_convenio(db, num_convenio)
        if convenios is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenio no encontrado")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-nit-institucion", status_code=status.HTTP_200_OK, response_model=RetornoConvenio)
def get_by_nit_institucion(nit_institucion:str, db: Session = Depends(get_db)):
    try:
        institucion = crud_convenios.obtener_convenios_by_nit_institucion(db, nit_institucion)
        if institucion is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenio no encontrado")
        return institucion
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-estado-convenio", status_code=status.HTTP_200_OK, response_model=RetornoConvenio)
def get_by_estado_convenio(estado_conv:str, db: Session = Depends(get_db)):
    try:
        estado_convenio = crud_convenios.obtener_convenios_by_estado_convenio(db, estado_conv)
        if estado_convenio is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenio no encontrado")
        return estado_convenio
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-nit-institucion-clave", status_code=status.HTTP_200_OK, response_model=RetornoConvenio)
def get_by_nit_institucion_clave(nit_institucion_seguro:str, db: Session = Depends(get_db)):
    try:
        nit_inst_seguro = crud_convenios.obtener_convenios_by_nit_security(db, nit_institucion_seguro)
        if nit_inst_seguro is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenio no encontrado")
        return nit_inst_seguro
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-tipo-convenio", status_code=status.HTTP_200_OK, response_model=RetornoConvenio)
def get_by_tipo_convenio(nit_institucion:str, db: Session = Depends(get_db)):
    try:
        tipo_conv = crud_convenios.obtener_convenios_by_tipo_convenio(db, nit_institucion)
        if tipo_conv is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenio no encontrado")
        return tipo_conv
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/editar/{id_convenio}")
def update_convenios(id_convenio: int, convenio: EditarConvenio, db: Session = Depends(get_db)):
    try:
        success = crud_convenios.update_convenios(db, id_convenio, convenio)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar institución")
        return {"message": "Institución actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/eliminar-por-id/{id_convenio}", status_code=status.HTTP_200_OK)
def delete_by_id(id_convenio:int, db: Session = Depends(get_db)):
    try:
        success= crud_convenios.eliminar_convenio(db, id_convenio)
        if success:
            return {"message": "Convenio eliminado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))