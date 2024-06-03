import hailo
from gsthailo import VideoFrame
from gi.repository import Gst
from color_utils import load_knn_model
from kafka_producer import send_to_kafka
from top_pants_detection import detect_top_pants_colors, process_mask

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

            if label == "person":
                for sub_obj in obj.get_objects():
                    if isinstance(sub_obj, hailo.HailoConfClassMask):
                        mask_data = sub_obj.get_data()
                        bbox_height = y_max - y_min
                        bbox_width = x_max - x_min

                        # Process mask
                        mask_np_binary = process_mask(mask_data, bbox_height, bbox_width)

                        # Detect colors for top and pants
                        top_color, pants_color = detect_top_pants_colors(mask_np_binary, frame, (x_min, y_min, x_max, y_max))

                        detection_data = {
                            "label": label,
                            "confidence": confidence,
                            "bbox": {
                                "x_min": x_min,
                                "y_min": y_min,
                                "x_max": x_max,
                                "y_max": y_max
                            },
                            "mask_data_shape": mask_np_binary.shape,
                            "top_color": top_color,
                            "pants_color": pants_color
                        }

                        # Send data to Kafka
                        send_to_kafka('detections', detection_data)

                        # Print detection data
                        print("Detected Object:")
                        print("Label:", label)
                        print("Confidence:", confidence)
                        print(f"BBox Coordinates: (x_min: {x_min}, y_min: {y_min}, x_max: {x_max}, y_max: {y_max})")
                        print("Mask Data Shape:", mask_np_binary.shape)
                        print("Top Color:", top_color)
                        print("Pants Color:", pants_color)

    return Gst.FlowReturn.OK

