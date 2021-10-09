# App not reziable
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '350')

# local imports
from utils.authenticator import Authenticator
from utils.logger import Logger
from utils.uploader import Uploader

# All Imports
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.behaviors import TouchBehavior
import requests

# Import UI
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup



# Create custom Login Button
class LoginButton(MDRaisedButton, TouchBehavior):
    AUTHENTICATOR = Authenticator()
    LOGGER = Logger()
    UPLOADER = Uploader()


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
        mail = self.parent.parent.ids.user.text
        if self.AUTHENTICATOR.valid_email(mail):
            self.parent.parent.ids.user.error = False
            self.parent.parent.ids.user.disabled = True
        else:
            self.parent.parent.ids.user.error = True
            return


        if self.text == "Teilnehmen":
            if not self.AUTHENTICATOR.valid_email(mail):
                return
            
            self.AUTHENTICATOR.authenticate(mail)

            # Dialog machen
            # TODO: Dialog Buttons ansteurn
            self.dialog = MDDialog(
                text="Ihre Daten werden nun aufgezeichnet. \nBitte bestätigen Sie Ihre E-Mail um mit der Aufzeichnung zu beginnen",
                buttons=[
                    MDFlatButton(
                        on_release=lambda _: self.dialog.dismiss(), text="OK", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
            self.dialog.open()

            self.start_tracking()
            self.recording_active()

        else:
            self.stop_tracking()
            self.recording_inactive()
        

# App definition
class MouseLoggerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Window.bind(on_request_close=self.on_request_close)
        return Builder.load_file('login.kv')

    # When App wnats to close
    def on_request_close(self, *args):
        Window.minimize()
        self.closeDialog()
        return True

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
