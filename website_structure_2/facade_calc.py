import os
import requests
from PIL import Image
import torch
from transformers import DPTFeatureExtractor, DPTForSemanticSegmentation
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import tensorflow as tf
from collections import defaultdict
import joblib
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point, LineString
import pandas as pd
import pyproj

# Initialize global variables
image_url = ""
lat, lon = 0.0, 0.0

# Function to save image
def save_image(image, path):
    image.save(path)

# Function to save and visualize segmentation
def save_segmentation(image, labels, classes, path):
    colored_segmentation = np.zeros((labels.shape[0], labels.shape[1], 3), dtype=np.uint8)
    for class_id, class_info in classes.items():
        colored_segmentation[labels == class_id] = class_info["color"]

    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.imshow(colored_segmentation, alpha=0.6)
    plt.axis('off')
    plt.savefig(path, bbox_inches='tight')
    plt.close()

def load_keras_model(filepath):
    with open(filepath, 'rb') as f:
        model = tf.keras.models.load_model(f)
    return model

# Adjust the function to load the model
classifier_model_url = "https://github.com/mohammadabid-macad/AIAStudioG03/raw/65f48a58e1f1ea1c8ac387facfa78a6ba20b467d/models/material_texture_classifier.keras"
response = requests.get(classifier_model_url)
classifier_model_path = 'material_texture_classifier.keras'
with open(classifier_model_path, 'wb') as file:
    file.write(response.content)
classifier_model = load_keras_model(classifier_model_path)

def calculate_facade_area_and_materials():
    global image_url, lat, lon

    # Download and preprocess the image
    original_image = download_image(image_url)
    inputs = feature_extractor(images=original_image, return_tensors="pt")

    # Perform segmentation
    with torch.no_grad():
        outputs = segmentation_model(**inputs)
        logits = outputs.logits
        upsampled_logits = torch.nn.functional.interpolate(logits, size=original_image.size[::-1], mode="bilinear", align_corners=False)
        predicted_labels = upsampled_logits.argmax(dim=1).squeeze().numpy()

    # Define the class mappings
    foliage_classes = [8, 10, 12, 17, 18, 19, 20]
    building_class = 1
    sky_class = 22

    new_predicted_labels = np.zeros_like(predicted_labels)
    new_predicted_labels[np.isin(predicted_labels, foliage_classes)] = 1
    new_predicted_labels[predicted_labels == building_class] = 2
    new_predicted_labels[predicted_labels == sky_class] = 3

    classes = {
        0: {"name": "Background", "color": [0, 0, 0]},
        1: {"name": "Foliage", "color": [107, 142, 35]},
        2: {"name": "Building", "color": [128, 64, 128]},
        3: {"name": "Sky", "color": [135, 206, 235]}
    }

    # Save the original image and segmentation image
    original_image_path = "static/original_image.png"
    segmentation_image_path = "static/segmentation_image.png"
    save_image(original_image, original_image_path)
    save_segmentation(original_image, new_predicted_labels, classes, segmentation_image_path)

    # Proceed with the rest of the facade and material calculations...

    # Return paths of the saved images along with other results
    results = {
        "closest_building": {
            # ... other data ...
        },
        "original_image_path": original_image_path,
        "segmentation_image_path": segmentation_image_path
    }

    return results
