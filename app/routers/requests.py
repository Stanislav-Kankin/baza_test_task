
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.request_service import RequestService

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("/")
def create_request(client_name: str, phone: str, address: str, problem_text: str, db: Session = Depends(get_db)):
    return RequestService.create_request(db, client_name, phone, address, problem_text)


@router.post("/{request_id}/assign/{master_id}")
def assign_master(request_id: int, master_id: int, db: Session = Depends(get_db)):
    return RequestService.assign_master(db, request_id, master_id)


@router.post("/{request_id}/cancel")
def cancel_request(request_id: int, db: Session = Depends(get_db)):
    return RequestService.cancel_request(db, request_id)


@router.post("/{request_id}/take/{master_id}")
def take_request(request_id: int, master_id: int, db: Session = Depends(get_db)):
    return RequestService.take_request(db, request_id, master_id)


@router.post("/{request_id}/complete/{master_id}")
def complete_request(request_id: int, master_id: int, db: Session = Depends(get_db)):
    return RequestService.complete_request(db, request_id, master_id)
