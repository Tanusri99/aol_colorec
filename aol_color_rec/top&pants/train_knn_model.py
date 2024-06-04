import os
import numpy as np
import cv2
from sklearn.neighbors import KNeighborsClassifier
import joblib

def extract_color_histogram(image, bins=(8, 8, 8)):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

def load_training_data(dataset_path):
    data = []
    labels = []

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)
                label = os.path.basename(root)
                hist = extract_color_histogram(image)
                data.append(hist)
                labels.append(label)

    return np.array(data), np.array(labels)

# Path to your training dataset
dataset_path = "/local/workspace/tappas/apps/h8/gstreamer/general/instance_segmentation/training_dataset"

# Load training data
data, labels = load_training_data(dataset_path)

# Train k-NN classifier
knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(data, labels)

# Save the k-NN model
model_path = "/local/workspace/tappas/apps/h8/gstreamer/general/instance_segmentation/knn_color_model.joblib"
joblib.dump(knn_model, model_path)
print(f"Model saved to {model_path}")

