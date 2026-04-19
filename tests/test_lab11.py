"""
Teste pentru Lab 11 — Python Paralelism.

Testele acoperă:
- Calcul factorial (serial și paralel)
- Pipeline procesare fișiere
"""

import json
import os
import pytest

from lab11.factorial import (
    factorial,
    parallel_factorial_multiprocessing,
    parallel_factorial_futures,
)
from lab11.pipeline import (
    read_file,
    count_words,
    write_result,
    process_files_pipeline,
)


class TestFactorial:
    """Teste pentru calcul factorial."""

    # ── Factorial serial ──────────────────────────────────────────────────────

    def test_factorial_zero(self) -> None:
        """0! = 1."""
        assert factorial(0) == 1

    def test_factorial_unu(self) -> None:
        """1! = 1."""
        assert factorial(1) == 1

    def test_factorial_cinci(self) -> None:
        """5! = 120."""
        assert factorial(5) == 120

    def test_factorial_zece(self) -> None:
        """10! = 3628800."""
        assert factorial(10) == 3628800

    def test_factorial_returneaza_int(self) -> None:
        """factorial() returnează întotdeauna un int."""
        assert isinstance(factorial(5), int)

    def test_factorial_negativ_ridica_eroare(self) -> None:
        """factorial(-1) aruncă ValueError."""
        with pytest.raises((ValueError, Exception)):
            factorial(-1)

    # ── Factorial paralel cu futures ──────────────────────────────────────────

    def test_parallel_futures_valori_simple(self) -> None:
        """ProcessPoolExecutor calculează corect factorialele."""
        rezultat = parallel_factorial_futures([5, 6, 7, 8])
        assert rezultat[5] == 120
        assert rezultat[6] == 720
        assert rezultat[7] == 5040
        assert rezultat[8] == 40320

    def test_parallel_futures_returneaza_dict(self) -> None:
        """parallel_factorial_futures returnează un dict."""
        rezultat = parallel_factorial_futures([5])
        assert isinstance(rezultat, dict)

    def test_parallel_futures_toate_cheile_prezente(self) -> None:
        """Toate valorile de intrare sunt chei în rezultat."""
        valori = [3, 4, 5]
        rezultat = parallel_factorial_futures(valori)
        for v in valori:
            assert v in rezultat

    def test_parallel_futures_lista_goala(self) -> None:
        """Listă goală returnează dict gol."""
        assert parallel_factorial_futures([]) == {}

    # ── Factorial paralel cu multiprocessing ──────────────────────────────────

    def test_parallel_multiprocessing_valori_simple(self) -> None:
        """multiprocessing.Queue calculează corect factorialele."""
        rezultat = parallel_factorial_multiprocessing([5, 6, 7, 8])
        assert rezultat[5] == 120
        assert rezultat[6] == 720
        assert rezultat[7] == 5040
        assert rezultat[8] == 40320

    def test_parallel_multiprocessing_returneaza_dict(self) -> None:
        """parallel_factorial_multiprocessing returnează un dict."""
        rezultat = parallel_factorial_multiprocessing([5])
        assert isinstance(rezultat, dict)

    def test_parallel_multiprocessing_toate_cheile(self) -> None:
        """Toate valorile sunt calculate și returnate."""
        valori = [1, 2, 3, 4]
        rezultat = parallel_factorial_multiprocessing(valori)
        assert rezultat == {1: 1, 2: 2, 3: 6, 4: 24}


