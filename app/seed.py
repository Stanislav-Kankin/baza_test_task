"""Seed initial data: 1 dispatcher, 2 masters, several requests.

Run:
  docker compose exec app python -m app.seed
"""

from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models.user import User
from app.models.request import Request


def seed_users(db: Session) -> dict[str, User]:
    dispatcher = db.query(User).filter(User.name == "dispatcher").one_or_none()
    if not dispatcher:
        dispatcher = User(name="dispatcher", role="dispatcher")
        db.add(dispatcher)

    master1 = db.query(User).filter(User.name == "master1").one_or_none()
    if not master1:
        master1 = User(name="master1", role="master")
        db.add(master1)

    master2 = db.query(User).filter(User.name == "master2").one_or_none()
    if not master2:
        master2 = User(name="master2", role="master")
        db.add(master2)

    db.commit()
    db.refresh(dispatcher)
    db.refresh(master1)
    db.refresh(master2)

    return {"dispatcher": dispatcher, "master1": master1, "master2": master2}


def seed_requests(db: Session, users: dict[str, User]) -> None:
    any_req = db.query(Request).first()
    if any_req:
        return

    db.add_all(
        [
            Request(
                client_name="Иван",
                phone="+7 900 000-00-01",
                address="Краснодар, ул. Красная 1",
                problem_text="Не работает розетка",
                status="new",
            ),
            Request(
                client_name="Мария",
                phone="+7 900 000-00-02",
                address="Краснодар, ул. Красная 2",
                problem_text="Течёт кран",
                status="new",
            ),
            Request(
                client_name="Пётр",
                phone="+7 900 000-00-03",
                address="Краснодар, ул. Красная 3",
                problem_text="Не греет батарея",
                status="assigned",
                assigned_to_id=users["master1"].id,
            ),
            Request(
                client_name="Ольга",
                phone="+7 900 000-00-04",
                address="Краснодар, ул. Красная 4",
                problem_text="Выбивает автомат",
                status="assigned",
                assigned_to_id=users["master2"].id,
            ),
        ]
    )
    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        users = seed_users(db)
        seed_requests(db, users)
        print("Seed complete. Users: dispatcher/master1/master2. Requests seeded.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
