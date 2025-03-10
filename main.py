import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine, Base
import models  # Asegura que los modelos se carguen
from routes import router  # Importa las rutas

app = FastAPI()

# 🔹 Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tl-showroom.equalitech.xyz"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Asegurar que la base de datos y las tablas se creen antes de arrancar
MAX_RETRIES = 5
for i in range(MAX_RETRIES):
    try:
        Base.metadata.create_all(bind=engine)  # Crear tablas en PostgreSQL
        print("✅ Tablas creadas en PostgreSQL")
        break
    except Exception as e:
        print(f"⚠️ Intento {i+1}/{MAX_RETRIES} fallido. Reintentando en 5s...")
        time.sleep(5)
else:
    print("❌ No se pudo conectar a la base de datos.")
    raise ConnectionError("Error al conectar con la base de datos")

# 🔹 Incluir rutas de la API
app.include_router(router)

@app.get("/", response_class=JSONResponse)
def read_root():
    return JSONResponse(content={"message": "🚀 FastAPI con SSL lista. Energizada con Docker Compose."}, media_type="application/json")