class TestPipeline:
    """Teste pentru pipeline-ul de procesare fișiere."""

    # ── count_words ───────────────────────────────────────────────────────────

    def test_count_words_simplu(self) -> None:
        """Numărare cuvinte pentru 'ana are mere'."""
        rezultat = count_words("ana are mere")
        assert rezultat == {"ana": 1, "are": 1, "mere": 1}

    def test_count_words_repetitii(self) -> None:
        """Cuvintele repetate sunt numărate corect."""
        rezultat = count_words("a a b")
        assert rezultat == {"a": 2, "b": 1}

    def test_count_words_text_gol(self) -> None:
        """Text gol returnează dict gol."""
        assert count_words("") == {}

    def test_count_words_mai_multe_spatii(self) -> None:
        """Spații multiple sunt tratate corect."""
        rezultat = count_words("ana  are  mere")
        assert rezultat["ana"] == 1
        assert rezultat["are"] == 1
        assert rezultat["mere"] == 1

    def test_count_words_cu_newline(self) -> None:
        """Newline-urile sunt tratate ca separatori."""
        rezultat = count_words("ana\nare\nmere")
        assert rezultat == {"ana": 1, "are": 1, "mere": 1}

    def test_count_words_returneaza_dict(self) -> None:
        """count_words returnează un dict."""
        assert isinstance(count_words("test"), dict)

    # ── read_file ─────────────────────────────────────────────────────────────

    def test_read_file_citeste_continut(self, tmp_path) -> None:
        """read_file citește corect conținutul unui fișier."""
        fisier = tmp_path / "test.txt"
        fisier.write_text("Conținut de test\n", encoding="utf-8")
        continut = read_file(str(fisier))
        assert "Conținut de test" in continut

    def test_read_file_fisier_inexistent(self, tmp_path) -> None:
        """read_file aruncă excepție pentru fișier inexistent."""
        with pytest.raises((FileNotFoundError, IOError, OSError)):
            read_file(str(tmp_path / "inexistent.txt"))

    # ── write_result ──────────────────────────────────────────────────────────

    def test_write_result_creaza_fisier(self, tmp_path) -> None:
        """write_result creează fișierul de ieșire."""
        output = str(tmp_path / "rezultat.json")
        write_result({"ana": 1, "mere": 2}, output)
        assert os.path.exists(output)

    def test_write_result_continut_valid(self, tmp_path) -> None:
        """write_result scrie date care pot fi citite înapoi."""
        output = str(tmp_path / "rezultat.json")
        data = {"ana": 1, "are": 1, "mere": 1}
        write_result(data, output)
        with open(output, encoding="utf-8") as f:
            citit = json.load(f)
        assert citit == data

    # ── process_files_pipeline ────────────────────────────────────────────────

    def test_pipeline_creaza_fisiere_output(self, tmp_path) -> None:
        """pipeline-ul creează fișierele de ieșire pentru fiecare input."""
        # Creare fișiere input
        fisier1 = tmp_path / "doc1.txt"
        fisier1.write_text("ana are mere", encoding="utf-8")
        fisier2 = tmp_path / "doc2.txt"
        fisier2.write_text("pere prune", encoding="utf-8")

        output_dir = str(tmp_path / "output")
        os.makedirs(output_dir)

        process_files_pipeline([str(fisier1), str(fisier2)], output_dir)

        assert os.path.exists(os.path.join(output_dir, "doc1.json"))
        assert os.path.exists(os.path.join(output_dir, "doc2.json"))

    def test_pipeline_continut_corect(self, tmp_path) -> None:
        """Pipeline-ul calculează corect frecvența cuvintelor."""
        fisier = tmp_path / "test.txt"
        fisier.write_text("ana are mere\nana pleaca", encoding="utf-8")

        output_dir = str(tmp_path / "output")
        os.makedirs(output_dir)

        process_files_pipeline([str(fisier)], output_dir)

        with open(os.path.join(output_dir, "test.json"), encoding="utf-8") as f:
            rezultat = json.load(f)

        assert rezultat["ana"] == 2
        assert rezultat["are"] == 1
        assert rezultat["mere"] == 1

    def test_pipeline_lista_goala(self, tmp_path) -> None:
        """Pipeline-ul cu listă goală nu aruncă eroare."""
        output_dir = str(tmp_path / "output")
        os.makedirs(output_dir)
        process_files_pipeline([], output_dir)  # Nu trebuie să arunce excepție
