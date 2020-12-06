import os
import cv2
import numpy as np

SIZE = (50, 50)

# resize images to a certain SIZE
def resize(DIR_NAME, RESULT_DIR_NAME):
    character_image_names_1 = os.listdir(DIR_NAME)
    max_height = 100
    max_width = 100

    for file_name in character_image_names_1:
        base_image = np.zeros((max_height, max_width))
        original_img = cv2.imread(DIR_NAME + file_name, cv2.IMREAD_GRAYSCALE)
        height, width = original_img.shape
        start_row = (max_height - height) // 2
        end_row = start_row + height
        start_column = (max_width - width) // 2
        end_column = start_column + width

        if height > max_height or width > max_width:
            continue

        for i in range(start_row, end_row):
            for j in range(start_column, end_column):
                base_image[i][j] = original_img[i - start_row][j - start_column]

        resized_image = cv2.resize(base_image, SIZE)
        cv2.imwrite(RESULT_DIR_NAME + file_name, resized_image)