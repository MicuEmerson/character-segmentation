import os
import cv2
from skimage.feature import hog

# compute HOG for image
def get_character_hog_metrics(path):
    image = cv2.imread(path)
    return hog(image, orientations=9, pixels_per_cell=(2, 2),
               cells_per_block=(1, 1), multichannel=True)


# compute HOG for every image in the folder
def get_data(dir_name):
    result = []
    character_image_names = os.listdir(dir_name)

    for file_name in character_image_names:
        path = dir_name + str(file_name)
        character_metrics = get_character_hog_metrics(path)
        result.append(character_metrics)

    return result