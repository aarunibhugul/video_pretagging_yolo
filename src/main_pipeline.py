# src/main_pipeline.py
import argparse
import os
import logging
import time # For timing stages
import json # For potential future JSON logging
import csv # For CSV logging

# Import functions from our refactored modules
from frame_extractor import extract_frames
from object_detector import pretag_images_and_generate_coco
from reporter import generate_markdown_report
from config import (
    DEFAULT_FRAME_OUTPUT_DIR,
    DEFAULT_COCO_OUTPUT_PATH,
    DEFAULT_FRAME_STEP,
    DEFAULT_MODEL_NAME,
    DEFAULT_REPORT_OUTPUT_PATH, # New
    DEFAULT_CSV_LOG_PATH # New
)

# Set up comprehensive logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#code to perform input file check

def validate_video_input(video_path: str) -> bool:
    """
    Performs basic validation on the input video file.

    Checks:
    1. If the file exists.
    2. If OpenCV can open it and determine its frame count (basic format check).

    Args:
        video_path (str): Path to the input video file.

    Returns:
        bool: True if validation passes, False otherwise.
    """

    if not validate_video_input(video_path, logger_instance):
        logging.error("Pipeline aborted due to input video validation failure.")
        return # Exit if a critical stage fails

    if not os.path.exists(video_path):
        logging.error(f"Validation Error: Input video file not found at '{video_path}'")
        return False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error(f"Validation Error: Could not open video file '{video_path}'. "
                      "It might be corrupted or in an unsupported format.")
        cap.release()
        return False

    # Check if the video has a valid frame count (more than 0 frames)
    # Some corrupted or invalid files might open but have 0 frames.
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count <= 0:
        logging.error(f"Validation Error: Video '{video_path}' has 0 or invalid frame count ({frame_count}). "
                      "It might be empty or severely corrupted.")
        cap.release()
        return False

    cap.release()
    logging.info(f"Input video '{video_path}' passed basic validation.")
    return True




def run_pipeline(video_path: str, output_base_dir: str, frame_step: int, model_name: str):
    """
    Runs the end-to-end video processing and object detection pipeline.

    Args:
        video_path (str): Path to the input video file.
        output_base_dir (str): Base directory for all outputs (frames, COCO file).
        frame_step (int): Interval for frame extraction.
        model_name (str): Name or path of the object detection model.
    """
    logging.info("Starting MLOps Video Pre-tagging Pipeline...")
    logging.info(f"Input Video: {video_path}")
    logging.info(f"Output Base Directory: {output_base_dir}")
    logging.info(f"Frame Step: {frame_step}")
    logging.info(f"Detection Model: {model_name}")

    pipeline_stage_times = {}
    all_metrics = {}

    # Stage 1: Frame Extraction
    start_time = time.time()
    frames_output_dir = os.path.join(output_base_dir, DEFAULT_FRAME_OUTPUT_DIR)
    try:
        frame_metrics = extract_frames(video_path, frames_output_dir, frame_step)
        #print(frame_metrics)
        all_metrics["frame_extraction_metrics"] = frame_metrics
        logging.info(f"Successfully extracted {frame_metrics.get('frames_extracted', 0)} frames.")
        logging.info(f"Frame drop ratio: {frame_metrics.get('frame_drop_ratio', 0):.2%}")
    except Exception as e:
        logging.error(f"Frame extraction failed: {e}")
        return # Exit if a critical stage fails
    pipeline_stage_times['frame_extraction_s'] = time.time() - start_time
    logging.info(f"Frame Extraction completed in {pipeline_stage_times['frame_extraction_s']:.2f} seconds.")

    # Stage 2: Object Detection and COCO Annotation Generation
    start_time = time.time()
    coco_output_path = os.path.join(output_base_dir, DEFAULT_COCO_OUTPUT_PATH)
    try:
        detection_result = pretag_images_and_generate_coco(frames_output_dir, coco_output_path, model_name)
        detection_metrics = detection_result["metrics"]
        all_metrics["object_detection_metrics"] = detection_metrics
        logging.info(f"Successfully detected {detection_metrics.get('total_detections', 0)} objects and generated COCO file.")
        logging.info(f"Average detections per frame: {detection_metrics.get('detections_per_frame_avg', 0):.2f}")
        logging.info(f"Class distribution: {detection_metrics.get('class_distribution', {})}")
    except Exception as e:
        logging.error(f"Object detection and COCO generation failed: {e}")
        return # Exit if a critical stage fails
    pipeline_stage_times['object_detection_s'] = time.time() - start_time
    logging.info(f"Object Detection completed in {pipeline_stage_times['object_detection_s']:.2f} seconds.")

    # Aggregate all pipeline timings
    all_metrics["pipeline_stage_times"] = pipeline_stage_times

    logging.info("Pipeline execution finished.")
    logging.info("--- Pipeline Stage Timings ---")
    for stage, duration in pipeline_stage_times.items():
        logging.info(f"  {stage.replace('_', ' ').title()}: {duration:.2f} seconds")

    # Generate the Markdown report
    report_output_path = os.path.join(output_base_dir, DEFAULT_REPORT_OUTPUT_PATH)
    try:
        print(all_metrics)
        generate_markdown_report(all_metrics, report_output_path)
        logging.info(f"Pipeline report generated at: {report_output_path}")
    except Exception as e:
        logging.error(f"Failed to generate pipeline report: {e}")
        logging.error(f"Failed to generate pipeline report: {e}")

    # Bonus: Basic CSV Logging
    csv_log_path = os.path.join(output_base_dir, DEFAULT_CSV_LOG_PATH)
    try:
        log_entry_flat = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "video_path": video_path,
            **{f"time_{k.replace('_s','')}": v for k, v in all_metrics.get("pipeline_stage_times", {}).items()},
            **{f"fe_{k}": v for k, v in all_metrics.get("frame_extraction_metrics", {}).items()},
            "od_class_distribution": json.dumps(all_metrics.get("object_detection_metrics", {}).get("class_distribution", {})),
            **{
                f"od_{k}": v
                for k, v in all_metrics.get("object_detection_metrics", {}).items()
                if k != "class_distribution"
            }
        }
        file_exists = os.path.exists(csv_log_path)

        with open(csv_log_path, 'a', newline='') as f: # newline='' for csv.writer
            writer = csv.DictWriter(f, fieldnames=log_entry_flat.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_entry_flat)
        logging.info(f"Metrics logged to CSV: {csv_log_path}")
    except Exception as e:
        logging.warning(f"Could not log metrics to CSV: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the MLOps video pre-tagging pipeline."
    )
    parser.add_argument(
        "--video_path", #whenever calling main.py use "--videopath#path"
        type=str,
        required=True,
        help="Path to the input video file (e.g., /app/input/sample.mp4)."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="output", # Default to an 'output' directory relative to where script is run
        help="Base directory to save all generated outputs (frames, COCO JSON, report)."
    )
    parser.add_argument(
        "--frame_step",
        type=int,
        default=DEFAULT_FRAME_STEP,
        help=f"Interval at which frames are extracted (default: {DEFAULT_FRAME_STEP})."
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default=DEFAULT_MODEL_NAME,
        help=f"Name or path of the object detection model (default: {DEFAULT_MODEL_NAME})."
    )

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    #running "runpipeline function"

    run_pipeline(
        video_path=args.video_path,
        output_base_dir=args.output_dir,
        frame_step=args.frame_step,
        model_name=args.model_name
    )