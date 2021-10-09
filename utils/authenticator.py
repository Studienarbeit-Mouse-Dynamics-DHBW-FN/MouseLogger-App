import re
import os
import json
import requests
from threading import Event, Thread
from getmac import get_mac_address as mac


from consts import AUTH_URL, AUTHENTICATION_INTERVAL_IN_S, CONFIG_PATH, FOLDER_PATH

class Authenticator:
    _authenticated = False
    _mail = ""

    _kill = Event()
    _authenticate = Event()


    def __init__(self) -> None:
        """checks if device is authenticated else start auth thread"""
        os.makedirs(FOLDER_PATH, exist_ok=True)
        if os.path.exists(CONFIG_PATH):
            with open(f"{CONFIG_PATH}", 'r', encoding="UTF-8") as config_file:
                data = json.load(config_file)
                self._mail = data["mail"]
                self._authenticated = True
            return

        Thread(name=Authenticator, daemon=True, target=self.auth_loop)

    def __delete__(self, _) -> None:
        self._kill.set()


    def is_authenticated(self) -> bool:
        return self._authenticated
    
    def get_mail(self) -> bool:
        return self._mail


    def valid_email(self, mail: str) -> bool:
        """return wheter the give mail matches a mail pattern"""
        return re.match(r"[^@]+@[^@]+\.[^@]+", mail)

    def authenticate(self, mail: str) -> bool:
        self._mail = mail
        self._authenticate.set()


    def save_authentication(self) -> None:
        self._authenticated = True
        self._authenticate.clear()
        self._kill.set()
        os.makedirs(FOLDER_PATH, exist_ok=True)
        with open(CONFIG_PATH, 'w', encoding="UTF-8") as file:
            file.write(json.dumps(dict(mail=self._mail)))


    def auth_loop(self) -> None:
        while not self._kill.wait(AUTHENTICATION_INTERVAL_IN_S):
            if self._authenticate.is_set():
                try:
                    response = requests.post(AUTH_URL, json=dict(mail=self._mail, id=mac()))
                    if response.json()["is_verified"]:
                        self.save_authentication()
                finally:
                    pass
