# Веб-сервис “Заявки в ремонтную службу” (test task)

Минимальное веб‑приложение для приёма и обработки заявок в ремонтную службу.
Стек: **FastAPI + Postgres + SQLAlchemy + Alembic + Docker Compose + Jinja2**.

## Быстрый старт (Docker Compose)

```bash
docker compose up -d --build
docker compose exec app alembic upgrade head
docker compose exec app python -m app.seed
```

Открыть приложение: `http://localhost:8090`

## Тестовые пользователи (сидятся командой seed)

- `dispatcher` — роль `dispatcher`
- `master1` — роль `master` (обычно id=2)
- `master2` — роль `master` (обычно id=3)

> Авторизация упрощённая: выбор пользователя на странице `/ui/login` (user_id хранится в cookie).

## UI (3 экрана по ТЗ)

- Создание заявки: `GET /ui/create`
- Панель диспетчера: `GET /ui/dispatcher`
- Панель мастера: `GET /ui/master`
- Логин: `GET /ui/login`

## API (минимум)

- `POST /requests/` — создать заявку (status=`new`)
- `GET /requests/?status=...` — список заявок (опциональный фильтр)
- `POST /requests/{request_id}/assign/{master_id}` — назначить мастера (status=`assigned`)
- `POST /requests/{request_id}/cancel` — отменить (status=`canceled`)
- `POST /requests/{request_id}/take/{master_id}` — мастер берёт в работу (status: `assigned → in_progress`, защита от гонки)
- `POST /requests/{request_id}/complete/{master_id}` — завершить (status: `in_progress → done`)

## Автотесты

В проекте есть минимум 2 теста (включая проверку гонки):

```bash
docker compose exec app pytest
```

## Проверка “гонки” take (обязательное условие)

Идея: два параллельных запроса на `take` одной и той же заявки — **один должен пройти**, второй получить **409 Conflict**.

### Вариант A — два терминала (PowerShell)

1) Создай заявку и назначь мастера (например `master1`, id=2).
2) В ДВУХ терминалах одновременно выполни:

```powershell
curl.exe -X POST "http://localhost:8090/requests/<ID>/take/2"
```

Ожидаемо:
- один ответ `200`
- второй ответ `409`

### Вариант B — скрипт PowerShell

```powershell
.\scripts\race_test.ps1 -RequestId <ID> -MasterId 2
```

## Полезное

Если база “пустая” после пересоздания контейнеров — повтори:

```bash
docker compose exec app alembic upgrade head
docker compose exec app python -m app.seed
```
