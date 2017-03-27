import numpy
import cv2
import threading
import time
from TimeAnalyzer import *
from picamera import PiCamera
from picamera.array import PiRGBArray
import io


class LineAnalyzer:
    def __init__(self, camera_x_resolution, camera_y_resolution, pic_format, robot):
        self.lock = threading.Lock()
        self.deviation = 0
        self.camera = PiCamera()
        self.camera.resolution = (camera_x_resolution, camera_y_resolution)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(camera_x_resolution, camera_y_resolution))
        self.pic_format = pic_format
        self.robot = robot
        self.send_info = False
        self.on_track = True
        self.manual_deviation = 0
        self.wait_for_manual_instruction = True
        self.tolerance_manual_control = 20
        self.tolerance_counter = 0

    # turn image 180 degrees
    def turn_img(self, img):
        heigth = img.shape[0]
        width = img.shape[1]
        M = cv2.getRotationMatrix2D((width / 2, heigth / 2), 180, 1)
        turned_img = cv2.warpAffine(img, M, (width, heigth))
        return turned_img

    def print_image(self, img):
        cv2.imshow('img', img)
        cv2.waitKey(0)
        return

    def crop_roi(self, img, start_x, start_y, width, height):
        turned_img = self.turn_img(img)
        resized_turned_img = turned_img[start_y:height, start_x:width]
        roi = self.turn_img(resized_turned_img)
        return roi

    def find_contours(self, roi):
        ret, thresh = cv2.threshold(roi, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    def draw_contour(self, roi, contour):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 1)
        return

    def parse_xcoordinates(self, contour):
        x_coordinates = []
        for value in contour:
            x_coordinates.append(value[0][0])
        return x_coordinates

    def calc_borderaverage(self, contour):
        x_coordinates = self.parse_xcoordinates(contour)
        border = sum(x_coordinates) / len(x_coordinates)
        print border
        return border

    def find_center_of_mass(self, img):
        time_analyzer = TimeAnalyzer("Center of Mass")
        time_analyzer.start()
        moments = cv2.moments(img, True)

        if moments['m00'] == 0:
            return 320
        center = moments['m10'] / moments['m00']

        time_analyzer.stop()

        return center

    def calculate_roi_start_height(self, height):
        return height - (height * 0.99)

    def calculate_roi_height(self, height):
        return height - (height * 0.9)

    def check_on_track(self, thresh):
        # HitMiss
        # kernel = numpy.ones((50, 50), numpy.uint8)
        # hitmiss = cv2.morphologyEx(thresh, cv2.MORPH_HITMISS, kernel)

        # Genug schwarz?
        brightness_avg = cv2.mean(thresh, mask=None)

        # Schwerpunkt Messen
        if (brightness_avg[0] > 10):
            self.on_track = True
            self.wait_for_manual_instruction = False
            self.tolerance_counter = 0
            print "Linie erkannt"
        elif (self.tolerance_counter == self.tolerance_manual_control):
            self.on_track = False
            print "Keine Linie"
        else:
            self.tolerance_counter += 1

    def set_deviation(self, middle, width):
        if (self.on_track):
            self.deviation = middle - (width / 2)
            self.deviation = numpy.int32(self.deviation).item()  # cast numpy data type to native data type
            self.deviation = self.deviation / (width / 2.0)
        else:
            if (self.wait_for_manual_instruction):
                self.robot.handbrake()
            else:
                self.deviation = self.manual_deviation

    def analyze_pipeline(self):
        time_analyzer = TimeAnalyzer("Analyze-Thread")
        for frame in self.camera.capture_continuous(self.rawCapture, format=self.pic_format, use_video_port=True):
            time_analyzer.start()
            image = frame.array
            self.rawCapture.truncate(0)

            # read greyscale image
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            height = img.shape[0]
            width = img.shape[1]

            start_x = 0
            start_y = self.calculate_roi_start_height(height)
            new_w = width
            new_h = self.calculate_roi_height(height)

            # crop ROI out of given image
            roi = self.crop_roi(img, start_x, start_y, new_w, new_h)

            brightness_limit = cv2.mean(roi, mask=None)[0] - 40

            ret, thresh = cv2.threshold(roi, 80, 255, cv2.THRESH_BINARY_INV)

            # crop white lines of image
            start_x = 1
            start_y -= 1
            new_w -= 1
            new_h -= 1

            thresh = self.crop_roi(thresh, start_x, start_y, new_w, new_h)

            cv2.imwrite("thresh.jpg", thresh)

            middle = self.find_center_of_mass(thresh)

            print "@@@@@@@@@Middle: " + str(middle)

            self.check_on_track(thresh)

            self.lock.acquire()
            self.set_deviation(middle, width)
            print "@@@@@@@@@Deviation: " + str(self.deviation)
            if not(self.wait_for_manual_instruction):
                self.robot.correct_deviation(self.deviation, self.on_track)
            self.lock.release()
            time_analyzer.stop()
            self.send_info = True
