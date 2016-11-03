import numpy
import cv2

def turn_img(img):
    width = img.shape[0]
    height = img.shape[1] #height and width are switched
    M = cv2.getRotationMatrix2D((height / 2, width / 2), 180, 1)
    turned_img = cv2.warpAffine(img, M, (height, width))
    return turned_img

def print_image(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    return

def crop_roi(img, start_x, start_y, width, height):
    turned_img = turn_img(img)
    resized_turned_img = turned_img[start_y:height, start_x:width]
    roi = turn_img(resized_turned_img)
    return roi


imgSource = '2016-05-14-04.08.10.bmp'

img = cv2.imread(imgSource,0)

height = img.shape[0]
width = img.shape[1]

start_x = 0
start_y = height -(height * 0.99)
new_w = width
new_h = height - (height * 0.9)

roi = crop_roi(img, start_x, start_y, new_w, new_h)

print_image(roi)

