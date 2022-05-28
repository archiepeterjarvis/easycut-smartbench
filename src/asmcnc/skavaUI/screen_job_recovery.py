from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
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

                        Label:
                            id: gcode_label
                            color: 0,0,0,1
                            font_size: dp(16)
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                            markup: True

                            canvas.before:
                                Color:
                                    rgba: hex('#A7D5FAFF')
                                Rectangle:
                                    size: self.parent.size[0], dp(20)
                                    pos: self.center_x - self.parent.size[0]/2, self.center_y - dp(3)

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
                            font_size: dp(20)
                            halign: 'left'
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: speed_label
                            text: "F: | S:"
                            color: 0,0,0,1
                            font_size: dp(20)
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
    max_index = 0
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
        self.m.jog_absolute_single_axis('Z', -10, 750)

        if self.jd.job_recovery_selected_line == -1:
            # Change this to get info by scraping file in the future
            self.pos_x, self.pos_y, self.pos_z, self.feed, self.speed = 0, 0, 0, 0, 0
            self.update_pos_speed_info()

            self.line_input.text = ""
            self.initial_line_index = self.jd.job_recovery_cancel_line
            self.selected_line_index = self.initial_line_index
            self.max_index = len(self.jd.job_gcode) - 1
            self.display_list = ["" for _ in range (6)] + [str(i) + ": " + self.jd.job_gcode[i] for i in range(self.max_index + 1)] + ["" for _ in range (6)]

            self.stopped_on_label.text = "Job stopped on line " + str(self.initial_line_index)
            self.display_list[self.selected_line_index + 6] = "[color=FF0000]" + self.display_list[self.selected_line_index + 6] + "[/color]"
            self.gcode_label.text = "\n".join(self.display_list[self.selected_line_index:self.selected_line_index + 13])

    def update_pos_speed_info(self):
        self.pos_label.text = "wX: %s | wY: %s | wZ: %s" % (str(self.pos_x), str(self.pos_y), str(self.pos_z))
        self.speed_label.text = "F: %s | S: %s" % (str(self.feed), str(self.speed))

    def scroll_up(self):
        if self.selected_line_index > 0:
            self.selected_line_index -= 1
            self.gcode_label.text = "\n".join(self.display_list[self.selected_line_index:self.selected_line_index + 13])

    def scroll_down(self):
        if self.selected_line_index < self.max_index:
            self.selected_line_index += 1
            self.gcode_label.text = "\n".join(self.display_list[self.selected_line_index:self.selected_line_index + 13])

    def jump_to_line(self, instance, value):
        if value:
            if value == "-":
                # Stop user inputting negative values
                instance.text = ""
            else:
                # If user inputs values outside of range, just show max line
                self.selected_line_index = min(int(value), self.max_index)
                self.gcode_label.text = "\n".join(self.display_list[self.selected_line_index:self.selected_line_index + 13])
        else:
            # If user clears input, return to initial line
            self.selected_line_index = self.initial_line_index
            self.gcode_label.text = "\n".join(self.display_list[self.selected_line_index:self.selected_line_index + 13])

    def get_info(self):

        info = "This is the job recovery screen."

        popup_info.PopupInfo(self.sm, self.l, 700, info)   

    def go_xy(self):
        self.m.jog_absolute_xy(self.pos_x, self.pos_y, 8000)

    def back_to_home(self):
        self.jd.job_recovery_selected_line = -1
        self.sm.current = 'home'

    def next_screen(self):
        self.jd.job_recovery_selected_line = self.selected_line_index
        self.sm.current = 'nudge'
