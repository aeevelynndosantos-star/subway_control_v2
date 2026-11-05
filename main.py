import threading

import cv2

import config
import hud
from controller import DryRunSender, GestureDebouncer, KeySender, LaneFollower
from gestures import classify, pointing_side
from hand_tracker import HandTracker

ACTION_SHOW_FRAMES = 15
LANE_LABEL = {"left": "ESQUERDA", "right": "DIREITA"}


class Hotkeys:

    def __init__(self):
        self.quit = threading.Event()
        self.recenter = threading.Event()
        self.paused = False
        try:
            from pynput import keyboard
            self._listener = keyboard.Listener(on_press=self._on_press)
            self._listener.start()
        except Exception:
            self._listener = None

    def _on_press(self, key) -> None:
        name = getattr(key, "name", None)
        if name == config.HOTKEY_QUIT:
            self.quit.set()
        elif name == config.HOTKEY_PAUSE:
            self.paused = not self.paused
        elif name == config.HOTKEY_RECENTER:
            self.recenter.set()

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()


def main() -> None:
    modes = ("apontar_posicao", "apontar_direcao", "gestos")
    if config.MODE not in modes:
        raise SystemExit(f"MODE inválido: {config.MODE!r}. Use: {list(modes)}")

    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    if not cap.isOpened():
        raise SystemExit(f"Não consegui abrir a câmera {config.CAMERA_INDEX}. "
                         "Tente outro CAMERA_INDEX em config.py.")

    try:
        sender = KeySender()
    except Exception as e:
        print(f"[AVISO] pynput indisponível ({e}). Instale: py -3.12 -m pip install pynput")
        sender = DryRunSender()

    tracker, debouncer, hotkeys = HandTracker(), GestureDebouncer(), Hotkeys()
    lanes = LaneFollower()
    shown_action, shown_left = None, 0

    cv2.namedWindow(config.WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(config.WINDOW_NAME, *config.WINDOW_SIZE)
    if config.WINDOW_ALWAYS_ON_TOP:
        try:
            cv2.setWindowProperty(config.WINDOW_NAME, cv2.WND_PROP_TOPMOST, 1)
        except cv2.error:
            pass

    try:
        while not hotkeys.quit.is_set():
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            if hotkeys.recenter.is_set():
                hotkeys.recenter.clear()
                lanes.recenter()

            pts = tracker.process(frame)
            gesture = classify(pts) if pts is not None else None
            if hotkeys.paused:
                gesture = None

            tip_xy = None
            action_key = None

            if config.MODE == "apontar_posicao":
                pointing = gesture == "UM_DEDO"
                tip_xy = pts[8] if pointing else None
                action_key = lanes.update(tip_xy[0] / w if pointing else None)
                if action_key:
                    sender.tap(action_key)
                    shown_action, shown_left = LANE_LABEL[action_key], ACTION_SHOW_FRAMES
                other = gesture if gesture in ("MAO_ABERTA", "PUNHO") else None
                fired = debouncer.update(other)
            else:
                if config.MODE == "apontar_direcao":
                    if gesture == "UM_DEDO":
                        gesture = pointing_side(pts)
                    elif gesture == "DOIS_DEDOS":
                        gesture = None
                fired = debouncer.update(gesture)

            if fired:
                label, key = config.ACTIONS[fired]
                sender.tap(key)
                shown_action, shown_left = label, ACTION_SHOW_FRAMES

            tracker.draw_skeleton(frame)
            if config.MODE == "apontar_posicao":
                hud.draw_lanes(frame, tip_xy, lanes.lane)
            if shown_left > 0:
                hud.draw_action(frame, shown_action)
                shown_left -= 1
            if hotkeys.paused:
                hud.draw_paused(frame)

            cv2.imshow(config.WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                break
    finally:
        hotkeys.stop()
        tracker.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()