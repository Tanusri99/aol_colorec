import hailo
from gsthailo import VideoFrame
from gi.repository import Gst
from color_utils import detect_color_in_mask, load_knn_model
from mask_utils import process_mask

def run(video_frame: VideoFrame):
    roi = video_frame.roi
    
    frame_width = video_frame.video_info.width
    frame_height = video_frame.video_info.height

    with video_frame.map_buffer() as map_info:
        frame = VideoFrame.numpy_array_from_buffer(map_info, video_frame.video_info)
        
         # Load the k-NN model
        model_path = "/local/workspace/tappas/apps/h8/gstreamer/general/instance_segmentation/knn_color_model.joblib"
        knn_model = load_knn_model(model_path)

        # Iterate over every detected object in the frame
        for obj in roi.get_objects_typed(hailo.HAILO_DETECTION):
            label = obj.get_label()
            confidence = obj.get_confidence()
            bbox = obj.get_bbox()

            # Extract bbox coordinates and ensure they are integers
            x_min = int(bbox.xmin() * frame_width)
            y_min = int(bbox.ymin() * frame_height)
            x_max = int(bbox.xmax() * frame_width)
            y_max = int(bbox.ymax() * frame_height)

            for sub_obj in obj.get_objects():
                if isinstance(sub_obj, hailo.HailoConfClassMask):
                    mask_data = sub_obj.get_data()
                    
                    bbox_height = y_max - y_min
                    bbox_width = x_max - x_min

                    # Process mask
                    mask_np_binary = process_mask(mask_data, bbox_height, bbox_width)
                    
                    # Determine the dominant color within the masked region
                    closest_color = detect_color_in_mask(mask_np_binary, frame, x_min, y_min, x_max, y_max, knn_model)
                    
                    # Print label, confidence, bbox coordinates, mask data, and color
                    print("Detected Object:")
                    print("Label:", label)
                    print("Confidence:", confidence)
                    print("BBox Coordinates: (x_min: {}, y_min: {}, x_max: {}, y_max: {})".format(x_min, y_min, x_max, y_max))
                    print("Mask Data Shape:", mask_np_binary.shape)
                    print("Color:", closest_color)

    return Gst.FlowReturn.OK

