import re
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.skavaUI import widget_status_bar
from asmcnc.skavaUI import widget_z_move_recovery
from asmcnc.skavaUI import popup_info

Builder.load_string("""
<JobRecoveryScreen>:
    status_container:status_container
    z_move_container:z_move_container

    gcode_label:gcode_label
    pos_label:pos_label
    speed_label:speed_label
    stopped_on_label:stopped_on_label

    line_input:line_input

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.9
            spacing: dp(15)
            canvas:
                Color:
                    rgba: hex('#E2E2E2FF')
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                padding: [dp(15), dp(15), dp(0), dp(15)]

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: 3.5
                        spacing: dp(15)

                        BoxLayout:
                            orientation: 'vertical'

                            Label:
                                text: "[b][color=333333]Go to line:[/color][/b]"
                                font_size: dp(25)
                                markup: True

                            BoxLayout:
                                padding: dp(5)
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                                TextInput:
                                    id: line_input
                                    font_size: dp(25)
                                    halign: 'center'
                                    input_filter: 'int'
                                    multiline: False
                                    background_color: (0,0,0,0)
                                    hint_text: "Enter #"

                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: 2
                            padding: [dp(50), dp(0)]
                            spacing: dp(10)

                            Button:
                                background_color: [0,0,0,0]
                                on_press: root.scroll_up()
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/skavaUI/img/arrow_up.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                            Button:
                                background_color: [0,0,0,0]
                                on_press: root.scroll_down()
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/skavaUI/img/arrow_down.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                    Button:
                        valign: "middle"
                        halign: "center"
                        markup: True
                        font_size: dp(30)
                        text_size: self.size
                        text: "GO XY"
                        background_normal: "./asmcnc/skavaUI/img/blank_small_button.png"
                        background_down: "./asmcnc/skavaUI/img/blank_small_button.png"
                        on_press: root.go_xy()

            BoxLayout:
                size_hint_x: 2
                padding: [dp(0), dp(15)]

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: 3.5
                        padding: [dp(12), dp(12), dp(12), dp(0)]
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                        FloatLayout:
                            Label:
                                id: gcode_label
                                color: 0,0,0,1
                                font_size: dp(16)
                                halign: "left"
                                valign: "top"
                                text_size: self.size[0] * 2, self.size[1]
                                size: self.parent.size
                                pos: self.parent.pos[0] + self.size[0]/2, self.parent.pos[1]
                                markup: True

                                canvas.before:
                                    Color:
                                        rgba: hex('#A7D5FAFF')
                                    Rectangle:
                                        size: self.parent.parent.size[0], dp(20)
                                        pos: self.parent.parent.pos[0], self.center_y - dp(3)

                        Label:
                            id: stopped_on_label
                            size_hint_y: 0.13
                            color: 1,0,0,1
                            font_size: dp(16)
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                    BoxLayout:
                        orientation: 'vertical'
                        padding: dp(12)
                        spacing: dp(10)
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                        Label:
                            size_hint_y: 0.75
                            text: "[b][color=333333]Job resumes at:[/color][/b]"
                            markup: True
                            font_size: dp(15)
                            halign: 'left'
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: pos_label
                            text: "wX: | wY: | wZ:"
                            color: 0,0,0,1
                            font_size: dp(16)
                            halign: 'left'
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: speed_label
                            text: "F: | S:"
                            color: 0,0,0,1
                            font_size: dp(16)
                            halign: 'left'
                            valign: 'middle'
                            text_size: self.size

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(15)

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(25)

                    BoxLayout:
                        padding: [dp(15), dp(15), dp(0), dp(15)]
                        Button:
                            background_color: [0,0,0,0]
                            on_press: root.get_info()
                            BoxLayout:
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True   

                    Button:
                        background_color: [0,0,0,0]
                        on_press: root.back_to_home()
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: 4
                    padding: [dp(0), dp(0), dp(15), dp(15)]
                    spacing: dp(15)

                    BoxLayout:
                        id: z_move_container
                        size_hint_y: 2.5
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:

                        padding: [(self.size[0] - dp(88)) / 2, (self.size[1] - dp(67)) / 2]

                        Button:
                            background_color: [0,0,0,0]
                            on_press: root.next_screen()
                            size_hint: (None, None)
                            height: dp(67)
                            width: dp(88)
                            BoxLayout:
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/arrow_next.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True

        # GREEN STATUS BAR

        BoxLayout:
            size_hint_y: 0.08
            id: status_container

""")

