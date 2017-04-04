import numpy

import AutoController
import Motor
import Robot
from BrickPi import *
from SettingsParser import *


class Controller:

    def __init__(self):
        self.initialize_brick_pi()
        self.__robot = Robot.Robot()
        self.initialize_robot()
        self.__auto_controller = AutoController.AutoController()
        self.__standard_motor_power = SettingsParser.get_value("robot", "standard_motor_power")
        self.__manual_motor_power = SettingsParser.get_value("robot", "manual_motor_power")
        self.__width = SettingsParser.get_value("camera", "camera_x_resolution")
        self.__tolerance_manual_control = SettingsParser.get_value("camera", "tolerance_manual_control")
        self.__tolerance_counter = 0
        self.__deviation

    def get_deviaton(self):
        return self.__deviation

    def initialize_robot(self):
        right_motor = Motor.Motor(PORT_B, "right")
        left_motor = Motor.Motor(PORT_C, "left")
        self.__robot.set_motors([left_motor, right_motor])

    @staticmethod
    def initialize_brick_pi():
        # setup the serial port for communication
        BrickPiSetup()

        BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
        BrickPi.MotorEnable[PORT_C] = 1  # Enable the Motor A

        # Send the properties of sensors to BrickPi. Set up the BrickPi
        BrickPiSetupSensors()
        # There's often a long wait for setup with the EV3 sensors.  Up to 5 seconds.

    def controll_robot(self, middle, on_track, manual_direction):
        deviation = self.set_deviation(middle, on_track, manual_direction)
        self.__robot.correct_deviation(deviation)

    def set_deviation(self, middle, on_track, manual_direction):
        if (on_track):
            self.__robot.set_standard_motor_power(self.__standard_motor_power)
            deviation = middle - (self.__width / 2)
            deviation = numpy.int32(deviation).item()  # cast numpy data type to native data type
            deviation = deviation / (self.__width / 2.0)
            self.__deviation = deviation
            self.__tolerance_counter = 0
            return self.__auto_controller.controll_direction(deviation)
        elif(self.__tolerance_counter >= self.__tolerance_manual_control):
            self.__robot.set_standard_motor_power(self.__manual_motor_power)
            return manual_direction
        else:
            self.__tolerance_counter += 1
            return self.__auto_controller.controll_direction(self.__deviation)

