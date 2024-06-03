#!/bin/bash
set -e

function init_variables() {
    print_help_if_needed $@
    script_dir=$(dirname $(realpath "$0"))
    source $script_dir/../../../../../scripts/misc/checks_before_run.sh

    readonly POSTPROCESS_DIR="$TAPPAS_WORKSPACE/apps/h8/gstreamer/libs/post_processes"
    readonly RESOURCES_DIR="$TAPPAS_WORKSPACE/apps/h8/gstreamer/general/instance_segmentation/resources"

    readonly DEFAULT_POSTPROCESS_SO="$POSTPROCESS_DIR/libyolov5seg_post.so"
    readonly DEFAULT_VIDEO_SOURCE="$RESOURCES_DIR/instance_segmentation.mp4"
    readonly DEFAULT_HEF_PATH="$RESOURCES_DIR/yolov5n_seg.hef"
    readonly DEFAULT_NETWORK_NAME="yolov5seg"
    readonly json_config_path="$RESOURCES_DIR/configs/yolov5seg.json"
    PYTHON_POST_PROC="$TAPPAS_WORKSPACE/apps/h8/gstreamer/general/instance_segmentation/main.py"
    KAFKA_CONSUMER="$TAPPAS_WORKSPACE/apps/h8/gstreamer/general/instance_segmentation/kafka_consumer.py"
    DB_PATH="$TAPPAS_WORKSPACE/apps/h8/gstreamer/general/instance_segmentation/detections.db"

    postprocess_so=$DEFAULT_POSTPROCESS_SO
    network_name=$DEFAULT_NETWORK_NAME
    video_source=$DEFAULT_VIDEO_SOURCE
    hef_path=$DEFAULT_HEF_PATH

    print_gst_launch_only=false
    additional_parameters=""

    video_sink_element=$([ "$XV_SUPPORTED" = "true" ] && echo "xvimagesink" || echo "ximagesink")
}

function print_usage() {
    echo "Sanity hailo pipeline usage:"
    echo ""
    echo "Options:"
    echo "  -h --help               Show this help"
    echo "  -i INPUT --input INPUT  Set the video source (default: $DEFAULT_VIDEO_SOURCE)"
    echo "  -p HEF_PATH             Set the HEF path (default: $DEFAULT_HEF_PATH)"
    echo "  -n NETWORK_NAME         Set the network name (default: $DEFAULT_NETWORK_NAME)"
    echo "  -c POSTPROCESS_SO       Set the postprocess .so path (default: $DEFAULT_POSTPROCESS_SO)"
    echo "  --print_gst_launch      Print only the gst-launch pipeline"
    echo ""
}

function print_help_if_needed() {
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        print_usage
        exit 0
    fi
}

function parse_args() {
    local ARGS
    ARGS=$(getopt -o "hi:p:n:c:" -l "help,input:,print_gst_launch" -- "$@")
    eval set -- "$ARGS"

    while true; do
        case "$1" in
        -h | --help)
            print_usage
            shift
            exit 0
            ;;
        -i | --input)
            video_source=$2
            shift 2
            ;;
        -p)
            hef_path=$2
            shift 2
            ;;
        -n)
            network_name=$2
            shift 2
            ;;
        -c)
            postprocess_so=$2
            shift 2
            ;;
        --print_gst_launch)
            print_gst_launch_only=true
            shift
            ;;
        --)
            shift
            break
            ;;
        esac
    done
}

parse_args "$@"
init_variables "$@"

PIPELINE="gst-launch-1.0 filesrc location=$video_source name=src_0 ! \
    decodebin ! \
    videoscale ! \
    video/x-raw, pixel-aspect-ratio=1/1 ! \
    videoconvert ! \
    queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
    hailonet hef-path=$hef_path ! \
    queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
    hailofilter function-name=$network_name so-path=$postprocess_so config-path=$json_config_path qos=false ! \
    queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
    hailooverlay qos=false ! \
    queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
    hailopython qos=false module=$PYTHON_POST_PROC function=run ! \
    queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
    videoconvert ! \
    fpsdisplaysink video-sink=fakesink name=hailo_display sync=false text-overlay=false"

if [ "$print_gst_launch_only" = true ]; then
    echo $PIPELINE
else
    eval $PIPELINE
fi

