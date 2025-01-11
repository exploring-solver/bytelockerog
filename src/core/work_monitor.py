import time
import queue
from ..utils.logging_setup import logger
import cv2
import logging
import numpy as np
from config.config import SystemConfig
import tensorflow as tf 
from typing import List, Dict, Tuple
class WorkMonitor:
    """Monitors workplace safety and efficiency"""
    def __init__(self, config: SystemConfig):
        self.config = config
        self.pose_model = None
        if config.enable_pose_detection:
            try:
                self.pose_model = tf.keras.models.load_model('models/pose_model.h5')
            except Exception as e:
                logging.warning(f"Pose model not loaded: {e}. Running without pose detection.")
                
    def monitor_safety(self, frame: np.ndarray, detections: List[Dict]) -> List[Dict]:
        """Monitor workplace safety violations"""
        violations = []
        
        if not self.pose_model:
            # Basic safety monitoring without pose detection
            for detection in detections:
                # Simple proximity-based violations
                bbox = detection['bbox']
                for other in detections:
                    if other != detection:
                        if self._check_proximity(bbox, other['bbox']):
                            violations.append({
                                'type': 'proximity_violation',
                                'location': ((bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2),
                                'confidence': detection['confidence']
                            })
        else:
            # Full pose-based safety monitoring
            for detection in detections:
                bbox = detection['bbox']
                person_roi = frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                if person_roi.size > 0:  # Check if ROI is valid
                    try:
                        pose = self.pose_model.predict(
                            cv2.resize(person_roi, (224, 224))[np.newaxis, ...],
                            verbose=0
                        )
                        if self._is_unsafe_pose(pose):
                            violations.append({
                                'type': 'unsafe_pose',
                                'location': ((bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2),
                                'confidence': detection['confidence']
                            })
                    except Exception as e:
                        logging.warning(f"Error in pose detection: {e}")
                        
        return violations
    
    def _check_proximity(self, bbox1: Tuple, bbox2: Tuple, min_distance: int = 50) -> bool:
        """Check if two bounding boxes are too close"""
        center1 = ((bbox1[0] + bbox1[2])/2, (bbox1[1] + bbox1[3])/2)
        center2 = ((bbox2[0] + bbox2[2])/2, (bbox2[1] + bbox2[3])/2)
        distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        return distance < min_distance
    
    def _is_unsafe_pose(self, pose) -> bool:
        """Analyze if pose is unsafe"""
        # Implementation depends on specific safety rules
        return False  # Placeholder
