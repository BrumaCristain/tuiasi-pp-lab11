# Lab 11 — Python Paralelism

Template GitHub Classroom pentru laboratorul 11 de Programare Python.

## Conținut

- **`lab11/factorial.py`** — Calcul factorial paralel cu multiprocessing (stub de implementat)
- **`lab11/pipeline.py`** — Pipeline procesare fișiere cu ThreadPoolExecutor (stub)
- **`lab11/main.py`** — Entry point demonstrativ
- **`tests/test_lab11.py`** — Suite de teste (nu modifica)

## Cum se rulează

```bash
# Rulare teste
uv run pytest

# Rulare cu output detaliat
uv run pytest -v

# Demonstrație
uv run python -m lab11.main
```

## Cum se instalează dependențele

```bash
uv sync
```

## Cerințe

- Python >= 3.11
- uv (package manager)
