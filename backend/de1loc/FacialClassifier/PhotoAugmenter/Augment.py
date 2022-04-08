from .ImageTransformation import ImageTransformation
import os
import string
import random

SAMPLE_CHARS = string.ascii_letters + string.digits
IMAGE_EXT = '.jpg'
IMAGE_NAME_MIN_LEN = 10
IMAGE_NAME_MAX_LEN = 50

IMAGE_WIDTH = 600
ROTATION_ANGLE_DEG = 5

BRIGHTNESS_WEIGHT1 = 10.0
BRIGHTNESS_WEIGHT2 = 25.0
BRIGHTNESS_WEIGHT3 = 50.0
BRIGHTNESS_WEIGHT4 = -10.0
BRIGHTNESS_WEIGHT5 = -25.0
BRIGHTNESS_WEIGHT6 = -50.0

# https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python
def generateImagePath(outdir):
    img_name_len = random.randint(IMAGE_NAME_MIN_LEN, IMAGE_NAME_MAX_LEN)
    img_name = ''.join(random.choice(SAMPLE_CHARS) for i in range(img_name_len))
    img_name += IMAGE_EXT
    return os.path.join(outdir, img_name)

def resize(image):
    return ImageTransformation.resize(image, IMAGE_WIDTH)

def augment(image):
    augmented_images = []
    resized = resize(image)

    augmented_images.append(resized)
    augmented_images.append(ImageTransformation.horizontalFlip(resized))
    augmented_images.append(ImageTransformation.rotate(resized, ROTATION_ANGLE_DEG))
    augmented_images.append(ImageTransformation.rotate(resized, -ROTATION_ANGLE_DEG))
    augmented_images.append(ImageTransformation.adjust_brightness(resized, BRIGHTNESS_WEIGHT2))
    augmented_images.append(ImageTransformation.adjust_brightness(resized, BRIGHTNESS_WEIGHT5))
    
    return augmented_images
