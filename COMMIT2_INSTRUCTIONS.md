# Commit 2: DB models + Alembic + seed

## 1) Copy files into your repo
Copy the contents of this archive into the root of your repository (preserve paths).

## 2) Start containers
docker compose up -d --build

## 3) Generate first migration
docker compose exec app alembic revision --autogenerate -m "init tables"

## 4) Apply migration
docker compose exec app alembic upgrade head

## 5) Seed data (separate step)
docker compose exec app python -m app.seed

## 6) Check health (DB ping)
curl http://localhost:8090/health
# -> {"status":"ok"}
