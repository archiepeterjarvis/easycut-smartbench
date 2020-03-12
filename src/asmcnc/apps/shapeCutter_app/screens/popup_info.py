'''
@author Letty
Created for info buttons in the shapecutter app
'''

import kivy

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image


class PopupInfo(Widget):

    def __init__(self, screen_manager, description):
        
        self.shapecutter_sm = screen_manager
        
#         description = "If this is your first time using the app, please go to the tutorial.\n\n" \
#                             "If you need help or support, please visit customer support at www.yetitool.com/support"
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), markup=True, halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[10,10])

        
        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [0.141, 0.596, 0.957, 1]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[50,20,50,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,10,40,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Help',
                      title_color=[0.141, 0.596, 0.957, 1],
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/background.png'
        
        ok_button.bind(on_press=popup.dismiss)

        popup.open()
        
    def go_tutorial(self, *args):
        self.shapecutter_sm.tutorial()