from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.schemas.usuarios import RetornoUsuario
from app.router.dependencies import get_current_user
from io import BytesIO
from app.crud.cargar_archivos import insertar_datos_en_bd
from core.database import get_db
from typing import Any
import re
from datetime import datetime

router = APIRouter()

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
VALORES_DEFECTO = {
    # Campos de texto
    "num_convenio": "N/A",
    "num_proceso": "N/A",
    "objetivo_convenio": "N/A",
    "duracion_convenio": "N/A",
    "duracion_total": "N/A",
    "enlace_secop": "N/A",
    "supervisor": "N/A",
    "tipo_convenio_sena": "N/A",
    "persona_apoyo_fpi": "N/A",
    "enlace_evidencias": "N/A",
    
    # Campos de fecha (ahora son VARCHAR en BD)
    "fecha_firma": "N/A",
    "fecha_inicio": "N/A",
    "plazo_ejecucion": "N/A",
    "prorroga": "N/A",
    "plazo_prorroga": "N/A",
    "fecha_publicacion_proceso": "N/A",
}

# Valores aceptados como "no aplica" para fechas
VALORES_NO_APLICA = [
    "no aplica",
    "n/a",
    "na",
    "no disponible",
    "sin información",
    "pendiente",
    ""
]

# ============================================================================
# FUNCIONES DE LIMPIEZA
# ============================================================================

def limpiar_texto(texto: Any) -> str:
    """
    Limpia texto eliminando tabulaciones, espacios extras y caracteres especiales.
    """
    if pd.isna(texto) or texto is None:
        return ""
    
    if not isinstance(texto, str):
        texto = str(texto)
    
    # Eliminar tabulaciones y saltos de línea
    texto = texto.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
    
    # Eliminar caracteres unicode problemáticos
    texto = texto.replace('\xa0', ' ')  # Non-breaking space
    
    # Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    
    # Eliminar espacios al inicio y final
    texto = texto.strip()
    
    return texto


def normalizar_fecha(fecha_valor: Any) -> str:
    """
    Normaliza fechas a formato ISO (YYYY-MM-DD) o retorna valores textuales válidos.
    
    Casos manejados:
    - Fechas en DD/MM/YYYY → YYYY-MM-DD
    - Timestamps de pandas → YYYY-MM-DD
    - "No aplica" y variantes → "N/A"
    - Valores vacíos → "N/A"
    - Fechas inválidas → "N/A"
    """
    # Limpiar texto primero
    fecha_limpia = limpiar_texto(fecha_valor)
    
    # Si está vacío o es NaN
    if not fecha_limpia or pd.isna(fecha_valor):
        return "N/A"
    
    # Verificar si es un valor "no aplica"
    if fecha_limpia.lower() in VALORES_NO_APLICA:
        return "N/A"
    
    # Si ya está en formato ISO correcto
    if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_limpia):
        return fecha_limpia
    
    try:
        # Manejar timestamps de pandas (2023-06-26 00:00:00)
        if re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', fecha_limpia):
            return fecha_limpia.split(' ')[0]
        
        # Intentar parsear con diferentes formatos
        formatos_comunes = [
            "%d/%m/%Y",      # 22/06/2023
            "%d-%m-%Y",      # 22-06-2023
            "%Y/%m/%d",      # 2023/06/22
            "%d.%m.%Y",      # 22.06.2023
            "%d/%m/%y",      # 22/06/23
            "%m/%d/%Y",      # 06/22/2023 (formato USA)
        ]
        
        for formato in formatos_comunes:
            try:
                fecha_obj = datetime.strptime(fecha_limpia, formato)
                return fecha_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        # Intentar conversión con pandas como último recurso
        fecha_convertida = pd.to_datetime(fecha_limpia, errors="coerce")
        if not pd.isna(fecha_convertida):
            return fecha_convertida.strftime("%Y-%m-%d")
        
        # Si no se pudo convertir, retornar N/A
        print(f"Fecha no convertible: '{fecha_valor}' → usando 'N/A'")
        return "N/A"
        
    except Exception as e:
        print(f"Error al convertir fecha '{fecha_valor}': {str(e)} → usando 'N/A'")
        return "N/A"