class JobRecoveryScreen(Screen):

    initial_line_index = 0
    selected_line_index = 0
    display_list = []

    def __init__(self, **kwargs):
        super(JobRecoveryScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.jd = kwargs['job']
        self.l = kwargs['localization']

        self.line_input.bind(text = self.jump_to_line)

        # Green status bar
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))

        # Z move widget
        self.z_move_container.add_widget(widget_z_move_recovery.ZMoveRecovery(machine=self.m, screen_manager=self.sm))

    def on_pre_enter(self):
        self.m.set_led_colour("WHITE")

        if self.jd.job_recovery_selected_line == -1:
            self.line_input.text = ""
            # Take away 1 so that user can't move to the position that was the target during cancellation
            self.initial_line_index = self.jd.job_recovery_cancel_line - 1
            self.selected_line_index = self.initial_line_index
            self.display_list = ["" for _ in range (6)] + [str(i) + ": " + self.jd.job_gcode[i] for i in range(self.initial_line_index + 1)] + ["" for _ in range (6)]

            self.stopped_on_label.text = "Job failed during line " + str(self.initial_line_index)
            self.display_list[self.selected_line_index + 6] = "[color=FF0000]" + self.display_list[self.selected_line_index + 6] + "[/color]"
            self.update_display()

    def scroll_up(self):
        if self.selected_line_index > 0:
            self.selected_line_index -= 1
            self.update_display()

    def scroll_down(self):
        if self.selected_line_index < self.initial_line_index:
            self.selected_line_index += 1
            self.update_display()

    def jump_to_line(self, instance, value):
        if value:
            if value == "-":
                # Stop user inputting negative values
                instance.text = ""
            else:
                # If user inputs values outside of range, just show max line
                self.selected_line_index = min(int(value), self.initial_line_index)
                self.update_display()
        else:
            # If user clears input, return to initial line
            self.selected_line_index = self.initial_line_index
            self.update_display()

    def update_display(self):
        self.gcode_label.text = "\n".join(self.display_list[self.selected_line_index:self.selected_line_index + 13])

        # Recover most recent spindle speed
        spindle_speed_line = next((s for s in reversed(self.jd.job_gcode[:self.selected_line_index + 1]) if 'S' in s), None)
        if spindle_speed_line:
            self.speed = spindle_speed_line[spindle_speed_line.find("S")+1:].split("M")[0]
        else:
            self.speed = "Undefined"

        # Recover most recent feedrate
        feedrate_line = next((s for s in reversed(self.jd.job_gcode[:self.selected_line_index + 1]) if 'F' in s), None)
        if feedrate_line:
            self.feed = re.match('\d+',feedrate_line[feedrate_line.find("F")+1:]).group()
        else:
            self.feed = "Undefined"

        # Recover most recent position
        x_line = next((s for s in reversed(self.jd.job_gcode[:self.selected_line_index + 1]) if 'X' in s), None)
        if x_line:
            self.pos_x = float(re.split('(X|Y|Z|F|S|I|J|K|G)', x_line)[re.split('(X|Y|Z|F|S|I|J|K|G)', x_line).index('X') + 1])
        else:
            self.pos_x = 0.0
        y_line = next((s for s in reversed(self.jd.job_gcode[:self.selected_line_index + 1]) if 'Y' in s), None)
        if y_line:
            self.pos_y = float(re.split('(X|Y|Z|F|S|I|J|K|G)', y_line)[re.split('(X|Y|Z|F|S|I|J|K|G)', y_line).index('Y') + 1])
        else:
            self.pos_y = 0.0
        z_line = next((s for s in reversed(self.jd.job_gcode[:self.selected_line_index + 1]) if 'Z' in s), None)
        if z_line:
            self.pos_z = float(re.split('(X|Y|Z|F|S|I|J|K|G)', z_line)[re.split('(X|Y|Z|F|S|I|J|K|G)', z_line).index('Z') + 1])
        else:
            self.pos_z = 0.0

        self.pos_label.text = "wX: %s | wY: %s | wZ: %s" % (str(self.pos_x), str(self.pos_y), str(self.pos_z))
        self.speed_label.text = "F: %s | S: %s" % (str(self.feed), str(self.speed))

    def get_info(self):

        info = ('This screen allows you to choose where to recover your job from.\n\n'
                'Use the arrows to navigate through the lines of the job file, and select a point to recover the job from. '
                'The red marker indicates where the stall event happened. We suggest starting a few lines before here.\n\n'
                'To confirm this start point, use the "GO XY" button. This will move the Z Head over the selected start point. '
                'You can lower the spindle to check the tool is approximately where you expect it to be in the XY plane. '
                'This XY position can be fine adjusted in the next screen. \n\n'
                'Note: the Z position will be automatically calculated when the job recovery starts.\n\n'
                'Note: when using job recovery for GCode containing G2 & G3 commands, '
                'the recovery point may be highlighted earlier in the file than actual, due to file streaming protocols.'
        )

        popup_info.PopupBigInfo(self.sm, self.l, 760, info)

    def go_xy(self):
        self.m.s.write_command('G90 G0 X%s Y%s' % (self.pos_x, self.pos_y))

    def back_to_home(self):
        self.jd.reset_recovery()
        self.sm.current = 'home'

    def next_screen(self):
        self.wait_popup = popup_info.PopupWait(self.sm, self.l)
        self.jd.job_recovery_selected_line = self.selected_line_index + 1
        self.m.s.write_command('G90 G0 X%s Y%s' % (self.pos_x, self.pos_y))
        Clock.schedule_once(self.proceed_to_next_screen, 0.4)

    def proceed_to_next_screen(self, dt):
        if self.m.state().startswith("Idle"):
            self.m.s.write_command('$#') # In preparation for nudge screen
            self.wait_popup.popup.dismiss()
            self.sm.current = 'nudge'
        else:
            Clock.schedule_once(self.proceed_to_next_screen, 0.4)
