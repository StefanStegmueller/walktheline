import threading

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

import TimeAnalyzer
from SettingsParser import *


class LineAnalyzer:
    def __init__(self):
        camera_x_resolution = SettingsParser.get_value("camera", "camera_x_resolution")
        camera_y_resolution = SettingsParser.get_value("camera", "camera_y_resolution")
        pic_format = SettingsParser.get_value("camera", "pic_format")
        self.__lock = threading.Lock()
        self.__camera = PiCamera()
        self.__camera.resolution = (camera_x_resolution, camera_y_resolution)
        self.__camera.framerate = 32
        self.__rawCapture = PiRGBArray(self.__camera, size=(camera_x_resolution, camera_y_resolution))
        self.__pic_format = pic_format
        self.__send_info = False
        self.__on_track = True
        self.__middle = 0

    def clear_send_info(self):
        self.__send_info = False

    def can_send_info(self):
        return self.__send_info

    def get_middle(self):
        return self.__middle

    def get_on_track(self):
        return self.__on_track

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
        moments = cv2.moments(img, True)

        if moments['m00'] == 0:
            return 320
        center = moments['m10'] / moments['m00']

        return center

    def calculate_roi_start_height(self, height):
        return height - (height * 0.99)

    def calculate_roi_height(self, height):
        return height - (height * 0.9)

    def check_on_track(self, thresh, lowest_brightness_average):

        # Genug schwarz?
        brightness_avg = cv2.mean(thresh, mask=None)

        # Schwerpunkt Messen
        if (brightness_avg[0] > lowest_brightness_average):
            self.__on_track = True
            print "Linie erkannt"
        else:
            self.__on_track = False
            print "Keine Linie"

    def analyze_pipeline(self):
        time_analyzer = TimeAnalyzer.TimeAnalyzer("Analyze-Thread")
        factor_for_average_brightness = SettingsParser.get_value("camera", "factor_for_average_brightness")
        lowest_brightness_average = SettingsParser.get_value("camera", "lowest_brightness_average")
        for frame in self.__camera.capture_continuous(self.__rawCapture, format=self.__pic_format, use_video_port=True):
            time_analyzer.start()
            image = frame.array
            self.__rawCapture.truncate(0)

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

            brightness_limit = cv2.mean(roi, mask=None)[0] * factor_for_average_brightness

            ret, thresh = cv2.threshold(roi, brightness_limit, 255, cv2.THRESH_BINARY_INV)

            # crop white lines of image
            start_x = 1
            start_y -= 1
            new_w -= 1
            new_h -= 1

            thresh = self.crop_roi(thresh, start_x, start_y, new_w, new_h)

            cv2.imwrite("thresh.jpg", thresh)

            self.__lock.acquire()

            self.__middle = self.find_center_of_mass(thresh)

            self.check_on_track(thresh, lowest_brightness_average)

            self.__lock.release()

            time_analyzer.stop()

            self.__send_info = True
