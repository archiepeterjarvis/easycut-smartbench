"""
Created on 1 Feb 2018
@author: Ed
"""
from kivy.graphics import RoundedRectangle, Color
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.components.buttons.spindle_button import SpindleButton
from asmcnc.core_UI.components.widgets.blinking_widget import BlinkingWidget

Builder.load_string(
    """
<CommonMove>

    speed_image:speed_image
    speed_toggle:speed_toggle
    vacuum_image:vacuum_image
    vacuum_toggle:vacuum_toggle
    vacuum_spindle_container:vacuum_spindle_container

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos      

        spacing:0.0416666666667*app.height
        
        orientation: "vertical"
        
        BoxLayout:
            spacing: 0
            padding:dp(0)
            size_hint_y: 1
            orientation: 'vertical'
            canvas:
                Color: 
                    rgba: 1,1,1,1
                RoundedRectangle: 
                    size: self.size
                    pos: self.pos 

            ToggleButton:
                font_size: str(0.01875 * app.width) + 'sp'
                id: speed_toggle
                on_press: root.set_jog_speeds()
                background_color: 1, 1, 1, 0 
                BoxLayout:
                    padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        id: speed_image
                        source: "./asmcnc/skavaUI/img/slow.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  
            
        BoxLayout:
            spacing: 0
            padding:dp(0)
            size_hint_y: 2
            orientation: 'vertical'
            id: vacuum_spindle_container
            canvas:
                Color: 
                    rgba: 1,1,1,1
                RoundedRectangle: 
                    size: self.size
                    pos: self.pos 

            ToggleButton:
                font_size: str(0.01875 * app.width) + 'sp'
                id: vacuum_toggle
                on_press: root.set_vacuum()
                background_color: 1, 1, 1, 0 
                BoxLayout:
                    padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                    size: self.parent.size
                    pos: self.parent.pos      
                    Image:
                        id: vacuum_image
                        source: "./asmcnc/skavaUI/img/vac_off.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True  
"""
)


class CommonMove(Widget):
    def __init__(self, **kwargs):
        super(CommonMove, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.set_jog_speeds()
        self.add_spindle_button()

    spindle_button = None

    def add_spindle_button(self):
        self.spindle_button = SpindleButton(self.m, self.m.s, self.sm,
                                            size_hint=(None, None),
                                            size=(scaling_utils.get_scaled_dp_width(71),
                                                  scaling_utils.get_scaled_dp_height(72)))
        self.vacuum_spindle_container.add_widget(self.spindle_button)

    fast_x_speed = 6000
    fast_y_speed = 6000
    fast_z_speed = 750

    def set_jog_speeds(self):
        if self.speed_toggle.state == "normal":
            self.speed_image.source = "./asmcnc/skavaUI/img/slow.png"
            self.feedSpeedJogX = self.fast_x_speed / 5
            self.feedSpeedJogY = self.fast_y_speed / 5
            self.feedSpeedJogZ = self.fast_z_speed / 5
        else:
            self.speed_image.source = "./asmcnc/skavaUI/img/fast.png"
            self.feedSpeedJogX = self.fast_x_speed
            self.feedSpeedJogY = self.fast_y_speed
            self.feedSpeedJogZ = self.fast_z_speed

    def set_vacuum(self):
        if self.vacuum_toggle.state == "normal":
            self.vacuum_image.source = "./asmcnc/skavaUI/img/vac_off.png"
            self.m.vac_off()
        else:
            self.vacuum_image.source = "./asmcnc/skavaUI/img/vac_on.png"
            self.m.vac_on()