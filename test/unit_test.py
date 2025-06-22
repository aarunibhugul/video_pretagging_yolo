# tests/test_frame_extractor.py
import os
import shutil
import pytest
from src.frame_extractor import extract_frames

# Fixture to set up a temporary directory for test outputs
@pytest.fixture
def temp_output_dir(tmp_path):
    """Provides a temporary directory for test outputs."""
    yield tmp_path / "extracted_frames_test"
    # Cleanup happens automatically by tmp_path fixture if not explicitly needed here

# You would need a tiny, short test video file for a real test
# For a robust test, you might mock cv2.VideoCapture to simulate video frames
# For simplicity, let's assume 'tests/data/sample_video.mp4' exists for now.
# In a real scenario, you'd use a smaller, pre-committed test video.

def test_extract_frames_basic(temp_output_dir):
    """Tests if frames are extracted and saved correctly."""
    # Create a dummy video file path (you'd need a real tiny video for this test)
    # For CI/CD, consider generating a dummy video or using a very small committed one.
    dummy_video_path = "tests/data/dummy_video_10_frames.mp4" # You would create this file

    # Create a dummy video for testing purposes (e.g., using moviepy or OpenCV)
    # This is complex to do in a simple test, often you just commit a tiny sample video.
    # For now, let's assume it's created or exists.
    if not os.path.exists("tests/data"):
        os.makedirs("tests/data")
    # Simulate creation of a dummy video if it doesn't exist
    # This part would be more robust in a real project (e.g., using OpenCV to create a few frames)
    # For the sake of this example, we'll just check if a dummy path exists.
    # In practice, you'd commit a tiny dummy_video_10_frames.mp4 to tests/data/
    if not os.path.exists(dummy_video_path):
        pytest.skip(f"Dummy video for testing not found at {dummy_video_path}. Skipping test.")

    # Call the function to test
    saved_count = extract_frames(dummy_video_path, str(temp_output_dir), frame_step=1)

    # Assertions
    assert temp_output_dir.is_dir()
    assert saved_count > 0 # Expect some frames to be saved
    # You could assert an exact count if your dummy video has a known number of frames
    # e.g., assert saved_count == 10

    # Check if specific frame files exist
    assert (temp_output_dir / "frame_00000.jpg").is_file()
    # assert (temp_output_dir / "frame_00001.jpg").is_file() # If frame_step=1


def test_extract_frames_invalid_path(temp_output_dir):
    """Tests behavior with an invalid video path."""
    with pytest.raises(FileNotFoundError):
        extract_frames("non_existent_video.mp4", str(temp_output_dir))

def test_extract_frames_empty_output_dir(temp_output_dir):
    """Tests if output directory is created."""
    dummy_video_path = "tests/data/dummy_video_10_frames.mp4"
    if not os.path.exists(dummy_video_path):
        pytest.skip(f"Dummy video for testing not found at {dummy_video_path}. Skipping test.")

    extract_frames(dummy_video_path, str(temp_output_dir), frame_step=5)
    assert temp_output_dir.is_dir()
    assert len(list(temp_output_dir.iterdir())) > 0 # Check that some files were written