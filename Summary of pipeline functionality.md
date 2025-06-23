# Video Object Detection Pipeline Overview

### Pipeline Summary

This pipeline automates the process of analyzing a video to detect objects and generate reports. It works in three main steps:

1. **Extract Pictures**  
   The pipeline takes your video and automatically pulls out individual pictures (frames) from it.

2. **Find Objects**  
   It looks at these pictures to find and identify different objects, such as people, cars, or animals.

3. **Create Reports**  
   Finally, it puts together simple reports that show what objects were found and how well the process worked.

---
## Summary of Pipeline Functionality
### 1. Configuration

**Script:** `config.py`  
**Functionality:** Stores constants and default output directories for the pipeline.

- **Constants:**  
  - Frame extraction step (interval)
  - Model name

- **Default Output Directories:**  
  - COCO JSON output path
  - CSV log output path
  - Markdown report output path

---

### 2. Frame Extraction

**Script:** `frame_extractor.py`  
**Functionality:** Reads a sample video (`.mp4`) file and extracts individual frames at a configurable interval.

- **Input Parameters:**
  - Path to sample video
  - Output directory for frames (JPG files)
  - Frame extraction step (interval)

- **Output:**  
  - Extracted frames as JPG files in the specified directory

---

### 3. Object Detection (Pre-tagging)

**Script:** `object_detector.py`  
**Functionality:** Performs object detection on each extracted frame using YOLO, generating bounding box annotations.

- **Input Parameters:**
  - Directory containing images to process (from frame extractor)
  - Output path for COCO-format JSON file
  - Model name or path for YOLO model (e.g., `yolov8n.pt`)

- **Output:**  
  - COCO-format annotation JSON file (e.g., `detections.json`)

---

### 4. Reporting and Logging

**Script:** `reporter.py`  
**Functionality:** Collects key metrics throughout the pipeline and generates human-readable reports (Markdown) and CSV logs.

- **Input Parameters:**
  - Metrics/statistics from frame extraction (e.g., total frames, extracted frames, dropped frames)
  - Metrics/statistics from object detection (e.g., total images processed, total detections, class distribution)
  - Output directory for reports

- **Output:**  
  - Markdown report file (`pipeline_report.md`)
  - CSV log file (`pipeline_metrics_log.csv`)

---
