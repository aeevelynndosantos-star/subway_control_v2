import numpy as np

import config

WRIST = 0
INDEX_MCP, INDEX_PIP, INDEX_TIP = 5, 6, 8
MIDDLE_PIP, MIDDLE_TIP = 10, 12
RING_PIP, RING_TIP = 14, 16
PINKY_PIP, PINKY_TIP = 18, 20


def _d(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def _up(p: np.ndarray, tip: int, pip: int) -> bool:
    # esticado = ponta mais longe do pulso que a articulação do meio
    return _d(p[tip], p[WRIST]) > _d(p[pip], p[WRIST])


def classify(p: np.ndarray) -> str | None:
    index = _up(p, INDEX_TIP, INDEX_PIP)
    middle = _up(p, MIDDLE_TIP, MIDDLE_PIP)
    ring = _up(p, RING_TIP, RING_PIP)
    pinky = _up(p, PINKY_TIP, PINKY_PIP)
    n = index + middle + ring + pinky  # polegar ignorado de propósito

    if n == 4:
        return "MAO_ABERTA"
    if n == 0:
        return "PUNHO"
    if index and not middle and not ring and not pinky:
        return "UM_DEDO"
    if index and middle and not ring and not pinky:
        return "DOIS_DEDOS"
    return None


def pointing_side(p: np.ndarray) -> str | None:
    dx = float(p[INDEX_TIP][0] - p[INDEX_MCP][0])
    dy = float(p[INDEX_TIP][1] - p[INDEX_MCP][1])
    if abs(dx) > config.POINT_SIDE_RATIO * abs(dy):
        return "APONTA_DIR" if dx > 0 else "APONTA_ESQ"
    return None