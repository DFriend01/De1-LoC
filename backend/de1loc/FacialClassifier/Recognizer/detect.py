import cv2 as cv
import os
import imutils
import numpy as np

# Model paths
MODELPATH = os.path.join(os.path.dirname(__file__), 'FaceDetector', 'opencv_face_detector.caffemodel')
PROTOPATH = os.path.join(os.path.dirname(__file__), 'FaceDetector', 'opencv_face_detector.prototxt')
CONFIDENCE = 0.7
IMAGE_WIDTH = 600

# https://pyimagesearch.com/2018/09/24/opencv-face-recognition/
class Detector:
    def __init__(self, modelpath=MODELPATH, protopath=PROTOPATH, imgwidth=IMAGE_WIDTH, confidence=CONFIDENCE):
        self.__model = cv.dnn.readNetFromCaffe(protopath, modelpath)
        self.__imgwidth = imgwidth
        self.__confidence = confidence

        self.__box = None
        self.__image = None

    def detectFace(self, imgpath=None, img=None):

        # Load the image
        if img is None:
            image = cv.imread(imgpath)
        elif imgpath is None:
            image = img
        else:
            return False

        image = imutils.resize(image, width=self.__imgwidth)

        (h, w) = image.shape[:2]

        # Construct a blob from the image
        imgBlob = cv.dnn.blobFromImage(
            cv.resize(image, (300, 300)),
            1.0,
            (300, 300),
            (104.0, 177.0, 123.0),
            swapRB=False,
            crop=False
        )

        # Apply the model to detect faces
        self.__model.setInput(imgBlob)
        detections = self.__model.forward()

        if len(detections) > 0:
            
            # Get the detection that we are the most confident about
            i = np.argmax(detections[0, 0, :, 2])
            confidence = detections[0, 0, i, 2]

            if confidence > self.__confidence:
            
                # Compute the (x, y) coordinates for the bounding box
                box = detections[0, 0, i, 3:7] * np.array([w,h,w,h])
                (left, top, right, bottom) = box.astype('int')

                # Swap order to work with the embedder properly
                self.__box = (top, right, bottom, left)

                # Swap colour channels for image
                self.__image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

                return True

            else:
                return False

        else:
            return False

    def getBoundingBox(self):
        return self.__box

    def getImage(self):
        return self.__image
