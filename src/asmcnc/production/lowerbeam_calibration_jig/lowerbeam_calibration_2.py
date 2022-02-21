from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string("""
<LBCalibration2>:
    
    canvas:
        Color:
            rgba: hex('#1976d2ff')

        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'

        Label:
            text: 'Calibrating...'
            font_size: dp(50)

    
""")

class LBCalibration2(Screen):
    def __init__(self, **kwargs):
        super(LBCalibration2, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

    def on_enter(self):
        self.run_calibration()

    def run_calibration(self):
        self.m.tune_Y_for_calibration()
        self.poll_for_tuning_completion = Clock.schedule_interval(self.start_calibrating, 0.4)

    def start_calibrating(self, dt):
        if not self.m.tuning_in_progress:
            Clock.unschedule(self.poll_for_tuning_completion)

            if not self.m.calibration_tuning_fail_info:
                self.m.calibrate_Y()
                self.poll_for_calibration_completion = Clock.schedule_interval(self.finish_calibrating, 0.4)

            else:
                self.calibration_label.text = self.m.calibration_tuning_fail_info


    def finish_calibrating(self, dt):
        if not self.m.run_calibration:
            Clock.unschedule(self.poll_for_calibration_completion)

            if not self.m.calibration_tuning_fail_info:
                self.enter_next_screen()

            else:
                self.calibration_label.text = self.m.calibration_tuning_fail_info


    def enter_next_screen(self, dt):
        self.sm.current = 'lbc3'