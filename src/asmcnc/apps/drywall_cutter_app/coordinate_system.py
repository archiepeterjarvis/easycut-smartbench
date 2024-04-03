'''
Class for handling the various coordinate systems we're using in the dwt app
'''

class CoordinateSystem(object):
    '''Class to store the coordinate system data.'''

    def __init__(self, m):
        self.m = m # Router machine instance
        self.machine_coordinates = self.MachineCoordinates(self.m)
        self.working_coordinates = self.WorkingCoordinates(self.m)
        self.drywall_tec_coordinates = self.DrywallTecCoordinates(self.machine_coordinates)
        self.drywall_tec_laser_coordinates = self.DrywallTecLaserCoordinates(self.drywall_tec_coordinates)

    class MachineCoordinates(object):
        '''Class to store the machine coordinates.'''

        def __init__(self, m):
            self.m = m
            self.x = self.m.mpos_x()
            self.y = self.m.mpos_y()
            self.z = self.m.mpos_z()

        def get_x(self):
            return self.m.mpos_x()

        def get_y(self):
            return self.m.mpos_y()

        def get_z(self):
            return self.m.mpos_z()

    class WorkingCoordinates(object):
        '''Class to store the working coordinates.'''

        def __init__(self, m):
            self.m = m
            self.x = m.wpos_x()
            self.y = m.wpos_y()
            self.z = m.wpos_z()

        def get_x(self):
            return self.m.wpos_x()

        def get_y(self):
            return self.m.wpos_y()

        def get_z(self):
            return self.m.wpos_z()

    class DrywallTecCoordinates(object):
        '''Class to store the drywall tec coordinates.'''

        def __init__(self, machine_coordinates):
            self.machine_coordinates = machine_coordinates
            self.x_delta = 0
            self.y_delta = 0
            self.z_delta = 0

        def get_x(self):
            return self.machine_coordinates.get_x() + self.x_delta

        def get_y(self):
            return self.machine_coordinates.get_y() + self.y_delta

        def get_z(self):
            return self.machine_coordinates.get_z() + self.z_delta

        def get_mx_from_dwx(self, dw_x):
            """
            Method to get the machine x-coordinate from the drywall tec x-coordinate.

            Parameters:
            dw_x (float): The drywall tec x-coordinate.

            Returns:
            float: The corresponding machine x-coordinate.
            """
            return dw_x - self.x_delta

        def get_my_from_dwy(self, dw_y):
            """
            Method to get the machine y-coordinate from the drywall tec y-coordinate.

            Parameters:
            dw_y (float): The drywall tec y-coordinate.

            Returns:
            float: The corresponding machine y-coordinate.
            """
            return dw_y - self.y_delta

        def get_mz_from_dwz(self, dw_z):
            """
            Method to get the machine z-coordinate from the drywall tec z-coordinate.

            Parameters:
            dw_z (float): The drywall tec z-coordinate.

            Returns:
            float: The corresponding machine z-coordinate.
            """
            return dw_z - self.z_delta

    class DrywallTecLaserCoordinates(object):
        '''Class to store the drywall tec coordinates (using laser as reference).'''

        def __init__(self, dwt_cooridnates):
            self.dwt_coordinates = dwt_cooridnates
            self.laser_delta_x = 0
            self.laser_delta_y = 0

        def get_x(self):
            return self.dwt_coordinates.get_x() + self.laser_delta_x

        def get_y(self):
            return self.dwt_coordinates.get_y() + self.laser_delta_y

        def get_z(self):
            return self.dwt_coordinates.get_z()

        # Methods to get machine coordinates from drywall tec laser coordinates

        def get_mx_from_dwlx(self, dwlx):
            """
            Method to get the machine x-coordinate from the drywall tec laser x-coordinate.

            Parameters:
            dwlx (float): The drywall tec laser x-coordinate.

            Returns:
            float: The corresponding machine x-coordinate.
            """
            return self.dwt_coordinates.get_mx_from_dwx(dwlx - self.laser_delta_x)

        def get_my_from_dwly(self, dwly):
            """
            Method to get the machine y-coordinate from the drywall tec laser y-coordinate.

            Parameters:
            dwly (float): The drywall tec laser y-coordinate.

            Returns:
            float: The corresponding machine y-coordinate.
            """
            return self.dwt_coordinates.get_my_from_dwy(dwly - self.laser_delta_y)

        def get_mz_from_dwlz(self, dwlz):
            """
            Method to get the machine z-coordinate from the drywall tec laser z-coordinate.

            Parameters:
            dwlz (float): The drywall tec laser z-coordinate.

            Returns:
            float: The corresponding machine z-coordinate.
            """
            return self.dwt_coordinates.get_mz_from_dwz(dwlz)