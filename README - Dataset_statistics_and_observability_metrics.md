## Data Observability & Reporting

The pipeline includes logging and metric collection to generate insights into its operation and the generated dataset.

* **Logging:** Detailed information about each stage's progress, success, and any errors is logged to the console using Python's `logging` module.
* **Metrics Tracked:**
    * **Frame Extraction:** Total frames in video, frames extracted, frames dropped, and frame drop ratio.
    * **Object Detection:** Total images processed, total detections, average detections per frame, and class distribution (e.g., how many "person" vs. "car" detections).
    * **Pipeline Timings:** Elapsed time for `frame_extraction` and `object_detection` stages.
* **Pipeline Report (`pipeline_report.md`):** A Markdown file is generated in the output directory, summarizing all the collected metrics in an easy-to-read format. This file provides a snapshot of each pipeline run's performance and dataset characteristics.
* **Basic CSV Logging (`pipeline_metrics_log.csv`):** For historical tracking, key metrics from each run are appended to a CSV file in the output directory. This allows for simple trend analysis over multiple pipeline executions.

