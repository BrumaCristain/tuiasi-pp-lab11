"""
Calcul factorial paralel folosind multiprocessing.

Tema 1: calculează n! simultan pentru mai multe valori,
folosind atât multiprocessing.Queue + Process cât și ProcessPoolExecutor.
"""

import multiprocessing
from concurrent.futures import ProcessPoolExecutor


# TODO: Implementează funcția factorial
def factorial(n: int) -> int:
    """Calculează n! (factorial).

    Args:
        n: Numărul pentru care se calculează factorialul. Trebuie să fie >= 0.

    Returns:
        n! ca întreg.

    Raises:
        ValueError: Dacă n este negativ.

    Exemple:
        factorial(0) == 1
        factorial(1) == 1
        factorial(5) == 120
    """
    raise NotImplementedError("De implementat")


def _worker_factorial(input_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue) -> None:
    """Funcție worker pentru procesul multiprocessing.

    Citește valori din input_queue, calculează factorialul și trimite
    rezultatele în output_queue sub forma (n, factorial(n)).

    Se oprește când primește None din input_queue.

    Args:
        input_queue: Coada de unde se citesc valorile n.
        output_queue: Coada unde se trimit perechile (n, rezultat).
    """
    # TODO: Implementează bucla worker
    raise NotImplementedError("De implementat")


# TODO: Implementează funcția parallel_factorial_multiprocessing
def parallel_factorial_multiprocessing(values: list[int]) -> dict[int, int]:
    """Calculează factorialul pentru mai multe valori în paralel.

    Folosește 4 procese worker cu multiprocessing.Queue și multiprocessing.Process.

    Args:
        values: Lista valorilor pentru care se calculează factorialul.

    Returns:
        Dict {n: factorial(n)} pentru toate valorile din lista.

    Exemplu:
        result = parallel_factorial_multiprocessing([5, 6, 7, 8])
        # {5: 120, 6: 720, 7: 5040, 8: 40320}
    """
    raise NotImplementedError("De implementat")


# TODO: Implementează funcția parallel_factorial_futures
def parallel_factorial_futures(values: list[int]) -> dict[int, int]:
    """Calculează factorialul pentru mai multe valori în paralel.

    Folosește concurrent.futures.ProcessPoolExecutor cu max_workers=4.

    Args:
        values: Lista valorilor pentru care se calculează factorialul.

    Returns:
        Dict {n: factorial(n)} pentru toate valorile din lista.

    Exemplu:
        result = parallel_factorial_futures([5, 6, 7, 8])
        # {5: 120, 6: 720, 7: 5040, 8: 40320}
    """
    raise NotImplementedError("De implementat")
