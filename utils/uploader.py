from threading import Event, Thread
import os
import requests
import json

from consts import CLICK_PATH, MOVE_PATH, SCROLL_PATH, UPLOAD_INTERVAL_IN_S, SEND_URL


class Uploader:
    _kill = Event()
    _upload = Event()

    def __init__(self) -> None:
        Thread(name="Uploader", daemon=True, target=self.upload_data).start()

    def __delete__(self, _) -> None:
        self._kill.set()


    def start(self) -> None:
        self._upload.set()

    def stop(self) -> None:
        self._upload.clear()


    def get_data(self, path: str) -> list[dict]:
        data = []
        for f in os.scandir(path):
            with open(f, 'r', encoding="UTF-8") as file:
                data.extend(json.load(file))
        return data

    def get_move_data(self) -> list[dict]:
        return self.get_data(MOVE_PATH)

    def get_click_data(self) -> list[dict]:
        return self.get_data(CLICK_PATH)

    def get_scroll_data(self) -> list[dict]:
        return self.get_data(SCROLL_PATH)


    def upload_data(self):
        while not self._kill.wait(UPLOAD_INTERVAL_IN_S):
            if self._upload.is_set():
                self.get_move_data()
                self.get_click_data()
                self.get_scroll_data()
                # # upload data successful -> delete files
                # try:
                #     # Daten die hochgeladen sind löschen
                #     res = requests.post(SEND_URL, json={'test': 'x'})
                #     print(res.text)
                # except:
                #     print('err: no data uploaded')
