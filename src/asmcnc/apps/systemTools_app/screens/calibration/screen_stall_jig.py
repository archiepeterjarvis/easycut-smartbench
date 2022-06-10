# -*- coding: utf-8 -*-
'''
Created Mayh 2019

@author: Letty

Basic screen 
'''
import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from  kivy.uix.boxlayout import BoxLayout
from  kivy.uix.label import Label
from  kivy.uix.button import Button
from kivy.clock import Clock
import sys, os
from functools import partial
from time import sleep
from datetime import datetime

from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar
from asmcnc.apps.systemTools_app.screens import widget_final_test_xy_move
from asmcnc.apps.systemTools_app.screens.popup_system import PopupStopStallJig


# Kivy UI bsystemTools_sm.uilder:
Builder.load_string("""

<StallJigScreen>:

    back_button : back_button
    run_button : run_button
    result_label : result_label
    reset_test_button : reset_test_button
    send_data_button : send_data_button
    unlock_button : unlock_button
    test_status_label : test_status_label

    stop_button : stop_button
    move_container : move_container
    home_button : home_button
    grbl_reset_button : grbl_reset_button


    x_grid_container : x_grid_container
    y_grid_container : y_grid_container
    z_grid_container : z_grid_container

    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'horizontal'

            BoxLayout: 
                size_hint_x: 0.25
                orientation: "vertical"

                Button:
                    id: back_button
                    size_hint_y: 1
                    text: "<< Back"
                    on_press: root.back_to_fac_settings()

                Button: 
                    id: run_button
                    size_hint_y: 1
                    background_normal: ""
                    background_color: root.pass_green
                    text: "PREP TEST"
                    on_press: root.run()

                Button:
                    id: result_label
                    size_hint_y: 1
                    background_normal: ""
                    background_down: ""
                    background_color: [0,0,0,1]

                Button: 
                    id: reset_test_button
                    size_hint_y: 1
                    text: "RESET CURRENT SUB-TEST"
                    on_press: root.reset_current_sub_test()

                BoxLayout: 
                    size_hint_y: 1
                    orientation: "horizontal"

                    Button:
                        id: send_data_button 
                        size_hint_x: 2
                        disabled: True
                        text: "SEND DATA"
                        on_press: root.do_data_send()

                    ToggleButton: 
                        id: unlock_button
                        size_hint_x: 1
                        text: "unlock"
                        on_press: root.enable_data_send()
                Label:
                    id: test_status_label
                    size_hint_y: 1

            BoxLayout: 
                size_hint_x: 0.4
                orientation: "vertical"

                Button:
                    id: stop_button
                    size_hint_y: 1
                    text: "STOP"
                    background_normal: ""
                    background_color: root.stop_red
                    on_press: root.stop()

                BoxLayout:
                    size_hint_y: 4
                    padding: [0,10]

                    BoxLayout:
                        id: move_container

                BoxLayout: 
                    size_hint_y: 1
                    orientation: 'horizontal'

                    Button:
                        id: home_button
                        size_hint_x: 0.5
                        text: "HOME"
                        background_normal: ""
                        background_color: root.easycut_blue
                        on_press: root.start_homing()

                    Button:
                        id: grbl_reset_button
                        size_hint_x: 0.5
                        text: "GRBL RESET"
                        on_press: root.grbl_reset()


            BoxLayout: 
                size_hint_x: 0.35
                orientation: "vertical"

                BoxLayout: 
                    id: x_grid_container
                    size_hint_y: len(root.threshold_dict["X"])
                    orientation: "vertical"

                BoxLayout: 
                    id: y_grid_container
                    size_hint_y: len(root.threshold_dict["Y"])
                    orientation: "vertical"

                BoxLayout: 
                    id: z_grid_container
                    size_hint_y: len(root.threshold_dict["Z"])
                    orientation: "vertical"

        BoxLayout:
            size_hint_y: 0.08
            id: status_container        

""")


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))


