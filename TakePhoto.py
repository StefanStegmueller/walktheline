import picamera
import cv2

camera = picamera.PiCamera()
img = camera.capture('image.jpg')
cv2.imwrite('test.jpg', img)
