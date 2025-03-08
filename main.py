import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
@app.get("/", response_class=JSONResponse)
def read_root():
    return JSONResponse(content={"message": "🚀 FastAPI sin SSL habilitado"}, media_type="application/json")
