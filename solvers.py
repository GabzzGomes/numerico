from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

import importlib
import numpy as np

Q1 = importlib.import_module("T1-Q3")
Q2 = importlib.import_module("T3-Q2")
Q3 = importlib.import_module("T4-Q1")
Circuit = importlib.import_module("T2-Q3")


@dataclass
class Q1Result:
    quantidades_minas: np.ndarray
    necessidades: np.ndarray
    obtido: np.ndarray
    erros: np.ndarray


@dataclass
class Q2Result:
    pontos_selecionados: List[Tuple[float, float]]
    valor_lagrange: float
    valor_newton: float
    diferenca: float


@dataclass
class Q3Result:
    distancias: List[float]
    profundidades: List[float]
    espacamento: float
    area_trapezio: float
    area_simpson: float
    diferenca: float
    diferenca_percentual: float


@dataclass
class CircuitResult:
    correntes: np.ndarray
    matriz: np.ndarray
    termos_independentes: np.ndarray


def solve_q1(necessidades: Sequence[float], composicao: Sequence[Sequence[float]]) -> Q1Result:
    """Resolve o sistema da Questão 1 e retorna métricas essenciais."""
    A, b = Q1.criar_sistema_mineracao(list(necessidades), [list(row) for row in composicao])
    solucao = Q1.eliminacao_gaussiana(A, b, mostrar_passos=False)
    obtido = A @ solucao
    erros = obtido - b
    return Q1Result(quantidades_minas=solucao, necessidades=b, obtido=obtido, erros=erros)


def solve_q2(
    x_pontos: Sequence[float],
    y_pontos: Sequence[float],
    x_alvo: float,
    grau: int,
) -> Q2Result:
    """Executa os métodos de Lagrange e Newton da Questão 2."""
    if len(x_pontos) != len(y_pontos):
        raise ValueError("As listas de x e y devem ter o mesmo tamanho.")
    if len(x_pontos) == 0:
        raise ValueError("Forneça ao menos um ponto.")
    if grau < 0:
        raise ValueError("O grau do polinômio deve ser não negativo.")
    if grau + 1 > len(x_pontos):
        raise ValueError("Número de pontos insuficiente para o grau desejado.")

    x_sel, y_sel = Q2.escolher_pontos_centralizados(list(x_pontos), list(y_pontos), x_alvo, grau)
    valor_lagrange = Q2.interpolacao_lagrange(x_sel, y_sel, x_alvo, mostrar_passos=False)
    valor_newton = Q2.interpolacao_newton(x_sel, y_sel, x_alvo, mostrar_passos=False)

    pontos = list(zip(x_sel, y_sel))
    diferenca = abs(valor_lagrange - valor_newton)

    return Q2Result(
        pontos_selecionados=pontos,
        valor_lagrange=valor_lagrange,
        valor_newton=valor_newton,
        diferenca=diferenca,
    )


def _infer_espacamento(distancias: Sequence[float]) -> float:
    if len(distancias) < 2:
        raise ValueError("São necessários pelo menos dois pontos para medir o espaçamento.")
    diffs = np.diff(distancias)
    if not np.allclose(diffs, diffs[0], rtol=1e-3, atol=1e-6):
        raise ValueError("Os pontos não estão igualmente espaçados.")
    return float(diffs[0])


def solve_q3(
    profundidades: Sequence[float],
    espacamento: float | None = None,
    distancias: Sequence[float] | None = None,
) -> Q3Result:
    """Calcula as áreas pelas regras de Trapézio e Simpson para a Questão 3."""
    if len(profundidades) < 2:
        raise ValueError("Forneça pelo menos dois pontos de profundidade.")
    if distancias is not None and len(distancias) != len(profundidades):
        raise ValueError("Listas de distâncias e profundidades devem ter o mesmo tamanho.")

    if espacamento is None:
        if distancias is None:
            raise ValueError("Informe o espaçamento ou a lista de distâncias acumuladas.")
        espacamento = _infer_espacamento(distancias)
    elif espacamento <= 0:
        raise ValueError("O espaçamento deve ser positivo.")

    if distancias is None:
        distancias = [i * espacamento for i in range(len(profundidades))]
    else:
        _ = _infer_espacamento(distancias)

    profundidade_arr = np.array(profundidades, dtype=float)
    area_trap = Q3.regra_trapezio(profundidade_arr, float(espacamento))
    area_simp = Q3.regra_simpson_1_3(profundidade_arr, float(espacamento), mostrar_aviso=False)
    diferenca = abs(area_trap - area_simp)
    diferenca_percentual = diferenca / area_simp * 100 if area_simp != 0 else 0.0

    return Q3Result(
        distancias=list(map(float, distancias)),
        profundidades=list(map(float, profundidades)),
        espacamento=float(espacamento),
        area_trapezio=float(area_trap),
        area_simpson=float(area_simp),
        diferenca=float(diferenca),
        diferenca_percentual=float(diferenca_percentual),
    )


def solve_circuit(
    matriz: Sequence[Sequence[float]],
    precision: float = 0.0001,
) -> CircuitResult:
    """Resolve o circuito usando Gauss-Seidel."""
    matriz_np = np.array(matriz, dtype=float)
    rows, cols = matriz_np.shape

    solucao = Circuit.gauss_sidel(matriz_np, rows, cols, precision=precision)

    A = matriz_np[:, :-1]
    b = matriz_np[:, -1]

    return CircuitResult(
        correntes=solucao,
        matriz=A,
        termos_independentes=b,
    )
