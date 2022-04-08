import imutils
import cv2 as cv

class ImageTransformation:
    def __init__(self):
        pass
    
    @staticmethod
    def resize(image, width):
        return imutils.resize(image, width=width)

    @staticmethod
    def rotate(image, angle):
        return imutils.rotate(image, angle=angle)

    @staticmethod
    def horizontalFlip(image):
        return cv.flip(image, 1)

    @staticmethod
    def adjust_brightness(image, brightness):
        return imutils.adjust_brightness_contrast(image, brightness)
