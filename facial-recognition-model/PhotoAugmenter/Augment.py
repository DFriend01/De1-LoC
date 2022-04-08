from PhotoAugmenter.ImageTransformation import ImageTransformation
import os
import string
import random
import cv2 as cv

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

def saveImage(image, outdir):
    path = generateImagePath(outdir)
    cv.imwrite(path, image)

def augment(imgpath, outdir):

    image = cv.imread(imgpath)
    resized = ImageTransformation.resize(image, IMAGE_WIDTH)

    saveImage(resized, outdir)
    saveImage(ImageTransformation.horizontalFlip(resized), outdir)
    saveImage(ImageTransformation.rotate(resized, ROTATION_ANGLE_DEG), outdir)
    saveImage(ImageTransformation.rotate(resized, -ROTATION_ANGLE_DEG), outdir)
    #saveImage(ImageTransformation.adjust_brightness(resized, BRIGHTNESS_WEIGHT1), outdir)
    saveImage(ImageTransformation.adjust_brightness(resized, BRIGHTNESS_WEIGHT2), outdir)
    #saveImage(ImageTransformation.adjust_brightness(resized, BRIGHTNESS_WEIGHT3), outdir)
    #saveImage(ImageTransformation.adjust_brightness(resized, BRIGHTNESS_WEIGHT4), outdir)
    saveImage(ImageTransformation.adjust_brightness(resized, BRIGHTNESS_WEIGHT5), outdir)
    #saveImage(ImageTransformation.adjust_brightness(resized, BRIGHTNESS_WEIGHT6), outdir)
