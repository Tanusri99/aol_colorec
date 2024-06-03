import os
import cv2
import numpy as np
import joblib
from sklearn.neighbors import KNeighborsClassifier

def extract_color_histogram(image, bins=(8, 8, 8)):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Compute a 3D color histogram in the HSV color space
    hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
    # Normalize the histogram
    hist = cv2.normalize(hist, hist).flatten()
    return hist

def load_training_data(training_path):
    data = []
    labels = []

    # Loop through each color directory
    for color_dir in os.listdir(training_path):
        color_path = os.path.join(training_path, color_dir)
        if os.path.isdir(color_path):
            # Loop through each image in the color directory
            for image_name in os.listdir(color_path):
                image_path = os.path.join(color_path, image_name)
                image = cv2.imread(image_path)
                if image is not None:
                    hist = extract_color_histogram(image)
                    data.append(hist)
                    labels.append(color_dir)
    
    return np.array(data), np.array(labels)

def train_knn_classifier(data, labels, k=3):
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(data, labels)
    return model

if __name__ == "__main__":
    training_path = "/local/workspace/tappas/apps/h8/gstreamer/general/instance_segmentation/training_dataset"
    data, labels = load_training_data(training_path)
    knn_model = train_knn_classifier(data, labels)

    # Save the trained model to a file
    model_path = "/local/workspace/tappas/apps/h8/gstreamer/general/instance_segmentation/knn_color_model.joblib"
    joblib.dump(knn_model, model_path)
    print("Model trained and saved to", model_path)

