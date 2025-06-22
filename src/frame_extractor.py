# src/frame_extractor.py
import cv2
import os
import logging
from tqdm import tqdm
from typing import Dict, Any

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_frames(video_path: str, output_dir: str, frame_step: int = 30) -> Dict[str, Any]:
    """
    This function Extracts frames from the video file

    Paramter/arguments:
        video_path: Path to the input video file.
        output_dir: folder where extracted frames will be saved.
        frame_step: Interval at which frames are extracted (e.g., 30 for every 30th frame).

    Returns:
        Dict[str, Any]: A dictionary containing extraction metrics
                        1.total_frames_in_video,
                        2.frames_extracted
                        3.frames_dropped
                        4.frame_drop_ratio.
    """

    # exceptionhandling for file not available or wrong path
    if not os.path.exists(video_path):
        logging.error(f"Video file not found: {video_path}")
        raise FileNotFoundError(f"Video file not found: {video_path}")

    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error(f"Could not open video file: {video_path}")
        raise IOError(f"Could not open video file: {video_path}")

    total_frames_in_video = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    logging.info(f"Total frames in video: {total_frames_in_video}")

    frame_idx, saved_idx, dropped_frames = 0, 0, 0

    logging.info(f"Extracting frames from '{video_path}' to '{output_dir}'...")

    # Using tqdm for a progress bar
    # Check if total_frames_in_video is valid before using in tqdm
    if total_frames_in_video > 0:
        for _ in tqdm(range(total_frames_in_video), desc="Extracting Frames"):
            success, frame = cap.read()
            if not success:
                dropped_frames += 1
                continue # Skip bad frames

            if frame_idx % frame_step == 0:
                frame_filename = os.path.join(output_dir, f"frame_{saved_idx:05d}.jpg")
                cv2.imwrite(frame_filename, frame)
                saved_idx += 1
            frame_idx += 1
    else:
        logging.warning("Could not determine total frames in video. Processing until end.")
        while True:
            success, frame = cap.read()
            if not success:
                dropped_frames += 1
                break # End of video or error

            if frame_idx % frame_step == 0:
                frame_filename = os.path.join(output_dir, f"frame_{saved_idx:05d}.jpg")
                cv2.imwrite(frame_filename, frame)
                saved_idx += 1
            frame_idx += 1
            total_frames_in_video += 1 # Increment as we process if CAP_PROP_FRAME_COUNT was 0


    cap.release()
    logging.info(f"Finished frame extraction.")
    logging.info(f"Saved {saved_idx} frames to {output_dir}/")
    logging.info(f"Dropped {dropped_frames} frames.")

    frame_drop_ratio = dropped_frames / total_frames_in_video if total_frames_in_video > 0 else 0

    return {
        "total_frames_in_video": total_frames_in_video,
        "frames_extracted": saved_idx,
        "frames_dropped": dropped_frames,
        "frame_drop_ratio": frame_drop_ratio
    }

'''
if __name__ == "__main__":
    # Example usage if run directly (for testing)
    test_video_path = "SampleVideo_1280x720_30mb.mp4" # Replace with a real video path for testing
    test_output_dir = "test_extracted_frames"


    if os.path.exists(test_video_path):
        metrics = extract_frames(test_video_path, test_output_dir, frame_step=30)
        logging.info(f"Frame extraction metrics: {metrics}")
    else:
        logging.warning(f"Test video not found at {test_video_path}. Skipping direct run example for frame_extractor.")
'''