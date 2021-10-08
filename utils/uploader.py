from threading import Event, Thread
import requests

from consts import UPLOAD_INTERVALS_IN_S, SEND_URL


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


    def upload_data(self):
        while not self._kill.wait(UPLOAD_INTERVALS_IN_S):
            if self._upload.is_set():
                try:
                    # Daten die hochgeladen sind löschen
                    res = requests.post(SEND_URL, json={'test': 'x'})
                    print(res.text)
                except:
                    print('err: no data uploaded')
