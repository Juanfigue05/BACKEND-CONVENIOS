from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
import logging
import re

from app.schemas.convenios_schema import CrearConvenio, EditarConvenio, RetornoConvenio

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validar_fecha_formato(fecha_str: str) -> bool:
    """Valida que una fecha esté en formato ISO (YYYY-MM-DD)"""
    if not fecha_str or fecha_str == "N/A":
        return True
    
    patron = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(patron, fecha_str))

def limpiar_texto_convenio(texto: str) -> str:
    """Limpia texto eliminando espacios múltiples y caracteres especiales"""
    if not texto or texto == "N/A":
        return texto
    
    # Eliminar tabulaciones y espacios múltiples
    texto = texto.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
    texto = texto.replace('\xa0', ' ')  # Non-breaking space
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def validar_longitud_campo(valor: str, nombre_campo: str, longitud_max: int) -> str:
    """Valida y trunca un campo si excede la longitud máxima"""
    if not valor or valor == "N/A":
        return valor
    
    if len(valor) > longitud_max:
        logger.warning(
            f"Campo '{nombre_campo}' excede longitud máxima ({longitud_max}). "
            f"Valor truncado: {valor[:50]}..."
        )
        return valor[:longitud_max]
    
    return valor

def normalizar_valor(valor, campo_nombre: str = "") -> Optional[str]:
    """
    Normaliza un valor para inserción en la base de datos.
    - Si es None o vacío, retorna None
    - Si es string, limpia y valida
    """
    if valor is None:
        return None
    
    if isinstance(valor, str):
        valor = valor.strip()
        if valor == "" or valor.upper() == "N/A":
            return None
        return valor
    
    return valor

# Definición de longitudes máximas según esquema de BD
LONGITUDES_MAXIMAS = {
    "tipo_convenio": 50,
    "num_convenio": 50,
    "nit_institucion": 20,
    "num_proceso": 50,
    "nombre_institucion": 120,
    "estado_convenio": 50,
    "tipo_proceso": 50,
    "fecha_firma": 50,
    "fecha_inicio": 50,
    "duracion_convenio": 20,
    "plazo_ejecucion": 50,
    "prorroga": 50,
    "plazo_prorroga": 50,
    "duracion_total": 20,
    "fecha_publicacion_proceso": 50,
    "enlace_secop": 1500,
    "supervisor": 400,
    "tipo_convenio_sena": 50,
    "persona_apoyo_fpi": 80,
}

