from skimage import measure
import cv2
import numpy as np
import os

UPPER_PERCENT = 0.45  # used for checking upper signs above the current label
GARBAGE_PIXELS = 4  # used for ignoring labels with no. pixels lower than GARBAGE_PIXELS (noise)
UPPER_SIGN_PERCENT = 0.50  # used for checking the upper sign pixels no.

def segmentation(INPUT_DIR, OUTPUT_DIR):
    file_names = os.listdir(INPUT_DIR)

    for file_name in file_names:
        no_characters = 0
        # image processing
        image = cv2.imread(INPUT_DIR + file_name, 0)

        _, im = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU, cv2.THRESH_BINARY_INV)
        blobs = im > im.mean()
        image_matrix = measure.label(blobs, background=0)

        # precalculate labels indexes and no. of pixels
        image_matrix_height, image_matrix_width = np.shape(image_matrix)
        dictionary = {}  # label = [[top,bottom,left,right], noPixels]

        for i in range(image_matrix_height):
            for j in range(image_matrix_width):
                if image_matrix[i][j] != 0:
                    if image_matrix[i][j] not in dictionary:
                        dictionary[image_matrix[i][j]] = [[image_matrix_height, 0, image_matrix_width, 0], 0]
                    dictionary[image_matrix[i][j]][0][0] = min(dictionary[image_matrix[i][j]][0][0], i)
                    dictionary[image_matrix[i][j]][0][1] = max(dictionary[image_matrix[i][j]][0][1], i)
                    dictionary[image_matrix[i][j]][0][2] = min(dictionary[image_matrix[i][j]][0][2], j)
                    dictionary[image_matrix[i][j]][0][3] = max(dictionary[image_matrix[i][j]][0][3], j)
                    dictionary[image_matrix[i][j]][1] += 1

        # we delete labels that are below GARBAGE_PIXELS pixels (garbage characters)
        for i in range(image_matrix_height):
            for j in range(image_matrix_width):
                if image_matrix[i][j] in dictionary and dictionary[image_matrix[i][j]][1] <= GARBAGE_PIXELS:
                    del dictionary[image_matrix[i][j]]

        # compute character average pixels, width and height (used for detecting upper label signs)
        character_pixels_no = 0
        character_width = 0
        character_height = 0
        for key in dictionary:
            character_pixels_no += dictionary[key][1]
            character_width += dictionary[key][0][1] - dictionary[key][0][0]
            character_height += dictionary[key][0][3] - dictionary[key][0][2]

        character_pixels_average = character_pixels_no / len(dictionary.keys())
        character_width_average = character_width / len(dictionary.keys())
        character_height_average = character_height / len(dictionary.keys())

        # segmentation for every character
        for label in dictionary:
            label_top = dictionary[label][0][0]
            label_bottom = dictionary[label][0][1]
            label_left = dictionary[label][0][2]
            label_right = dictionary[label][0][3]

            # we search for upper signs, using UPPER_PROCENT of initial character height
            upper_number_pixels = int((label_bottom - label_top) * UPPER_PERCENT)
            upper_sign_labels = {}

            new_label_top = max(label_top - upper_number_pixels - 1, 0)
            new_label_bottom = max(label_top, 0)

            for i in range(new_label_top, new_label_bottom):
                for j in range(label_left, label_right):
                    if image_matrix[i][j] in dictionary:
                        upper_sign_labels[image_matrix[i][j]] = True

            # we check the upper labels found above your label to see if they are signs
            # and recompute the segmentation size of the character (new coordonates to top,left,right) that will include and signs
            for upper_label in upper_sign_labels:
                upper_label_pixel = dictionary[upper_label][1]
                if upper_label_pixel <= character_pixels_average * UPPER_SIGN_PERCENT:
                    upper_label_top = dictionary[upper_label][0][0]
                    upper_label_bottom = dictionary[upper_label][0][1]
                    upper_label_left = dictionary[upper_label][0][2]
                    upper_label_right = dictionary[upper_label][0][3]

                    label_top = upper_label_top
                    label_left = min(label_left, upper_label_left)
                    label_right = max(label_right, upper_label_right)

            # we extract from initial photo (matrix) only the part for current character (labeL)
            character_shape = (label_bottom - label_top + 1, label_right - label_left + 1)
            new_image = np.zeros(character_shape)

            ii = 0
            jj = 0
            total_no_pixels_for_new_img = 0
            for i in range(label_top, label_bottom + 1):
                for j in range(label_left, label_right + 1):
                    if image_matrix[i][j] == label:
                        new_image[ii][jj] = 255
                        total_no_pixels_for_new_img += 1
                    else:
                        new_image[ii][jj] = 0

                    for upper_label in upper_sign_labels:  # check for upper labels
                        if image_matrix[i][j] == upper_label:
                            new_image[ii][jj] = 255
                            total_no_pixels_for_new_img += 1
                    jj += 1
                jj = 0
                ii += 1

            new_image = np.array(new_image)

            no_characters += 1

            if total_no_pixels_for_new_img >= 50:  # remove dots
                if character_shape[0] <= character_height_average * 2.3 and character_shape[1] \
                        <= character_width_average * 1.9:
                    cv2.imwrite(OUTPUT_DIR[:-1] + "_normal/" + file_name + '_ch' + str(label) + '.png', new_image)
                else:
                    cv2.imwrite(OUTPUT_DIR[:-1] + "_big/" + file_name + '_ch' + str(label) + '.png', new_image)
