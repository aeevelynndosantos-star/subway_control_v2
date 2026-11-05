import cv2
import numpy as np

import config


class HandTracker:
    def __init__(self):
        import mediapipe as mp

        if not hasattr(mp, "solutions"):
            raise SystemExit(
                "Esta versão do MediaPipe não tem a API 'solutions'.\n"
                "Instale: py -3.12 -m pip install mediapipe==0.10.21"
            )
        self._hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=config.DETECTION_CONFIDENCE,
            min_tracking_confidence=config.TRACKING_CONFIDENCE,
        )
        self._draw = mp.solutions.drawing_utils
        self._conn = mp.solutions.hands.HAND_CONNECTIONS
        self._raw = None

    def process(self, frame_bgr: np.ndarray) -> np.ndarray | None:
        h, w = frame_bgr.shape[:2]
        res = self._hands.process(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
        self._raw = res.multi_hand_landmarks
        if not self._raw:
            return None
        lm = self._raw[0].landmark
        return np.array([[p.x * w, p.y * h] for p in lm], dtype=np.float32)

    def draw_skeleton(self, frame: np.ndarray) -> None:
        for lm in self._raw or []:
            self._draw.draw_landmarks(frame, lm, self._conn)

    def close(self) -> None:
        self._hands.close()