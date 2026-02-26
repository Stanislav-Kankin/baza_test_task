from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.db import get_db
from app.models import User, Request as RequestModel
from app.services.request_service import RequestService

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="templates")

STATUSES = ["new", "assigned", "in_progress", "done", "canceled"]


def _get_current_user(request: Request, db: Session):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return None
    try:
        user_id_int = int(user_id)
    except ValueError:
        return None
    return db.get(User, user_id_int)


@router.get("/login")
def login_page(request: Request, db: Session = Depends(get_db)):
    users = db.execute(select(User).order_by(User.id)).scalars().all()
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "title": "Логин", "users": users, "current_user": _get_current_user(request, db)},
    )


@router.post("/login")
def login_submit(user_id: int = Form(...)):
    resp = RedirectResponse(url="/ui/create", status_code=303)
    resp.set_cookie("user_id", str(user_id), httponly=True)
    return resp


@router.get("/logout")
def logout():
    resp = RedirectResponse(url="/ui/login", status_code=303)
    resp.delete_cookie("user_id")
    return resp


@router.get("/create")
def create_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "create.html",
        {"request": request, "title": "Создать заявку", "current_user": _get_current_user(request, db)},
    )


@router.post("/create")
def create_submit(
    request: Request,
    client_name: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    problem_text: str = Form(...),
    db: Session = Depends(get_db),
):
    RequestService.create_request(db, client_name, phone, address, problem_text)
    return RedirectResponse(url="/ui/dispatcher", status_code=303)


@router.get("/dispatcher")
def dispatcher_page(request: Request, status: str | None = None, db: Session = Depends(get_db)):
    q = select(RequestModel).order_by(RequestModel.id.desc())
    if status:
        q = q.where(RequestModel.status == status)

    requests = db.execute(q).scalars().all()
    masters = db.execute(select(User).where(User.role == "master").order_by(User.id)).scalars().all()

    return templates.TemplateResponse(
        "dispatcher.html",
        {
            "request": request,
            "title": "Диспетчер",
            "requests": requests,
            "masters": masters,
            "statuses": STATUSES,
            "status_filter": status or "",
            "current_user": _get_current_user(request, db),
        },
    )


@router.post("/dispatcher/assign")
def dispatcher_assign(request_id: int = Form(...), master_id: int = Form(...), db: Session = Depends(get_db)):
    RequestService.assign_master(db, request_id, master_id)
    return RedirectResponse(url="/ui/dispatcher", status_code=303)


@router.post("/dispatcher/cancel")
def dispatcher_cancel(request_id: int = Form(...), db: Session = Depends(get_db)):
    RequestService.cancel_request(db, request_id)
    return RedirectResponse(url="/ui/dispatcher", status_code=303)


@router.get("/master")
def master_page(request: Request, db: Session = Depends(get_db)):
    current_user = _get_current_user(request, db)
    requests = []
    if current_user and current_user.role == "master":
        q = select(RequestModel).where(RequestModel.assigned_to_id == current_user.id).order_by(RequestModel.id.desc())
        requests = db.execute(q).scalars().all()

    return templates.TemplateResponse(
        "master.html",
        {
            "request": request,
            "title": "Мастер",
            "requests": requests,
            "current_user": current_user,
        },
    )


@router.post("/master/take")
def master_take(request: Request, request_id: int = Form(...), db: Session = Depends(get_db)):
    current_user = _get_current_user(request, db)
    if not current_user or current_user.role != "master":
        return RedirectResponse(url="/ui/login", status_code=303)

    try:
        RequestService.take_request(db, request_id, current_user.id)
    except Exception:
        # просто возвращаемся на страницу, в UI не делаем сложные ошибки (можно улучшить позже)
        pass
    return RedirectResponse(url="/ui/master", status_code=303)


@router.post("/master/complete")
def master_complete(request: Request, request_id: int = Form(...), db: Session = Depends(get_db)):
    current_user = _get_current_user(request, db)
    if not current_user or current_user.role != "master":
        return RedirectResponse(url="/ui/login", status_code=303)

    try:
        RequestService.complete_request(db, request_id, current_user.id)
    except Exception:
        pass
    return RedirectResponse(url="/ui/master", status_code=303)
