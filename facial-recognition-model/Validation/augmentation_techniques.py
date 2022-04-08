import os
import sys
import numpy as np
import random
import pandas as pd
from tqdm import tqdm
from imutils import paths

DATASET_ROOT = 'test_photos'  # Directory containing test photos
NUM_PHOTOS = 20               # Number of photos to test on
TRANSFORMATIONS = ['Rotation', 'Horizontal Flip', 'Brighter Image', 'Darker Image']
IMG_WIDTH = 600

ROTATION_ANGLE = 5 # Rotation angle in degrees
BRIGHTNESS = 10.0

# Append path so we can access parent folders
sys.path.append('../')

# Imports from parent directory
from Recognizer.detect import Detector
from Recognizer.embedder import Embedder
from PhotoAugmenter.ImageTransformation import ImageTransformation

# Select random images from the test dataset
images = list(paths.list_images(DATASET_ROOT))
image_idx_rand = [random.randint(0, len(images)-1) for i in range(NUM_PHOTOS)]

# Define list to store data in
results = []

# Define face detection objects
detector = Detector()

# Computes relative error of the norms between two values relative to the first norm
def diffNorm(first, second):
    return np.linalg.norm(first - second)

# Get the embeddings
def compute_embeddings(imagepath=None, img=None):
    detected = detector.detectFace(imgpath=imagepath) if (img is None) else detector.detectFace(img=img)
    if detected:
        box = detector.getBoundingBox()
        image = detector.getImage()
        return Embedder.extractEmbeddings(image, box)
    else:
        return None

# Progress bar
pbar = tqdm(desc='Augmentations', total=len(TRANSFORMATIONS))

# Evaluate Rotations
sum = 0
length = NUM_PHOTOS
for i in image_idx_rand:
    actual_embedding = compute_embeddings(imagepath=images[i])
    rotated = ImageTransformation.rotate(detector.getImage(), ROTATION_ANGLE)
    rotation_embedding = compute_embeddings(img=rotated)
    if rotation_embedding is not None:
        sum += diffNorm(actual_embedding, rotation_embedding)
    else:
        length -= 1
results.append(sum / length)
pbar.update(1)

# Evaluate Horizontal Flip
sum = 0
length = NUM_PHOTOS
for i in image_idx_rand:
    actual_embedding = compute_embeddings(imagepath=images[i])
    flipped = ImageTransformation.horizontalFlip(detector.getImage())
    flip_embedding = compute_embeddings(img=flipped)
    if flip_embedding is not None:
        sum += diffNorm(actual_embedding, flip_embedding)
    else:
        length -= 1
results.append(sum / length)
pbar.update(1)

# Evaluate lighter image
sum = 0
length = NUM_PHOTOS
for i in image_idx_rand:
    actual_embedding = compute_embeddings(imagepath=images[i])
    brightness = ImageTransformation.adjust_brightness(detector.getImage(), -BRIGHTNESS)
    brightness_embedding = compute_embeddings(img=brightness)
    if brightness_embedding is not None:
        sum += diffNorm(actual_embedding, brightness_embedding)
    else:
        length -= 1
results.append(sum / length)
pbar.update(1)

# Evaluate darker image
sum = 0
length = NUM_PHOTOS
for i in image_idx_rand:
    actual_embedding = compute_embeddings(imagepath=images[i])
    brightness = ImageTransformation.adjust_brightness(detector.getImage(), -BRIGHTNESS)
    brightness_embedding = compute_embeddings(img=brightness)
    if brightness_embedding is not None:
        sum += diffNorm(actual_embedding, brightness_embedding)
    else:
        length -= 1
results.append(sum / length)
pbar.update(1)

pbar.close()

# Save the results
if not os.path.exists('results/'):
    os.makedirs('results/')

df = pd.DataFrame([results], index=['Average Relative Errors'], columns=TRANSFORMATIONS)
df.to_csv('results/augmentation_results.csv')
