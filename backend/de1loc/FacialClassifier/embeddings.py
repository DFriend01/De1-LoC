import os
import string
import random
import numpy as np

from .PhotoAugmenter.Augment import augment
from .Recognizer.detect import Detector
from .Recognizer.embedder import Embedder

SAMPLE_CHARS = string.ascii_letters + string.digits
NPARRAY_EXT = '.npy'
EMBEDDING_NAME_MIN_LEN = 10
EMBEDDING_NAME_MAX_LEN = 50

# https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python
def genEmbeddingFilename():
    emb_name_len = random.randint(EMBEDDING_NAME_MIN_LEN, EMBEDDING_NAME_MAX_LEN)
    emb_name = ''.join(random.choice(SAMPLE_CHARS) for _ in range(emb_name_len))
    emb_name += NPARRAY_EXT
    return emb_name

def compute_embeddings(image, user_id):

    # Make the directory to store embeddings if it does not exist yet
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'embeddings', str(user_id))):
        os.makedirs(os.path.join(os.path.dirname(__file__), 'embeddings', str(user_id)))

    # Get the augmented images
    augmented_images = augment(image)

    # Compute the embeddings for each image and save it on disk
    detector = Detector()
    for img in augmented_images:
        if detector.detectFace(img=img):
            box = detector.getBoundingBox()
            detector_image = detector.getImage()

            embedding = Embedder.extractEmbeddings(detector_image, box)

            if embedding is not None:
                filename = genEmbeddingFilename()
                np.save(os.path.join(os.path.dirname(__file__), 'embeddings', str(user_id), filename), embedding)
