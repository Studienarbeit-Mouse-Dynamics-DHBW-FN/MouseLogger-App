import time
from pathlib import Path
from threading import Event, Thread
import os
import json
from pynput.mouse import Listener, Button

from utils.directions import Direction


MS_TO_NS = 1e6
NS_TO_MS = 1e-6

SAVE_INTERVALS_IN_S = 5


class Logger:
    _kill = Event()

    _LISTENER: Listener
    _listen = Event()
    _dump = Event()

    _RECORD_INTERVAL_NS = 25 * MS_TO_NS

    _movement_data = []
    _lastMovementRecord = 0

    _click_data = []
    _click_times = dict()
    _click_positions = dict()

    _scroll_data = []


    def dump(self, filename: str, data: list) -> None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding="UTF-8") as file:
            file.write(json.dumps(data, indent=2))

    def dump_data(self) -> None:
        while not self._kill.wait(SAVE_INTERVALS_IN_S):
            if self._dump.is_set():
                self.dump(f'{Path.home()}/mouseDynamics/move/{int(time.time_ns() * NS_TO_MS)}.json', self._movement_data)
                self._movement_data = []
                self.dump(f'{Path.home()}/mouseDynamics/click/{int(time.time_ns() * NS_TO_MS)}.json', self._click_data)
                self._click_data = []
                self.dump(f'{Path.home()}/mouseDynamics/scroll/{int(time.time_ns() * NS_TO_MS)}.json', self._scroll_data)
                self._scroll_data = []


    def __init__(self) -> None:
        Thread(name="Dumper", daemon=True, target=self.dump_data).start()

        self._LISTENER = Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self._LISTENER.start()
        self._LISTENER.wait()

    def __delete__(self, _) -> None:
        self._kill.set()
        self._LISTENER.stop()


    def start(self) -> None:
        self._listen.set()
        self._dump.set()

    def stop(self) -> None:
        self._listen.clear()
        self._dump.clear()


    def on_move(self, x: int, y: int) -> None:
        """record movement in set timesteps"""
        if not self._listen:
            return
        if self._lastMovementRecord + self._RECORD_INTERVAL_NS <= time.time_ns():
            self._movement_data.append(dict(
                timestamp=int(time.time_ns() * NS_TO_MS),
                position=dict(x=x, y=y)))
            self._lastMovementRecord = time.time_ns()

    def on_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        """record clicks with clicked button, time, duration and positions"""
        if not self._listen:
            return
        if pressed:
            self._click_times[button.name] = time.time_ns()
            self._click_positions[button.name] = (x, y)
        else:
            try:
                self._click_data.append(dict(
                    startTime=int(self._click_times[button.name] * NS_TO_MS),
                    duration=int((time.time_ns()-self._click_times[button.name]) * NS_TO_MS),
                    button=button.name,
                    startPosition=dict(x=self._click_positions[button.name][0], y=self._click_positions[button.name][1]),
                    endPosition=dict(x=x, y=y)))
            except:
                pass

    def on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """record scrolling with time, position and direction"""
        if not self._listen:
            return
        self._scroll_data.append(dict(
            timestamp=int(time.time_ns() * NS_TO_MS),
            position=dict(x=x, y=y),
            direction=Direction((dx, dy)).name))



if __name__ == '__main__':
    logger = Logger()
    logger.start()
    input()
    logger.stop()
