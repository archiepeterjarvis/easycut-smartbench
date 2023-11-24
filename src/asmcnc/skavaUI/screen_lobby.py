# -*- coding: utf-8 -*-
'''
Created on 19 Aug 2017

@author: Ed
'''
# config

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.clock import Clock


import sys, os, textwrap
from os.path import expanduser
from shutil import copy

from asmcnc.skavaUI import popup_info


Builder.load_string("""

<LobbyScreen>:

    carousel:carousel

    pro_app_label: pro_app_label
    shapecutter_app_label: shapecutter_app_label
    wifi_app_label: wifi_app_label
    calibrate_app_label: calibrate_app_label
    update_app_label: update_app_label
    maintenance_app_label: maintenance_app_label
    system_tools_app_label: system_tools_app_label
    upgrade_app_label:upgrade_app_label

    shapecutter_container:shapecutter_container
    drywall_app_container:drywall_app_container
    upgrade_app_container:upgrade_app_container

    canvas.before:
        Color: 
            rgba: hex('#0d47a1FF')
        Rectangle: 
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        size: self.parent.size
        pos: self.parent.pos
        padding: 0
        spacing: 0

        BoxLayout:
            size_hint_y: 70
            padding: [10, 10, 734, 0]
            orientation: 'horizontal'

        Carousel:
            size_hint_y: 270
            id: carousel
            loop: True
                            
            BoxLayout:
                orientation: 'horizontal'
                padding: [100, 20, 100, 50]
                spacing: 20

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.pro_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_pro.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: pro_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'CAD / CAM'


                   
                BoxLayout:
                    id: shapecutter_container
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
                                             
                    Button:
                        
                        disabled: False
                        size_hint_y: 8
                        background_color: hex('#FFFFFF00')
                        on_release:                 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.shapecutter_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_app_shapecutter.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: shapecutter_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Shape Cutter'


                BoxLayout:
                    id: drywall_app_container
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
                    padding: [65,0]

                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release:
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.drywall_cutter_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/apps/drywall_cutter_app/img/lobby_logo.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                    Label:
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Drywall cutter'
                        markup: True

                        
            # Carousel pane 2
            BoxLayout:
                orientation: 'horizontal'
                padding: [100, 20, 100, 50]
                spacing: 20

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.wifi_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_app_wifi.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: wifi_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Wi-Fi'
                
                
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.calibrate_smartbench()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_app_calibrate.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: calibrate_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Calibrate'
                        markup: True

            # Carousel pane 3
            BoxLayout:
                orientation: 'horizontal'
                padding: [100, 20, 100, 50]
                spacing: 20

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.update_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/skavaUI/img/lobby_update.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: update_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Update'
                
                
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
    
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.maintenance_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/apps/maintenance_app/img/lobby_maintenance.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: maintenance_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Maintenance'

            # Carousel pane 4
            BoxLayout:
                orientation: 'horizontal'
                padding: [100, 20, 100, 50]
                spacing: 20

                BoxLayout:
                    id: upgrade_app_container
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20

                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.upgrade_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/apps/upgrade_app/img/lobby_upgrade.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: upgrade_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'Upgrade'
                        markup: True

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 1
                    spacing: 20
                
                    Button:
                        size_hint_y: 8
                        disabled: False
                        background_color: hex('#FFFFFF00')
                        on_release: 
                            self.background_color = hex('#FFFFFF00')
                        on_press:
                            root.developer_app()
                            self.background_color = hex('#FFFFFF00')
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                id: image_select
                                source: "./asmcnc/apps/systemTools_app/img/lobby_system.png"
                                center_x: self.parent.center_x
                                center_y: self.parent.center_y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True 
                    Label:
                        id: system_tools_app_label
                        size_hint_y: 1
                        font_size: '25sp'
                        text: 'System Tools'
                        markup: True

        BoxLayout:
            size_hint_y: 6
            size: self.parent.size
            pos: self.parent.pos
          
            Image:
                source: "./asmcnc/skavaUI/img/lobby_separator.png"

        BoxLayout:
            size_hint_y: 134
            orientation: 'horizontal'

            BoxLayout:
                size_hint_x: None
                width: 720
                height: self.parent.height
                padding: [80, 40, 0, 40]
                orientation: 'horizontal'
                
                Button:
                    disabled: False
                    size_hint_y: 1
                    background_color: hex('#FFFFFF00')
                    on_release: 
                        carousel.load_previous()
                        self.background_color = hex('#FFFFFF00')
                    on_press:
                        self.background_color = hex('#FFFFFF00')
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_cancel
                            source: "./asmcnc/skavaUI/img/lobby_scrollleft.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True 
                Label:
                    size_hint_y: 0.8

                Button:
                    id: shutdown_button
                    size_hint_y: 1
                    background_color: hex('#FFFFFF00')
                    on_press: root.shutdown_console()

                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_select
                            source: "./asmcnc/skavaUI/img/shutdown.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                Label:
                    size_hint_y: 0.8

                Button:
                    id: load_button
                    disabled: False
                    size_hint_y: 1
                    background_color: hex('#FFFFFF00')
                    on_release: 
                        carousel.load_next(mode='next')
                        self.background_color = hex('#FFFFFF00')
                    on_press:
                        self.background_color = hex('#FFFFFF00')
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_select
                            source: "./asmcnc/skavaUI/img/lobby_scrollright.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

            BoxLayout:
                size_hint: (None, None)
                size: (80,80)
                orientation: 'horizontal'
                padding: [29,29,10,10]
                Button:
                    disabled: False
                    background_color: hex('#FFFFFF00')
                    on_press: root.help_popup()
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: image_select
                            source: "./asmcnc/skavaUI/img/lobby_help.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
                
""")


