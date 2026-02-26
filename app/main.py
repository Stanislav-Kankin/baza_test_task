from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Repair Service Requests")

@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})