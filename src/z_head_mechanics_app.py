from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from asmcnc.comms.router_machine import RouterMachine
from settings.settings_manager import Settings
from asmcnc.job.job_data import JobData
from asmcnc.comms.localization import Localization
from kivy.clock import Clock
from asmcnc.comms import smartbench_flurry_database_connection

from asmcnc.skavaUI.screen_home import HomeScreen
from asmcnc.skavaUI import screen_door
from asmcnc.skavaUI import screen_error
from asmcnc.production.z_head_mechanics_jig.z_head_mechanics import ZHeadMechanics
from asmcnc.production.z_head_mechanics_jig.z_head_mechanics_monitor import ZHeadMechanicsMonitor
from asmcnc.production.z_head_mechanics_jig.z_head_mechanics_booting import ZHeadMechanicsBooting

from datetime import datetime


Cmport = 'COM3'


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + message)

class ZHeadMechanicsApp(App):
    def build(self):
        log('Starting diagnostics')

        sm = ScreenManager(transition=NoTransition())

        sett = Settings(sm)

        l = Localization()

        jd = JobData(localization = l, settings_manager = sett)

        m = RouterMachine(Cmport, sm, sett, l, jd)

        db = smartbench_flurry_database_connection.DatabaseEventManager(sm, m, sett)

        if m.s.is_connected():
            Clock.schedule_once(m.s.start_services, 4)

        home_screen = HomeScreen(name = 'home', screen_manager = sm, machine = m, job = jd, settings = sett, localization = l)
        sm.add_widget(home_screen)

        error_screen = screen_error.ErrorScreenClass(name = 'errorScreen', screen_manager = sm, machine = m, job = jd, database = db, localization = l)
        sm.add_widget(error_screen)

        door_screen = screen_door.DoorScreen(name = 'door', screen_manager = sm, machine =m, job = jd, database = db, localization = l)
        sm.add_widget(door_screen)

        z_head_mechanics = ZHeadMechanics(name = 'mechanics', sm = sm, m = m)
        sm.add_widget(z_head_mechanics)

        z_head_mechanics_monitor = ZHeadMechanicsMonitor(name = 'monitor', sm = sm, m = m, l = l)
        sm.add_widget(z_head_mechanics_monitor)

        z_head_mechanics_booting = ZHeadMechanicsBooting(name = 'booting', sm = sm, m = m)
        sm.add_widget(z_head_mechanics_booting)

        sm.current = 'booting'
        return sm

if __name__ == '__main__':
    ZHeadMechanicsApp().run()
