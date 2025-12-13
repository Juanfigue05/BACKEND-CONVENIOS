from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
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
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        crear = crud_instituciones.create_institucion(db, institucion)
        if crear:
            return{"message": "Institución creada correctamente"}
        else:
            return {"message": "La institución no puede ser creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-nit", status_code=status.HTTP_200_OK)
def get_by_nit(nit_institucion: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        instituciones = crud_instituciones.get_institucion_by_nit(db, nit_institucion)
        if instituciones is None or len(instituciones) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Institución no encontrada")
        return instituciones
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/obtener-por-nombre", status_code=status.HTTP_200_OK)
async def get_by_name(nombre_institucion: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para buscar la institución")
        
        institucion = crud_instituciones.get_institucion_by_name(db, nombre_institucion)
        if institucion is None or len(institucion) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Institución no encontrada")
        return institucion
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-direccion", status_code=status.HTTP_200_OK)
def get_by_direccion(direccion: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        instituciones = crud_instituciones.get_institucion_by_direccion(db, direccion)
        if instituciones is None or len(instituciones) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Institución no encontrada")
        return instituciones
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-municipio", status_code=status.HTTP_200_OK)
def get_by_municipio(id_municipio: int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        instituciones = crud_instituciones.get_institucion_by_municipio(db, id_municipio)
        if instituciones is None or len(instituciones) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se encontraron instituciones en este municipio")
        return instituciones
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-convenios", status_code=status.HTTP_200_OK)
def get_by_convenios(cant_convenios: int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        instituciones = crud_instituciones.get_institucion_by_convenios(db, cant_convenios)
        if instituciones is None or len(instituciones) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se encontraron instituciones con esa cantidad de convenios")
        return instituciones
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-rango-convenios", status_code=status.HTTP_200_OK)
def get_by_rango_convenios(
    min_convenios: int = Query(0, ge=0),
    max_convenios: int = Query(100, ge=0),
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        if min_convenios > max_convenios:
            raise HTTPException(status_code=400, detail="El mínimo no puede ser mayor que el máximo")
        
        instituciones = crud_instituciones.get_institucion_by_rango_convenios(db, min_convenios, max_convenios)
        if instituciones is None or len(instituciones) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se encontraron instituciones en ese rango de convenios")
        return instituciones
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-todas", status_code=status.HTTP_200_OK)
def get_all_instituciones(db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        instituciones = crud_instituciones.get_all_instituciones(db)
        if instituciones is None or len(instituciones) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se encontraron instituciones")
        return instituciones
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/busqueda-avanzada", status_code=status.HTTP_200_OK)
def busqueda_avanzada(
    nit_institucion: Optional[str] = None,
    nombre_institucion: Optional[str] = None,
    direccion: Optional[str] = None,
    id_municipio: Optional[int] = None,
    min_convenios: Optional[int] = None,
    max_convenios: Optional[int] = None,
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        instituciones = crud_instituciones.busqueda_avanzada_instituciones(
            db, nit_institucion, nombre_institucion, direccion, 
            id_municipio, min_convenios, max_convenios
        )
        if instituciones is None or len(instituciones) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se encontraron instituciones con esos criterios")
        return instituciones
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/editar/{nit_institucion}")
def update_institucion(nit_institucion: str, institucion: EditarInstitucion, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        success = crud_instituciones.institucion_update(db, nit_institucion, institucion)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar institución")
        return {"message": "Institución actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/eliminar-por-nit/{nit_institucion}")
def delete_institucion(nit_institucion: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos")
        
        institucion = crud_instituciones.institucion_delete(db, nit_institucion)
        if institucion:
            return {"message": "Institución eliminada correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Institución no encontrada")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))