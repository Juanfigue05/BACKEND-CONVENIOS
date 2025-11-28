from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.estadistica_schema import EstadisticaCategoriaBase, RetornoEstadisticaCategoria, EditarEstadisticaCategoria
from sqlalchemy.orm import Session
from app.schemas.usuarios import RetornoUsuario
from app.router.dependencies import get_current_user
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from app.crud import estadistica_crud as crud_estadistica
from typing import List

router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def create_estadistica(estadistica: EstadisticaCategoriaBase, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para crear estadística")
        
        crear = crud_estadistica.crear_estadistica_categoria(db, estadistica)
        if crear:
            return{"message": "Estadística creada correctamente"}
        else:
            return {"message": "La estadística no pudo ser creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-todas", status_code=status.HTTP_200_OK, response_model=List[RetornoEstadisticaCategoria])
def get_all_estadisticas(db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar estadísticas")
        
        estadisticas = crud_estadistica.obtener_todas_estadisticas(db)
        if not estadisticas:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No se encontraron estadísticas")
        return estadisticas
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-id/{id_estadistica}", status_code=status.HTTP_200_OK, response_model=RetornoEstadisticaCategoria)
def get_by_id(id_estadistica: int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar estadísticas")
        
        estadistica = crud_estadistica.obtener_estadistica_by_id(db, id_estadistica)
        if estadistica is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Estadística no encontrada")
        return estadistica
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-categoria", status_code=status.HTTP_200_OK, response_model=List[RetornoEstadisticaCategoria])
def get_by_categoria(categoria: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar estadísticas")
        
        estadisticas = crud_estadistica.obtener_estadisticas_by_categoria(db, categoria)
        if not estadisticas:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Estadísticas no encontradas")
        return estadisticas
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-nombre", status_code=status.HTTP_200_OK, response_model=List[RetornoEstadisticaCategoria])
def get_by_nombre(nombre: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar estadísticas")
        
        estadisticas = crud_estadistica.obtener_estadisticas_by_nombre(db, nombre)
        if not estadisticas:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Estadísticas no encontradas")
        return estadisticas
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/obtener-por-categoria-exacta", status_code=status.HTTP_200_OK, response_model=List[RetornoEstadisticaCategoria])
def get_by_categoria_exacta(categoria: str, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para consultar estadísticas")
        
        estadisticas = crud_estadistica.obtener_estadisticas_by_categoria_exacta(db, categoria)
        if not estadisticas:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Estadísticas no encontradas")
        return estadisticas
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/editar/{id_estadistica}")
def update_estadistica(id_estadistica: int, estadistica: EditarEstadisticaCategoria, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para editar estadísticas")
        
        success = crud_estadistica.update_estadistica(db, id_estadistica, estadistica)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la estadística")
        return {"message": "Estadística actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/eliminar-por-id/{id_estadistica}", status_code=status.HTTP_200_OK)
def delete_by_id(id_estadistica: int, db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    try:
        if user_token.id_rol != 1:
            raise HTTPException(status_code=401, detail="No tienes permisos para eliminar estadísticas")
        
        success = crud_estadistica.eliminar_estadistica(db, id_estadistica)
        if success:
            return {"message": "Estadística eliminada correctamente"}
        else:
            raise HTTPException(status_code=400, detail="No se pudo eliminar la estadística")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))