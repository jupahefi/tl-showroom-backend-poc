import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

"""app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tl-showroom.equalitech.xyz"],  # Asegura que coincida con tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)"""

@app.get("/", response_class=JSONResponse)
def read_root():
    return JSONResponse(content={"message": "🚀 FastAPI funcionando correctamente con CORS habilitado! y un mensaje porque asi reconoces que si llegue"}, media_type="application/json")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="/etc/letsencrypt/live/equalitech.xyz/privkey.pem",
        ssl_certfile="/etc/letsencrypt/live/equalitech.xyz/fullchain.pem"
    )
