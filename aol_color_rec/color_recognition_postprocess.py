# Importing VideoFrame before importing GST is must
from gsthailo import VideoFrame
from gi.repository import Gst
import hailo 
import numpy as np
# import json
# import color_histogram_feature_extraction
# import knn_classifier
import cv2
# import os
# import os.path
# import subprocess
 
# Pre-defined color ranges for color recognition
# COLOR_RANGES = {
#     'red': ((0, 50, 50), (10, 255, 255)),
#     'blue': ((100, 50, 50), (140, 255, 255)),
#     'green': ((40, 50, 50), (80, 255, 255)),
#     'yellow': ((20, 50, 50), (30, 255, 255)),
#     'black': ((0, 0, 0), (180, 255, 30)),
#     'white': ((0, 0, 200), (180, 30, 255)),
# }

# def detect_color(image):
    # """Detect the dominant color in an image using color histograms."""
    # hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # for color, (lower, upper) in COLOR_RANGES.items():
    #     mask = cv2.inRange(hsv_image, lower, upper)
    #     if np.sum(mask) > 0:
    #         return color
    # return 'unknown'

# def extract_instances(tensor):
    # Extract bounding boxes and masks from the tensor output.
    # instances = []
    # # Assuming tensor has shape [num_instances, 85] where each instance is [x, y, w, h, conf, class_id, ...mask]
    # for data in tensor:
    #     bbox = data[:4]  # Assuming the first 4 values are bbox coordinates
    #     # confidence = data[4]  # Assuming the 5th value is confidence score
    #     # class_id = int(data[5])  # Assuming the 6th value is class ID
    #     # mask = data[6:]  # Extract mask (assuming remaining values are the mask)
        
    #     # Convert bbox from normalized coordinates to pixel values
    #     x, y, w, h = bbox
    #     xmin = int(x - w / 2)
    #     ymin = int(y - h / 2)
    #     xmax = int(x + w / 2)
    #     ymax = int(y + h / 2)
        
    #     instance = {
    #         'bbox': [xmin, ymin, xmax, ymax]
    #         # 'confidence': confidence,
    #         # 'class_id': class_id,
    #         # 'mask': mask
    #     }
    #     instances.append(instance)
    # return instances

# def run(tensors, video_frame: VideoFrame):
    # Extract tensor output from the neural network
    # tensors = video_frame.roi.get_tensors()
    # for tensor in tensors:
    #     array = np.array(tensor, copy=False)
    #     # Perform instance segmentation post-processing here
    #     instances = extract_instances(array)

    #     # Assuming `instances` is the result of the post-process with bounding boxes and masks
    #     for instance in instances:
    #         bbox = instance['bbox']
    #         # mask = instance['mask']
    #         # class_id = instance['class_id']
    #         # confidence = instance['confidence']

    #         # Extract the region of interest (ROI) from the original frame
    #         roi = video_frame.frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    #         shirt_color = detect_color(roi)
            
    #         # Print the result
    #         print(f"Detected person with shirt color: {shirt_color} at bbox: {bbox}")

    #         # # Add the detection result to the video frame
    #         # detection = hailo.HailoDetection(
    #         #     type='person', confidence=confidence, bbox=bbox, additional_info={'shirt_color': shirt_color}
    #         # )
    #         # video_frame.roi.add_object(detection)

    # return Gst.FlowReturn.OK

# def run(video_frame: VideoFrame, tensors):
    # Extract tensor output from the neural network
    # for tensor in tensors:
    #     array = np.array(tensor, copy=False)
    #     print(f"Tensor shape: {array.shape}")
    #     print(f"Tensor values: {array}")

    # return Gst.FlowReturn.OK
#--------------------------------------------------------------------------

#def run(video_frame : VideoFrame):
#    roi = video_frame.roi
#    print(roi)
    # # detection_result = []   
    # # iterate over every detected object in the frame
    # for obj in roi.get_hailo_detections(hailo.HAILO_ROI):
    #     print(obj)
          # how to get tracked ID (search sub objects in metadata)
         # for sub_obj in obj.get_objects():
            # print(sub_obj)
            # tracking_id = sub_obj.get_id()
        
        #  if obj.get_type() == hailo.HAILO_DETECTION:
        #     # what type the object is (class) eg. person/car/etc.
        #     label = obj.get_label()
        #     confidence = obj.get_confidence()
        #     bbox = obj.get_bbox()
        #     xmin = (np.clip(bbox.xmin(), 0, 1))
        #     ymin = (np.clip(bbox.ymin(), 0, 1))
        #     xmax = (np.clip(bbox.xmax(), 0, 1))
        #     ymax = (np.clip(bbox.ymax(), 0, 1))
            
        #     width = xmax - xmin
        #     height = ymax - ymin
        #     detection_result = {
        #         'label': label,
        #         'confidence': confidence,
        #         'xmin': xmin,
        #         'ymin': ymin,
        #         'xmax': xmax,
        #         'ymax': ymax,
        #         'width': width,
        #         'height': height
        #     }
        #     detection_result.append(detection_result)
            
        #     print(detection_result)
            
#    return Gst.ReturnFlow.OK
        
            
# # Perform color classification on the instance segmentation results
# #color_predictions = perform_color_classification(frame)
       
 
 
# def perform_color_classification(frame):
#     # Process instance segmentation results
#     # Assuming instance_segmentation_results is a list of dictionaries representing each detection
    
#     color_predictions = []
    
#     # Perform color classification for each detection
#     for frame in instance_segmentation_result:
#         # Extract relevant information for color classification from detection
#         # Assuming xmin, ymin, xmax, ymax represent the bounding box coordinates
        
#         # Crop the object on the frame based on bounding box
#         # Assuming frame is the full frame where detection occured
#         object_frame = frame[int(frame['ymin']*frame.shape[0]):int(frame['ymax']*frame.shape[0]),
#                              int(frame['xmin']*frame.shape[1]):int(frame['xmax']*frame.shape[1])]
        
#         # Perform color classification on the cropped object
#         color_prediction = color_classification_webcam(object_frame)
        
#         # Append color prediction to the list of color predictions
#         color_predictions.append(color_prediction)
    
#     return color_predictions
 
# def color_classification_webcam(object_frame):
#     color = 'n.a.'
#     PATH = './training.data'
#     if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
#        print ('training data is ready, classifier is loading...')
#     else:
#        print ('training data is being created...')
#        open('training.data', 'w')
#        color_histogram_feature_extraction.training()
#        print ('training data is ready, classifier is loading...')
       
#     while True:
        
#         cv2.putText(
#         object_frame,
#         'Prediction: ' + color,
#         (15, 45),
#         cv2.FONT_HERSHEY_COMPLEX,
#         1,
#         100,
#         )
        
#         color_histogram_feature_extraction.color_histogram_of_test_image(object_frame)
#         prediction = knn_classifier.main('training.data', 'test.data')
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
   
#         # Assuming this function performs color classification and returns predictions
#         # Example color predictions
#         predictions = ['red', 'blue', 'green', 'yellow', 'orange', 'white', 'black' ]  
#         return predictions
