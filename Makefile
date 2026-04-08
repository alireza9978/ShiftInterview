PYTHON := python3
VENV := .venv
VENV_BIN := $(VENV)/bin
PIP := $(VENV_BIN)/pip
PYTEST := $(VENV_BIN)/pytest
UVICORN := $(VENV_BIN)/uvicorn
RUFF := $(VENV_BIN)/ruff
BLACK := $(VENV_BIN)/black
MYPY := $(VENV_BIN)/mypy

APP_MODULE ?= app.main:app
HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: help venv install run dev lint format type typecheck tests test test-cov nice all clean

help:
	@echo "Available targets:"
	@echo "  make venv       - Create virtual environment"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run FastAPI app"
	@echo "  make dev        - Run FastAPI app with auto-reload"
	@echo "  make lint       - Run ruff lint checks"
	@echo "  make format     - Format code with black"
	@echo "  make typecheck  - Run mypy type checks"
	@echo "  make test       - Run test suite"
	@echo "  make test-cov   - Run tests with coverage"
	@echo "  make tests      - Run test, and test-cov"
	@echo "  make nice       - Run lint, format, and typecheck"
	@echo "  make all        - Run nice and tests, then clean"
	@echo "  make clean      - Remove caches and build artifacts"

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) $(APP_MODULE) --host $(HOST) --port $(PORT)

dev:
	$(UVICORN) $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

lint:
	$(RUFF) check .

format:
	$(BLACK) .

typecheck:
	$(MYPY) .

test:
	$(PYTEST) -q

test-cov:
	$(PYTEST) --cov=. --cov-report=term-missing

tests: test test-cov

nice: lint format typecheck

all: nice tests clean

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +