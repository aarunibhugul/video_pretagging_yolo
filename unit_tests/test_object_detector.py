import os
import shutil
import numpy as np
import cv2
import pytest
from src.object_detector import pretag_images_and_generate_coco

TEST_IMG_DIR = "unit_test_input/frame"
COCO_PATH = "unit_test_output/test_output_coco.json"


def test_pretag_images_and_generate_coco():
    os.makedirs(TEST_IMG_DIR, exist_ok=True)

    result = pretag_images_and_generate_coco(TEST_IMG_DIR, COCO_PATH)
    metrics = result["metrics"]
    assert "images_processed" in metrics
    assert os.path.exists(COCO_PATH)
    assert metrics["images_processed"] == 3