"""
Paralelización real con numba. Se usa sobre todo con arrays numericos
"""

from databank_mlops.logger.logger import logger

import numpy as np
from numba import njit, prange
import time


def ejecucion_serie(A_1, B_1, C_1, D_1, N, M):
    """
    Codigo en serie
    """
    # Bucle externo: i de 1 a N
    for i in range(N):
        for j in range(M):
            if (i > 0) and (j > 0):
                D_1[i, j] = D_1[i-1, j-1] + 1.
            if (i - 1 >= 0) and (j + 4 < M):
                B_1[i-1, j+4] = D_1[i, j] - 1.
            C_1[i, j] = A_1[i, j] * B_1[i, j] / 1000.
            if (i + 1 < N) and (j + 1 < M) and (j - 2 >= 0) and (i - 1 >= 0):
                A_1[i+1, j+1] = (C_1[i, j-2] / 2.) + (C_1[i-1, j] * 3.)


@njit(parallel=True)
def ejecucion_paralelo(A, B, C, D, N, M):
    """
    Codigo que se ha paralelizado
    """
    # Bucle externo: i de 1 a N
    for i in range(N):
        # Primer bloque (doall j): S1 y S3
        for j in prange(M):
            if (i > 0) and (j > 0):
                # S1: D[i, j] = D[i-1, j-1] + 1
                D[i, j] = D[i-1, j-1] + 1.
            # S3: C[i, j] = A[i, j] * B[i, j]
            C[i, j] = A[i, j] * B[i, j] / 1000.
        # Al finalizar el bucle prange se produce una sincronización implícita

        # Segundo bloque (doall j): S4
        for j in prange(M):
            if (i + 1 < N) and (j + 1 < M) and (j - 2 >= 0) and (i -1 >= 0):
                # S4: A[i+1, j+1] = C[i, j-2] / 2 + C[i-1, j] * 3
                A[i+1, j+1] = C[i, j-2] / 2. + C[i-1, j] * 3.
        # La sincronización implícita de los bucles prange garantiza que todas las iteraciones de j terminen antes de pasar a la siguiente iteración de i.

    # Barrera implícita tras finalizar el bucle externo.

    # Bloque final (doall i): S2
    for i in prange(N):
        for j in range(M):
            if (i - 1 >= 0) and (j + 4 < M):
                # S2: B[i-1, j+4] = D[i, j] - 1
                B[i-1, j+4] = D[i, j] - 1.
    # Al finalizar este bloque, los hilos se sincronizan implícitamente.


if __name__ == "__main__":
    # Parámetros de tamaño
    N = 4000  # iteraciones i
    M = 4000  # iteraciones j

    # Se crean las matrices serie
    np.random.seed(202504)
    A_1 = np.random.randint(0, 10, (N, M)).astype(np.float64)
    B_1 = np.random.randint(0, 10, (N, M)).astype(np.float64)
    D_1 = np.random.randint(0, 10, (N, M)).astype(np.float64)
    C_1 = np.random.randint(0, 10, (N, M)).astype(np.float64)

    # Se crean las matrices paralelo
    np.random.seed(202504)
    A = np.random.randint(0, 10, (N, M)).astype(np.float64)
    B = np.random.randint(0, 10, (N, M)).astype(np.float64)
    D = np.random.randint(0, 10, (N, M)).astype(np.float64)
    C = np.random.randint(0, 10, (N, M)).astype(np.float64)

    logger.info("Validacion se parte de las mismas Matrices:")
    logger.info(f"Matriz D_1:\n {D_1}")
    logger.info(f"Matriz D:\n {D}")
    logger.info(f"Matriz C_1:\n {C_1}")
    logger.info(f"Matriz C:\n {C}")
    logger.info(f"Matriz A_1:\n {A_1}")
    logger.info(f"Matriz A:\n {A}")
    logger.info(f"Matriz B_1:\n {B_1}")
    logger.info(f"Matriz B:\n {B}")
    logger.info("===============================")

    logger.info("Comparación tiempos:")
    # Serie
    start_time = time.time()
    ejecucion_serie(A_1, B_1, C_1, D_1, N, M)
    logger.info(f"Tiempo de ejecución en serie: {time.time() - start_time} segundos")
    # Paralelo
    start_time = time.time()
    ejecucion_paralelo(A, B, C, D, N, M)
    logger.info(f"Tiempo de ejecución en paralelo: {time.time() - start_time} segundos")

    # Mostrar resultados para validar da mismos resultados
    time.sleep(10)
    logger.info("===============================")
    logger.info("Validación da mismos resultados:")
    logger.info(f"Matriz D_1 actualizada:\n {D_1}")
    logger.info(f"Matriz D actualizada:\n {D}")
    logger.info(f"Matriz C_1 actualizada:\n {C_1}")
    logger.info(f"Matriz C actualizada:\n {C}")
    logger.info(f"Matriz A_1 actualizada:\n {A_1}")
    logger.info(f"Matriz A actualizada:\n {A}")
    logger.info(f"Matriz B_1 actualizada:\n {B_1}")
    logger.info(f"Matriz B actualizada:\n {B}")
