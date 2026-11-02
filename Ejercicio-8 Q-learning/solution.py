#!/usr/bin/env python3
"""Implementa Q-learning tabular para el problema del acantilado de 4 × 12."""

from __future__ import annotations

import csv
import random
from pathlib import Path

Estado = tuple[int, int]
Accion = str
Transicion = tuple[Estado, float, bool]

FILAS = 4
COLUMNAS = 12
INICIO: Estado = (3, 0)
META: Estado = (3, 11)
ACANTILADO = {(3, columna) for columna in range(1, 11)}
ACCIONES: tuple[Accion, ...] = ("N", "E", "S", "W")
DESPLAZAMIENTOS: dict[Accion, Estado] = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}
ALFA = 0.5
GAMMA = 1.0
EPSILON = 0.1
EPISODIOS = 500
MAXIMO_PASOS = 200
SEMILLA = 42
ARCHIVO_SALIDA = Path(__file__).with_name("episode_returns.csv")


def transicion(estado: Estado, accion: Accion) -> Transicion:
    """Devuelve el estado siguiente, la recompensa y si termina el episodio."""
    fila, columna = estado
    desplazamiento_fila, desplazamiento_columna = DESPLAZAMIENTOS[accion]
    siguiente_estado = (
        fila + desplazamiento_fila,
        columna + desplazamiento_columna,
    )

    if not (
        0 <= siguiente_estado[0] < FILAS
        and 0 <= siguiente_estado[1] < COLUMNAS
    ):
        siguiente_estado = estado
    if siguiente_estado in ACANTILADO:
        return INICIO, -100.0, False
    if siguiente_estado == META:
        return META, -1.0, True
    return siguiente_estado, -1.0, False


def crear_tabla_q() -> dict[Estado, dict[Accion, float]]:
    estados = (
        (fila, columna)
        for fila in range(FILAS)
        for columna in range(COLUMNAS)
        if (fila, columna) not in ACANTILADO and (fila, columna) != META
    )
    return {estado: {accion: 0.0 for accion in ACCIONES} for estado in estados}


def accion_voraz(
    tabla_q: dict[Estado, dict[Accion, float]], estado: Estado
) -> Accion:
    """Devuelve la primera acción con valor máximo en el orden fijo."""
    return max(ACCIONES, key=lambda accion: tabla_q[estado][accion])


def accion_epsilon_voraz(
    tabla_q: dict[Estado, dict[Accion, float]],
    estado: Estado,
    generador: random.Random,
) -> Accion:
    if generador.random() < EPSILON:
        return generador.choice(ACCIONES)
    return accion_voraz(tabla_q, estado)


def entrenar(
    generador: random.Random,
) -> tuple[dict[Estado, dict[Accion, float]], list[float]]:
    tabla_q = crear_tabla_q()
    recompensas_episodios: list[float] = []

    for _ in range(EPISODIOS):
        estado = INICIO
        recompensa_episodio = 0.0

        for _ in range(MAXIMO_PASOS):
            accion = accion_epsilon_voraz(tabla_q, estado, generador)
            siguiente_estado, recompensa, terminado = transicion(estado, accion)
            futuro = (
                0.0
                if terminado
                else max(tabla_q[siguiente_estado].values())
            )
            valor_anterior = tabla_q[estado][accion]
            objetivo = recompensa + GAMMA * futuro
            tabla_q[estado][accion] = valor_anterior + ALFA * (
                objetivo - valor_anterior
            )
            recompensa_episodio += recompensa
            estado = siguiente_estado
            if terminado:
                break

        recompensas_episodios.append(recompensa_episodio)

    return tabla_q, recompensas_episodios


def evaluar_voraz(
    tabla_q: dict[Estado, dict[Accion, float]],
) -> tuple[list[Estado], list[Accion], float]:
    estado = INICIO
    camino = [estado]
    acciones_elegidas: list[Accion] = []
    recompensa_episodio = 0.0

    for _ in range(MAXIMO_PASOS):
        accion = accion_voraz(tabla_q, estado)
        siguiente_estado, recompensa, terminado = transicion(estado, accion)
        acciones_elegidas.append(accion)
        camino.append(siguiente_estado)
        recompensa_episodio += recompensa
        estado = siguiente_estado
        if terminado:
            return camino, acciones_elegidas, recompensa_episodio

    raise RuntimeError(
        f"La evaluación voraz no llegó a G en {MAXIMO_PASOS} pasos"
    )


def imprimir_politica(tabla_q: dict[Estado, dict[Accion, float]]) -> None:
    flechas = {"N": "^", "E": ">", "S": "v", "W": "<"}
    for fila in range(FILAS):
        casillas: list[str] = []
        for columna in range(COLUMNAS):
            estado = (fila, columna)
            if estado == INICIO:
                casillas.append(" S ")
            elif estado == META:
                casillas.append(" G ")
            elif estado in ACANTILADO:
                casillas.append(" C ")
            else:
                casillas.append(f" {flechas[accion_voraz(tabla_q, estado)]} ")
        print("".join(casillas))


def guardar_recompensas(
    recompensas_episodios: list[float], ruta: Path = ARCHIVO_SALIDA
) -> None:
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(("episodio", "recompensa", "media_movil_10"))
        for indice, recompensa in enumerate(recompensas_episodios):
            ventana = recompensas_episodios[max(0, indice - 9) : indice + 1]
            escritor.writerow(
                (
                    indice + 1,
                    f"{recompensa:g}",
                    f"{sum(ventana) / len(ventana):.2f}",
                )
            )


def comprobar_transiciones() -> None:
    assert transicion(INICIO, "N") == ((2, 0), -1.0, False)
    assert transicion(INICIO, "E") == (INICIO, -100.0, False)
    assert transicion((2, 11), "S") == (META, -1.0, True)


def principal() -> None:
    comprobar_transiciones()
    tabla_q, recompensas_episodios = entrenar(random.Random(SEMILLA))
    camino, acciones_elegidas, retorno_voraz = evaluar_voraz(tabla_q)
    guardar_recompensas(recompensas_episodios)

    print(f"alfa={ALFA}, gamma={GAMMA:g}, epsilon={EPSILON}, episodios={EPISODIOS}")
    print(f"Inicialización de Q=0, semilla={SEMILLA}, orden de desempate={', '.join(ACCIONES)}")
    print("\nPolítica voraz (N ^, E >, S v, W <):")
    imprimir_politica(tabla_q)
    print(f"\nCamino voraz: {' -> '.join(acciones_elegidas)}")
    print(f"Pasos del camino voraz: {len(acciones_elegidas)}")
    print(f"Retorno voraz: {retorno_voraz:g}")
    print(f"Recompensas de entrenamiento: {ARCHIVO_SALIDA}")
    print(
        "Recompensa media de los 500 episodios de entrenamiento: "
        f"{sum(recompensas_episodios) / len(recompensas_episodios):.2f}"
    )

    acciones_esperadas = ["N", *("E" for _ in range(11)), "S"]
    if acciones_elegidas != acciones_esperadas or retorno_voraz != -13.0:
        raise RuntimeError(
            "La ejecución con semilla fija no aprendió el camino voraz requerido de 13 pasos"
        )


if __name__ == "__main__":
    principal()
