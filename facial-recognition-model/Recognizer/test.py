from detect import Detector
from embedder import Embedder
import os

imgpath = os.path.join('test_photos', 'L2A_Group_Photo.jpg')

detector = Detector()

if detector.detectFace(imgpath):
    box = detector.getBoundingBox()
    image = detector.getImage()

    print(Embedder.extractEmbeddings(image, box))
