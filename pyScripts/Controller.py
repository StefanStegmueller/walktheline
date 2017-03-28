import numpy
import AutoController
from SettingsParser import *
from BrickPi import *
import Robot
import Motor

class Controller:

    def __init__(self):
        self.__deviation = 0
        self.initialize_brick_pi()
        self.__robot = Robot.Robot()
        self.initialize_robot()
        self.__auto_controller = AutoController.AutoController()
        self.__standard_motor_power = SettingsParser.get_value("robot", "standard_motor_power")
        self.__manual_motor_power = SettingsParser.get_value("robot", "manual_motor_power")

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
        width = SettingsParser.get_value("camera", "camera_x_resolution")
        self.set_deviation(middle, width, on_track, manual_direction)
        self.__robot.correct_deviation(self.__deviation)

    def set_deviation(self, middle, width, on_track, manual_direction): 
        if (on_track):
            self.__robot.standard_motor_power = self.__standard_motor_power
            self.__deviation = middle - (width / 2)
            self.__deviation = numpy.int32(self.__deviation).item()  # cast numpy data type to native data type
            self.__deviation = self.__deviation / (width / 2.0)
            self.__deviation = self.__auto_controller.controll_direction(self.__deviation)
        else:
            self.__deviation = manual_direction
            self.__robot.standard_motor_power = self.__manual_motor_power

