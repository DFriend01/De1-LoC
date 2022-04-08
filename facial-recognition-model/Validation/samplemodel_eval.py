import os
import sys
import cv2 as cv
import pickle
import argparse

SPACE_UNICODE = 32

# Append path so we can access parent folders
sys.path.append('../')

from Recognizer.detect import Detector
from Recognizer.embedder import Embedder
from Classifier.RandomForest import RandomForest

# https://answers.opencv.org/question/196531/how-can-i-take-multiple-pictures-with-one-button-press/
def getImageByCamera():

    # Open the camera
    camera = cv.VideoCapture(0)
    if not camera.isOpened():
        raise Exception("The camera did not open")

    # Wait for the user to take the picture
    while True:

        isReturned, image = camera.read()

        if isReturned:
            cv.imshow('Camera', image)

            if cv.waitKey(1) & 0xFF == SPACE_UNICODE:
                camera.release()
                cv.destroyAllWindows()
                return image

def getEmbedding(image):
    detector = Detector()

    if detector.detectFace(img=image):
        box = detector.getBoundingBox()
        img = detector.getImage()
        embedding = Embedder.extractEmbeddings(img, box)
        return embedding
    else:
        return None

def classify(embedding):
    file = open('samplemodel/model', 'rb')
    model = pickle.load(file)
    file.close()
    pred, conf = model.eval(embedding)
    return pred, conf

if __name__ == '__main__':
    assert os.path.exists('samplemodel/model')

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="Path to input image on disk")

    args = parser.parse_args()

    if args.image:
        image = cv.imread(args.image)
    else:
        image = getImageByCamera()

    embedding = getEmbedding(image)

    if embedding is None:
        print("Face Not Detected")
    else:
        pred, conf = classify(embedding)
        if(not conf):
            print("Person: U")
        else:
            print(f"Person: {pred}")
