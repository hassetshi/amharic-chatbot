"""
YOLOv8 Object Detection Module
Detects objects in images and returns detection results
"""

from ultralytics import YOLO
from PIL import Image
import numpy as np
from typing import List, Dict, Tuple
import cv2


class ObjectDetector:
    """YOLOv8-based object detector"""

    def __init__(self, model_path: str = "yolov8n.pt"):
        """
        Initialize the object detector

        Args:
            model_path: Path to YOLOv8 model weights (default: yolov8n.pt for nano model)
        """
        self.model = YOLO(model_path)

    def detect(self, image: Image.Image, confidence: float = 0.5) -> Tuple[Image.Image, List[Dict]]:
        """
        Detect objects in an image

        Args:
            image: PIL Image object
            confidence: Minimum confidence threshold (0-1)

        Returns:
            Tuple of (annotated image, list of detection dictionaries)
        """
        # Run inference
        results = self.model(image, conf=confidence)

        # Get annotated image
        annotated_image = results[0].plot()
        annotated_image = Image.fromarray(annotated_image)

        # Extract detection information
        detections = []
        for result in results[0].boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = result
            class_name = self.model.names[int(cls)]

            detections.append({
                "class": class_name,
                "confidence": round(conf, 2),
                "bbox": [int(x1), int(y1), int(x2), int(y2)]
            })

        return annotated_image, detections

    def get_detection_summary(self, detections: List[Dict]) -> str:
        """
        Create a summary of detected objects

        Args:
            detections: List of detection dictionaries

        Returns:
            Summary string in English
        """
        if not detections:
            return "No objects detected in the image."

        # Count objects by class
        object_counts = {}
        for det in detections:
            class_name = det["class"]
            object_counts[class_name] = object_counts.get(class_name, 0) + 1

        # Create summary
        summary_parts = []
        for obj, count in object_counts.items():
            if count == 1:
                summary_parts.append(f"1 {obj}")
            else:
                summary_parts.append(f"{count} {obj}s")

        summary = f"I detected: {', '.join(summary_parts)}"

        # Add confidence information
        avg_conf = sum(d["confidence"] for d in detections) / len(detections)
        summary += f" (average confidence: {avg_conf:.0%})"

        return summary
