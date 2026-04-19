"""
Entry point pentru demonstrarea paralelismului.

Utilizare:
    uv run python -m lab11.main
"""

from lab11.factorial import factorial, parallel_factorial_multiprocessing, parallel_factorial_futures
from lab11.pipeline import count_words, process_files_pipeline
import tempfile
import os


def main() -> None:
    """Demonstrează funcționalitățile de paralelism."""
    print("=== Factorial paralel ===\n")

    valori = [5, 6, 7, 8]

    print("Factoriale individuale:")
    for n in valori:
        print(f"  {n}! = {factorial(n)}")

    print("\nCu multiprocessing.Queue + Process:")
    rezultate_mp = parallel_factorial_multiprocessing(valori)
    for n, rez in sorted(rezultate_mp.items()):
        print(f"  {n}! = {rez}")

    print("\nCu ProcessPoolExecutor:")
    rezultate_futures = parallel_factorial_futures(valori)
    for n, rez in sorted(rezultate_futures.items()):
        print(f"  {n}! = {rez}")

    print("\n=== Pipeline fișiere ===\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Creare fișiere de test
        fisier1 = os.path.join(tmpdir, "doc1.txt")
        fisier2 = os.path.join(tmpdir, "doc2.txt")

        with open(fisier1, "w") as f:
            f.write("ana are mere\nana pleaca")
        with open(fisier2, "w") as f:
            f.write("mere pere prune\npere prune")

        output_dir = os.path.join(tmpdir, "output")
        os.makedirs(output_dir)

        process_files_pipeline([fisier1, fisier2], output_dir)

        print("Fișiere procesate:")
        for fisier in os.listdir(output_dir):
            print(f"  {fisier}")

    print("\ncount_words('ana are mere'):", count_words("ana are mere"))


if __name__ == "__main__":
    main()
