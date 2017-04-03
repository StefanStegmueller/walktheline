import numpy
from SettingsParser import *
from BrickPi import *  # import BrickPi.py file to use BrickPi operations

# This class is an abstract representation of a Robot, consisting of sensors and actors
class Robot:
    """This class is an abstract representation of a Robot, consisting of sensors and actors"""

    def __init__(self):
        self.__motors = []
        self.__sensors = []
        self.__standard_motor_power = SettingsParser.get_value("robot", "standard_motor_power")

    def set_motors(self, motor_list):
        self.__motors = motor_list

    def set_sensors(self, sensor_list):
        self.__sensors = sensor_list

    def set_standard_motor_power(self, power):
        self.__standard_motor_power = power

    def set_motor_power(self, position, motor_power_level):
        motor_power_level = numpy.int32(motor_power_level).item()
        for each_motor in self.__motors:
            if each_motor.get_position() == position:
                each_motor.set_power(motor_power_level)

    def get_motor_power(self, position):
        for each_motor in self.__motors:
            if each_motor.get_position() == position:
                each_motor.get_power()

    def set_both_motor_powers(self, motor_power_level):
        motor_power_level = numpy.int32(motor_power_level).item()
        for each_motor in self.__motors:
            BrickPi.MotorSpeed[each_motor.get_port()] = motor_power_level

    def drive_backwards(self, seconds, motor_power_level):
        """Let the robot drive backwards for a given amount of seconds"""
        if motor_power_level > 0:
            motor_power_level = -motor_power_level
        self.set_both_motor_powers(motor_power_level)

        start_time = time.time()
        while time.time() - start_time < seconds:
            BrickPiUpdateValues()
            time.sleep(0.1)

    def drive_forward(self, seconds, motor_power_level):
        """Let the robot drive forward for a given amount of seconds"""
        if motor_power_level < 0:
            motor_power_level = -motor_power_level
        self.set_both_motor_powers(motor_power_level)

        ot = time.time()
        while time.time() - ot < seconds:
            BrickPiUpdateValues()
            time.sleep(0.1)

    def handbrake(self):
        """Stops the engines hard"""
        self.set_both_motor_powers(0)

    def turn_around_z_axis(self, seconds, motor_power_value):
        """Let the robot turn around the Z axis"""
        # if motor_power is negative, the robot turns to the right and if it's positive, it turns to the left
        self.set_motor_power("left", -motor_power_value)
        self.set_motor_power("right", motor_power_value)

        start_time = time.time()
        while time.time() - start_time < seconds:
            BrickPiUpdateValues()
            time.sleep(0.1)

    def correct_deviation(self, deviation):
        curve_speed_factor = 0.4
        print "+++++++++++++++++++++++++++++Deviation: " + str(deviation)
        if(deviation == -2):
            self.handbrake()
            return

        if(deviation <= 0):
            self.set_motor_power("right", self.__standard_motor_power + self.__standard_motor_power * deviation * curve_speed_factor)
        else:
            self.set_motor_power("right", self.__standard_motor_power - (deviation * self.__standard_motor_power))


        if(deviation >= 0):
            self.set_motor_power("left", self.__standard_motor_power - self.__standard_motor_power * deviation * curve_speed_factor)
        else:
            self.set_motor_power("left", self.__standard_motor_power + (deviation * self.__standard_motor_power))
	

