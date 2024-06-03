import os
import cv2
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier
from color_histogram import extract_color_histogram

def load_training_data(training_dir):
    data = []
    labels = []

    for subdir in os.listdir(training_dir):
        subdir_path = os.path.join(training_dir, subdir)
        if os.path.isdir(subdir_path):
            label = subdir  # Use the subdirectory name as the label
            for file_name in os.listdir(subdir_path):
                if file_name.endswith(('.png', '.jpg', '.jpeg')):
                    # Read the image
                    image_path = os.path.join(subdir_path, file_name)
                    image = cv2.imread(image_path)
                    if image is not None:
                        # Extract features
                        features = extract_color_histogram(image)
                        data.append(features)
                        labels.append(label)

    return np.array(data), np.array(labels)

def train_knn(training_dir, model_output_path, k=3):
    data, labels = load_training_data(training_dir)
    # Create and train the k-NN classifier
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(data, labels)
    # Save the model to disk
    with open(model_output_path, 'wb') as f:
        pickle.dump(knn, f)
    print(f"Model trained and saved to {model_output_path}")

if __name__ == '__main__':
    training_dir = '/local/workspace/tappas/apps/h8/gstreamer/general/instance_segmentation/training_dataset'
    model_output_path = 'color_knn_model.pkl'
    train_knn(training_dir, model_output_path)

