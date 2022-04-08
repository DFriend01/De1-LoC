import os
import sys
import numpy as np
from tqdm import tqdm
from imutils import paths

# Append path so we can access parent folders
sys.path.append('../')

# Imports to generate embeddings
from PhotoAugmenter.Augment import augment
from Recognizer.detect import Detector
from Recognizer.embedder import Embedder

CATEGORIES = ['other', 'Devon', 'Declan', 'Harshil', 'Aswin']
DATASET_ROOT = 'test_photos'
DATASET_PATH = 'augmented_photos'
EMBEDDINGS_ROOT = 'embeddings'
NPARRAY_EXT = '.npy'

def augmentPhotos(dataset_root, augmented_root, categories):
    if os.path.exists(augmented_root):
        return

    inpaths = [os.path.join(dataset_root, c) for c in categories]
    outpaths = [os.path.join(augmented_root, c) for c in categories]

    for path in inpaths:
        assert os.path.exists(path)
        assert os.path.isdir(path)

    for path in outpaths:
        os.makedirs(path)
    
    nimgs = 0
    for c in categories:
        nimgs += len(list(paths.list_images(os.path.join(dataset_root, c))))

    pbar = tqdm(desc='Images to Augment', total=nimgs)
    
    for inpath, outpath in zip(inpaths, outpaths):
        imagePaths = paths.list_images(inpath)

        for image in imagePaths:
            augment(imgpath=image, outdir=outpath)
            pbar.update(1)

    pbar.close()

def get_filename_without_ext(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def compute_embeddings(inpath, outpath):

    # Objects for embeddings
    detector = Detector()

    # Create the new directory to store output (throws an error if it already exists)
    os.makedirs(outpath)

    # Extract the embeddings from all the images store in "inpath"
    images = list(paths.list_images(inpath))

    # Progress bar
    nimgs = len(images)
    pbar = tqdm(desc='Embedding Computation', total=nimgs)

    for imagepath in images:
        
        if detector.detectFace(imgpath=imagepath):
            box = detector.getBoundingBox()
            image = detector.getImage()

            embedding = Embedder.extractEmbeddings(image, box)

            if embedding is not None:
                filename = get_filename_without_ext(imagepath) + NPARRAY_EXT
                arrpath = os.path.join(outpath, filename)
                np.save(arrpath, embedding)

        pbar.update(1)

    pbar.close()

if __name__ == '__main__':
    # Generate augmented dataset
    augmentPhotos(
        dataset_root=DATASET_ROOT,
        augmented_root=DATASET_PATH,
        categories=CATEGORIES
    )

    pbar = tqdm(desc='Categories Completed', total=len(CATEGORIES))

    # Calculate the embeddings for each photo
    for category in CATEGORIES:
        inpath = os.path.join(DATASET_PATH, category)
        outpath = os.path.join(EMBEDDINGS_ROOT, category)
        compute_embeddings(inpath, outpath)
        pbar.update(1)

    pbar.close()
