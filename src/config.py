# src/config.py

# Default output directories and file names (already in videopipeline.pynb)
DEFAULT_FRAME_OUTPUT_DIR = 'frames'
DEFAULT_COCO_OUTPUT_PATH = 'detections.json'
# Additions - for outputs - md file and csv logging
DEFAULT_REPORT_OUTPUT_PATH = 'pipeline_report.md' #Markdown report name
DEFAULT_CSV_LOG_PATH = 'pipeline_metrics_log.csv' #CSV log name

# Frame extraction settings
DEFAULT_FRAME_STEP = 30 # Save every Nth frame

# Object detection model settings
DEFAULT_MODEL_NAME = 'yolov8n.pt'