def crear_convenio(db: Session, convenio: CrearConvenio) -> Optional[bool]:
    try:
        datos_convenio = convenio.model_dump()
        
        # Validar campos obligatorios
        campos_obligatorios = ['tipo_convenio', 'num_convenio', 'nit_institucion', 
                              'nombre_institucion', 'estado_convenio']
        for campo in campos_obligatorios:
            if not datos_convenio.get(campo):
                raise ValueError(f"El campo {campo} es obligatorio")
        
        # Normalizar todos los campos opcionales
        for campo in datos_convenio:
            if campo not in campos_obligatorios:
                datos_convenio[campo] = normalizar_valor(datos_convenio[campo], campo)

        # Regla de negocio: si precio_estimado viene vacío o nulo, guardarlo como 0
        if datos_convenio.get('precio_estimado') is None:
            datos_convenio['precio_estimado'] = 0
        
        # Validar y limpiar fechas (VARCHAR(50))
        campos_fecha = [
            "fecha_firma", "fecha_inicio", "plazo_ejecucion",
            "prorroga", "plazo_prorroga", "fecha_publicacion_proceso"
        ]
        
        for campo in campos_fecha:
            if datos_convenio.get(campo):
                # Si no es formato válido, convertir a None en lugar de "N/A"
                if not validar_fecha_formato(datos_convenio[campo]):
                    logger.warning(f"Fecha inválida en {campo}: {datos_convenio[campo]}, se guardará como texto")
                # Asegurar que no exceda VARCHAR(50)
                if datos_convenio[campo]:
                    datos_convenio[campo] = validar_longitud_campo(
                        datos_convenio[campo], campo, 50
                    )
        
        # Limpiar y validar longitud de campos de texto VARCHAR
        for campo, longitud_max in LONGITUDES_MAXIMAS.items():
            if datos_convenio.get(campo):
                datos_convenio[campo] = limpiar_texto_convenio(datos_convenio[campo])
                datos_convenio[campo] = validar_longitud_campo(
                    datos_convenio[campo], campo, longitud_max
                )
        
        # Limpiar campos TEXT (objetivo_convenio, enlace_evidencias)
        if datos_convenio.get("objetivo_convenio"):
            datos_convenio["objetivo_convenio"] = limpiar_texto_convenio(
                datos_convenio["objetivo_convenio"]
            )
        
        if datos_convenio.get("enlace_evidencias"):
            datos_convenio["enlace_evidencias"] = limpiar_texto_convenio(
                datos_convenio["enlace_evidencias"]
            )
        
        # Convertir valores None a NULL en la query
        query = text("""
            INSERT INTO convenios (
                tipo_convenio, num_convenio, nit_institucion, num_proceso, nombre_institucion,
                estado_convenio, objetivo_convenio, tipo_proceso, fecha_firma, fecha_inicio, 
                duracion_convenio, plazo_ejecucion, prorroga, plazo_prorroga, duracion_total, 
                fecha_publicacion_proceso, enlace_secop, supervisor, precio_estimado, 
                tipo_convenio_sena, persona_apoyo_fpi, enlace_evidencias
            ) VALUES (
                :tipo_convenio, :num_convenio, :nit_institucion, :num_proceso, :nombre_institucion,
                :estado_convenio, :objetivo_convenio, :tipo_proceso, :fecha_firma, :fecha_inicio, 
                :duracion_convenio, :plazo_ejecucion, :prorroga, :plazo_prorroga, :duracion_total, 
                :fecha_publicacion_proceso, :enlace_secop, :supervisor, :precio_estimado, 
                :tipo_convenio_sena, :persona_apoyo_fpi, :enlace_evidencias
            )
        """)
        
        db.execute(query, datos_convenio)
        db.commit()
        logger.info(f" Convenio creado exitosamente: {datos_convenio.get('num_convenio')}")
        return True
        
    except ValueError as e:
        logger.error(f" Error de validación: {str(e)}")
        raise Exception(f"Error de validación: {str(e)}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f" Error SQL al crear el convenio: {str(e)}")
        raise Exception(f"Error de base de datos al crear el convenio: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f" Error inesperado al crear el convenio: {str(e)}")
        raise Exception(f"Error al crear el convenio: {str(e)}")

def obtener_todos_convenios(db: Session) -> List[RetornoConvenio]:
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            ORDER BY 
                CASE 
                    WHEN convenios.fecha_firma IS NULL OR convenios.fecha_firma = 'N/A'
                    THEN '9999-12-31'
                    ELSE convenios.fecha_firma
                END DESC,
                convenios.id_convenio DESC
        """)
        result = db.execute(query).mappings().all()
        logger.info(f" Se obtuvieron {len(result)} convenios")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f" Error al obtener todos los convenios: {str(e)}")
        raise Exception(f"Error de base de datos al obtener los convenios: {str(e)}")

def obtener_convenio_by_id(db: Session, id_convenio: int):
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.id_convenio = :id_conv
        """)
        result = db.execute(query, {"id_conv": id_convenio}).mappings().first()
        
        if result:
            logger.info(f" Convenio encontrado con ID: {id_convenio}")
        else:
            logger.warning(f" No se encontró convenio con ID: {id_convenio}")
            
        return result
        
    except SQLAlchemyError as e:
        logger.error(f" Error al buscar el convenio por id: {str(e)}")
        raise Exception(f"Error de base de datos al buscar el convenio por id: {str(e)}")

def obtener_convenios_by_num_convenio(db: Session, num_conv: str):
    try:
        filtro = f"%{num_conv}%"
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.num_convenio LIKE :num_convenio
            ORDER BY 
                CASE 
                    WHEN convenios.fecha_firma IS NULL OR convenios.fecha_firma = 'N/A'
                    THEN '9999-12-31'
                    ELSE convenios.fecha_firma
                END DESC
        """)
        result = db.execute(query, {"num_convenio": filtro}).mappings().all()
        logger.info(f"🔍 Se encontraron {len(result)} convenios con número: {num_conv}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f" Error al buscar el convenio por número: {str(e)}")
        raise Exception(f"Error de base de datos al buscar el convenio por número: {str(e)}")

def obtener_convenios_by_rango_fechas_firma(db: Session, fecha_ini: str, fecha_fin: str):
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.fecha_firma IS NOT NULL 
                AND convenios.fecha_firma != 'N/A'
                AND convenios.fecha_firma REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}'
                AND convenios.fecha_firma >= :fecha_inicio 
                AND convenios.fecha_firma <= :fecha_fin
            ORDER BY convenios.fecha_firma DESC
        """)
        result = db.execute(query, {"fecha_inicio": fecha_ini, "fecha_fin": fecha_fin}).mappings().all()
        logger.info(f" Se encontraron {len(result)} convenios firmados entre {fecha_ini} y {fecha_fin}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f" Error al buscar los convenios por rango de fechas de firma: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por rango de fechas: {str(e)}")

def obtener_convenios_by_rango_fechas_inicio(db: Session, fecha_ini: str, fecha_fin: str):
    try:
        query = text("""
            SELECT  
                convenios.id_convenio, convenios.tipo_convenio, convenios.num_convenio, 
                convenios.nit_institucion, convenios.num_proceso, convenios.nombre_institucion,
                convenios.estado_convenio, convenios.objetivo_convenio, convenios.tipo_proceso, 
                convenios.fecha_firma, convenios.fecha_inicio, convenios.duracion_convenio,
                convenios.plazo_ejecucion, convenios.prorroga, convenios.plazo_prorroga, 
                convenios.duracion_total, convenios.fecha_publicacion_proceso, convenios.enlace_secop,
                convenios.supervisor, convenios.precio_estimado, convenios.tipo_convenio_sena, 
                convenios.persona_apoyo_fpi, convenios.enlace_evidencias
            FROM convenios
            WHERE convenios.fecha_inicio IS NOT NULL 
                AND convenios.fecha_inicio != 'N/A'
                AND convenios.fecha_inicio REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}'
                AND convenios.fecha_inicio >= :fecha_inicio 
                AND convenios.fecha_inicio <= :fecha_fin
            ORDER BY convenios.fecha_inicio DESC
        """)
        result = db.execute(query, {"fecha_inicio": fecha_ini, "fecha_fin": fecha_fin}).mappings().all()
        logger.info(f" Se encontraron {len(result)} convenios iniciados entre {fecha_ini} y {fecha_fin}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f" Error al buscar los convenios por rango de fechas de inicio: {str(e)}")
        raise Exception(f"Error de base de datos al buscar los convenios por rango de fechas de inicio: {str(e)}")

def actualizar_convenio(db: Session, id_conve: int, convenio_actualizar: EditarConvenio) -> bool:
    try:
        campos = convenio_actualizar.model_dump(exclude_unset=True)
        
        if not campos:
            logger.warning(f" No se proporcionaron campos para actualizar en convenio ID: {id_conve}")
            return False
        
        # Normalizar campos opcionales
        for campo in list(campos.keys()):
            campos[campo] = normalizar_valor(campos[campo], campo)
            # Si el campo se normalizó a None, dejarlo para que se actualice a NULL

        # Si el precio_estimado fue enviado pero vacío, actualizar a 0 (regla de negocio)
        if 'precio_estimado' in campos and campos['precio_estimado'] is None:
            campos['precio_estimado'] = 0
        
        # Validar y limpiar fechas (VARCHAR(50))
        campos_fecha = [
            "fecha_firma", "fecha_inicio", "plazo_ejecucion",
            "prorroga", "plazo_prorroga", "fecha_publicacion_proceso"
        ]
        
        for campo in campos_fecha:
            if campo in campos and campos[campo]:
                if not validar_fecha_formato(campos[campo]):
                    logger.warning(f" Fecha inválida en {campo}: {campos[campo]}, se guardará como texto")
                campos[campo] = validar_longitud_campo(campos[campo], campo, 50)
        
        # Limpiar y validar longitud de campos VARCHAR
        for campo, longitud_max in LONGITUDES_MAXIMAS.items():
            if campo in campos and campos[campo]:
                campos[campo] = limpiar_texto_convenio(campos[campo])
                campos[campo] = validar_longitud_campo(campos[campo], campo, longitud_max)
        
        # Limpiar campos TEXT
        if "objetivo_convenio" in campos and campos["objetivo_convenio"]:
            campos["objetivo_convenio"] = limpiar_texto_convenio(campos["objetivo_convenio"])
        
        if "enlace_evidencias" in campos and campos["enlace_evidencias"]:
            campos["enlace_evidencias"] = limpiar_texto_convenio(campos["enlace_evidencias"])
        
        clausula_set = ", ".join([f"{clave} = :{clave}" for clave in campos])
        campos["id_conven"] = id_conve

        query = text(f"""
            UPDATE convenios 
            SET {clausula_set} 
            WHERE id_convenio = :id_conven
        """)
        
        resultado = db.execute(query, campos)
        db.commit()
        
        if resultado.rowcount > 0:
            logger.info(f" Convenio actualizado exitosamente: ID {id_conve}")
            return True
        else:
            logger.warning(f" No se encontró convenio con ID: {id_conve}")
            return False
            
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f" Error al actualizar el convenio: {str(e)}")
        raise Exception(f"Error de base de datos al actualizar el convenio: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f" Error inesperado al actualizar el convenio: {str(e)}")
        raise Exception(f"Error al actualizar el convenio: {str(e)}")

def eliminar_convenio(db: Session, id_convenio: int) -> bool:
    try:
        query = text("""
            DELETE FROM convenios
            WHERE convenios.id_convenio = :id_eliminar
        """)
        resultado = db.execute(query, {"id_eliminar": id_convenio})
        db.commit()
        
        if resultado.rowcount > 0:
            logger.info(f" Convenio eliminado exitosamente: ID {id_convenio}")
            return True
        else:
            logger.warning(f" No se encontró convenio con ID: {id_convenio}")
            return False
            
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f" Error al eliminar convenio por id: {str(e)}")
        raise Exception(f"Error de base de datos al eliminar el convenio: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f" Error inesperado al eliminar convenio: {str(e)}")
        raise Exception(f"Error al eliminar el convenio: {str(e)}")

# Las demás funciones de búsqueda permanecen igual...
# (obtener_convenios_by_num_proceso, obtener_convenios_by_nit_institucion, etc.)