# App not reziable
from kivy.config import Config
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '450')
Config.set('graphics', 'resizable', False)
Config.set('kivy','window_icon','icon_red.png')

# local imports
from utils.authenticator import Authenticator
from utils.logger import Logger
from utils.uploader import Uploader

# All Imports
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.behaviors import TouchBehavior

# Import UI
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window


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
                Window.set_icon("icon_red.png")
                return

            self.start_tracking()
            self.recording_active()
            self._running = True
            Window.set_icon("icon_green.png")
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


# App definition
class MouseLoggerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Window.bind(on_request_close=self.on_request_close)
        return Builder.load_string(""" 
        
#:kivy 1.0.9

MDScreen:
        MDCard: 
                size_hint: None, None
                size: 400, 250
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                elevantion: 10
                padding: 25
                spacing: 25
                orientation: "vertical"

                MDLabel:
                        id: welcome_label
                        text: "MouseLogger"
                        font_size: 40
                        halign: 'center'
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding_y: 15

                MDTextField:
                        id: user
                        hint_text: "E-Mail"
                        icon_right: "email"
                        width: 200
                        font_size: 18
                        pos_hint: {"center_x": 0.5}
                        helper_text: "korrektes E-Mail-Format erforderlich"
                        helper_text_mode: "on_error"

                MDTextField:
                        id: device
                        hint_text: "Device"
                        width: 200
                        font_size: 18
                        pos_hint: {"center_x": 0.5}
                        helper_text: "Typ des genutzten Gerätes erforderlich (z.B. Laptop)"
                        helper_text_mode: "on_error"

                LoginButton:
                        id: btn
                        text: "Teilnehmen"
                        color: 0,255,0,1
                        pos_hint: {"center_x": .5, "center_y": .5}
                

        MDProgressBar:
                id: status_indicator
                value: 100
                color: 255,0,0,1
                halign: 'center'
                size_hint_y: None
                padding_y: 15

        MDLabel:
                id: data_status
                text: "Keine Daten werden aufgenommen"
                font_size: 10
                halign: 'center'
                size_hint_y: None
                height: self.texture_size[1]
                padding_y: 15
                theme_text_color: "Custom"
                text_color: 1, 0, 0, 1


# Wenn läuft = X = minimieren
# Wenn nicht läuft schließt app
        
        """)
        # return Builder.load_file('login.kv')

    def on_start(self):
        """if device already authenticated set mail"""
        if AUTHENTICATOR.is_authenticated():
            self.root.ids["user"].text = AUTHENTICATOR.get_mail()
            self.root.ids["user"].disabled = True
            self.root.ids["device"].text = AUTHENTICATOR.get_device()
            self.root.ids["device"].disabled = True
        return super().on_start()

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
