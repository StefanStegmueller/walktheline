from BrickPi import *
from SettingsParser import *
import TimeAnalyzer
import HttpService
import Controller
import LineAnalyzer
from threading import Thread

class LineWalker:
    def __init__(self):
        """This method initializes and starts the whole software"""
        # Start worker processes for pattern detection
        self.line_analyzer = LineAnalyzer.LineAnalyzer()
        self.controller = Controller.Controller()
        self.main(self)

    def communicate_to_server(self, roi_position, roi_height, path_position, url, file):
        http_service = HttpService.HttpService()

        http_service.set_data(roi_position, roi_height, path_position)
        http_service.send_data(url, file)

        return http_service.get_manual_direction()

    @staticmethod
    def main(self):
        """This is the main loop of the LineWalker software, iterating without specified end"""

        # Starting threads
        self.start_new_analyze_worker()

        roi_position = self.line_analyzer.calculate_roi_start_height(SettingsParser.get_value("camera", "camera_x_resolution"))
        roi_height = self.line_analyzer.calculate_roi_height(SettingsParser.get_value("camera", "camera_x_resolution"))

        url = SettingsParser.get_value("server", "url")
        file = SettingsParser.get_value("server", "file_to_upload")

        manual_direction = -2

        # main loop
        while True:
            result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/motors
            if (self.line_analyzer.can_send_info()):
                path_position = self.controller.get_deviaton()
                manual_direction = self.communicate_to_server(roi_position, roi_height, path_position, url, file)
                self.line_analyzer.clear_send_info()
            self.controller.controll_robot(self.line_analyzer.get_middle(),
                   self.line_analyzer.get_on_track,
                   manual_direction)


    def start_new_analyze_worker(self):
        print "Starting new analyze worker"
        line_detection_thread = Thread(target=self.line_analyzer.analyze_pipeline)
        line_detection_thread.daemon = True
        line_detection_thread.start()

#######################################################
# END OF FUNCTION DEFINITIONS /// BEGINNING OF MAIN ###
#######################################################
lineWalker = LineWalker()
