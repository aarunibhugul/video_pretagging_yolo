
## Project Name: Vision Tag AI

### 1. Overview of pipeline

![image](https://github.com/user-attachments/assets/75aaf602-782b-4f05-b8a1-6642ef412f55)

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
   Instructions to run this pipeline can be found in the [Readme-pipeline execution file](https://github.com/aarunibhugul/video_pretagging_yolo/blob/main/1.%20README%20-%20pipeline%20execution.md)

![image](https://github.com/user-attachments/assets/683ea5f1-d95e-4797-b14a-605fabee87e7)


### 3. Rationale for tooling:

![image](https://github.com/user-attachments/assets/dcb37f64-a664-4587-b068-7eed22708770)

### 4. Suggestions for Improvements & Scaling to many sites (cloud region):

![image](https://github.com/user-attachments/assets/e630155b-90ef-407a-a2cd-53ab408d4088)




