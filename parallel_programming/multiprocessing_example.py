"""
El **multiprocessing** implica la ejecución de múltiples procesos, cada uno con su propio espacio de memoria y recursos. Cada proceso tiene su propio intérprete de Python, lo que significa que no comparten memoria entre sí de manera directa.

Características clave:
* Procesos independientes.
* Paralelismo real
* Adecuado para tareas intensivas en CPU
* Comunicación entre procesos
"""
from databank_mlops.logger.logger import logger

import multiprocessing
import time


def tarea_lenta(n):
    suma = 0
    for i in range(n):
        suma += i**2

    return suma


if __name__ == '__main__':
    N = 1000000

    CORES = multiprocessing.cpu_count()
    logger.info(f"CORES: {CORES}")

    start_time = time.time()
    results_serie = [tarea_lenta(N) for _ in range(CORES * 2)]
    logger.info(f"tiempo en serie: {time.time() - start_time}")

    start_time = time.time()
    with multiprocessing.Pool(CORES) as pool:
        results_paralelo = pool.map(tarea_lenta, [N] * (CORES * 2))
    print("##########################################################################################################")
    logger.info(f"tiempo en paralelo: {time.time() - start_time}")
