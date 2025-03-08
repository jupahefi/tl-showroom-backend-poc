from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tl-showroom.equalitech.xyz"],  # Reemplaza con el dominio correcto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=JSONResponse)
def read_root():
    return JSONResponse(content={"message": "🚀 FastAPI funcionando correctamente con CORS habilitado!"}, media_type="application/json")
