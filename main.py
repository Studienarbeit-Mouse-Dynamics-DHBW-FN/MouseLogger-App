# App not reziable
from kivy.config import Config
Config.set('graphics', 'resizable', False)

# All Imports
from kivymd.app import MDApp
from kivy.lang import Builder
import time
from pynput import mouse
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.behaviors import TouchBehavior
import threading
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


# Global Vars
isActive = False
x = []
y = []

# Get Cursor Data
def getData():
    global isActive
    isActive = True
    controller = mouse.Controller()
    current_position = controller.position
    while isActive:
        if current_position != controller.position:
            # Uncomment for testing
            # print(time.time_ns(), controller.position)
            current_position = controller.position
            x.append(controller.position[0])
            y.append(controller.position[1])
        time.sleep(.0025)
    print(x,y)

# Upload Cursor Data
def uploadData():
    url = 'http://localhost:3000/senddata'
    res = requests.post(url, json={'test': 'x'})
    print(res.text)

# Send and verify Email
def sendUsername(username):
    url = 'http://localhost:3000/sendmail'
    res = requests.post(url, json={'email': username})
    print(res.text)


# Create custom Login Button
class LoginButton(MDRaisedButton, TouchBehavior):
    def on_press(self, *args):
        print("touched")
        if self.text == "Teilnehmen":


            email = self.parent.parent.ids.user.text # E-Mail of User
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
                        text="Abbrechen", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
            self.dialog.open()

            # Update UI
            self.text = "Teilnahme beenden"
            self.parent.parent.ids.status_indicator.color = 0,255,0,1 
            self.parent.parent.ids.data_status.text_color = 0,1,0,1
            self.parent.parent.ids.data_status.text = "Ihre Daten werden aufgenommen"

            # Start get Data
            thread = threading.Thread(target=getData, args=())  # Create thread
            thread.daemon = True                                # Daemonize thread
            thread.start()                                      # Start the execution
        else:
            # End get Data
            self.text = "Teilnehmen"
            global isActive 
            isActive = False

            # Send Data to Server
            uploadData()

            # Update UI
            self.parent.parent.ids.status_indicator.color = 255,0,0,1
            self.parent.parent.ids.data_status.text_color = 1,0,0,1
            self.parent.parent.ids.data_status.text = "Keine Daten werden aufgenommen"
        

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