def limpiar_valor(valor: Any, nombre_campo: str) -> Any:
    """
    Limpia un valor individual según el tipo de campo.
    """
    # Si es un campo de fecha, usar normalización específica
    campos_fecha = [
        "fecha_firma", "fecha_inicio", "plazo_ejecucion",
        "prorroga", "plazo_prorroga", "fecha_publicacion_proceso"
    ]
    
    if nombre_campo in campos_fecha:
        return normalizar_fecha(valor)
    
    # Para campos de texto
    valor_limpio = limpiar_texto(valor)
    
    # Si está vacío, usar valor por defecto
    if not valor_limpio:
        return VALORES_DEFECTO.get(nombre_campo, "N/A")
    
    return valor_limpio


def procesar_campos_opcionales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa todos los campos aplicando limpieza y valores por defecto.
    """
    df_procesado = df.copy()
    
    # Procesar cada campo que tiene valor por defecto
    for columna, valor_defecto in VALORES_DEFECTO.items():
        if columna in df_procesado.columns:
            df_procesado[columna] = df_procesado[columna].apply(
                lambda x: limpiar_valor(x, columna)
            )
        else:
            df_procesado[columna] = valor_defecto
    
    return df_procesado


def validar_y_reportar_fechas(df: pd.DataFrame) -> None:
    """
    Valida las fechas procesadas y reporta estadísticas.
    """
    campos_fecha = [
        "fecha_firma", "fecha_inicio", "plazo_ejecucion",
        "prorroga", "plazo_prorroga", "fecha_publicacion_proceso"
    ]
    
    print("\n" + "=" * 80)
    print("REPORTE DE FECHAS PROCESADAS")
    print("=" * 80)
    
    for campo in campos_fecha:
        if campo not in df.columns:
            continue
        
        total = len(df)
        fechas_validas = df[campo].str.match(r'^\d{4}-\d{2}-\d{2}$').sum()
        valores_na = (df[campo] == "N/A").sum()
        otros = total - fechas_validas - valores_na
        
        if otros > 0:
            print(f" Otros valores: {otros}")
            # Mostrar algunos ejemplos
            ejemplos = df[~df[campo].str.match(r'^\d{4}-\d{2}-\d{2}$|^N/A$', na=False)][campo].head(3).tolist()
            if ejemplos:
                print(f"     Ejemplos: {ejemplos}")


# ============================================================================
# ENDPOINT PRINCIPAL
# ============================================================================

@router.post("/upload-excel-convenios/")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_token: RetornoUsuario = Depends(get_current_user)
):
    """
    Endpoint para cargar convenios desde Excel con limpieza robusta de datos.
    """
    if user_token.id_rol != 1:
        raise HTTPException(
            status_code=401, 
            detail="No tienes permisos para cargar archivos"
        )
    
    try:
        # ================================================================
        # 1. LECTURA DEL ARCHIVO
        # ================================================================
        contents = await file.read()
        df = pd.read_excel(
            BytesIO(contents),
            engine="openpyxl",
            usecols=[
                "No", "TIPO", "NUMERO_CONVENIO", "NIT_PROVEEDOR", 
                "NUMERO_PROCESO", "PROVEEDOR", "ESTADO", "OBJETIVO_CONVENIO", 
                "TIPO_PROCESO", "FECHA_FIRMA_CONVENIO", "FECHA_INICIO_EJECUCION", 
                "DURACION_CONVENIO", "PLAZO_EJECUCION", "PRORROGA", 
                "PLAZO_PRORROGA", "DURACION_TOTAL", "FECHA_PUBLICACION_PROCESO",
                "ENLACE_SECOP", "SUPERVISOR", "PRECIO_ESTIMADO", 
                "TIPO_CONVENIO", "PERSONA_APOYO_FPI", "ENLACE_EVIDENCIAS"
            ],
            dtype=str  # Todo como string para control total
        )
        
        print("=" * 80)
        print("PASO 1: ARCHIVO CARGADO")
        print("=" * 80)
        print(f"Total de registros: {len(df)}")
        
        # ================================================================
        # 2. RENOMBRAR COLUMNAS
        # ================================================================
        df = df.rename(columns={
            "TIPO": "tipo_convenio",
            "NUMERO_CONVENIO": "num_convenio",
            "NIT_PROVEEDOR": "nit_institucion",
            "NUMERO_PROCESO": "num_proceso",
            "PROVEEDOR": "nombre_institucion",
            "ESTADO": "estado_convenio",
            "OBJETIVO_CONVENIO": "objetivo_convenio",
            "TIPO_PROCESO": "tipo_proceso",
            "FECHA_FIRMA_CONVENIO": "fecha_firma",
            "FECHA_INICIO_EJECUCION": "fecha_inicio",
            "DURACION_CONVENIO": "duracion_convenio",
            "PLAZO_EJECUCION": "plazo_ejecucion",
            "PRORROGA": "prorroga",
            "PLAZO_PRORROGA": "plazo_prorroga",
            "DURACION_TOTAL": "duracion_total",
            "FECHA_PUBLICACION_PROCESO": "fecha_publicacion_proceso",
            "ENLACE_SECOP": "enlace_secop",
            "SUPERVISOR": "supervisor",
            "PRECIO_ESTIMADO": "precio_estimado",
            "TIPO_CONVENIO": "tipo_convenio_sena",
            "PERSONA_APOYO_FPI": "persona_apoyo_fpi",
            "ENLACE_EVIDENCIAS": "enlace_evidencias"
        })
        
        # ================================================================
        # 3. VALIDAR CAMPOS OBLIGATORIOS
        # ================================================================
        print("\n" + "=" * 80)
        print("PASO 2: VALIDANDO CAMPOS OBLIGATORIOS")
        print("=" * 80)
        
        required_fields = [
            "tipo_convenio", "nit_institucion", "nombre_institucion", 
            "estado_convenio", "tipo_proceso"
        ]
        
        registros_totales = len(df)
        df = df.dropna(subset=required_fields, how='all')
        registros_validos = len(df)
        registros_eliminados = registros_totales - registros_validos
        
        if registros_eliminados > 0:
            print(f"Eliminados {registros_eliminados} registros por campos obligatorios vacíos")
        
        if len(df) == 0:
            raise HTTPException(
                status_code=400,
                detail="No hay registros válidos. Verifica campos obligatorios."
            )
        
        # ================================================================
        # 4. LIMPIEZA PROFUNDA DE DATOS
        # ================================================================
        print("\n" + "=" * 80)
        print("PASO 3: LIMPIEZA DE DATOS")
        print("=" * 80)
        
        # Limpiar tabulaciones y espacios en TODOS los campos de texto
        for col in df.columns:
            if col != "precio_estimado":  # Excluir campo numérico
                df[col] = df[col].apply(limpiar_texto)
        
        # ================================================================
        # 5. PROCESAR CAMPOS OPCIONALES Y FECHAS
        # ================================================================
        print("\n" + "=" * 80)
        print("PASO 4: PROCESANDO CAMPOS OPCIONALES Y FECHAS")
        print("=" * 80)
        
        df = procesar_campos_opcionales(df)
        
        # Validar y reportar fechas
        validar_y_reportar_fechas(df)
        
        # ================================================================
        # 6. CONVERTIR PRECIO ESTIMADO
        # ================================================================
        print("\n" + "=" * 80)
        print("PASO 5: PROCESANDO CAMPOS NUMÉRICOS")
        print("=" * 80)
        
        df["precio_estimado"] = pd.to_numeric(
            df["precio_estimado"], 
            errors="coerce"
        ).fillna(0).astype("Int64")
        
        print(f"Precio estimado convertido a numérico")
        
        # ================================================================
        # 7. LIMPIEZA FINAL
        # ================================================================
        if 'No' in df.columns:
            df = df.drop('No', axis=1)
        
        # ================================================================
        # 8. VERIFICACIÓN FINAL
        # ================================================================
        print("\n" + "=" * 80)
        print("PASO 6: VERIFICACIÓN FINAL")
        print("=" * 80)
        print(f"Total de registros a insertar: {len(df)}")
        print("\nPrimeros 3 registros (muestra):")
        print(df[["num_convenio", "fecha_firma", "prorroga", "nombre_institucion"]].head(3))
        
        # Verificar que no haya tabulaciones
        tiene_tabs = False
        for col in df.columns:
            if df[col].astype(str).str.contains('\t').any():
                print(f"ADVERTENCIA: Columna '{col}' aún tiene tabulaciones")
                tiene_tabs = True
        
        if not tiene_tabs:
            print("No se detectaron tabulaciones en los datos")
        
        # ================================================================
        # 9. INSERTAR EN BASE DE DATOS
        # ================================================================
        resultados = insertar_datos_en_bd(db, df)
        
        resultados["registros_procesados"] = registros_totales
        resultados["registros_validos"] = registros_validos
        resultados["registros_eliminados"] = registros_eliminados
        
        return resultados
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo: {str(e)}"
        )