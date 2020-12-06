import os
import cv2
import shutil

# iterate no_times times through folder and remove those characters that are bigger than average size
def remove_garbage_images(DIR_NAME, no_times, height_percent, width_percent, copy_dir_name=None):
    for i in range(0, no_times):
        sum_height, sum_width, average_height, average_width = 0, 0, 0, 0
        character_image_names = os.listdir(DIR_NAME)
        count = 0

        for file_name in character_image_names:
            original_img = cv2.imread(DIR_NAME + file_name, cv2.IMREAD_GRAYSCALE)
            height, width = original_img.shape
            sum_height += height
            sum_width += width

        average_height = sum_height / len(character_image_names)
        average_width = sum_width / len(character_image_names)

        for file_name in character_image_names:
            original_img = cv2.imread(dir_name + file_name, cv2.IMREAD_GRAYSCALE)
            height, width = original_img.shape

            if height > average_height * height_percent or width > average_width * width_percent:

                # we copy the characters that we want to remove from normal into big folder
                # because we do not want to loose them (they might be good actually)
                if copy_dir_name is not None:
                    shutil.copyfile(DIR_NAME + file_name, copy_dir_name + file_name)

                os.remove(DIR_NAME + file_name)
                count += 1

        # print("\tround:", i, " , deleted:", count)