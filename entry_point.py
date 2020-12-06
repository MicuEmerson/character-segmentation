import os
import time
import shutil
import logging

from character_segmentation import segmentation
from remove_garbage_images import remove_garbage_images
from resize_images import resize
from character_image_clustering import som_clustering

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger('generate-dataset')

INPUT_DIR_NAME = 'input/'
OUTPUT_DIR_NAME = 'output/'

# delete previous results
DIRS = ['characters_normal', 'characters_big', 'som_normal', 'som_big', 'resized_normal', 'resized_big', 'big_chars']

for dir_name in DIRS:
    if os.path.exists(OUTPUT_DIR_NAME + dir_name):
        shutil.rmtree(OUTPUT_DIR_NAME + dir_name)
    os.mkdir(OUTPUT_DIR_NAME + dir_name)

start_all = time.time()
log.info("Start generating dataset...\n")

############################################# --- SEGMENTATION --- #####################################################

log.info("Start segmentation")
start_segmentation = time.time()
segmentation(INPUT_DIR_NAME, OUTPUT_DIR_NAME + 'characters/')
log.info("Segmentation duration: %s seconds\n" % str(time.time() - start_segmentation))

############################################# --- REMOVE GARBAGE IMAGES  --- ###########################################

log.info("Start remove garbage")
start_remove_garbage = time.time()
remove_garbage_images(OUTPUT_DIR_NAME + 'characters_normal/', no_times = 5, height_percent = 2, width_percent = 2, copy_dir_name =OUTPUT_DIR_NAME + 'characters_big/')
remove_garbage_images(OUTPUT_DIR_NAME + 'characters_big/', no_times = 5, height_percent = 1.5, width_percent = 2, copy_dir_name =OUTPUT_DIR_NAME + 'big_chars/')
log.info("removed garbage images: %s seconds\n" % str(time.time() - start_remove_garbage))

############################################# --- RESIZE  --- ##########################################################

log.info("Start resize")
start_resize = time.time()
resize(OUTPUT_DIR_NAME + 'characters_normal/', OUTPUT_DIR_NAME + 'resized_normal/')
resize(OUTPUT_DIR_NAME + 'characters_big/', OUTPUT_DIR_NAME + 'resized_big/')
log.info("resized duration: %s seconds\n" % str(time.time() - start_resize))


############################################# --- CLUSTERIZATION SOM --- ###############################################

log.info("Start clustering")
start_clustering = time.time()
som_clustering(OUTPUT_DIR_NAME + 'resized_normal/', OUTPUT_DIR_NAME + 'som_normal/')
log.info("clusterization normal duration: % seconds" % str(time.time() - start_clustering))

start_clustering = time.time()
som_clustering(OUTPUT_DIR_NAME + 'resized_big/', OUTPUT_DIR_NAME + 'som_big/')
log.info("clusterization big duration: % seconds\n" % str(time.time() - start_clustering))

log.info("TOTAL DURATION: % seconds" % str(time.time() - start_all))

