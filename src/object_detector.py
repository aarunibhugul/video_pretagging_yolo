# src/object_detector.py
import os
import json
import logging
from ultralytics import YOLO
from tqdm import tqdm
from collections import defaultdict
from typing import Dict, List, Any

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pretag_images_and_generate_coco(
    image_dir: str,
    output_coco_path: str,
    #model_name: str = 'yolov8n.pt'
    model_name: str
) -> Dict[str, Any]:


    """
    function - performs object detection on images and generates COCO-format annotations.

    paramters arguments:
        image_dir (str): Directory containing the images to be processed.
        output_coco_path (str): Full path where the COCO JSON file will be saved.
        model_name (str): Name or path of the YOLO model to use (e.g., 'yolov8n.pt').

    Returns:
        Dict[str, Any]: A dictionary containing COCO-format annotations and detection metrics.
    """
    if not os.path.exists(image_dir):
        logging.error(f"Image directory not found: {image_dir}")
        raise FileNotFoundError(f"Image directory not found: {image_dir}")

    logging.info(f"Loading YOLO model: {model_name}")
    try:
        model = YOLO(model_name)
    except Exception as e:
        logging.error(f"Failed to load YOLO model {model_name}: {e}")
        raise

    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    if not image_files:
        logging.warning(f"No image files found in '{image_dir}'. Skipping detection.")
        return {
            "coco_data": {
                "images": [],
                "annotations": [],
                "categories": []
            },
            "metrics": {
                "images_processed": 0,
                "total_detections": 0,
                "detections_per_frame_avg": 0,
                "class_distribution": {}
            }
        }

    coco_output: Dict[str, Any] = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    category_map: Dict[str, int] = {}
    next_image_id, next_ann_id, next_category_id = 1, 1, 1

    total_detections = 0
    detections_per_frame_counts = []
    class_distribution = defaultdict(int)

    logging.info(f"Starting pre-tagging of {len(image_files)} images...")

    for image_file in tqdm(image_files, desc="Pre-tagging Images"):
        img_path = os.path.join(image_dir, image_file)
        
        current_frame_detections = 0
        try:
            results = model(img_path, verbose=False)[0] # verbose=False to reduce console output
        except Exception as e:
            logging.error(f"Error processing image {image_file}: {e}")
            continue # Skip to next image on error

        height, width = results.orig_shape

        coco_output["images"].append({
            "id": next_image_id,
            "file_name": image_file,
            "height": height,
            "width": width
        })

        for det in results.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls_id = det
            cls_id = int(cls_id)
            label = model.names[cls_id]

            if label not in category_map:
                category_map[label] = next_category_id
                coco_output["categories"].append({
                    "id": next_category_id,
                    "name": label
                })
                next_category_id += 1

            bbox_width = x2 - x1
            bbox_height = y2 - y1
            coco_output["annotations"].append({
                "id": next_ann_id,
                "image_id": next_image_id,
                "category_id": category_map[label],
                "bbox": [x1, y1, bbox_width, bbox_height], # COCO bbox is [x, y, width, height]
                "area": bbox_width * bbox_height,
                "iscrowd": 0, # Assuming individual objects
                "segmentation": [], # Not generating segmentation in this basic pipeline
                "confidence": float(conf) # Added confidence for potential reporting
            })
            next_ann_id += 1
            total_detections += 1
            current_frame_detections += 1
            class_distribution[label] += 1
        
        detections_per_frame_counts.append(current_frame_detections)
        next_image_id += 1

    # Ensure categories are added even if no detections, for consistency in COCO file structure
    if not coco_output["categories"] and model.names:
        for cls_id, name in model.names.items():
            if name not in category_map:
                category_map[name] = next_category_id
                coco_output["categories"].append({
                    "id": next_category_id,
                    "name": name
                })
                next_category_id += 1

    logging.info(f"Pre-tagging complete. Saving annotations to '{output_coco_path}'")
    try:
        with open(output_coco_path, 'w') as f:
            json.dump(coco_output, f, indent=2)
    except IOError as e:
        logging.error(f"Failed to save COCO output to {output_coco_path}: {e}")
        raise

    logging.info(f"COCO-format annotations saved to {output_coco_path}")

    # Calculate final metrics
    images_processed = len(image_files)
    detections_per_frame_avg = sum(detections_per_frame_counts) / images_processed if images_processed > 0 else 0

    metrics = {
        "images_processed": images_processed,
        "total_detections": total_detections,
        "detections_per_frame_avg": detections_per_frame_avg,
        "class_distribution": dict(class_distribution) # Convert defaultdict to dict for output
    }

    return {
        "coco_data": coco_output,
        "metrics": metrics
    }

if __name__ == "__main__":
    # Example usage if run directly (for testing)
    # This requires 'test_extracted_frames' directory with images
    test_image_dir = "test_extracted_frames"
    test_coco_output_path = "test_detections.json"

    if os.path.exists(test_image_dir) and os.listdir(test_image_dir):
        logging.info(f"Running object_detector.py in test mode with images from '{test_image_dir}'")
        result = pretag_images_and_generate_coco(test_image_dir, test_coco_output_path)
        logging.info(f"Detection metrics: {result['metrics']}")
    else:
        logging.warning(f"No images found in '{test_image_dir}' or directory does not exist. "
                        "Skipping direct run example for object_detector.")
        logging.warning("Please run frame_extractor.py first or ensure test_extracted_frames has images.")
