import os
import json
import time

from threading import Event, Thread
from pynput.mouse import Listener, Button
from sentry_sdk import capture_exception

from utils.directions import Direction
from consts import CLICK_PATH, GB_TO_B, MOVE_PATH, MS_TO_NS, NS_TO_MS, SAVE_INTERVAL_IN_S, RECORD_INTERVAL_IN_MS, SCROLL_PATH



class Logger:
    _kill = Event()

    _LISTENER: Listener
    _listen = Event()
    _dump = Event()

    _movement_data = []
    _last_movement_record = 0

    _click_data = []
    _click_times = dict()
    _click_positions = dict()

    _scroll_data = []


    def __init__(self) -> None:
        Thread(name="Dumper", daemon=True, target=self.execute_all).start()

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
        if self._last_movement_record + (RECORD_INTERVAL_IN_MS * MS_TO_NS) <= time.time_ns():
            self._movement_data.append(dict(
                timestamp=int(time.time_ns() * NS_TO_MS),
                position=dict(x=x, y=y)))
            self._last_movement_record = time.time_ns()

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
            except Exception as e:
                capture_exception(e)
            except:
                pass

    def on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        """record scrolling with time, position and direction"""
        if not self._listen:
            return
        self._scroll_data.append(dict(
            timestamp=int(time.time_ns() * NS_TO_MS),
            position=dict(x=x, y=y),
            direction=Direction.getDirection(dx, dy).name))


    def directory_sized(self, path: str, size: int) -> None:
        while sum([os.stat(it).st_size for it in os.scandir(path)]) > size*GB_TO_B:
            oldest_file = min(os.scandir(path), key=os.path.getctime)
            os.remove(os.path.abspath(oldest_file))

    def dump(self, path: str, data: list) -> None:
        with open(f"{path}/{int(time.time_ns() * NS_TO_MS)}.json", 'w', encoding="UTF-8") as file:
            file.write(json.dumps(data))

    def execute(self, path: str, max_size_in_gb: int, data: list) -> list:
        os.makedirs(path, exist_ok=True)
        self.directory_sized(path, max_size_in_gb)
        self.dump(path, data)
        data.clear()

    def execute_all(self) -> None:
        while not self._kill.wait(SAVE_INTERVAL_IN_S):
            if self._dump.is_set():
                try:
                    self.execute(MOVE_PATH, 3, self._movement_data)
                    self.execute(CLICK_PATH, 1, self._click_data)
                    self.execute(SCROLL_PATH, 1, self._scroll_data)
                finally:
                    pass
