from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI funcionando correctamente con Nginx y Docker!"}