job_cache_dir = './jobCache/'    # where job files are cached for selection (for last used history/easy access)
job_q_dir = './jobQ/'            # where file is copied if to be used next in job
ftp_file_dir = '/home/sysop/router_ftp'   # Linux location where incoming files are FTP'd to

class LobbyScreen(Screen):

    no_preview_found_img_path = './asmcnc/skavaUI/img/image_preview_inverted_large.png'
    trigger_update_popup = False
    welcome_popup_description = ''
    update_message = ''
    upgrade_app_hidden = False
    
    def __init__(self, **kwargs):
        super(LobbyScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.am=kwargs['app_manager']
        self.l=kwargs['localization']

        self.update_strings()

        # If it's a SmartCNC machine, then show the drywalltec app instead of shapecutter
        if "DRYWALLTEC" in self.m.smartbench_model():
            self.shapecutter_container.parent.remove_widget(self.shapecutter_container)
        else:
            self.drywall_app_container.parent.remove_widget(self.drywall_app_container)

    def on_pre_enter(self):
        # Hide upgrade app if older than V1.3, and only if it has not been hidden already
        if not ("V1.3" in self.m.smartbench_model()) and not self.upgrade_app_hidden:
            self.upgrade_app_container.parent.remove_widget(self.upgrade_app_container)
            self.upgrade_app_hidden = True

        elif self.upgrade_app_hidden and "V1.3" in self.m.smartbench_model():
            pass # reinstate upgrade_app_container, tbc - this is placeholder for now

    def on_enter(self):
        if not sys.platform == "win32":
            self.m.set_led_colour('GREEN')

        # Tell user to update if update is available
        if self.trigger_update_popup:
            popup_info.PopupInfo(self.sm, self.l, 450, self.update_message)

        # Trigger welcome popup is machine is being used for the first time
        if self.m.trigger_setup: self.help_popup()

    def help_popup(self):
        popup_info.PopupWelcome(self.sm, self.m, self.l, self.welcome_popup_description)
 
    def pro_app(self):
        self.am.start_pro_app()
        self.sm.current = 'home'
    
    def shapecutter_app(self):
        self.m.run_led_rainbow_ending_green()
        self.am.start_shapecutter_app()
    
    def calibrate_smartbench(self):
        self.am.start_calibration_app('lobby')
    
    def wifi_app(self):
        self.am.start_wifi_app()
    
    def update_app(self):
        self.am.start_update_app()    
    
    def developer_app(self):
        # popup_info.PopupDeveloper(self.sm)
        self.am.start_systemtools_app()

    def maintenance_app(self):
        self.am.start_maintenance_app('laser_tab') 

    def upgrade_app(self):
        # Need to set $51 on entry, requires idle
        if self.m.state().startswith('Idle'):
            self.am.start_upgrade_app()
        else:
            popup_info.PopupError(self.sm, self.l, self.l.get_str("Please ensure machine is idle before continuing."))

    def drywall_cutter_app(self):
        self.am.start_drywall_cutter_app()

    def shutdown_console(self):
        if sys.platform != 'win32' and sys.platform != 'darwin': 
            os.system('sudo shutdown -h')
        popup_info.PopupShutdown(self.sm, self.l)

    def update_strings(self):
        self.pro_app_label.text = self.l.get_str('CAD / CAM')
        self.shapecutter_app_label.text = self.l.get_str('Shape Cutter')
        self.wifi_app_label.text = self.l.get_str('Wifi')
        self.calibrate_app_label.text = self.l.get_str('Calibrate')
        self.update_app_label.text = self.l.get_str('Update')
        self.maintenance_app_label.text = self.l.get_str('Maintenance')
        self.system_tools_app_label.text = self.l.get_str('System Tools')
        self.upgrade_app_label.text = self.l.get_str('Upgrade')

        self.welcome_popup_description = (
            self.format_command(
                self.l.get_str('Use the arrows to go through the menu, and select an app to get started.')
                ) + '\n\n' + \

            self.format_command(
                ((self.l.get_str('If this is your first time, make sure you use the Wifi, Maintenance, ' + \
                    'and Calibrate apps to set up SmartBench.'
                    ).replace(self.l.get_str('Wifi'), self.l.get_bold('Wifi'))
                    ).replace(self.l.get_str('Maintenance'), self.l.get_bold('Maintenance'))
                    ).replace(self.l.get_str('Calibrate'), self.l.get_bold('Calibrate')
                )
            ) + '\n\n' + \
            self.format_command(
                self.l.get_str('For more help, please visit:')
            ) + '\n' + \
            '[b]https://www.yetitool.com/support[/b]' + '\n'
            )

        self.update_message = (
            self.l.get_str('New software update available for download!') + '\n\n' + \
            self.l.get_str(
                'Please use the Update app to get the latest version.'
                ).replace(self.l.get_str('Update'), self.l.get_bold('Update'))
            )

    def format_command(self, cmd):
        wrapped_cmd = textwrap.fill(cmd, width=50, break_long_words=False)
        return wrapped_cmd
