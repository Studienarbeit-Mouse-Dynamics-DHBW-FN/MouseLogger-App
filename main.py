# App not reziable
from kivy.config import Config
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '450')
Config.set('graphics', 'resizable', False)
Config.set('kivy', 'window_icon', 'favicon.ico')

# local imports
from utils.authenticator import Authenticator
from utils.logger import Logger
from utils.uploader import Uploader
from layout import LAYOUT
import os
import json

# All Imports
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.behaviors import TouchBehavior

# Import UI
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window

from consts import PARTIC_PATH, FOLDER_PATH

AUTHENTICATOR = Authenticator()

# Create custom Login Button
class LoginButton(MDRaisedButton, TouchBehavior):
    LOGGER = Logger()
    UPLOADER = Uploader(AUTHENTICATOR)

    _running = False


    def start_tracking(self) -> None:
        """start tracking and schedule tasks"""
        self.LOGGER.start()
        self.UPLOADER.start()

    def stop_tracking(self) -> None:
        """stop tracking and stop scheduled tasks"""
        self.LOGGER.stop()
        self.UPLOADER.stop()


    def recording_active(self) -> None:
        """change UI to reflect active recording"""
        self.text = "Teilnahme zurückziehen"
        self.parent.parent.ids.status_indicator.color = 0,255,0,1
        self.parent.parent.ids.data_status.text_color = 0,1,0,1
        self.parent.parent.ids.data_status.text = "Ihre Daten werden aufgenommen"

    def recording_inactive(self) -> None:
        """change UI to reflect inactive recording"""
        self.text = "Teilnehmen"
        self.parent.parent.ids.status_indicator.color = 255,0,0,1
        self.parent.parent.ids.data_status.text_color = 1,0,0,1
        self.parent.parent.ids.data_status.text = "Keine Daten werden aufgenommen"


    def on_press(self) -> None:
        if AUTHENTICATOR.is_authenticated():
            self.parent.parent.ids["user"].text = AUTHENTICATOR.get_mail()
            self.parent.parent.ids["user"].disabled = True

            if self._running:
                self.stop_tracking()
                self.recording_inactive()
                self._running = False
                return

            self.start_tracking()
            self.recording_active()
            self._running = True
            return

        requested_mail = self.parent.parent.ids["user"].text
        if not AUTHENTICATOR.valid_email(requested_mail):
            self.parent.parent.ids["user"].error = True
            return
        self.parent.parent.ids["user"].error = False

        device_type = self.parent.parent.ids["device"].text
        if not device_type:
            self.parent.parent.ids["device"].error = True
            return
        self.parent.parent.ids["device"].error = False

        AUTHENTICATOR.authenticate(requested_mail, device_type)
        it = MDDialog(
            text="Ihre E-Mail-Adresse wurde erfolgreich übermittelt.\n\nBitte identifizieren Sie sich in der erhaltenen E-Mail und betätigen diesen Kopf erneut.",
            buttons=[
                MDFlatButton(
                    on_release=lambda _: it.dismiss(), text="OK", text_color=self.theme_cls.primary_color
                ),
            ],
        )
        it.open()


# App definition
class MouseLoggerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        # Window.bind(on_request_close=self.on_request_close)
        return Builder.load_string(LAYOUT)

    def on_start(self):
        """if device already authenticated set mail"""
        if AUTHENTICATOR.is_authenticated():
            self.root.ids["user"].text = AUTHENTICATOR.get_mail()
            self.root.ids["user"].disabled = True
            self.root.ids["device"].text = AUTHENTICATOR.get_device()
            self.root.ids["device"].disabled = True

            # Check if user want to use app always
            os.makedirs(FOLDER_PATH, exist_ok=True)
            if os.path.exists(PARTIC_PATH):
                with open(f"{PARTIC_PATH}", 'r', encoding="UTF-8") as config_file:
                    data = json.load(config_file)
                    part = data["participate"]
                    self.root.ids["parti"].active = part
                    
                    if part:
                        self.root.ids["btn"].on_press()

        return super().on_start()

    # Change Value of Checkbox
    def on_checkbox_active(self, checkbox, value):
        # Save state
        os.makedirs(FOLDER_PATH, exist_ok=True)
        with open(PARTIC_PATH, 'w', encoding="UTF-8") as file:
            file.write(json.dumps(dict(participate=value)))


    # When App wnats to close
    # def on_request_close(self, *args):
    #     Window.minimize()
    #     self.closeDialog()
    #     return True

    # Verify Close dialog
    def closeDialog(self):
        self.dialog = MDDialog(
            text="Möchten Sie die Applikation wirklich schließen?",
            buttons=[
                MDFlatButton(
                  on_release=lambda _: self.dialog.dismiss(), text="Abbrechen", text_color=self.theme_cls.primary_color
                ),
                MDRaisedButton(
                    on_release=self.stop, text="Schließen"
                ),
            ],
        )
        self.dialog.open()

# Run App
MouseLoggerApp().run()
