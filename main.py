
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import usuarios as users
from app.router import cargar_archivos as cargar
from app.router import convenios_router as convenios
from app.router import auth
from app.router import institucion
from app.router import homologaciones_router as homologaciones
from app.router import municipio
from app.router import estadistica_router as estadisticas
from app.router import meta

app = FastAPI()

# Incluir en el objeto app los routers
app.include_router(auth.router, prefix="/access", tags=["servicios de login"])
app.include_router(users.router, prefix="/usuario", tags=["Servicios usuarios"])
app.include_router(cargar.router, prefix="/cargar", tags=["Servicios de carga de archivos"])
app.include_router(convenios.router, prefix="/convenios", tags=["Servicios de convenios"])
app.include_router(institucion.router, prefix="/institucion", tags=["Servicios de instituciones"])
app.include_router(municipio.router, prefix="/municipio", tags=["Servicios de municipios"])
app.include_router(homologaciones.router, prefix="/homologaciones", tags=["Servicios de homologaciones"]) 
app.include_router(estadisticas.router, prefix="/estadisticas", tags=["Estadisticas secundarias"]) 
app.include_router(meta.router, prefix="/meta", tags=["Metadatos"])


# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

@app.get("/")
def read_root():
    return {
                "message": "Todo funciona correctamente",
                "autor": "ADSO 2925888"
            }

