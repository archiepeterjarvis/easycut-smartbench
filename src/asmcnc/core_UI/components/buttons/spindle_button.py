import os
from functools import partial

from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty

from asmcnc.core_UI import path_utils
from asmcnc.core_UI.components.buttons.button_base import ImageButtonBase
from asmcnc.core_UI.components.widgets.blinking_widget import BlinkingWidget

SKAVA_UI_PATH = path_utils.get_path("skavaUI")[0]  # bug with get_path currently returns a list
SKAVA_UI_IMG_PATH = os.path.join(SKAVA_UI_PATH, "img")
SPINDLE_ON_IMAGE = os.path.join(SKAVA_UI_IMG_PATH, "spindle_on.png")
SPINDLE_OFF_IMAGE = os.path.join(SKAVA_UI_IMG_PATH, "spindle_off.png")


class SpindleButton(ImageButtonBase, BlinkingWidget):
    """A custom button widget used for spindle functionality."""

    source = StringProperty(SPINDLE_OFF_IMAGE)
    allow_stretch = BooleanProperty(True)

    def __init__(self, router_machine, serial_connection, screen_manager, **kwargs):
        super(SpindleButton, self).__init__(**kwargs)

        self.router_machine = router_machine
        self.serial_connection = serial_connection
        self.screen_manager = screen_manager

        self.serial_connection.bind(spindle_on=self.__on_spindle_on)
        self.bind(on_press=self.__on_press)

    def __on_press(self, *args):
        """
        Handles what happens when the button is pressed.
        If the spindle is off, it shows the safety popup.
        If the spindle is on, it turns it off.

        :return: None
        """
        if not self.serial_connection.spindle_on:
            self.screen_manager.pm.show_spindle_safety_popup(None, self.router_machine.turn_on_spindle)
        else:
            self.router_machine.turn_off_spindle()

    def __on_spindle_on(self, instance, value):
        """
        Callback for the spindle_on event. Changes the button image and starts/stops the blinking.
        The call to Clock.schedule_once is necessary because otherwise the image would not update.

        :param instance: the instance of the variable that changed
        :param value: the new value of the spindle_on property from SerialConnection
        :return: None
        """
        Clock.schedule_once(partial(self.__update_image_source, value))
        self.blinking = value

    def __update_image_source(self, value, *args):
        """
        Updates the spindle image based on the spindle_on property of the SerialConnection.

        :param value: the new value of the spindle_on property from SerialConnection
        :param args: unused dt parameter from Clock
        :return: None
        """
        self.source = SPINDLE_ON_IMAGE if value else SPINDLE_OFF_IMAGE
