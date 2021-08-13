# -*- coding: utf-8 -*-
'''
Created on 30 March 2019

Screen to give a safety warning to the user when they switch on SmartBench.

@author: Letty
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, StringProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.button import Button

import sys, os
from datetime import datetime

from asmcnc.skavaUI import widget_status_bar # @UnresolvedImport

# Kivy UI builder:
Builder.load_string("""

# <RoundedButton@Button>:
#     background_color: 0,0,0,0
#     canvas.before:
#         Color:
#             rgba: hex('#1976d2ff')
#         RoundedRectangle:
#             pos: self.pos
#             size: self.size
#             radius: [dp(30), dp(30)]

<SafetyScreen>:

    status_container:status_container

    header_label : header_label
    confirm_button : confirm_button

    label_r1_c1 : label_r1_c1
    label_r2_c1 : label_r2_c1
    label_r3_c1 : label_r3_c1
    label_r4_c1 : label_r4_c1 
    label_r1_c2 : label_r1_c2
    label_r2_c2 : label_r2_c2
    label_r3_c2 : label_r3_c2
    label_r4_c2 : label_r4_c2 


    canvas:
        Color:
            rgba: hex('#E5E5E5FF')
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
    
        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos  
                
        BoxLayout:
            size_hint_y: 0.9
            orientation: 'vertical'
            padding: [dp(40), dp(40), dp(40), dp(20)]
            size: self.parent.size
            pos: self.parent.pos
      
            BoxLayout:
                size_hint_y: .7
    
                orientation: 'vertical'
                size: self.parent.size
                pos: self.parent.pos
            
                Label:
                    id: header_label
                    text: '[color=333333][b]Safety Warning[/b][/color]'
                    markup: True
                    font_size: '29sp' 
                    valign: 'middle'
                    halign: 'center'
                    size:self.texture_size
                    text_size: self.size
                    color: hex('#333333ff')
                
            BoxLayout:
                size_hint_y: 4.1
    
                padding: [15,0]
                orientation: 'vertical'
                BoxLayout:
                    orientation: 'horizontal'    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            id: label_r1_c1
                            size_hint_x: 6
                            halign: 'left'
                            text: '[color=333333]Improper use of SmartBench can cause serious injury[/color]'
                            markup: True
                            size:self.size
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
                            
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            id: label_r1_c2
                            size_hint_x: 6
                            text: '[color=333333]Always wear ear defenders, eye protection and a dust mask[/color]'
                            markup: True    
                            halign: 'left' 
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
        
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            id: label_r2_c1
                            size_hint_x: 6
                            text: '[color=333333]Risk of injury from rotating tools and axis motion[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            id: label_r2_c2
                            size_hint_x: 6
                            text: '[color=333333]Never put hands into moving machinery[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
    
                            
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            id: label_r3_c1
                            size_hint_x: 6
                            text: '[color=333333]Danger to life by magnetic fields - do not use near a pacemaker[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            id: label_r3_c2
                            size_hint_x: 6
                            text: '[color=333333]Ensure the machine is powered from an earthed supply[/color]'
                            markup: True
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            halign: 'left'
                            color: hex('#333333ff')

                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            id: label_r4_c1
                            size_hint_x: 6
                            text: '[color=333333]Never leave the machine unattended while power is on[/color]'
                            markup: True
                            halign: 'left'
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            color: hex('#333333ff')
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing:20
                        Image:
                            size_hint_x: 1
                            keep_ratio: True
                            allow_stretch: True                           
                            source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        Label:
                            id: label_r4_c2
                            size_hint_x: 6
                            text: '[color=333333]Ensure all plugs are fully inserted and secured[/color]'
                            markup: True
                            valign: 'middle'
                            size:self.texture_size
                            text_size: self.size
                            halign: 'left'
                            color: hex('#333333ff')
  

            BoxLayout:
                size_hint_y: 1.2
                orientation: 'horizontal'

                Button:
                    id: confirm_button
                    width: dp(700)
                    height: dp(90)
                    on_press: root.go_to_next_screen()
                    markup: True
                    font_size: '24sp'
                    text_size: self.size
                    valign: "middle"
                    halign: "center"
                    background_normal: "./asmcnc/skavaUI/img/blank_long_button.png"
                    background_down: "./asmcnc/skavaUI/img/blank_long_button.png"
                    border: [dp(30)]*4
              

""")


def log(message):
    
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)


# class RoundedButton(Button):
#     pass

class SafetyScreen(Screen):


    def __init__(self, **kwargs):
        
        super(SafetyScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']
        
        # Status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)
        self.status_bar_widget.cheeky_color = '#1976d2'

        self.update_strings()


    def on_enter(self):

        log('Safety screen UP')
        
        
    def go_to_next_screen(self):
        
        self.sm.current = 'squaring_decision'
        
        
    def on_leave(self):
        
        if self.sm.current != 'alarmScreen' and self.sm.current != 'errorScreen' and self.sm.current != 'door': 
            self.sm.remove_widget(self.sm.get_screen('safety'))

    def update_strings(self):

        self.header_label.text = self.l.get_str("Safety Warning")

        self.label_r1_c1.text = "|" + self.l.get_str("Improper use of SmartBench can cause serious injury") + "|"
        self.label_r2_c1.text = "|" + self.l.get_str("Always wear ear defenders, eye protection and a dust mask") + "|"
        self.label_r3_c1.text = "|" + self.l.get_str("Risk of injury from rotating tools and axis motion") + "|"
        self.label_r4_c1.text = "|" + self.l.get_str("Never put hands into moving machinery") + "|"
        self.label_r1_c2.text = "|" + self.l.get_str("Danger to life by magnetic fields - do not use near a pacemaker") + "|"
        self.label_r2_c2.text = "|" + self.l.get_str("Ensure the machine is powered from an earthed supply") + "|"
        self.label_r3_c2.text = "|" + self.l.get_str("Never leave the machine unattended while power is on") + "|"
        self.label_r4_c2.text = "|" + self.l.get_str("Ensure all plugs are fully inserted and secured") + "|"

        self.confirm_button.text = self.l.get_str("I have read and understood the instruction manual")
            
        self.print_if_clipped()

    def print_if_clipped(self):

        self.confirm_button.shorten = True
        if self.confirm_button.is_shortened: print("Button clipped in " + str(self.l.lang))