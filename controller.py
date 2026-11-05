import config


class GestureDebouncer:

    def __init__(self):
        self._cand = None
        self._count = 0
        self._fired = False
        self._cool = 0

    def update(self, gesture: str | None) -> str | None:
        if self._cool > 0:
            self._cool -= 1
        if gesture != self._cand:
            self._cand, self._count, self._fired = gesture, 0, False
        if gesture is None:
            return None

        self._count += 1
        if self._count >= config.STABLE_FRAMES and self._cool == 0:
            if not self._fired:
                self._fired = True
                self._cool = config.COOLDOWN_FRAMES
                return gesture
            if (config.REPEAT_FRAMES > 0 and
                    (self._count - config.STABLE_FRAMES) % config.REPEAT_FRAMES == 0):
                self._cool = config.COOLDOWN_FRAMES
                return gesture
        return None


class LaneFollower:

    def __init__(self):
        self.recenter()
        self._cool = 0

    def recenter(self) -> None:
        self.lane = config.START_LANE
        self.target = config.START_LANE
        self._cand, self._cand_n, self._synced = self.target, 0, True

    @staticmethod
    def zone(x: float) -> int:
        if x < config.ZONE_LEFT:
            return 0
        if x > config.ZONE_RIGHT:
            return 2
        return 1

    def update(self, x: float | None) -> str | None:
        if self._cool > 0:
            self._cool -= 1
        if x is None:
            self._cand_n = 0
            return None

        z = self.zone(x)
        if z == self.target:
            self._cand, self._cand_n = z, 0
        else:
            self._cand_n = self._cand_n + 1 if z == self._cand else 1
            self._cand = z
            if self._cand_n >= config.ZONE_STABLE_FRAMES:
                self.target, self._cand_n, self._synced = z, 0, False

        if self._cool > 0:
            return None
        if self.lane != self.target:
            step = 1 if self.target > self.lane else -1
            self.lane += step
            self._cool = config.LANE_STEP_COOLDOWN
            return "right" if step > 0 else "left"
        if config.SYNC_AT_EDGES and not self._synced and self.target in (0, 2):
            self._synced = True
            self._cool = config.LANE_STEP_COOLDOWN
            return "left" if self.target == 0 else "right"
        self._synced = True
        return None


class KeySender:

    def __init__(self):
        from pynput.keyboard import Controller, Key

        self._kb = Controller()
        self._special = {"up": Key.up, "down": Key.down, "left": Key.left,
                         "right": Key.right, "space": Key.space}

    def tap(self, name: str) -> None:
        key = self._special.get(name, name)
        self._kb.press(key)
        self._kb.release(key)


class DryRunSender:

    def tap(self, name: str) -> None:
        print(f"[tecla] {name}")