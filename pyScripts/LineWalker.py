#!/usr/bin/env python
# Original Authors: Markus Germann, Markus Barthel, Marc Aurel Hildinger
# Initial Date: 19.11.2015
# BRICKPI LEGO EV3 TOUCH SENSOR MOTOR
############################################
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# NOTE: This program is in PRE-ALPHA now
# 
# This example will show you how to use the LEGO EV3 Touch sensor with the BrickPi for stopping the motors on contact.  
#
# This program uses the touch sensor.  The analog values of the 6th line are read (SDA/Blue Line) and then filtered.
#
# This code is for initial testing purpose
#
# import BrickPi as BrickPi
from BrickPi import *  # import BrickPi.py file to use BrickPi operations
from Robot import *
from RotationTower import *
import LineAnalyzer
import Robot
import os
from threading import Thread
import threading

# from BrickPi.BrickPi import PORT_C, PORT_B, PORT_3, PORT_2, BrickPiSetup, BrickPiSetupSensors


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(APP_ROOT, 'web/watchdog-status.txt')

class LineWalker:
    """This class represents the whole software architecture with the main loop"""

    @staticmethod
    def initialize_brick_pi():
        # setup the serial port for communication
        BrickPiSetup()

        BrickPi.MotorEnable[PORT_B] = 1  # Enable the Motor B
        BrickPi.MotorEnable[PORT_C] = 1  # Enable the Motor A

        BrickPi.MotorEnable[PORT_A] = 1 # Enable the Motor D for the rotation tower

        # Send the properties of sensors to BrickPi. Set up the BrickPi
        BrickPiSetupSensors()
        # There's often a long wait for setup with the EV3 sensors.  Up to 5 seconds.

    def initialize_robot(self):
        left_motor = Motor(PORT_B, "left")
        right_motor = Motor(PORT_C, "right")
        self.robot.set_motors([left_motor, right_motor])

        self.rotating_camera_tower = RotationTower(PORT_A, "rotating_camera_tower", self.robot)

    @staticmethod
    def main(self):
        """This is the main loop of the WATCHDOG software, iterating without specified end"""
        power = 200  # power level with which the motors run, if the run forward
        distance_on_collision = 1.5  # seconds to drive backwards on touch collision
        speed_on_collision = power/2  # power level with which the motors run backwards on touch collision
        amount_of_pattern_detection_threads = 1
        speed_on_turn = speed_on_collision + speed_on_collision/2

        self.on_hold = False
        self.on_hold_counter = 0
        self.on_hold_counter_threshold = 50

        robot = self.robot

        #main loop
        while True:
            result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors
            if not result:
                if self.on_hold:
                    robot.handbrake()
                else:
                    robot.set_both_motor_powers(power)

                # One additional active thread is the main thread
                if threading.active_count() < amount_of_pattern_detection_threads + 1: #start new line detection thread if broken
                    self.start_new_line_worker()

                self.robot.correct_deviation(self.line_analyzer.deviation, self.camera_x_resolution, power)

                time.sleep(0.01)  # sleep for 10ms

    def start_new_line_worker(self):
        print "Starting new worker"
        line_detection_thread = Thread(target=self.line_analyzer.analyze())
        line_detection_thread.start()

    def __init__(self):
        """This method initializes and starts the whole software"""
        # Start worker processes for pattern detection
        self.camera_x_resolution = 640
        self.camera_y_resolution = 480
        self.initialize_brick_pi()
        self.robot = Robot.Robot()
        self.line_analyzer = LineAnalyzer.LineAnalyzer(self.camera_x_resolution, self.camera_y_resolution)
        self.already_rotated_tower = False
        self.initialize_robot()
        self.main(self)


#######################################################
# END OF FUNCTION DEFINITIONS /// BEGINNING OF MAIN ###
#######################################################
lineWalker = LineWalker()
