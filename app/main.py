from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.db import get_db
from app.routers.requests import router as requests_router

app = FastAPI(title="Repair Service Requests")

app.include_router(requests_router)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return JSONResponse({"status": "ok"})
