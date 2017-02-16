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
import json

# from BrickPi.BrickPi import PORT_C, PORT_B, PORT_3, PORT_2, BrickPiSetup, BrickPiSetupSensors


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(APP_ROOT, 'web/watchdog-status.txt')

class LineWalker:
    """This class represents the whole software architecture with the main loop"""

    def read_settings(self):
        with open('settings') as json_data_file:
            data = json.load(json_data_file)
        return data

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
        right_motor = Motor(PORT_B, "right")
        left_motor = Motor(PORT_C, "left")
        self.robot.set_motors([left_motor, right_motor])

        self.rotating_camera_tower = RotationTower(PORT_A, "rotating_camera_tower", self.robot)

    @staticmethod
    def main(self):
        """This is the main loop of the LineWalker software, iterating without specified end"""
        power = self.settings["robot"]["standard_motor_power"]  # power level with which the motors run, if the run forward
        distance_on_collision = 1.5  # seconds to drive backwards on touch collision
        speed_on_collision = power/2  # power level with which the motors run backwards on touch collision
        current_thread_count = 2
        speed_on_turn = speed_on_collision + speed_on_collision/2

        self.on_hold = False
        self.on_hold_counter = 0
        self.on_hold_counter_threshold = 50

        robot = self.robot

        print 'initialization complete'

        iteration = 0

        #main loop
        while True:
            #Analyze main thread
            start_time = time.time()
            result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors
            if not result:
                if self.on_hold:
                    robot.handbrake()
                else:
                    robot.set_both_motor_powers(power)

                # One additional active thread is the main thread
                if threading.active_count() < current_thread_count: #start new line detection thread if broken
                    self.start_new_line_worker()
                                    
                print 'start correcting deviation'
                self.robot.correct_deviation(self.line_analyzer.deviation,
                                             self.settings["robot"]["correction_tolerance"],
                                             self.settings["camera"]["camera_x_resolution"],
                                             power)
                BrickPiUpdateValues()

                time.sleep(self.settings["threads"]["main_thread_sleep_seconds"])  # sleep
                now = time.time() - start_time
                print "Runtime for one Iteration" + iteration + " in Main_Tread: " + now
                iteration += 1

    def start_new_line_worker(self):
        print "Starting new worker"
        line_detection_thread = Thread(target=self.line_analyzer.analyze_pipeline)
        line_detection_thread.daemon = True
        line_detection_thread.start()

    def __init__(self):
        """This method initializes and starts the whole software"""
        # Start worker processes for pattern detection
        self.settings = self.read_settings()
        self.initialize_brick_pi()
        self.robot = Robot.Robot()
        self.line_analyzer = LineAnalyzer.LineAnalyzer(self.settings["camera"]["camera_x_resolution"],
                                                       self.settings["camera"]["camera_y_resolution"],
                                                       self.settings["camera"]["pic_format"],
                                                       self.settings["threads"]["pic_analysis_thread_sleep_seconds"])
        self.already_rotated_tower = False
        self.initialize_robot()
        self.main(self)


#######################################################
# END OF FUNCTION DEFINITIONS /// BEGINNING OF MAIN ###
#######################################################
lineWalker = LineWalker()
