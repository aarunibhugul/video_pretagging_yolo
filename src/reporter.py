# src/reporter.py
import os
from typing import Dict, Any

def generate_markdown_report(metrics: Dict[str, Any], output_path: str):
    """
    Generates a Markdown report summarizing pipeline metrics.

    Args:
        metrics (Dict[str, Any]): A dictionary containing all collected pipeline metrics.
        output_path (str): The full path where the Markdown report will be saved.
    """
    report_content = "# MLOps Pipeline Report\n\n"
    report_content += "This report summarizes the key metrics and performance of the video pre-tagging pipeline.\n\n"

    report_content += "## Pipeline Timings (github actions)\n"
    if "pipeline_stage_times" in metrics and metrics["pipeline_stage_times"]:
        for stage, duration in metrics["pipeline_stage_times"].items():
            report_content += f"- **{stage.replace('_', ' ').title()}:** {duration:.2f} seconds\n"
    else:
        report_content += "No pipeline stage timing data available.\n"
    report_content += "\n"

    report_content += "## Dataset Statistics\n"
    
    # Frame Extraction Metrics
    report_content += "### Frame Extraction Metrics\n"
    if "frame_extraction_metrics" in metrics:
        fe_metrics = metrics["frame_extraction_metrics"]
        report_content += f"- **Total Frames in Video:** {fe_metrics.get('total_frames_in_video', 'N/A')}\n"
        report_content += f"- **Frames Extracted:** {fe_metrics.get('frames_extracted', 'N/A')}\n"
        report_content += f"- **Frames Dropped:** {fe_metrics.get('frames_dropped', 'N/A')}\n"
        report_content += f"- **Frame Drop Ratio:** {fe_metrics.get('frame_drop_ratio', 0.0):.2%}\n"
    else:
        report_content += "No frame extraction metrics available.\n"
    report_content += "\n"

    # Object Detection Metrics
    report_content += "### Object Detection Metrics\n"
    if "object_detection_metrics" in metrics:
        od_metrics = metrics["object_detection_metrics"]
        report_content += f"- **Images Processed:** {od_metrics.get('images_processed', 'N/A')}\n"
        report_content += f"- **Total Detections:** {od_metrics.get('total_detections', 'N/A')}\n"
        report_content += f"- **Average Detections per Frame:** {od_metrics.get('detections_per_frame_avg', 0.0):.2f}\n"

        report_content += "\n#### Class Distribution\n"
        class_dist = od_metrics.get('class_distribution', {})
        if class_dist:
            # Sort by count descending for readability
            sorted_classes = sorted(class_dist.items(), key=lambda item: item[1], reverse=True)
            for cls, count in sorted_classes:
                report_content += f"- **{cls}:** {count} detections\n"
        else:
            report_content += "No detections found or class distribution data available.\n"
    else:
        report_content += "No object detection metrics available.\n"
    report_content += "\n"

    # Save the report
    try:
        with open(output_path, 'w') as f:
            f.write(report_content)
        print(f"Report saved to: {output_path}")
    except IOError as e:
        print(f"Error saving report to {output_path}: {e}")
        raise

if __name__ == "__main__":
    # sample to test report.py --> needs to passed as an argument
    sample_metrics = {
                        'frame_extraction_metrics': {
                          'total_frames_in_video': 4271,
                          'frames_extracted': 143,
                          'frames_dropped': 0,
                          'frame_drop_ratio': 0.0
                        },
                        'object_detection_metrics': {
                          'images_processed': 143,
                          'total_detections': 265,
                          'detections_per_frame_avg': 1.8531468531468531,
                          'class_distribution': {
                            'cat': 11,
                            'bird': 58,
                            'sheep': 31,
                            'person': 34,
                            'cow': 36,
                            'apple': 2,
                            'dog': 45,
                            'kite': 9,
                            'frisbee': 4,
                            'elephant': 1,
                            'horse': 21,
                            'bear': 1,
                            'chair': 1,
                            'sports ball': 6,
                            'umbrella': 4,
                            'giraffe': 1
                          }
                        },
                        'pipeline_stage_times': {
                          'frame_extraction_stage': 12.778194904327393,
                          'object_detection_stage': 15.81555438041687
                        }

}

    test_report_path = "pipeline_report.md"
    #test_report_path = "pipeline_report.md"
    generate_markdown_report(sample_metrics, test_report_path)
    print(f"Test report generated at {test_report_path}")
