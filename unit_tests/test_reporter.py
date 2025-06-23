'''
to test reporter file we need to arguments/paramters:
1. dictionary -> a sample metrics which json/dictionary representation of md file of oberved mtrics
2.out file path
'''


from src.reporter import generate_markdown_report
import pytest
import os


def test_generate_markdown_report():
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
            'frame_extraction_s': 12.778194904327393,
            'object_detection_s': 15.81555438041687
        }

    }


    output_path = "unit_test_output/test_reporter.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    generate_markdown_report(sample_metrics, output_path)
    assert os.path.exists(output_path)
    with open(output_path, 'r') as f:
        content = f.read()
        assert "# MLOps Pipeline Report" in content
        assert "person" in content
    #os.remove(output_path)


