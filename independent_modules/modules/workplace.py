import cv2
import numpy as np
import sqlite3
import datetime
import json
import tensorflow as tf
from tensorflow.keras.models import load_model
from typing import Dict, Any

class WorkplaceSafetyMonitor:
    def __init__(self, db_path='workplace_safety.db', model_path=None):
        """
        Initialize Workplace Safety Monitoring module
        
        Args:
            db_path (str): Path to SQLite database
            model_path (str, optional): Path to pre-trained PPE detection model
        """
        self.db_path = db_path
        self._create_database()
        
        # Load or create PPE detection model
        self.ppe_model = self._load_or_create_ppe_model(model_path)
    
    def _create_database(self):
        """Create database tables for workplace safety"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS safety_incidents (
                    timestamp DATETIME,
                    location TEXT,
                    incident_type TEXT,
                    severity INTEGER,
                    ppe_compliance REAL,
                    additional_details TEXT
                )
            ''')
            conn.commit()
    
    def _load_or_create_ppe_model(self, model_path=None):
        """
        Load or create a PPE detection model
        
        Args:
            model_path (str, optional): Path to existing model
        
        Returns:
            tf.keras.Model: PPE detection model
        """
        if model_path:
            try:
                return load_model(model_path)
            except Exception:
                pass
        
        # Create a simple PPE detection model if no existing model
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(3, activation='softmax')  # helmet, vest, no-ppe
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
    
    def detect_ppe(self, frame, location: str):
        """
        Detect Personal Protective Equipment (PPE) in the frame
        
        Args:
            frame (numpy.ndarray): Input video frame
            location (str): Workplace location
        
        Returns:
            dict: PPE detection results
        """
        # Preprocess frame
        resized_frame = cv2.resize(frame, (224, 224))
        input_frame = np.expand_dims(resized_frame, axis=0) / 255.0
        
        # Predict PPE
        predictions = self.ppe_model.predict(input_frame)
        ppe_classes = ['helmet', 'vest', 'no_ppe']
        detected_ppe = ppe_classes[np.argmax(predictions)]
        
        # Compliance calculation
        ppe_compliance = predictions[0][ppe_classes.index('helmet')] * 0.5 + \
                         predictions[0][ppe_classes.index('vest')] * 0.5
        
        # Prepare safety incident data
        safety_data = {
            'timestamp': datetime.datetime.now(),
            'location': location,
            'incident_type': 'PPE_CHECK',
            'severity': 2 if detected_ppe == 'no_ppe' else 1,
            'ppe_compliance': float(ppe_compliance),
            'additional_details': json.dumps({
                'detected_ppe': detected_ppe,
                'confidence': float(np.max(predictions))
            })
        }
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO safety_incidents 
                (timestamp, location, incident_type, severity, 
                 ppe_compliance, additional_details) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                safety_data['timestamp'],
                safety_data['location'],
                safety_data['incident_type'],
                safety_data['severity'],
                safety_data['ppe_compliance'],
                safety_data['additional_details']
            ))
            conn.commit()
        
        return safety_data
    
    def detect_slip_and_trip(self, frame, location: str):
        """
        Detect potential slip and trip hazards
        
        Args:
            frame (numpy.ndarray): Input video frame
            location (str): Workplace location
        
        Returns:
            dict: Slip and trip detection results
        """
        # Convert to grayscale for better edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours that might represent hazards
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analyze contours for potential hazards
        potential_hazards = [
            cv2.contourArea(contour) for contour in contours 
            if cv2.contourArea(contour) > 500  # Minimum area threshold
        ]
        
        # Prepare slip/trip incident data
        slip_trip_data = {
            'timestamp': datetime.datetime.now(),
            'location': location,
            'incident_type': 'SLIP_TRIP_CHECK',
            'severity': 3 if potential_hazards else 1,
            'hazard_count': len(potential_hazards),
            'additional_details': json.dumps({
                'hazard_areas': [float(area) for area in potential_hazards]
            })
        }
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO safety_incidents 
                (timestamp, location, incident_type, severity, 
                 ppe_compliance, additional_details) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                slip_trip_data['timestamp'],
                slip_trip_data['location'],
                slip_trip_data['incident_type'],
                slip_trip_data['severity'],
                0.0,  # No PPE compliance for slip/trip
                slip_trip_data['additional_details']
            ))
            conn.commit()
        
        return slip_trip_data

# Example usage
if __name__ == "__main__":
    safety_monitor = WorkplaceSafetyMonitor()
    
    # Simulated frame (in practice, this would come from a camera)
    dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Detect PPE
    ppe_result = safety_monitor.detect_ppe(dummy_frame, "Construction Site A")
    print("PPE Detection Result:", ppe_result)
    
    # Detect Slip and Trip Hazards
    slip_trip_result = safety_monitor.detect_slip_and_trip(dummy_frame, "Industrial Floor")
    print("Slip/Trip Detection Result:", slip_trip_result)