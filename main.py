from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las conexiones (en producción usa solo los dominios necesarios)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI funcionando correctamente con CORS habilitado!"}
