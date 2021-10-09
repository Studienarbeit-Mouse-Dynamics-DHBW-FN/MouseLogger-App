from pathlib import Path

MS_TO_NS = 1e6
NS_TO_MS = 1e-6

GB_TO_B = 1e9


RECORD_INTERVAL_IN_MS = 25
SAVE_INTERVAL_IN_S = 5


FOLDER_PATH = f"{Path.home()}/mouseDynamics"
CONFIG_PATH = f"{FOLDER_PATH}/config"
MOVE_PATH = f"{FOLDER_PATH}/move"
CLICK_PATH = f"{FOLDER_PATH}/click"
SCROLL_PATH = f"{FOLDER_PATH}/scroll"


UPLOAD_INTERVAL_IN_S = 5

BASE_URL = "http://localhost:3000"
AUTH_URL = f"{BASE_URL}/auth"
SEND_URL = f"{BASE_URL}/send"


AUTHENTICATION_INTERVAL_IN_S = 15