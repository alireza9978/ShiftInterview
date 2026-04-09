# ShiftInterview

Simple FastAPI project to manage users and their permissions.

## What This Project Does

- Creates, lists, and deletes users.
- Grants, lists, and revokes permissions.
  - Create a permission and grants it to a user.
- Supports user search by family name.

## Architecture

- `api/routes`: HTTP endpoints, request parsing, and response/error mapping.
- `services`: business rules and use-case orchestration.
- `repositories`: database access and query logic.
- `models`: SQLAlchemy ORM entities (`User`, `Permission`).
- `schemas`: Pydantic request/response contracts and validation.
- `core`: app settings and database/session wiring.
- `tests`: unit and API tests by layer.

## How To Run (Make)

From project root:

```bash
make install
make run
```

Then open:

- API docs: `http://localhost:8000/docs`
- Postman Collection: [Link](https://lively-zodiac-203348.postman.co/workspace/My-Workspace~95ddfeff-4182-4331-8235-29ad019898e1/collection/25453922-80c96f7f-85bd-49b4-a72e-af7b414bd2de?action=share&source=copy-link&creator=25453922)
- Health check: `http://localhost:8000/health`

Useful commands:

```bash
make dev       # run with auto-reload
make tests     # run tests
make nice      # lint + format + typecheck
```