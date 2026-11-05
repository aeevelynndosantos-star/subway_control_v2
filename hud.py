import cv2
import numpy as np

import config


def _text(img, txt, org, scale=0.55, color=config.WHITE, thick=1):
    cv2.putText(img, txt, org, cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thick + 3, cv2.LINE_AA)
    cv2.putText(img, txt, org, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick, cv2.LINE_AA)


def draw_lanes(frame: np.ndarray, tip_xy, lane: int) -> None:
    h, w = frame.shape[:2]
    for frac in (config.ZONE_LEFT, config.ZONE_RIGHT):
        x = int(frac * w)
        cv2.line(frame, (x, 0), (x, h), config.GREEN, 1, cv2.LINE_AA)
    names = ("ESQ", "MEIO", "DIR")
    centers = (config.ZONE_LEFT / 2, (config.ZONE_LEFT + config.ZONE_RIGHT) / 2,
               (config.ZONE_RIGHT + 1) / 2)
    for i, c in enumerate(centers):
        on = i == lane
        _text(frame, names[i], (int(c * w) - 18, h - 20), 0.55,
              config.GREEN if on else config.WHITE, 2 if on else 1)
    if tip_xy is not None:
        cv2.circle(frame, (int(tip_xy[0]), int(tip_xy[1])), 9, config.GREEN, -1, cv2.LINE_AA)


def draw_action(frame: np.ndarray, action: str | None) -> None:
    if not action:
        return
    w = frame.shape[1]
    (tw, _), _ = cv2.getTextSize(action, cv2.FONT_HERSHEY_SIMPLEX, 1.4, 3)
    _text(frame, action, (w - tw - 20, 60), 1.4, config.RED, 3)


def draw_paused(frame: np.ndarray) -> None:
    _text(frame, "PAUSADO", (10, 30), 0.8, config.RED, 2)
