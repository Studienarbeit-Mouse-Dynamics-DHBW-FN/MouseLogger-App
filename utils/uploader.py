from threading import Event, Thread
import os
import requests
import json
from utils.authenticator import Authenticator
from sentry_sdk import capture_exception

from consts import CLICK_PATH, CLICK_URL, DELETE_UPLOADED_DATA, MOVE_PATH, SCROLL_PATH, SCROLL_URL, UPLOAD_INTERVAL_IN_S, MOVE_URL


class Uploader:
    _kill = Event()
    _upload = Event()

    _authenticator: Authenticator

    def __init__(self, auth: Authenticator) -> None:
        self._authenticator = auth
        Thread(name="Uploader", daemon=True, target=self.upload_data).start()

    def __delete__(self, _) -> None:
        self._kill.set()


    def start(self) -> None:
        self._upload.set()

    def stop(self) -> None:
        self._upload.clear()


    def upload_single_data(self, path: str, url: str) -> None:
        for file in os.scandir(path):
            try:
                file_data = open(file, 'r', encoding="UTF-8").read()
                if file_data == "" or file_data == "\n" or file_data == "[]" or file_data == "[]\n":
                    os.remove(file)
                    continue

                data = json.loads(file_data)
                response = requests.post(url, json=dict(mac=self._authenticator.get_mac(), data=data), timeout=15)
                if response.ok and DELETE_UPLOADED_DATA:
                    os.remove(file)
                response.close()
            except Exception as e:
                capture_exception(e)

    def upload_data(self):
        while not self._kill.wait(UPLOAD_INTERVAL_IN_S):
            if self._upload.is_set():
                try:
                    self.upload_single_data(MOVE_PATH, MOVE_URL)
                    self.upload_single_data(CLICK_PATH, CLICK_URL)
                    self.upload_single_data(SCROLL_PATH, SCROLL_URL)
                except Exception as e:
                    capture_exception(e)