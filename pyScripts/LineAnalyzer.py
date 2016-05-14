import numpy
import cv2
import threading
import time
import picamera
import io

class LineAnalyzer:

    def take_a_photo(self):
        """This method takes a picture from the piCam,
        thread-lock has to be manually released after calling this method"""
        print "Analyze-Thread: Fall asleep"
        time.sleep(0.2)
        print "Analyze-Thread: Wake up"
        # Get the picture (low resolution, so it should be quite fast)
        # Here also other parameters can be specified (e.g.: rotate the image)
        with picamera.PiCamera() as camera:
            camera.resolution = (self.camera_x_resolution, self.camera_y_resolution)

            # Create a memory stream so pictures don't need to be saved in a file
            self.stream = io.BytesIO()
            camera.capture(self.stream, format='bmp')
            # Convert the picture into a numpy array
            buffer = numpy.fromstring(self.stream.getvalue(), dtype=numpy.uint8)

            # Now creates an OpenCV image
            frame = cv2.imdecode(buffer, 1)

            return frame

    #turn image 180 degrees
    def turn_img(self, img):
        width = img.shape[0]
        height = img.shape[1] #height and width are switched
        M = cv2.getRotationMatrix2D((height / 2, width / 2), 180, 1)
        turned_img = cv2.warpAffine(img, M, (height, width))
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

    def calc_borderaverage (self, contour):
        x_coordinates = self.parse_xcoordinates(contour)
        border = sum(x_coordinates) / len(x_coordinates)
        print border
        return border

    def find_middle(self, roi, contours):
        borders = []
        for contour in contours:
            moment = cv2.moments(contour)
            if(moment['m00'] > 0):
                self.draw_contour(roi, contour)
                borders.append(self.calc_borderaverage(contour))
        if(len(borders) == 2):
            middle = min(borders) + (abs(borders[0] - borders[1])/2)
        else:
            print 'More or less than two borders detected: ' + len(borders).__str__() + ' borders'
            return False
        return middle

    def analyze_pipeline(self):
        print 'Analyze-Thread: threadcount ', threading.active_count()
        # Locking down the critical section as of PiCamera only being accessible once
        self.lock.acquire()
        image = self.take_a_photo()
        self.lock.release()

        #read greyscale image
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        height = img.shape[0]
        width = img.shape[1]

        start_x = 0
        start_y = height - (height * 0.99)
        new_w = width
        new_h = height - (height * 0.9)

        #crop ROI out of given image
        roi = self.crop_roi(img, start_x, start_y, new_w, new_h)
        #smooth image
        blur = cv2.bilateralFilter(roi, 11, 17, 17)

        #detect edges
        edged = cv2.Canny(blur, 30, 200)

        contours, hierarchy = self.find_contours(edged)

        middle = self.find_middle(roi, contours)       

        #cv2.drawContours(roi, contours, -1, (0, 255, 0), 3)
        if(middle != False):
            cv2.line(roi, (middle, 0), (middle, roi.shape[0]), (255, 0, 0), 1)
            self.deviation = middle - (width / 2)
            self.deviation = numpy.int32(self.deviation).item() # cast numpy data type to native data type
        return


    def __init__(self, camera_x_resolution, camera_y_resolution):
        self.lock = threading.Lock()
        self.deviation = 0
        self.camera_x_resolution = camera_x_resolution
        self.camera_y_resolution = camera_y_resolution
        return


