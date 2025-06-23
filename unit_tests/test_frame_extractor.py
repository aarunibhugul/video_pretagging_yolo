'''
to test frame extractor file we need two arguments/paramters:
1. path of test sample video sample
2.out file path to store jpg frames
'''


from src.frame_extractor import extract_frames
import pytest
import os


def test_extract_frames():
    TEST_VIDEO = "unit_test_input/unit_sample_video_1280x720_5mb.mp4"
    TEST_OUTPUT_DIR = "unit_test_output/test_output_frames/"
    os.makedirs(os.path.dirname(TEST_OUTPUT_DIR), exist_ok=True)

    metrics = extract_frames(TEST_VIDEO, TEST_OUTPUT_DIR, frame_step=10)
    files = os.listdir(TEST_OUTPUT_DIR)
    jpgs = [f for f in files if f.endswith(".jpg")]
    assert len(jpgs) > 0, "No frames extracted"
    assert "frames_extracted" in metrics
    assert metrics["frames_extracted"] == len(jpgs)







