"""
El **multithreading** se refiere a la ejecución de múltiples hilos dentro de un mismo proceso. Los hilos comparten el mismo espacio de memoria y recursos, lo que facilita la comunicación entre ellos.

Características clave:
* Hilos dentro de un proceso
* No hay paralelismo real (debido al GIL)
    * GIL (Global Interpreter Lock) en Python es un bloqueo global que restringe la ejecución de múltiples hilos en CPython (la implementación estándar de Python)
* Mejor para tareas I/O-bound
* Comunicación sencilla
"""
from databank_mlops.logger.logger import logger

import threading
import time


def worker(n):
    logger.info(f"Inicio de tarea {n}")
    time.sleep(2)
    logger.info(f"Fin de tarea {n}")


if __name__ == '__main__':

    N = 5

    start_time = time.time()
    for i in range(N):
        worker(i,)
    logger.info(f"tiempo en serie: {time.time() - start_time} segundos")

    start_time = time.time()
    threads = []
    for i in range(N):
        t = threading.Thread(target=worker, args=(i, ))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    logger.info(f"tiempo en paralelo: {time.time() - start_time} segundos")
