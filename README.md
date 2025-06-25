
## Project Name: Vision Tag AI

### 1. Overview of pipeline

![image](https://github.com/user-attachments/assets/279a5d3c-144b-4a4b-911a-2ebea9568a97)

The **Vision Tag AI** pipeline automates video analysis with the following steps:

1. **Frame Extraction:**  
   Automatically extracts individual frames from a video file.
2. **Analysis & Annotation:**  
   Analyzes each frame to detect and annotate objects.
3. **Report Generation:**  
   Generates reports in [Markdown](https://github.com/aarunibhugul/video_pretagging_yolo/blob/main/output/pipeline_report.md), [JSON](https://github.com/aarunibhugul/video_pretagging_yolo/blob/main/output/detections.json), and [CSV](https://github.com/aarunibhugul/video_pretagging_yolo/blob/main/output/pipeline_metrics_log.csv) formats.

**Outputs include:**  
- Detailed metrics  
- Annotations  
- Detection summaries  

These outputs make it easy to review and log the results of the video analysis.

### 2. Pipeline flow (design decision):

![image](https://github.com/user-attachments/assets/b68a55ff-692d-4eb2-81ab-5ac5a35b3d1b)

### 3. Rationale for tooling:

![image](https://github.com/user-attachments/assets/dcb37f64-a664-4587-b068-7eed22708770)

### 4. Suggestions for Improvements & Scaling to many sites (cloud region):

![image](https://github.com/user-attachments/assets/e630155b-90ef-407a-a2cd-53ab408d4088)




