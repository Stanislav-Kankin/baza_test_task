
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models import Request, User


class RequestService:

    @staticmethod
    def create_request(db: Session, client_name: str, phone: str, address: str, problem_text: str):
        request = Request(
            client_name=client_name,
            phone=phone,
            address=address,
            problem_text=problem_text,
            status="new",
        )
        db.add(request)
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def assign_master(db: Session, request_id: int, master_id: int):
        request = db.get(Request, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")

        if request.status != "new":
            raise HTTPException(status_code=400, detail="Only NEW requests can be assigned")

        master = db.get(User, master_id)
        if not master or master.role != "master":
            raise HTTPException(status_code=400, detail="Invalid master")

        request.assigned_to_id = master_id
        request.status = "assigned"
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def cancel_request(db: Session, request_id: int):
        request = db.get(Request, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")

        if request.status in ["done", "canceled"]:
            raise HTTPException(status_code=400, detail="Cannot cancel finished request")

        request.status = "canceled"
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def take_request(db: Session, request_id: int, master_id: int):
        # Safe take using SELECT FOR UPDATE
        stmt = select(Request).where(Request.id == request_id).with_for_update()
        request = db.execute(stmt).scalar_one_or_none()

        if not request:
            raise HTTPException(status_code=404, detail="Request not found")

        if request.status != "assigned":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Request already taken or invalid status",
            )

        if request.assigned_to_id != master_id:
            raise HTTPException(status_code=403, detail="Not assigned to this master")

        request.status = "in_progress"
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def complete_request(db: Session, request_id: int, master_id: int):
        request = db.get(Request, request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")

        if request.status != "in_progress":
            raise HTTPException(status_code=400, detail="Request not in progress")

        if request.assigned_to_id != master_id:
            raise HTTPException(status_code=403, detail="Not assigned to this master")

        request.status = "done"
        db.commit()
        db.refresh(request)
        return request
