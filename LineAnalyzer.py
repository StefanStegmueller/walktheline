import numpy
import cv2

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

    def draw_rectangles_on_line(self, roi, contours):
        for cont in contours:
            moment = cv2.moments(cont)
            if(moment['m00'] > 0):
                x, y, w, h = cv2.boundingRect(cont)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return

    def analyze(self):
        imgSource = '2016-05-14-04.08.34.bmp'

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
        gray = cv2.bilateralFilter(roi, 11, 17, 17)
        #detect edges
        edged = cv2.Canny(gray, 30, 200)

        contours, hierarchy = self.find_contours(edged)

        self.draw_rectangles_on_line(roi, contours)

        #cv2.drawContours(roi, contours, -1, (0, 255, 0), 3)

        self.print_image(roi)
        return


    def __init__(self):
        self.analyze()
        return



#######################################################
# END OF FUNCTION DEFINITIONS /// BEGINNING OF MAIN ###
#######################################################
lineAnalyzer = LineAnalyzer()


