import numpy as np
from sklearn.externals import joblib

def load_knn_model(model_path):
    return joblib.load(model_path)

def detect_color_in_region(mask, region):
    """
    Detects the dominant color in a given region of the frame.

    Args:
        mask: Binary mask for the region.
        region: Region of the frame.

    Returns:
        color_name: Detected color name.
    """
    # Apply the mask to the region
    masked_region = cv2.bitwise_and(region, region, mask=mask)

    # Convert the region to the required color space
    hsv_region = cv2.cvtColor(masked_region, cv2.COLOR_BGR2HSV)

    # Calculate the histogram and find the most frequent color
    hist = cv2.calcHist([hsv_region], [0], mask, [256], [0, 256])
    dominant_color_index = np.argmax(hist)

    # Map the dominant color index to a color name (you need a predefined mapping)
    color_name = map_color_index_to_name(dominant_color_index)

    return color_name

def map_color_index_to_name(index):
    """
    Maps a color index to a color name.

    Args:
        index: Color index.

    Returns:
        color_name: Corresponding color name.
    """
    color_map = {
        # This should contain the mapping from index to color name
        0: "black",
        1: "white",
        2: "red",
        3: "green",
        4: "blue",
        # Add other colors as needed
    }
    return color_map.get(index, "unknown")

