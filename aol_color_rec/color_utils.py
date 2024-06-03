import numpy as np
import cv2
import joblib
from sklearn.cluster import KMeans
import warnings

def extract_color_histogram(image, bins=(8, 8, 8)):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

def load_knn_model(model_path):
    return joblib.load(model_path)

def detect_color_in_mask(mask_np_binary, frame, x_min, y_min, x_max, y_max, knn_model):
    frame_region = frame[y_min:y_max, x_min:x_max]
    masked_image = cv2.bitwise_and(frame_region, frame_region, mask=mask_np_binary)
    masked_image_hsv = cv2.cvtColor(masked_image, cv2.COLOR_BGR2HSV)

    pixels = masked_image_hsv[mask_np_binary > 0]

    if len(pixels) == 0:
        return 'black'

    hist = extract_color_histogram(masked_image)
    hist = hist.reshape(1, -1)
    color_prediction = knn_model.predict(hist)[0]

    return color_prediction

# # Suppress future warnings for sklearn
# warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")

# # Define normalized RGB values for the reference colors
# color_references = {
#     "black": np.array([0.0, 0.0, 0.0]),
#     "white": np.array([1.0, 1.0, 1.0]),
#     "red": np.array([1.0, 0.0, 0.0]),
#     "green": np.array([0.0, 1.0, 0.0]),
#     "blue": np.array([0.0, 0.0, 1.0]),
#     "yellow": np.array([1.0, 1.0, 0.0]),
#     "orange": np.array([1.0, 0.5, 0.0])
# }

# def detect_color(normalized_pixel):
#     min_distance = float('inf')
#     detected_color = None
    
#     for color_name, color_value in color_references.items():
#         distance = np.linalg.norm(normalized_pixel - color_value)
#         if distance < min_distance:
#             min_distance = distance
#             detected_color = color_name
    
#     return detected_color

# def detect_color_in_mask(mask_np_binary, frame, x_min, y_min, x_max, y_max):
#     # Ensure bbox coordinates are integers
#     x_min = int(x_min)
#     y_min = int(y_min)
#     x_max = int(x_max)
#     y_max = int(y_max)
    
#     # Extract the frame region corresponding to the bounding box
#     frame_region = frame[y_min:y_max, x_min:x_max]
    
#     # Ensure the mask size matches the frame region size
#     mask_height, mask_width = mask_np_binary.shape
#     frame_region_resized = cv2.resize(frame_region, (mask_width, mask_height))
    
#     # Apply the mask to the resized image
#     masked_image = cv2.bitwise_and(frame_region_resized, frame_region_resized, mask=mask_np_binary)
    
#     # Normalize the masked image to range [0, 1]
#     masked_image_normalized = masked_image / 255.0

#     # Reshape the image to be a list of pixels
#     pixels = masked_image_normalized.reshape(-1, 3)
    
#     # Filter out black pixels (close to zero in all channels)
#     pixels = pixels[np.any(pixels > [0, 0, 0], axis=1)]
    
#     if len(pixels) == 0:
#         return 'black'

#     # Use KMeans to find the most common color
#     kmeans = KMeans(n_clusters=1, random_state=0, n_init=10)
#     kmeans.fit(pixels)
#     dominant_color = kmeans.cluster_centers_[0]

#     # Map the dominant color to the closest predefined color
#     closest_color = detect_color(dominant_color)

#     return closest_color

