# App not reziable
from kivy.config import Config
Config.set('graphics', 'resizable', False)

# local imports
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



# Send and verify Email
def sendUsername(username):
    url = 'http://localhost:3000/sendmail'
    try:
        res = requests.post(url, json={'email': username})
        print(res.text)
    except:
        print('err: no username send')

# Create custom Login Button
class LoginButton(MDRaisedButton, TouchBehavior):

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


    def on_press(self):
        # Check if text is E-Mail
        email = self.parent.parent.ids.user.text # E-Mail of User
        # REGEX: [^@]+@[^@]+\.[^@]+
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print('email wrong')
            self.parent.parent.ids.user.error = True
            
            return
        else:
            self.parent.parent.ids.user.error = False
            self.parent.parent.ids.user.disabled = True

        if self.text == "Teilnehmen":


            
            print(email)
            if email == '':
                return
            sendUsername(email)
            # Identify E-Mail

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

            # Update UI
            self.text = "Teilnahme beenden"
            self.parent.parent.ids.status_indicator.color = 0,255,0,1 
            self.parent.parent.ids.data_status.text_color = 0,1,0,1
            self.parent.parent.ids.data_status.text = "Ihre Daten werden aufgenommen"

            self.start_tracking()

        else:
            self.text = "Teilnehmen"
            self.stop_tracking()

            # Update UI
            self.parent.parent.ids.status_indicator.color = 255,0,0,1
            self.parent.parent.ids.data_status.text_color = 1,0,0,1
            self.parent.parent.ids.data_status.text = "Keine Daten werden aufgenommen"
            self.parent.parent.ids.user.disabled = False
        

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
