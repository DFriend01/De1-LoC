from .Recognizer.detect import Detector
from .Recognizer.embedder import Embedder
import pickle
import os

MODELDIR = 'model'
MODEL_FILENAME = 'model'

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
    modelpath = os.path.join(os.path.dirname(__file__), MODELDIR, MODEL_FILENAME)
    file = open(modelpath, 'rb')
    model = pickle.load(file)
    file.close()
    pred, conf = model.eval(embedding)
    return pred, conf


def evalModel(image, actual_uid):
    embedding = getEmbedding(image)
    if embedding is not None:
        pred, conf = classify(embedding)
        return (pred == actual_uid) and conf
    else:
        return False
