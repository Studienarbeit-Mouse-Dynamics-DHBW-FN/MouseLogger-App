LAYOUT = """ 
#:kivy 1.0.9

MDScreen:
    MDCard: 
        size_hint: None, None
        size: 400, 290
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
            icon_right_color: [1, 1, 1, 1]
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

        MDCard: 
            size_hint: None, None
            size: "160dp", "20dp"
            orientation: "horizontal"
            pos_hint: {'center_x': .5, 'center_y': .5}
            elevation: 0

            MDLabel:
                text: "Teilnahme merken"

            MDCheckbox:
                id: parti
                size_hint: None, None
                size: "20dp", "20dp"
                pos_hint: {'center_x': .5, 'center_y': .5}
                selected_color: [144, 238, 144, 1]
                unselected_color: [144, 238, 144, 1]
                on_active: app.on_checkbox_active(*args)

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
"""
