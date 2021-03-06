from pathlib import Path

DELETE_UPLOADED_DATA = True

MS_TO_NS = 1e6
NS_TO_MS = 1e-6

GB_TO_B = 1e9


RECORD_INTERVAL_IN_MS = 16
SAVE_INTERVAL_IN_S = 30


FOLDER_PATH = f"{Path.home()}/mouseDynamics"
CONFIG_PATH = f"{FOLDER_PATH}/config"
PARTIC_PATH = f"{FOLDER_PATH}/participate"
MOVE_PATH = f"{FOLDER_PATH}/move"
CLICK_PATH = f"{FOLDER_PATH}/click"
SCROLL_PATH = f"{FOLDER_PATH}/scroll"


UPLOAD_INTERVAL_IN_S = 30

API_VERSION = "v1"
BASE_URL = f"https://api.mouselogger.de/{API_VERSION}"
AUTH_URL = f"{BASE_URL}/auth"

MOVE_URL = f"{BASE_URL}/movedata"
CLICK_URL = f"{BASE_URL}/clickdata"
SCROLL_URL = f"{BASE_URL}/scrolldata"




AUTHENTICATION_INTERVAL_IN_S = 10