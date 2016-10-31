import numpy
import cv2

img = cv2.imread('2016-05-14-04.08.10.bmp',0)

height, width, channels = img.shape

x = width / 2
y = height / 2
w = 500
h = 500

rect=[x,y,w,h]

roi= numpy.zeros((rect[3],rect[2],3),numpy.uint8)
cv2.rectangle(img,(x,y),(w+x,h+y),[255,0,0],thickness=1)

cv2.imshow('image',img)
cv2.waitKey(0)
