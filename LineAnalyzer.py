import numpy
import cv2

class LineAnalyzer:

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

    def analyze(self):
        imgSource = '2016-05-14-04.08.10.bmp'

        img = cv2.imread(imgSource, 0)

        height = img.shape[0]
        width = img.shape[1]

        start_x = 0
        start_y = height - (height * 0.99)
        new_w = width
        new_h = height - (height * 0.9)

        roi = self.crop_roi(img, start_x, start_y, new_w, new_h)

        self.print_image(roi)
        return


    def __init__(self):
        self.analyze()
        return



#######################################################
# END OF FUNCTION DEFINITIONS /// BEGINNING OF MAIN ###
#######################################################
lineAnalyzer = LineAnalyzer()


