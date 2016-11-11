import numpy
import cv2
import os

class LineAnalyzer:

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



    def analyze(self):
        directory = 'D:\Entwickel\walktheline\Kamera'
        success = 0
        total = 0

        for filename in os.listdir(directory):

            head, tail = os.path.split(filename)
            imgSource = 'Kamera/' + tail

            #read greyscale image
            img = cv2.imread(imgSource, 0)

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
                #self.print_image(roi)
                success = success + 1
            total = total + 1
        failed = total - success
        print 'result: total(' + str(total) + ') success(' + str(success) + ') failed(' + str(failed) + ')'
        return


    def __init__(self):
        self.analyze()
        return



#######################################################
# END OF FUNCTION DEFINITIONS /// BEGINNING OF MAIN ###
#######################################################
lineAnalyzer = LineAnalyzer()


