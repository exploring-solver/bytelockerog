import cv2
import torch
import face_recognition
import pickle
import os
import logging
import numpy as np
from typing import List, Dict

# Assuming SystemConfig is properly defined elsewhere
class SystemConfig:
    pass

class PersonDetector:
    """Handles person detection using YOLOv5"""
    def __init__(self, config: SystemConfig):
        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            self.config = config
            self.known_face_encodings = {}
            self.load_face_encodings()
        except Exception as e:
            logging.error(f"Error loading YOLOv5 model: {e}")
            raise

    def load_face_encodings(self):
        if os.path.exists('face_data'):
            for file in os.listdir('face_data'):
                if file.endswith('_encodings.pkl'):
                    name = file.replace('_encodings.pkl', '')
                    with open(f'face_data/{file}', 'rb') as f:
                        self.known_face_encodings[name] = pickle.load(f)
    
    def detect(self, frame: np.ndarray) -> List[Dict]:
        results = self.model(frame)
        detections = []
        
        # Get face locations and encodings
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            for known_name, known_encodings in self.known_face_encodings.items():
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                if True in matches:
                    name = known_name
                    break
                    
            detections.append({
                'bbox': (left, top, right, bottom),
                'confidence': 1.0,
                'name': name
            })
            
        return detections


def main():
    # Initialize the detector
    config = SystemConfig()
    detector = PersonDetector(config)

    # Start video capture
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Detect faces
        detections = detector.detect(small_frame)

        # Draw bounding boxes and names on the original frame
        for detection in detections:
            left, top, right, bottom = detection['bbox']
            name = detection['name']

            # Scale back up face locations since the frame we used was scaled to 0.5
            left *= 2
            top *= 2
            right *= 2
            bottom *= 2

            # Draw rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
