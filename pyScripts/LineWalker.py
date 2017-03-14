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
from Motor import *
from TimeAnalyzer import *
import LineAnalyzer
import Robot
import os
from threading import Thread
import threading
import json
import requests

# from BrickPi.BrickPi import PORT_C, PORT_B, PORT_3, PORT_2, BrickPiSetup, BrickPiSetupSensors


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class LineWalker:

    def __init__(self):
        """This method initializes and starts the whole software"""
        # Start worker processes for pattern detection
        self.settings = self.read_settings()
        self.initialize_brick_pi()
        self.robot = Robot.Robot()
        self.line_analyzer = LineAnalyzer.LineAnalyzer(self.settings["camera"]["camera_x_resolution"],
                                                       self.settings["camera"]["camera_y_resolution"],
                                                       self.settings["camera"]["pic_format"],
						       self.robot)
        self.initialize_robot(self.settings["robot"]["standard_motor_power"])
        self.main(self)

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

        # Send the properties of sensors to BrickPi. Set up the BrickPi
        BrickPiSetupSensors()
        # There's often a long wait for setup with the EV3 sensors.  Up to 5 seconds.

    def initialize_robot(self, standard_power):
        right_motor = Motor(PORT_B, "right")
        left_motor = Motor(PORT_C, "left")
        self.robot.set_motors([left_motor, right_motor])
        self.robot.standard_motor_power = standard_power

    def send_info(self):
        json = {
            "roi_position" : self.line_analyzer.calculate_roi_start_height(self.settings["camera"]["camera_x_resolution"]),
            "roi_height" : self.line_analyzer.calculate_roi_height(self.settings["camera"]["camera_x_resolution"]),
            "path_position" : self.line_analyzer.deviation,
            "path_width" : 0
        }
        url = "http://192.168.0.101/upload.php"
        files = {'file': open('thresh.jpg')}
        response = requests.post(url, files = files,  data = json)

    @staticmethod
    def main(self):
        """This is the main loop of the LineWalker software, iterating without specified end"""
        robot = self.robot

        # Starting threads
        self.start_new_analyze_worker()

        time_analyzer = TimeAnalyzer("Main_Thread")

        #main loop
        while True:
            result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors
            if(self.line_analyzer.send_info):
                self.send_info()
                self.line_analyzer.send_info = False

    def start_new_analyze_worker(self):
        print "Starting new analyze worker"
        line_detection_thread = Thread(target=self.line_analyzer.analyze_pipeline)
        line_detection_thread.daemon = True
        line_detection_thread.start()



#######################################################
# END OF FUNCTION DEFINITIONS /// BEGINNING OF MAIN ###
#######################################################
lineWalker = LineWalker()
