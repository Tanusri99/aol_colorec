import cv2
import numpy as np
from color_utils import detect_color_in_region

def detect_top_pants_colors(mask, frame, bbox):
    """
    Detects the colors of the top and pants of a person based on the mask and bounding box.
    
    Args:
        mask: Binary mask of the person.
        frame: Original video frame.
        bbox: Bounding box coordinates (x_min, y_min, x_max, y_max).
    
    Returns:
        top_color: Detected color of the top.
        pants_color: Detected color of the pants.
    """
    x_min, y_min, x_max, y_max = bbox
    person_height = y_max - y_min
    person_width = x_max - x_min

    # Split the mask into top and pants regions
    top_mask = mask[:person_height//2, :]
    pants_mask = mask[person_height//2:, :]

    # Get the corresponding regions in the frame
    top_region = frame[y_min:y_min + person_height//2, x_min:x_max]
    pants_region = frame[y_min + person_height//2:y_max, x_min:x_max]

    # Detect colors in the regions
    top_color = detect_color_in_region(top_mask, top_region)
    pants_color = detect_color_in_region(pants_mask, pants_region)

    return top_color, pants_color

def process_mask(mask_data, bbox_height, bbox_width):
    """
    Process the mask data to create a binary mask.
    
    Args:
        mask_data: Raw mask data.
        bbox_height: Height of the bounding box.
        bbox_width: Width of the bounding box.
    
    Returns:
        mask_np_binary: Binary mask.
    """
    mask_np = np.array(mask_data, dtype=np.uint8)
    mask_np = cv2.resize(mask_np, (bbox_width, bbox_height), interpolation=cv2.INTER_NEAREST)
    _, mask_np_binary = cv2.threshold(mask_np, 127, 255, cv2.THRESH_BINARY)
    return mask_np_binary
    
    
    
    
    
    
    #-----------------------------------------------------#
    
import cv2
import numpy as np
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier

def detect_top_pants_colors(mask, frame, bbox, knn_model):
    x_min, y_min, x_max, y_max = bbox
    print(f"Original bbox: {bbox}")
    print(f"Original mask shape: {mask.shape}")
    
    masked_frame = frame[y_min:y_max, x_min:x_max] * mask[..., None]

    # Assuming the upper half is the top and the lower half is the pants
    top_half = masked_frame[:mask.shape[0] // 2]
    bottom_half = masked_frame[mask.shape[0] // 2:]

    # Flatten the arrays and convert to appropriate format for k-NN
    top_colors = top_half.reshape(-1, 3)
    bottom_colors = bottom_half.reshape(-1, 3)

    # Remove zero entries (background)
    top_colors = top_colors[np.any(top_colors != [0, 0, 0], axis=1)]
    bottom_colors = bottom_colors[np.any(bottom_colors != [0, 0, 0], axis=1)]

    # Predict colors using k-NN model
    top_color = knn_model.predict([np.mean(top_colors, axis=0)])[0] if top_colors.size else None
    pants_color = knn_model.predict([np.mean(bottom_colors, axis=0)])[0] if bottom_colors.size else None

    return top_color, pants_color


