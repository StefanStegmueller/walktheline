from Robot import *
from Motor import *
from TimeAnalyzer import *
from HttpService import *
import LineAnalyzer
import Robot
from threading import Thread
import json

class LineWalker:
    def __init__(self):
        """This method initializes and starts the whole software"""
        # Start worker processes for pattern detection
        self.settings = self.read_settings()
        self.initialize_brick_pi()
        self.robot = Robot.Robot()
        self.initialize_robot(self.settings["robot"]["standard_motor_power"])
        self.line_analyzer = LineAnalyzer.LineAnalyzer(self.settings["camera"]["camera_x_resolution"],
                                                       self.settings["camera"]["camera_y_resolution"],
                                                       self.settings["camera"]["pic_format"],
                                                       self.robot)
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

    def communicate_to_server(self):
        http_service = HttpService()
        roi_position = self.line_analyzer.calculate_roi_start_height(self.settings["camera"]["camera_x_resolution"])
        roi_height = self.line_analyzer.calculate_roi_height(self.settings["camera"]["camera_x_resolution"])
        path_position = self.line_analyzer.deviation
        on_track = self.line_analyzer.on_track
        wait_for_manual_instruction = self.line_analyzer.wait_for_manual_instruction

        url = "http://192.168.0.101/upload.php"
        file = "thresh.jpg"

        http_service.set_data(roi_position, roi_height, path_position, on_track, wait_for_manual_instruction)
        http_service.send_data(url, file)
	if not (self.line_analyzer.on_track):
        	self.line_analyzer.manual_deviation = http_service.direction
        self.line_analyzer.wait_for_manual_instruction = http_service.wait_for_manual_instruction


    @staticmethod
    def main(self):
        """This is the main loop of the LineWalker software, iterating without specified end"""
        robot = self.robot

        # Starting threads
        self.start_new_analyze_worker()

        time_analyzer = TimeAnalyzer("Main_Thread")

        # main loop
        while True:
            result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors
            if (self.line_analyzer.send_info):
                self.communicate_to_server()
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
