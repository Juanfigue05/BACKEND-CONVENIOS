
from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
from sqlalchemy.orm import Session
from io import BytesIO
from app.crud.cargar_archivos import insertar_datos_en_bd
from core.database import get_db

router = APIRouter()

@router.post("/upload-excel-convenios/")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    df = pd.read_excel(
        BytesIO(contents),
        engine="openpyxl",
        usecols=["No","TIPO", "NUMERO_CONVENIO", "NIT_PROVEEDOR", "NUMERO_PROCESO", "PROVEEDOR", "ESTADO", "OBJETIVO_CONVENIO", "TIPO_PROCESO", "FECHA_FIRMA_CONVENIO", "FECHA_INICIO_EJECUCION", "DURACION_CONVENIO", "PLAZO_EJECUCION", "PRORROGA", "PLAZO_PRORROGA", "DURACION_TOTAL","FECHA_PUBLICACION_PROCESO","ENLACE_SECOP","SUPERVISOR","PRECIO_ESTIMADO","TIPO_CONVENIO","PERSONA_APOYO_FPI","ENLACE_EVIDENCIAS"],  # Nombres reales
        dtype=str
    )
    print(df.head())  # paréntesis
    print(df.columns)
    print(df.dtypes)

    # Renombrar columnas
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
        "FECHA_PUBLICACION_PROCESO":"fecha_publicacion_proceso",
        "ENLACE_SECOP":"enlace_secop",
        "SUPERVISOR":"supervisor",
        "PRECIO_ESTIMADO":"precio_estimado",
        "TIPO_CONVENIO":"tipo_convenio_sena",
        "PERSONA_APOYO_FPI":"persona_apoyo_fpi",
        "ENLACE_EVIDENCIAS":"enlace_evidencias"
    })

    print(df.head())  # paréntesis

    # si quieren que funcione en todos los centros de pais 
    # # crear codigo para llenar regionales centros y eliminar la siguiente linea.
    # df = df[df["cod_centro"] == '9121']

    # Eliminar filas con valores faltantes en campos obligatorios
    required_fields = [
        "tipo_convenio","nit_institucion","nombre_institucion","estado_convenio","tipo_proceso"
    ]
    df = df.dropna(subset=required_fields)

    # Convertir columnas a tipo numérico
    for col in ["precio_estimado"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    print(df.head())  # paréntesis
    print(df.dtypes)

    # # Convertir fechas
    # df["fecha_firma"] = pd.to_datetime(df["fecha_firma"], errors="coerce").dt.date
    # df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce").dt.date

    # # Asegurar columnas no proporcionadas
    # df["num_convenio"] = "N/A"
    df["num_proceso"] = "N/A"
    df["objetivo_convenio"] = "N/A"
    df["fecha_firma"] = "0001-01-01"
    # ejemplo 2 de fecha firma: 2023-08-15T00:00:00.000Z
    
    df["fecha_inicio"] = "0001-01-01"
    df["duracion_convenio"] = "N/A"
    df["plazo_ejecucion"] = "0001-01-01"
    df["prorroga"] = "0001-01-01"
    df["plazo_prorroga"] = "0001-01-01"
    df["duracion_total"] = "N/A"
    df["fecha_publicacion_proceso"] = "0001-01-01"
    df["enlace_secop"] = "N/A"
    df["supervisor"] = "N/A"
    # df["precio_estimado"] = 0
    df["tipo_convenio_sena"] = "N/A"
    df["persona_apoyo_fpi"] = "N/A"
    df["enlace_evidencias"] = "N/A"
    
    # # Crear DataFrame de convenios únicos
    # df_convenios = df[[""]].drop_duplicates()
    # df_convenios["horas_lectivas"] = 0
    # df_convenios["horas_productivas"] = 0

    # print(df_convenios.head())

    # Eliminar la columna nombre del df.
    df = df.drop('No', axis=1)
    print(df.head())

    resultados = insertar_datos_en_bd(db, df)
    return resultados