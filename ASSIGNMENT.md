# Lab 11 — Python Paralelism

## Descriere

Implementează calcul factorial paralel și un pipeline de procesare a fișierelor, folosind `multiprocessing` și `concurrent.futures`.

## Structura proiectului

```
lab11/
  lab11/
    __init__.py
    factorial.py   ← calcul factorial paralel (stub)
    pipeline.py    ← pipeline procesare fișiere (stub)
    main.py        ← entry point demonstrativ
  tests/
    __init__.py
    test_lab11.py  ← teste complete
  .github/workflows/classroom.yml
  pyproject.toml
  ASSIGNMENT.md
  README.md
```

## Cerințe

### Tema 1 — Factorial paralel

#### `factorial.py`

##### `factorial(n: int) -> int`

Calcul factorial (recursiv sau iterativ):

```python
assert factorial(0) == 1
assert factorial(5) == 120
assert factorial(10) == 3628800
```

##### `parallel_factorial_multiprocessing(values: list[int]) -> dict[int, int]`

Calculează factorialul în paralel folosind **4 procese** cu `multiprocessing.Queue` + `multiprocessing.Process`:

```python
rezultat = parallel_factorial_multiprocessing([5, 6, 7, 8])
# {5: 120, 6: 720, 7: 5040, 8: 40320}
```

**Arhitectură:**
1. Crează `input_queue` și `output_queue`
2. Lansează 4 procese `Process(target=_worker_factorial, ...)`
3. Pune toate valorile în `input_queue`
4. Trimite `None` pentru fiecare worker (semnal de oprire)
5. Colectează rezultatele din `output_queue`
6. Returnează dict-ul complet

##### `parallel_factorial_futures(values: list[int]) -> dict[int, int]`

Calculează factorialul în paralel folosind **`ProcessPoolExecutor`** cu `max_workers=4`:

```python
rezultat = parallel_factorial_futures([5, 6, 7, 8])
# {5: 120, 6: 720, 7: 5040, 8: 40320}
```

**Hint:**
```python
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(factorial, n): n for n in values}
    # sau: executor.map(factorial, values)
```

### Tema 2 — Pipeline procesare fișiere

#### `pipeline.py`

##### `read_file(path: str) -> str`

Citește conținutul unui fișier text:

```python
continut = read_file("/tmp/doc.txt")
```

##### `count_words(text: str) -> dict[str, int]`

Numără frecvența cuvintelor. Separatori: spații și newline-uri:

```python
assert count_words("ana are mere") == {'ana': 1, 'are': 1, 'mere': 1}
assert count_words("a a b") == {'a': 2, 'b': 1}
assert count_words("") == {}
```

##### `write_result(result: dict, output_path: str) -> None`

Scrie rezultatul în format JSON:

```python
write_result({'ana': 2, 'mere': 1}, "/tmp/doc.json")
# Fișierul /tmp/doc.json conține JSON valid
```

##### `process_files_pipeline(input_paths: list[str], output_dir: str) -> None`

Procesează mai multe fișiere **simultan** cu `ThreadPoolExecutor`:

```python
process_files_pipeline(
    ["/tmp/doc1.txt", "/tmp/doc2.txt"],
    "/tmp/output/"
)
# Creează /tmp/output/doc1.json și /tmp/output/doc2.json
```

**Pipeline pentru fiecare fișier:**
1. `read_file(path)` → text
2. `count_words(text)` → dict
3. `write_result(dict, output_path)` → fișier JSON

## Exemple de utilizare

### Rulare demonstrație:
```bash
uv run python -m lab11.main
```

**Output exemplu:**
```
=== Factorial paralel ===

Factoriale individuale:
  5! = 120
  6! = 720
  7! = 5040
  8! = 40320

Cu multiprocessing.Queue + Process:
  5! = 120
  ...

Cu ProcessPoolExecutor:
  5! = 120
  ...

=== Pipeline fișiere ===

count_words('ana are mere'): {'ana': 1, 'are': 1, 'mere': 1}
```

### Rulare teste:
```bash
uv run pytest
uv run pytest -v
```

## Tabel evaluare

| Cerință | Punctaj |
|---------|---------|
| `factorial(n)` corect | 10p |
| `parallel_factorial_futures()` — rezultate corecte | 20p |
| `parallel_factorial_futures()` — folosește ProcessPoolExecutor | 10p |
| `parallel_factorial_multiprocessing()` — rezultate corecte | 20p |
| `parallel_factorial_multiprocessing()` — 4 procese cu Queue | 10p |
| `count_words()` corect | 10p |
| `write_result()` → JSON valid | 5p |
| `process_files_pipeline()` — procesare paralelă corectă | 15p |
| **Total** | **100p** |

## Resurse

- [multiprocessing — Python docs](https://docs.python.org/3/library/multiprocessing.html)
- [concurrent.futures — Python docs](https://docs.python.org/3/library/concurrent.futures.html)
- [ThreadPoolExecutor vs ProcessPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor)
