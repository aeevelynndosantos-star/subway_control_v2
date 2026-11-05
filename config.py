CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
WINDOW_NAME = "Gesture Control"
WINDOW_SIZE = (480, 360)
WINDOW_ALWAYS_ON_TOP = True

DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.6

MODE = "apontar_posicao"

ZONE_LEFT = 0.40
ZONE_RIGHT = 0.60
ZONE_STABLE_FRAMES = 3
LANE_STEP_COOLDOWN = 6
START_LANE = 1
SYNC_AT_EDGES = False

POINT_SIDE_RATIO = 1.2

ACTIONS = {
    "UM_DEDO":     ("ESQUERDA", "left"),
    "DOIS_DEDOS":  ("DIREITA",  "right"),
    "APONTA_ESQ":  ("ESQUERDA", "left"),
    "APONTA_DIR":  ("DIREITA",  "right"),
    "MAO_ABERTA":  ("PULAR",    "up"),
    "PUNHO":       ("ROLAR",    "down"),
}

LEGENDS = {
    "gestos": [
        ("UM_DEDO",    "1 dedo",        "ESQUERDA"),
        ("DOIS_DEDOS", "2 dedos",       "DIREITA"),
        ("MAO_ABERTA", "Mao aberta",    "PULAR"),
        ("PUNHO",      "Punho fechado", "ROLAR"),
    ],
    "apontar_posicao": [
        ("UM_DEDO",    "Dedo apontando", "SEGUE O DEDO"),
        ("MAO_ABERTA", "Mao aberta",     "PULAR"),
        ("PUNHO",      "Punho fechado",  "ROLAR"),
    ],
    "apontar_direcao": [
        ("APONTA_ESQ", "Dedo p/ esquerda", "ESQUERDA"),
        ("APONTA_DIR", "Dedo p/ direita",  "DIREITA"),
        ("MAO_ABERTA", "Mao aberta",       "PULAR"),
        ("PUNHO",      "Punho fechado",    "ROLAR"),
    ],
}

STABLE_FRAMES = 3
COOLDOWN_FRAMES = 8
REPEAT_FRAMES = 0
HOTKEY_QUIT = "f8"
HOTKEY_PAUSE = "f9"
HOTKEY_RECENTER = "f10"

GREEN = (80, 255, 90)
RED = (60, 60, 255)
WHITE = (255, 255, 255)