class StallJigScreen(Screen):

    # ALL NUMBERS ARE DECLARED HERE, SO THAT THEY CAN BE EASILY EDITED AS/WHEN REQUIRED

    ## AXES, FEEDS, AND THRESHOLDS

    axes = ["X","Y","Z"]

    feed_dict = {

        "X": [8000,6000,4500,3000,2000,1200,600],
        "Y": [6000,5000,4000,3000,2000,1200,600],
        "Z": [750,600,500,400,300,150,75] 

    }

    # Min threshold, Max threshold, Step between thresholds

    threshold_dict = {

        "X": range(150, 350, 25),
        "Y": range(150, 350, 25),
        "Z": range(100, 240, 20) 

    }

    ## INDEX DICTIONARY

    ### This dictionary keeps track of which index we are "on"
    ### at any given stage

    ### This is used in conjunction with the feed and threshold dicts to extract values. 

    indices = {

        "axis": 0,
        "threshold": 0,
        "feed": 0

    }

    ## POSITIONS

    ### ABSOLUTE START POSITION OF ALL TESTS 
    ### RELATIVE TO TRUE HOME

    absolute_start_pos = {

        "X": -1100,
        "Y": -2400,
        "Z": -160

    }

    ### START POSITIONS WHEN HOMED AGAINST THE MAGNET JIG
    ### (SO NOT TRUE MACHINE COORDS)
    start_pos_x_test = {

        "X": -1100,
        "Y": -2400,
        "Z": -160

    }

    start_pos_y_test = {

        "X": -750,
        "Y": -2400,
        "Z": -160

    }

    start_pos_z_test = {

        "X": -1200,
        "Y": -2300,
        "Z": -140

    }

    start_positions = {

        "X": start_pos_x_test,
        "Y": start_pos_y_test,
        "Z": start_pos_z_test
    }


    ### CURRENT POSITION DEFINED IN CLASS INIT
    ### AS PULLS FUNCTIONS FROM ROUTER_MACHINE

    current_position = {}

    ## DEFAULT FEEDS

    fast_travel = {

        "X": 8000,
        "Y": 6000,
        "Z": 750

    }

    three_axis_max_feed = 6000

    ## ALL THE OTHER EXPERIMENTAL PARAMETERS

    stall_tolerance = {

        "X": 3,
        "Y": 3,
        "Z": 1

    }

    overjog = {

        "X": 8,
        "Y": 8,
        "Z": 8

    }

    backoff = {

        "X": 10,
        "Y": -10,
        "Z": 10

    }

    limit_pull_off = {

        "X": -5,
        "Y": 5,
        "Z": 5

    }    

    initial_move_distance = {

        "X": -10,
        "Y": 10,
        "Z": -10

    }

    travel_to_stall_pos = {

        "X": None,
        "Y": None,
        "Z": None

    }


    ## DIS/ENABLE MOTORS DEFINED IN CLASS INIT
    ## AS PULLS FUNCTIONS FROM ROUTER_MACHINE

    disable_motors = {}
    enable_motors = {}

    ## FLAGS FOR TEST EVENTS

    setting_up_axis_for_test = False
    expected_limit_found = False
    threshold_reached = False
    all_tests_completed = False
    test_stopped = False

    ## CLOCK OBJECTS

    poll_for_homing_completion_loop = None
    poll_for_ready_to_check_calibration = None
    poll_for_going_to_start_pos = None
    poll_to_set_travel = None
    poll_for_stall_position_found = None
    poll_for_threshold_detection = None
    poll_for_back_off_completion = None
    poll_to_relax_motors = None
    stadib_event = None

    ## DATABASE OBJECTS

    id_stage = ""
    stall_test_events = []
    stall_test_data_col_names = [

            "ID Stage: ",
            "Axis: ",
            "Test Feed: ",
            "Threshold: ",
            "Reported Feed: ",
            "Load at detection: ",
            "Stall coordinate: "
    ]

    ## STORE ALL THE GRID BUTTONS

    grid_button_objects = {}

    ## COLOURS: 

    fail_orange = [245./255, 176./255, 65./255, 1]
    pass_green = [0./255, 204./255, 51./255, 1]
    bright_pass_green = [51./255, 255./255, 0./255, 1]
    highlight_yellow = [1, 1, 0, 1]
    stop_red = [1, 0, 0, 1]
    easycut_blue = [25./255, 118./255, 210./255, 1]

    VERBOSE = True # For debugging

    
    def __init__(self, **kwargs):

        super(StallJigScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs['systemtools']
        self.l=kwargs['localization']
        self.m=kwargs['machine']

        # FUNCTION DICTIONARIES

        self.current_position = {

            "X": self.m.mpos_x,
            "Y": self.m.mpos_y,
            "Z": self.m.mpos_z

        }

        self.disable_motors = {

            "X": self.m.disable_x_motors,
            "Y": self.m.disable_y_motors,
            "Z": self.m.disable_z_motor

        }

        self.enable_motors = {

            "X": self.m.enable_x_motors,
            "Y": self.m.enable_y_motors,
            "Z": self.m.enable_z_motor

        }


        # GUI SET UP

        ## FEED/THRESHOLD GRIDS FOR EACH AXIS
        self.populate_axis_grid(self.x_grid_container, 0)
        self.populate_axis_grid(self.y_grid_container, 1)
        self.populate_axis_grid(self.z_grid_container, 2)

        ## MOVE AND STATUS WIDGETS
        self.move_container.add_widget(widget_final_test_xy_move.FinalTestXYMove(machine=self.m, screen_manager=self.systemtools_sm.sm))
        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.systemtools_sm.sm))


    # UNSCHEDULE ALL CLOCK OBJECTS --------------------------------------------------------------------------

    def unschedule_all_events(self):
        if self.poll_for_homing_completion_loop != None: Clock.unschedule(self.poll_for_homing_completion_loop)
        if self.poll_for_ready_to_check_calibration != None: Clock.unschedule(self.poll_for_ready_to_check_calibration)
        if self.poll_for_going_to_start_pos != None: Clock.unschedule(self.poll_for_going_to_start_pos)
        if self.poll_to_set_travel != None: Clock.unschedule(self.poll_to_set_travel)
        if self.poll_for_stall_position_found != None: Clock.unschedule(self.poll_for_stall_position_found)
        if self.poll_for_threshold_detection != None: Clock.unschedule(self.poll_for_threshold_detection)
        if self.poll_for_back_off_completion != None: Clock.unschedule(self.poll_for_back_off_completion)
        if self.poll_to_relax_motors != None: Clock.unschedule(self.poll_to_relax_motors)
        if self.stadib_event != None: Clock.unschedule(self.stadib_event)
        log("Unschedule all events")

    # RESET FLAGS -------------------------------------------------------------------------------------------

    def reset_flags(self):

        self.setting_up_axis_for_test = False
        self.expected_limit_found = False
        self.threshold_reached = False
        self.all_tests_completed = False
        self.test_stopped = False
        log("Reset flags")

    ## DISABLE/ENABLE BUTTON FUNCTIONS ----------------------------------------------------------------------

    def disable_all_buttons_except_stop(self):

        self.disable_run(True)
        self.disable_most_buttons(True)

    def enable_all_buttons_except_run(self):

        self.disable_most_buttons(False)

    def disable_run(self, disable_bool):

        self.run_button.disabled = disable_bool

    def disable_most_buttons(self, disable_bool):

        self.back_button.disabled = disable_bool
        self.unlock_button.disabled = disable_bool
        self.home_button.disabled = disable_bool
        self.grbl_reset_button.disabled = disable_bool
        self.reset_test_button.disabled = disable_bool

        for key in self.grid_button_objects:
            self.grid_button_objects[key].disabled = disable_bool


    # SET UP FEED THRESHOLD GRIDS USING PRE-DEFINED DICTIONARIES ---------------------------------------------

    def populate_axis_grid(self, grid_container, axis):
        
        first_row = BoxLayout(orientation = "horizontal")
        first_row.add_widget(Label(text = self.axes[axis], size_hint_x = 1))
        rows = []

        for i in self.feed_dict[self.axes[axis]]:

            first_row.add_widget(Label(text = str(i), size_hint_x = 1))

        grid_container.add_widget(first_row)

        for tidx, i in enumerate(self.threshold_dict[self.axes[axis]]): 
            rows.append(BoxLayout(orientation = "horizontal"))
            rows[tidx].add_widget(Label(text = str(i), size_hint_x = 1))

            for fidx, j in enumerate(self.feed_dict[self.axes[axis]]):

                new_button = Button(size_hint_x = 1)
                test_func = partial(self.choose_test, axis, tidx, fidx)
                new_button.bind(on_press = test_func)
                rows[tidx].add_widget(new_button)
                self.store_button(axis, tidx, fidx, new_button)

            grid_container.add_widget(rows[tidx])

    ##  FUNCTIONS FOR HANDLING/ACCESSING GRID BUTTONS

    def generate_grid_key(self, aidx, tidx, fidx):

        return (str(aidx) + str(tidx) + str(fidx))

    def store_button(self, aidx, tidx, fidx, button):

        self.grid_button_objects[self.generate_grid_key(aidx, tidx, fidx)] = button

    def get_grid_button(self, aidx, tidx, fidx):

        return self.grid_button_objects[self.generate_grid_key(aidx, tidx, fidx)]

    def colour_current_grid_button(self, colour):

        aidx = self.indices["axis"]
        tidx = self.indices["threshold"]
        fidx = self.indices["feed"]

        button_object = self.grid_button_objects[self.generate_grid_key(aidx, tidx, fidx)]
        button_object.background_normal = ''
        button_object.background_color = colour
        button_object.background_disabled_normal = ''


    ## FUNCTION THAT IS BOUND TO EACH GRID BUTTON TO CHOOSE TESTS

    def choose_test(self, axis_index, threshold_index, feed_index, instance=None):

        self.indices["axis"] = axis_index
        self.indices["threshold"] = threshold_index
        self.indices["feed"] = feed_index

        axis = self.axes[axis_index]
        feed = self.feed_dict[axis][feed_index]
        threshold = self.threshold_dict[axis][threshold_index]

        # BY SETTING THIS TRAVEL_TO_STALL_POS VALUE TO NONE,
        # RUN FUNCTION KNOWS TO SET UP THAT AXIS AGAIN & RE-"HOME" AND REPOSITION
        self.travel_to_stall_pos[axis] = None
        self.reset_flags()
        self.disable_run(False)
        self.colour_current_grid_button(self.highlight_yellow)
        self.result_label.text = ""
        self.result_label.background_color = [0,0,0,1]

        log("CHOOSE TEST: " + str(axis) + ", " + str(feed) + ", " + str(threshold))
        self.test_status_label.text = str(axis) + ", " + str(feed) + ", " + str(threshold)

    # SCREEN MISC -------------------------------------------------------------------------------

    # RETURN TO FACTORY SETTINGS

    def back_to_fac_settings(self):
        self.m.enable_only_soft_limits()
        self.restore_acceleration()
        self.systemtools_sm.open_factory_settings_screen()
        log("Return to factory settings")

    # SET UP SCREEN BEFORE ENTERING

    def on_pre_enter(self):

        self.test_status_label.text = self.l.get_str('STALL JIG') + '...'
        self.run_button.text = self.l.get_str('PREP TEST') + '...'
        log("Opening stall experiment wizard")

    # STALL/LIMIT EVENT DETECTION -----------------------------------------------------------------

    ## USE THE ON PRE-LEAVE FUNCTION TO DETECT IF THE SCREEN IS GOING TO CHANGE TO AN ALARM
    ## AND THEN THIS TRIGGERS CHECKS FOR WHETHER AN EXPECTED STALL ALARM OR A LIMIT

    def on_pre_leave(self):

        if not self.systemtools_sm.sm.current.startswith('alarm'):
            log("Leaving stall jig...")
            return

        self.systemtools_sm.sm.current = 'stall_jig'

        # UPDATE USER ON WHAT ALARM IS HAPPENING, IN CASE IT'S A GENERAL ONE
        self.test_status_label.text = self.m.s.alarm.alarm_code

        if self.expected_stall_alarm_detected():
            self.register_threshold_detection()

        if self.expected_limit_alarm():
            self.register_hard_limit_found()


    ## FUNCTIONS TO ANALYSE TRIGGERS AND UPDATE FOLLOWING FLAGS: 
    ## - THRESHOLD_REACHED 
    ## - EXPECTED_LIMIT_FOUND

    def expected_stall_alarm_detected(self):

        if not (
            self.m.s.alarm.sg_alarm and
            self.current_axis() in self.m.s.alarm.stall_axis
            ):
            return False

        log("Imminent stall detected: " + self.m.s.alarm.stall_axis)
        self.m.s.alarm.sg_alarm = False
        self.m.s.alarm.stall_axis = "W"
        return True


    def register_threshold_detection(self):

        self.m.resume_from_alarm()
        self.result_label.text = "THRESHOLD REACHED"
        self.result_label.background_color = self.bright_pass_green
        self.threshold_reached = True
        self.test_status_label.text = "PASS"
        log("Threshold reached (imminent stall detected), test passed")


    def expected_limit_alarm(self):
        if not self.current_axis() in self.m.s.alarm.trigger_description:
            return False

        return True

    def register_hard_limit_found(self):
        self.m.resume_from_alarm()
        self.test_status_label.text = "LIMIT FOUND"
        self.expected_limit_found = True
        log("Hard limit found, position known")

    # HOMING --------------------------------------------------------------------------------------------

    def start_homing(self):

        log("Begin homing")

        # Issue homing commands
        normal_homing_sequence = ['$H']
        self.m.s.start_sequential_stream(normal_homing_sequence)

        # Due to polling timings, and the fact grbl doesn't issues status during homing, EC may have missed the 'home' status, so we tell it.
        self.m.set_state('Home') 
        self.test_status_label.text = "HOMING"

        # Check for completion - since it's a sequential stream, need a poll loop
        self.poll_for_homing_completion_loop = Clock.schedule_once(self.check_for_homing_completion, 2)
       
     
    def check_for_homing_completion(self, dt):

        # if alarm state is triggered which prevents homing from completing, stop checking for success
        if self.m.state().startswith('Alarm'):
            log("Poll for homing success unscheduled")
            if self.poll_for_homing_completion_loop != None: Clock.unschedule(self.poll_for_homing_completion_loop)
            self.test_status_label.text = "ALARM"
            return

        # if sequential_stream completes successfully
        if self.m.s.is_sequential_streaming == False:
            log("Homing detected as success!")
            if self.poll_for_homing_completion_loop != None: Clock.unschedule(self.poll_for_homing_completion_loop)
            self.test_status_label.text = "READY"
            return

        if self.VERBOSE: log("Poll for homing completion")
        self.poll_for_homing_completion_loop = Clock.schedule_once(self.check_for_homing_completion, 2)


    # GENERAL ANCILLARY FUNCTIONS ------------------------------------------------------------------

    ## STOP BUTTON FUNCTION

    def stop(self):
        self.test_stopped = True
        PopupStopStallJig(self.m, self.systemtools_sm.sm, self.l, self)
        log("Tests stopped")

    ## RESET FROM ALARMS ETC.

    def grbl_reset(self):

        self.m.resume_from_alarm()
        self.test_status_label.text = "GRBL RESET"
        log("GRBL reset")

    ## RESET CURRENT SUB-TEST (DOESN'T RESTART THOUGH - WAITS FOR USER INPUT)

    def reset_current_sub_test(self):
        self.test_status_label.text = "TEST RESET"
        self.choose_test(self.indices["axis"], self.indices["threshold"], self.indices["feed"])
        log("Current test reset")


    ## UNLOCK DATA SEND (IN CASE USER WANTS/NEEDS TO SEND INCOMPLETE DATA SET)

    def enable_data_send(self):

        if self.unlock_button.state == "down":
            self.unlock_button.text = "lock"
            self.send_data_button.disabled = False
            log("Data send enabled")

        else:
            self.unlock_button.text = "unlock"
            self.send_data_button.disabled = True
            log("Data send disabled")

    ## DO DATA SEND

    def do_data_send(self):
        self.test_status_label.text = "SENDING DATA"
        log("Sending data...")


    # THE MAIN EVENT ----------------------------------------------------------------------------------------------------
    # HANDLES THE MANAGEMENT OF ALL STAGES OF THE TEST

    def run(self):

        self.disable_all_buttons_except_stop()
        self.threshold_reached = False
        self.result_label.text = ""
        self.result_label.background_color = [0,0,0,1]

        log("Run next test")
        self.test_status_label.text = "RUNNING"
        
        # If no tests have been started yet, SB will need to do a prep sequence instead
        if self.start_of_all_tests():
            return

        if self.end_of_all_tests():
            return

        if not self.travel_to_stall_pos[self.current_axis()]:
            self.set_up_axis_for_test()
            return

        self.colour_current_grid_button(self.highlight_yellow)
        threshold_idx = self.indices["threshold"]
        feed_idx = self.indices["feed"]
        self.set_threshold_and_drive_into_barrier(self.current_axis(), threshold_idx, feed_idx)
        self.poll_for_threshold_detection = Clock.schedule_once(self.sb_has_travelled_or_detected, 1)


    # CORE TEST FUNCTIONS -------------------------------------------------------------------------------------------

    ## RETURN CURRENT AXIS AS "X" "Y" OR "Z"

    def current_axis(self): return self.axes[self.indices["axis"]]

    ## MAX OUT ACCELERATION

    def max_out_acceleration(self):

        max_acceleration_values = [

                '$120=1300.0',     #X Acceleration, mm/sec^2
                '$121=1300.0'     #Y Acceleration, mm/sec^2
                ]

        self.m.s.start_sequential_stream(max_acceleration_values)
        log("Maxing out acceleration values for X and Y (to 1300)")

    ## PUT ACCELERATION BACK TO NORMAL

    def restore_acceleration(self):

        default_acceleration_values = [

                '$120=130.0',     #X Acceleration, mm/sec^2
                '$121=130.0'     #Y Acceleration, mm/sec^2

                ]

        self.m.s.start_sequential_stream(default_acceleration_values)
        log("Restoring acceleration values for X and Y (to 130)")


    ## FUNCTION TO NEATLY MOVE TO ABSOLUTE POSITION STORED IN WHATEVER POS DICTIONARY (AT MAX FEED)

    def move_all_axes(self, pos_dict):

        # Move Z up, 
        # Move to XY position
        # Move Z back down

        log("Moving all axes...")

        move_sequence = [

                        "G0 G53 Z-" + str(self.m.s.setting_27),
                        "G90" + "X" + pos_dict["X"] + "Y" + pos_dict["Y"] + self.fast_travel["Y"],
                        "G90" + "Z" + pos_dict["Z"] + self.fast_travel["Z"]
        ]

        self.m.s.start_sequential_stream(move_sequence)



    ## FUNCTION TO SET THE THRESHOLD AND CRASH INTO AN OBSTACLE

    def set_threshold_and_drive_into_barrier(self, axis, threshold_idx, feed_idx):

        if (not self.m.state().startswith("Idle")) or self.test_stopped:
            if self.VERBOSE: log("Poll for set threshold and drive into barrier")
            self.stadib_event = Clock.schedule_once(lambda dt: self.set_threshold_and_drive_into_barrier(axis, threshold_idx, feed_idx), 2)
            return

        threshold = self.threshold_dict[axis][threshold_idx]
        feed = self.feed_dict[axis][feed_idx]

        log("Setting threshold to " + str(threshold) + "for " + axis + ", and drive into barrier at feed: " + str(feed))

        self.m.set_threshold_for_axis(axis, threshold)
        sleep(1)
        self.m.send_any_gcode_command("G91 " + axis + str(self.move_distance[axis]) + " F" + str(feed))


    ## REPOSITIONING PROCEDURE

        ## THESE FUNCTIONS ARE CALLED AS PART OF MULTIPLE PROCEDURES (E.G. AXIS SET UP, INDIVIDUAL EXPERIMENTS)
        ## ORDER OF EVENTS IS:
        ## - BACK OFF FROM THE CRASH SITE INTO A HARD LIMIT
        ## - USE THIS LIMIT TO PLACE SB FOR THE NEXT PROCEDURE
        ## - DE-ENERGIZE AND RE-ENERGIZE THE MOTORS (AS A MINI RE-SQUARE)
        ## - CARRY OUT ANY PROCEDURE/OUTCOME SPECIFIC FUNCTIONS (E.G. UNSETTING SETTING_UP FLAG OR STORING RESULT)
        ## - AND THEN CALL RUN FUNCTION AGAIN

    def back_off_and_find_position(self):

        if not self.result_label.text == "THRESHOLD REACHED":
            self.result_label.text = "THRESHOLD NOT REACHED"
            self.result_label.background_color = self.fail_orange

        log("Back off and find position")
        self.test_status_label.text = "REFIND POS"
        self.m.enable_only_hard_limits()
        move_command = "G91 " + self.current_axis() + str(self.back_off[axis]) + " F" + str(self.fast_travel[axis])
        self.m.send_any_gcode_command(move_command)
        self.poll_for_back_off_completion = Clock.schedule_once(lambda dt: self.back_off_completed(), 1)


    def back_off_completed(self):

        if (not self.expected_limit_found) or self.test_stopped:
            if self.VERBOSE: log("Poll for back off completed")
            self.poll_for_back_off_completion = Clock.schedule_once(lambda dt: self.back_off_completed(), 1)
            return

        log("Position found")
        self.test_status_label.text = "POS FOUND"
        self.m.disable_only_hard_limits()
        self.expected_limit_found = False
        log("Pull off from limit")
        move_command = "G91 " + self.current_axis() + str(self.limit_pull_off[axis]) + " F" + str(self.fast_travel[axis])
        self.m.send_any_gcode_command(move_command)
        self.poll_to_relax_motors = Clock.schedule_once(lambda dt: self.relax_motors(), 1)


    def relax_motors(self):

        if (not self.m.state().startswith("Idle")) or self.test_stopped:
            if self.VERBOSE: log("Poll for relax motors")
            self.poll_to_relax_motors = Clock.schedule_once(lambda dt: self.relax_motors(), 1)
            return

        log("De-energize motors")
        self.test_status_label.text = "MOTORS OFF"
        self.disable_motors[self.current_axis()]()
        sleep(1)
        log("Energize motors")
        self.test_status_label.text = "MOTORS ON"
        self.enable_motors[self.current_axis()]()
        sleep(2)
        self.m.enable_only_hard_limits()
        self.finish_procedure_and_start_next_test()


    def finish_procedure_and_start_next_test(self):

        log("Procedure finished...")

        self.test_status_label.text = "RECORDING RESULT"

        if self.setting_up_axis_for_test: 
            self.test_status_label.text = "AXIS READY"
            log("Axis set up")
            self.setting_up_axis_for_test = False

        elif self.threshold_reached:
            log("Recording stall detection event - test passed")
            self.colour_current_grid_button(self.pass_green)
            self.record_stall_event()
            self.go_to_next_threshold()

        else:
            log("Stall was not detected - test failed")
            self.colour_current_grid_button(self.fail_orange)
            self.go_to_next_feed_set()

        log("Moved to next test indices - starting new run")
        self.run()


    # START TEST SEQUENCE (PREP TEST): ----------------------------------------------------------------------------------

        ## HAPPENS BEFORE MAGNETS HAVE BEEN INSTALLED

        ## HOMES NORMALLY
        ## RUNS CALIBRATION CHECK (SO WE KNOW IN ADVANCE IF SOMETHING 
        ## IS GOING TO FAIL DUE TO DODGY CALIBRATION)
        ## DISABLE SOFT LIMITS
        ## MOVES
        ## TELL USER TO FIX MAGNETS
        ## USER WILL MANUALLY PRESS RUN

    def start_of_all_tests(self):

        if self.run_button.text == "RUN":
            return False

        log("Set up for all tests")
        self.test_status_label.text = "SETTING UP"

        self.start_homing()

        # CALIBRATION CHECK
        self.poll_for_ready_to_check_calibration = Clock.schedule_once(lambda dt: self.full_calibration_check(), 2)
        return True


    def full_calibration_check(self):
        if (not self.m.state().startswith("Idle")) or self.test_stopped:
            if self.VERBOSE: log("Poll for ready to check calibration")
            self.poll_for_ready_to_check_calibration = Clock.schedule_once(lambda dt: self.full_calibration_check(), 2)
            return

        log("Run a calibration check in all axes")
        self.test_status_label.text = "CHECK CALIBRATION"
        self.m.check_x_y_z_calibration()
        Clock.schedule_interval(self.ready_to_run_tests, 5)


    def ready_to_run_tests(self, dt):

        if self.m.checking_calibration_in_progress:
            return

        if self.m.checking_calibration_fail_info:
            self.test_status_label.text = "CAL CHECK FAIL"
            return

        if (not self.m.state().startswith("Idle")) or self.test_stopped:
            return

        log("Ready to run tests, disabling limits & maxing acceleration")
        self.m.disable_only_soft_limits()
        self.max_out_acceleration()
        sleep(1)

        log("Move to start position")
        # go to absolute start position (relative to true home)
        self.move_all_axes(self.absolute_start_pos)

        log("Tell user to put the magnets on to set up fake home")
        # update labels for user input
        self.test_status_label.text = "FIX MAGNETS"
        self.run_button.text = "RUN"


    # NECESSARY SET UP THAT'S DONE EACH TIME A NEW AXIS IS TESTED ----------------------------------------------------------

    def set_up_axis_for_test(self):

        self.setting_up_axis_for_test = True
        self.test_status_label.text = "SET UP AXIS"

        log("Set up axis for test")

        log("Home against the magnets that give fake home position")
        self.start_homing()

        # go to start pos for the axis (relative to the magnets)
        self.poll_for_going_to_start_pos = Clock.schedule_once(self.go_to_start_pos, 2)


    def go_to_start_pos(self, dt):

        if (not self.m.state().startswith("Idle")) or self.test_stopped:
            if self.VERBOSE: log("Poll for going to start position")
            self.poll_for_going_to_start_pos = Clock.schedule_once(self.go_to_start_pos, 2)
            return

        log("Go to start pos for the axis (relative to the magnets)")
        self.test_status_label.text = "GO TO START POS"

        # go to test start position, relative to faux home
        self.move_all_axes(self.start_positions[self.current_axis()])

        # when start pos set up, set travel for stall
        self.poll_to_set_travel = Clock.schedule_once(self.set_travel, 1)

    ## LOWER THE THRESHOLD AND MAX OUT THE FEED TO RECORD THE POSITION WHERE WE EXPECT SB TO STALL

    def set_travel(self):

        if (not self.m.state().startswith("Idle")) or self.test_stopped:
            if self.VERBOSE: log("Poll for setting travel")
            self.poll_to_set_travel = Clock.schedule_once(self.set_travel, 1)
            return

        log("Set expected travel to stall position")
        self.test_status_label.text = "SET TRAVEL"

        start_pos = self.current_position[self.current_axis()]()
        self.set_threshold_and_drive_into_barrier(self.current_axis(), 0, 0)
        self.poll_for_stall_position_found = Clock.schedule_once(lambda dt: self.stall_position_found(axis, start_pos), 1)


    def stall_position_found(self, axis, start_pos):

        # NB: THIS TEST WILL NOT TIME OUT IF IT DOES NOT REACH THRESHOLD
        # THE USER WILL HAVE TO MANUALLY STOP IN THIS INSTANCE AND TRY AGAIN. 

        if (not self.threshold_reached) or self.test_stopped:
            if self.VERBOSE: log("Poll for finding stall position")
            self.poll_for_stall_position_found = Clock.schedule_once(lambda dt: self.stall_position_found(axis, start_pos), 1)
            return

        self.test_status_label.text = "STALL POS FOUND"
        log("Stall position found")
        self.travel_to_stall_pos[axis] = self.current_position[axis]() - start_pos
        self.back_off_and_find_position()


    # PARSE RESULTS OF EXPERIMENT ------------------------------------------------------------------------------------------

    ## POLLED EVENT, WHEN SB IS NO LONGER MOVING AND ALARMS HAVE BEEN RESET, IT WILL START THE REPOSITIONING PROCEDURE
    def sb_has_travelled_or_detected(self, dt):

        if (not self.m.state().startswith("Idle")) or self.test_stopped:
            if self.VERBOSE: log("Poll for threshold detection")
            self.poll_for_threshold_detection = Clock.schedule_once(self.sb_has_travelled_or_detected, 1)
            return

        log("SB has either completed its move command, or it has detected that a limit has been reached!")
        self.back_off_and_find_position()

    ## RECORD STALL EVENT TO SEND TO DATABASE AT END OF ALL EXPERIMENTS 
    ## NOTE THAT THIS IS ONLY CALLED IF THE TEST PASSES - WE DO NOT RECORD FAILED EXPERIMENT DATA IN THE DATABASE

    def record_stall_event(self):

        log("Record stall event")

        # Calculate feed rate at stall
        if self.indices["axis"] == 0: 
            step_rate = self.m.s.setting_100
            stall_coord = self.m.s.last_stall_x_coord

        if self.indices["axis"] == 1: 
            step_rate = self.m.s.setting_101
            stall_coord = self.m.s.last_stall_y_coord

        if self.indices["axis"] == 2: 
            step_rate = self.m.s.setting_102
            stall_coord = self.m.s.last_stall_z_coord

        step_us = float(self.m.s.last_stall_motor_step_size)
        rpm = 60.0*(1000000.0/step_us)/3200.0
        reported_feed = 3200.0 / float(step_rate) * float(rpm)

        # Example data: 
        # ["ID, "X", 6000, 150, 5999, 170, -1100.4 ]

        last_test_pass = [

            id_stage,
            self.current_axis(),
            self.feed_dict[self.current_axis()][self.indices["feed"]],
            self.threshold_dict[self.current_axis()][self.indices["threshold"]],
            reported_feed,
            self.m.s.last_stall_load,
            stall_coord
        ]

        self.stall_test_events.append(last_test_pass)

        log("Stall data: ")
        for i in range(len(self.last_test_pass)):
            log(self.stall_test_data_col_names[i] + last_test_pass[i])


    ## IF TEST PASSES, GO TO NEXT THRESHOLD (UNLESS DONE ALL THRESHOLDS IN FEED SET)

    def go_to_next_threshold(self):

        if self.indices["threshold"] + 1 < len(self.threshold_dict[self.current_axis()]):
            self.indices["threshold"] = self.indices["threshold"] + 1
            log("Next threshold index: " + self.indices["threshold"])

        else: 
            self.go_to_next_feed_set()

    # IF TEST FAILS, OR ALL THRESHOLDS TESTED FOR ONE FEED, GO TO NEXT FEED SET

    def go_to_next_feed_set(self):

        if self.indices["feed"] + 1 < len(self.feed_dict[self.current_axis()]):
            self.indices["feed"] = self.indices["feed"] + 1
            self.indices["threshold"] = 0

            log("Next feed index: " + self.indices["feed"])
            log("Next threshold index: " + self.indices["threshold"])

        else:
            self.go_to_next_axis()

    # IF AXIS COMPLETED, GO TO NEXT ONE
    ## IF ALL FEED SETS AND AXES ARE COMPLETED, 

    def go_to_next_axis(self):

        if self.indices["axis"] + 1 < len(self.axes):
            self.indices["axis"] = self.indices["axis"] + 1
            self.indices["feed"] = 0
            self.indices["threshold"] = 0

            log("Next feed index: " + self.indices["feed"])
            log("Next threshold index: " + self.indices["threshold"])
            log("Next axis index: " + self.indices["axis"])

        else: 
            self.all_tests_completed = True

    # END OF ALL TESTS ------------------------------------------------------------------------------------

    ## WHEN ALL EXPERIMENTS ARE COMPLETE, DATA CAN BE SENT, AND SETTINGS REVERTED

    def end_of_all_tests(self):

        if self.all_tests_completed:

            log("All tests completed!!")
            self.test_status_label.text = "TESTS COMPLETE"

            log("Enable soft limits and restore acceleration")
            self.m.enable_only_soft_limits()
            self.restore_acceleration()
            sleep(1)

            log("Send data")
            self.do_data_send()

            return True


    # testing

    # measurement creating & refactoring
    # set up database queries etc. 











