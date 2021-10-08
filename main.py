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
import re

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

    # Neue Logic
    # Alle 20min stoppen
    # Daten speichern

    # Neu hochladen
    # Daten in intervallen hochladen?
    newUploadThread = threading.Thread(target=uploadData, args=())  # Create thread
    newUploadThread.daemon = True                                # Daemonize thread
    newUploadThread.start()                                      # Start the execution

    # Daten auf DB Speichern



# Upload Cursor Data
def uploadData():
    url = 'http://localhost:3000/senddata'
    try:
        # Daten die hochgeladen sind löschen
        res = requests.post(url, json={'test': 'x'})
        print(res.text)
    except:
        print('err: no data uploaded')
        # Sleep and try again
        time.sleep(10)
        uploadData()


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
    def on_press(self, *args):

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

        print("touched")
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
            # Start get Data
            uploadThread = threading.Thread(target=uploadData, args=())  # Create thread
            uploadThread.daemon = True                                # Daemonize thread
            uploadThread.start()                                      # Start the execution

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