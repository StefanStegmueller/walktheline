import numpy
import cv2

imgSource = '2016-05-14-04.08.10.bmp'

img = cv2.imread(imgSource,0)

height = img.shape[0]
width = img.shape[1]

x = 0
y = height - 100
w = width
h = height / 20

cv2.rectangle(img,(x,y),(w+x,h+y),[255,0,0],thickness=1)

resizedImg = img[y:h, x:w]

newH = resizedImg.shape[0]
newW = resizedImg.shape[1]

print newH, newW


cv2.imshow('image',resizedImg)
cv2.waitKey(0)
