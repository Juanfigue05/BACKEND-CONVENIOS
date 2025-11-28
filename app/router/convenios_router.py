from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.convenios_schema import ConvenioBase, RetornoConvenio, EditarConvenio
from sqlalchemy.orm import Session
from app.schemas.usuarios import RetornoUsuario
from app.router.dependencies import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import convenios_crud as crud_convenios
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_convenio(convenio: ConvenioBase, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear convenio")
        
        crear = crud_convenios.crear_convenio(db, convenio)
        if crear:
            return{"message": "Convenio creado correctamente"}
        else:
            return {"message": "El convenio no pudo ser creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-todos", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_all_convenios(db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_todos_convenios(db)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se encontraron convenios")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-id/{id_convenio}", status_code=status.HTTP_200_OK, response_model=RetornoConvenio)
def get_by_id(id_convenio: int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenio = crud_convenios.obtener_convenio_by_id(db, id_convenio)
        if convenio is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenio no encontrado")
        return convenio
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-numero-convenio", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_numero(num_convenio: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_num_convenio(db, num_convenio)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenio no encontrado")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-nit-institucion", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_nit_institucion(nit_institucion: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_nit_institucion(db, nit_institucion)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-nombre-institucion", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_nombre_institucion(nombre_institucion: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_nombre_institucion(db, nombre_institucion)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-estado-convenio", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_estado_convenio(estado_conv: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_estado_convenio(db, estado_conv)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/obtener-por-tipo-convenio", status_code=status.HTTP_200_OK, response_model=RetornoConvenio)
def get_by_tipo_convenio(tipo_proceso:str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_tipo_proceso(db, tipo_proceso)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-supervisor", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_supervisor(supervisor: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_supervisor(db, supervisor)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-tipo-convenio-sena", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_tipo_convenio_sena(tipo_convenio_sena: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_tipo_convenio_sena(db, tipo_convenio_sena)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-persona-apoyo", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_persona_apoyo(persona_apoyo_fpi: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_persona_apoyo(db, persona_apoyo_fpi)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-rango-fechas-firma", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_rango_fechas_firma(fecha_inicio: datetime, fecha_fin: datetime, 
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_rango_fechas_firma(db, fecha_inicio, fecha_fin)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-rango-fechas-inicio", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_rango_fechas_inicio(fecha_inicio: datetime, fecha_fin: datetime,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_rango_fechas_inicio(db, fecha_inicio, fecha_fin)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-numero-proceso", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def get_by_numero_proceso(num_proceso: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.obtener_convenios_by_num_proceso(db, num_proceso)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/buscar-por-objetivo", status_code=status.HTTP_200_OK, response_model=List[RetornoConvenio])
def search_by_objetivo(palabra_clave: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar convenios")
        
        convenios = crud_convenios.buscar_convenios_by_objetivo(db, palabra_clave)
        if not convenios:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Convenios no encontrados")
        return convenios
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/editar/{id_convenio}")
def update_convenios(id_convenio: int, convenio: EditarConvenio, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para editar convenios")
        
        success = crud_convenios.update_convenios(db, id_convenio, convenio)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el convenio")
        return {"message": "Convenio actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/eliminar-por-id/{id_convenio}", status_code=status.HTTP_200_OK)
def delete_by_id(id_convenio: int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para eliminar convenios")
        
        success = crud_convenios.eliminar_convenio(db, id_convenio)
        if success:
            return {"message": "Convenio eliminado correctamente"}
        else:
            raise HTTPException(status_code=400, detail="No se pudo eliminar el convenio")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))