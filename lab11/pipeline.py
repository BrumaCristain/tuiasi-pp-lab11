"""
Pipeline de procesare paralelă a fișierelor.

Tema 2: procesează mai multe fișiere simultan în 3 etape:
1. Citire conținut
2. Numărare cuvinte
3. Scriere rezultat
"""

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


# TODO: Implementează funcția read_file
def read_file(path: str) -> str:
    """Citește conținutul unui fișier text.

    Args:
        path: Calea absolută sau relativă a fișierului.

    Returns:
        Conținutul fișierului ca string.

    Raises:
        FileNotFoundError: Dacă fișierul nu există.
        IOError: La erori de citire.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# TODO: Implementează funcția count_words
def count_words(text: str) -> dict[str, int]:
    """Numără frecvența fiecărui cuvânt din text.

    Cuvintele sunt separate prin spații și/sau newline-uri.
    Comparația este case-sensitive (nu se face lowercase).

    Args:
        text: Textul de analizat.

    Returns:
        Dict {cuvânt: număr_apariții}.

    Exemple:
        count_words("ana are mere") == {'ana': 1, 'are': 1, 'mere': 1}
        count_words("a a b") == {'a': 2, 'b': 1}
        count_words("") == {}
    """
    words = text.split()
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


# TODO: Implementează funcția write_result
def write_result(result: dict, output_path: str) -> None:
    """Scrie rezultatul numărării cuvintelor în fișier JSON.

    Args:
        result: Dict-ul {cuvânt: frecvență} de scris.
        output_path: Calea fișierului de ieșire.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f)


def _process_single_file(args: tuple[str, str]) -> None:
    """Procesează un singur fișier prin cele 3 etape.

    Args:
        args: Tuplu (input_path, output_path).
    """
    # TODO: Implementează procesarea unui fișier individual
    # 1. Citește conținutul
    # 2. Numără cuvintele
    # 3. Scrie rezultatul
    input_path, output_path = args
    text = read_file(input_path)
    counts = count_words(text)
    write_result(counts, output_path)


# TODO: Implementează funcția process_files_pipeline
def process_files_pipeline(input_paths: list[str], output_dir: str) -> None:
    """Procesează mai multe fișiere în paralel folosind un pipeline cu ThreadPoolExecutor.

    Fișierele sunt procesate simultan (nu secvențial).
    Fișierul de ieșire are același nume ca cel de intrare, cu extensia .json.

    Args:
        input_paths: Lista căilor fișierelor de intrare.
        output_dir: Directorul unde se scriu fișierele de ieșire.

    Exemplu:
        process_files_pipeline(
            ["/tmp/doc1.txt", "/tmp/doc2.txt"],
            "/tmp/output/"
        )
        # Creează /tmp/output/doc1.json și /tmp/output/doc2.json
    """
    output_path_obj = Path(output_dir)
    output_path_obj.mkdir(parents=True, exist_ok=True)

    args_list = []
    for input_path in input_paths:
        stem = Path(input_path).stem
        output_path = str(output_path_obj / f"{stem}.json")
        args_list.append((input_path, output_path))

    with ThreadPoolExecutor() as executor:
        executor.map(_process_single_file, args_list)
