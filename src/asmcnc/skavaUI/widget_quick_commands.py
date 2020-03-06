'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock
from asmcnc.skavaUI import popup_stop_press

import sys

Builder.load_string("""


<QuickCommands>

    stop_reset_button_image:stop_reset_button_image
    home_image:home_image
    home_button:home_button

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        padding: 0
        spacing: 10
        orientation: "vertical"

        BoxLayout:
            size_hint_y: 1
            center: self.parent.center
            size: self.parent.size
            pos: self.parent.pos             
            Button:
                id:home_button
#                size_hint: None, None
                center: self.parent.center
    
                background_color: hex('#F4433600')
                on_release: 
                    root.home()
                    self.background_color = hex('#F4433600')
                on_press:
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: home_image
                        source: "./asmcnc/skavaUI/img/home.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True   
        Button:
            size_hint_y: 1
            background_color: hex('#F4433600')
            on_release: 
                root.unlock()
                self.background_color = hex('#F4433600')
            on_press:
                self.background_color = hex('#F44336FF')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/unlock.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True   
        Button:
            size_hint_y: 1
            background_color: hex('#F4433600')
            on_release: 
                root.reset()
                self.background_color = hex('#F4433600')
            on_press:
                self.background_color = hex('#F44336FF')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/reset.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True   
        
        Button:
            size_hint_y: 1
            background_color: hex('#F4433600')
            on_release: 
                root.proceed_to_go_screen()
                self.background_color = hex('#F4433600')
            on_press:
                self.background_color = hex('#F44336FF')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/resume.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True
  
        Button:
            size_hint_y: 1
            background_color: hex('#F4433600')
            on_release: 
                root.stop()
                self.background_color = hex('#F4433600')
            on_press:
                self.background_color = hex('#F44336FF')
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    id: stop_reset_button_image
                    source: "./asmcnc/skavaUI/img/stop.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True   
  
        
""")
    
# Valid states types: Idle, Run, Hold, Jog, Alarm, Door, Check, Home, Sleep



class QuickCommands(Widget):



    def __init__(self, **kwargs):
    
        super(QuickCommands, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
      

            
    def home(self):
        self.m.home_all()

    def unlock(self):
        self.m.unlock_after_alarm()
    
    def reset(self):
        self.m.soft_reset()
    
    
    def stop(self):
        self.m.hold()        
        popup_stop_press.PopupStop(self.m, self.sm)

    def proceed_to_go_screen(self):
        
        # NON-OPTIONAL CHECKS (bomb if non-satisfactory)
        
        # GCode must be loaded.
        # Machine state must be idle.
        # Machine must be homed.
        # Job must be within machine bounds.

        if self.sm.get_screen('home').job_gcode ==[]:
            pass

        elif self.m.state() != 'Idle':
            self.sm.current = 'mstate'
            
        elif self.m.is_machine_homed == False:
            self.sm.get_screen('homingWarning').user_instruction = 'Please home SmartBench first!'
            self.sm.get_screen('homingWarning').error_msg = 'Cannot start Job.'
            self.sm.current = 'homingWarning'
                
        elif self.is_job_within_bounds() == False and sys.platform != "win32":                   
            self.sm.current = 'boundary'

        else:
            self.sm.get_screen('go').job_gcode = self.sm.get_screen('home').job_gcode
            self.sm.get_screen('go').job_filename  = self.sm.get_screen('home').job_filename
            self.sm.get_screen('go').return_to_screen = 'home'
            self.sm.get_screen('go').cancel_to_screen = 'home'      
            self.sm.current = 'go'
        
    def is_job_within_bounds(self):

        errorfound = 0
        job_box = self.sm.get_screen('home').job_box
        
        # Mins
        
        if -(self.m.x_wco()+job_box.range_x[0]) >= (self.m.grbl_x_max_travel - self.m.limit_switch_safety_distance):
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job target is too close to the X home position. The job will crash into the home position." + '\n\n[/color]')
            errorfound += 1 
        if -(self.m.y_wco()+job_box.range_y[0]) >= (self.m.grbl_y_max_travel - self.m.limit_switch_safety_distance):
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job target is too close to the Y home position. The job will crash into the home position." + '\n\n[/color]')
            errorfound += 1 
        if -(self.m.z_wco()+job_box.range_z[0]) >= (self.m.grbl_z_max_travel - self.m.limit_switch_safety_distance):
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job target is too far from the Z home position. The router will not reach that far." + '\n\n[/color]')
            errorfound += 1 
            
        # Maxs

        if self.m.x_wco()+job_box.range_x[1] >= -self.m.limit_switch_safety_distance:
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job target is too far from the X home position. The router will not reach that far." + '\n\n[/color]') 
            errorfound += 1 
        if self.m.y_wco()+job_box.range_y[1] >= -self.m.limit_switch_safety_distance:
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job target is too far from the Y home position. The router will not reach that far." + '\n\n[/color]') 
            errorfound += 1 
        if self.m.z_wco()+job_box.range_z[1] >= -self.m.limit_switch_safety_distance:
            self.sm.get_screen('boundary').job_box_details.append('[color=#FFFFFF]' + \
            "The job target is too close to the Z home position. The job will crash into the home position." + '\n\n[/color]')
            errorfound += 1 

        if errorfound > 0: return False
        else: return True

        
