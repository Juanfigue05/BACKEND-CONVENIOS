import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def insertar_datos_en_bd(db: Session, df_convenios):
    convenios_insertados = 0
    convenios_actualizados = 0
    errores = []

    # Realizar condicion para verificar si el convenio ya existe utilizando una consulta SQL
    for index, row in df_convenios.iterrows():
        # Verificar si el convenio ya existe
        verificar_convenio_sql = text("""
            SELECT * FROM convenios 
            WHERE num_proceso = :num_proceso AND num_convenio = :num_convenio
        """)
        
        encontro = db.execute(verificar_convenio_sql, {
            "num_proceso": row["num_proceso"], 
            "num_convenio": row["num_convenio"]
        }).first()
        
        print(f"Verificando convenio {row['num_convenio']} - Encontró:", encontro is not None)
        
        if encontro:
            # ACTUALIZAR convenio existente
            actualizar_convenio_sql = text("""
                UPDATE convenios SET
                    tipo_convenio = :tipo_convenio,
                    nit_institucion = :nit_institucion,
                    estado_convenio = :estado_convenio,
                    nombre_institucion = :nombre_institucion,
                    objetivo_convenio = :objetivo_convenio,
                    tipo_proceso = :tipo_proceso,
                    fecha_firma = :fecha_firma,
                    fecha_inicio = :fecha_inicio,
                    duracion_convenio = :duracion_convenio,
                    plazo_ejecucion = :plazo_ejecucion,
                    prorroga = :prorroga,
                    plazo_prorroga = :plazo_prorroga,
                    duracion_total = :duracion_total,
                    fecha_publicacion_proceso = :fecha_publicacion_proceso,
                    enlace_secop = :enlace_secop,
                    supervisor = :supervisor,
                    precio_estimado = :precio_estimado,
                    tipo_convenio_sena = :tipo_convenio_sena,
                    persona_apoyo_fpi = :persona_apoyo_fpi,
                    enlace_evidencias = :enlace_evidencias
                WHERE num_proceso = :num_proceso AND num_convenio = :num_convenio
            """)
            
            try:
                # Convertir la fila a diccionario y manejar valores None/NaN
                row_dict = row.to_dict()
                # Reemplazar NaN por None para SQL
                row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
                
                result = db.execute(actualizar_convenio_sql, row_dict)
                db.commit()
                convenios_actualizados += 1
                logger.info(f"Convenio actualizado: {row['num_convenio']}")
                
            except SQLAlchemyError as e:
                msg = f"Error al actualizar convenio {row['num_convenio']}: {e}"
                errores.append(msg)
                logger.error(msg)
                db.rollback()
                
        else:
            # INSERTAR nuevo convenio
            insertar_convenio_sql = text("""
                INSERT INTO convenios (
                    tipo_convenio, num_convenio, nit_institucion, num_proceso, nombre_institucion,
                    estado_convenio, objetivo_convenio, tipo_proceso, fecha_firma,
                    fecha_inicio, duracion_convenio, plazo_ejecucion, prorroga,
                    plazo_prorroga, duracion_total, fecha_publicacion_proceso,
                    enlace_secop, supervisor, precio_estimado, tipo_convenio_sena,
                    persona_apoyo_fpi, enlace_evidencias
                ) VALUES (
                    :tipo_convenio, :num_convenio, :nit_institucion, :num_proceso, :nombre_institucion,
                    :estado_convenio, :objetivo_convenio, :tipo_proceso, :fecha_firma,
                    :fecha_inicio, :duracion_convenio, :plazo_ejecucion, :prorroga,
                    :plazo_prorroga, :duracion_total, :fecha_publicacion_proceso,
                    :enlace_secop, :supervisor, :precio_estimado, :tipo_convenio_sena,
                    :persona_apoyo_fpi, :enlace_evidencias
                )
            """)
            
            try:
                row_dict = row.to_dict()
                row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
                
                result = db.execute(insertar_convenio_sql, row_dict)
                db.commit()
                convenios_insertados += 1
                logger.info(f"Convenio insertado: {row['num_convenio']}")
                
            except SQLAlchemyError as e:
                msg = f"Error al insertar convenio {row['num_convenio']}: {e}"
                errores.append(msg)
                logger.error(msg)
                db.rollback()

    # Retornar resultado final después del loop
    return {
        "programas_insertados": convenios_insertados,
        "programas_actualizados": convenios_actualizados,
        "errores": errores,
        "mensaje": f"Proceso completado: {convenios_insertados} insertados, {convenios_actualizados} actualizados"
    }
