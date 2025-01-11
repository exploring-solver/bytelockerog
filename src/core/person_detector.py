import torch
import face_recognition
import pickle
import os
import logging
from typing import List, Dict
from config.config import SystemConfig
import numpy as np

class PersonDetector:
    """Handles person detection using YOLOv5"""
    def __init__(self, config: SystemConfig):
        try:
            print("Initializing YOLOv5 model...")
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            self.config = config
            self.known_face_encodings = {}
            self.load_face_encodings()
            print("YOLOv5 model initialized successfully.")
        except Exception as e:
            logging.error(f"Error loading YOLOv5 model: {e}")
            print(f"Error loading YOLOv5 model: {e}")
            raise

    def load_face_encodings(self):
        print("Loading known face encodings...")
        face_data_dir = os.path.abspath('src/core/face_data')  # Absolute path

        if os.path.exists(face_data_dir):
            for file in os.listdir(face_data_dir):
                if file.endswith('_encodings.pkl'):
                    name = file.replace('_encodings.pkl', '')
                    with open(os.path.join(face_data_dir, file), 'rb') as f:
                        self.known_face_encodings[name] = pickle.load(f)
                    print(f"Loaded encodings for: {name}")
        else:
            print(f"No face data directory found at {face_data_dir}.")
        print("Finished loading face encodings.")

    def detect(self, frame: np.ndarray) -> List[Dict]:
        print("Detecting objects in the frame...")
        results = self.model(frame)
        detections = []

        print("Detecting faces in the frame...")
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        print(f"Found {len(face_locations)} face(s) in the frame.")

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            print(f"Processing face at location: {(top, right, bottom, left)}")
            for known_name, known_encodings in self.known_face_encodings.items():
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                if True in matches:
                    name = known_name
                    print(f"Match found: {name}")
                    break
            else:
                print("No match found for this face.")

            detections.append({
                'bbox': (left, top, right, bottom),
                'confidence': 1.0,
                'name': name
            })

        print(f"Detections completed. Found {len(detections)} face(s).")
        return detections
