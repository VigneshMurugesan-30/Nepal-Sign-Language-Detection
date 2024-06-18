# -*- coding: utf-8 -*-
"""Train YOLOV8.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w4bfd48lsXGVR3JjpLKX6WeGz4UVellz

# FILE LOCATIONS

*   ANNOTATIONS_DIRECTORY_PATH = '/dataset/train/labels'
*   IMAGES_DIRECTORY_PATH = "/dataset/train/images"
*   DATA_YAML_PATH = '/dataset/data.yaml'

By looking at the directories mentioned in the code itself you can able identify the path.

# REQUIREMENTS
"""

!nvidia-smi

!pip install -q \
autodistill \
autodistill-grounded-sam \
autodistill-yolov8 \
roboflow \
supervision==0.9.0

# prompt: mmount gdrive

from google.colab import drive
drive.mount('/content/drive')

"""# DISPLAY ANNOTATED IMAGES"""

ANNOTATIONS_DIRECTORY_PATH = '/content/drive/MyDrive/dataset3/train/labels'
IMAGES_DIRECTORY_PATH = "/content/drive/MyDrive/dataset3/train/images"
DATA_YAML_PATH = '/content/drive/MyDrive/dataset3/data.yaml'

import supervision as sv

dataset = sv.DetectionDataset.from_yolo(
    images_directory_path=IMAGES_DIRECTORY_PATH,
    annotations_directory_path=ANNOTATIONS_DIRECTORY_PATH,
    data_yaml_path=DATA_YAML_PATH)

len(dataset)

SAMPLE_SIZE = 16
SAMPLE_GRID_SIZE = (4, 4)
SAMPLE_PLOT_SIZE = (16, 16)

import supervision as sv

image_names = list(dataset.images.keys())[:SAMPLE_SIZE]

mask_annotator = sv.MaskAnnotator()
box_annotator = sv.BoxAnnotator()

images = []
for image_name in image_names:
    image = dataset.images[image_name]
    annotations = dataset.annotations[image_name]
    labels = [
        dataset.classes[class_id]
        for class_id
        in annotations.class_id]
    annotates_image = mask_annotator.annotate(
        scene=image.copy(),
        detections=annotations)
    annotates_image = box_annotator.annotate(
        scene=annotates_image,
        detections=annotations,
        labels=labels)
    images.append(annotates_image)

sv.plot_images_grid(
    images=images,
    titles=image_names,
    grid_size=SAMPLE_GRID_SIZE,
    size=SAMPLE_PLOT_SIZE)

"""# TRAIN WITH YOLO V8"""

ANNOTATIONS_DIRECTORY_PATH = '/content/drive/MyDrive/dataset3/train/labels'
IMAGES_DIRECTORY_PATH = "/content/drive/MyDrive/dataset3/train/images"
DATA_YAML_PATH = '/content/drive/MyDrive/dataset3/data.yaml'

from autodistill_yolov8 import YOLOv8

target_model = YOLOv8("yolov8n.pt")
target_model.train(DATA_YAML_PATH, epochs=50)

"""# EVALUATION"""

from IPython.display import Image

Image(filename=f'/runs/detect/train/confusion_matrix.png', width=600)

from IPython.display import Image

Image(filename=f'/runs/detect/train/results.png', width=600)

from IPython.display import Image

Image(filename=f'/runs/detect/train/val_batch0_pred.jpg', width=600)

"""# TEST WITH SAMPLE VIDEO"""

INPUT_VIDEO_PATH = TEST_VIDEO_PATHS[0]
OUTPUT_VIDEO_PATH = f"/content/drive/MyDrive/Experts/S6_NSL_Consonant_Unprepared.mov"
TRAINED_MODEL_PATH = f"/runs/detect/train/weights/best.pt"

import os

# Set locale to UTF-8
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

# Define paths
INPUT_VIDEO_PATH = TEST_VIDEO_PATHS[0]
OUTPUT_VIDEO_PATH = f"/content/drive/MyDrive/Experts/S6_NSL_Consonant_Unprepared.mov"
TRAINED_MODEL_PATH = f"/runs/detect/train/weights/best.pt"

# Run YOLO prediction
!yolo predict model={TRAINED_MODEL_PATH} source={INPUT_VIDEO_PATH}