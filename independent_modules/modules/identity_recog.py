import cv2
import numpy as np
import sqlite3
import datetime
import json
from typing import Tuple, Dict, Optional
import torch
from pathlib import Path

class YOLOCrowdAnalytics:
    def __init__(self, db_path='crowd_analytics.db'):
        """
        Initialize YOLO-based Crowd Analytics module
        
        Args:
            db_path (str): Path to SQLite database for storing crowd data
        """
        self.db_path = db_path
        
        # Initialize YOLO model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        # Set model parameters
        self.model.conf = 0.25  # Confidence threshold
        self.model.classes = [0]  # Only detect persons (class 0 in COCO)
        
        # Create database with proper schema
        self._create_database()
        
    def _create_database(self):
        """Create database tables for crowd analytics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Drop existing table if it exists to ensure correct schema
                cursor.execute('DROP TABLE IF EXISTS crowd_density')
                
                cursor.execute('''
                    CREATE TABLE crowd_density (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME,
                        location TEXT,
                        density_level INTEGER,
                        people_count INTEGER,
                        detection_boxes TEXT,
                        frame_width INTEGER,
                        frame_height INTEGER,
                        average_confidence REAL
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
    
    def process_frame(self, frame: np.ndarray, location: str) -> Tuple[np.ndarray, Dict]:
        """
        Process a video frame to detect people using YOLO and generate visualization
        
        Args:
            frame (np.ndarray): Input video frame
            location (str): Location identifier
        
        Returns:
            Tuple[np.ndarray, Dict]: Processed frame with visualizations and analysis data
        """
        try:
            # Make a copy of the frame for visualization
            display_frame = frame.copy()
            height, width = frame.shape[:2]
            
            # Run YOLO detection
            results = self.model(frame)
            
            # Create heatmap layer
            heatmap = np.zeros((height, width), dtype=np.float32)
            
            # Process detections
            processed_boxes = []
            confidences = []
            
            # Get detections from YOLO results
            detections = results.xyxy[0].cpu().numpy()
            
            if len(detections) > 0:
                for detection in detections:
                    x1, y1, x2, y2, conf, cls = detection
                    
                    if cls == 0:  # Person class
                        # Convert to integers
                        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                        
                        # Store detection data
                        processed_boxes.append({
                            'x': x1,
                            'y': y1,
                            'width': x2 - x1,
                            'height': y2 - y1,
                            'confidence': float(conf)
                        })
                        confidences.append(conf)
                        
                        # Draw rectangle around person
                        cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        # Add confidence text
                        cv2.putText(display_frame, f'{conf:.2f}', (x1, y1-10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        # Add to heatmap
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        radius = int((y2 - y1) * 0.3)  # Radius based on person height
                        cv2.circle(heatmap, (center_x, center_y), radius, conf, -1)
                
                # Process heatmap
                if np.max(heatmap) > 0:
                    heatmap = cv2.GaussianBlur(heatmap, (99, 99), 0)
                    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
                    heatmap = cv2.applyColorMap(heatmap.astype(np.uint8), cv2.COLORMAP_JET)
                    
                    # Blend heatmap with original frame
                    overlay = cv2.addWeighted(display_frame, 0.7, heatmap, 0.3, 0)
                else:
                    overlay = display_frame
            else:
                overlay = display_frame
            
            # Calculate metrics
            people_count = len(processed_boxes)
            density_per_area = people_count / (width * height) * 10000  # per 10000 pixels
            avg_confidence = np.mean(confidences) if confidences else 0
            
            # Prepare analysis data
            analysis_data = {
                'timestamp': datetime.datetime.now(),
                'location': location,
                'people_count': people_count,
                'density_level': people_count,
                'density_per_area': density_per_area,
                'detection_boxes': processed_boxes,
                'frame_width': width,
                'frame_height': height,
                'average_confidence': avg_confidence
            }
            
            # Store in database
            self._store_analysis(analysis_data)
            
            # Add text overlay with information
            cv2.putText(overlay, f"People: {people_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(overlay, f"Density: {density_per_area:.2f}/10k px", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(overlay, f"Avg Conf: {avg_confidence:.2f}", (10, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            return overlay, analysis_data
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            return frame, None
    
    def _store_analysis(self, analysis_data: Dict):
        """
        Store analysis data in database
        
        Args:
            analysis_data (Dict): Analysis results to store
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO crowd_density 
                    (timestamp, location, density_level, people_count, detection_boxes,
                     frame_width, frame_height, average_confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    analysis_data['timestamp'],
                    analysis_data['location'],
                    analysis_data['density_level'],
                    analysis_data['people_count'],
                    json.dumps(analysis_data['detection_boxes']),
                    analysis_data['frame_width'],
                    analysis_data['frame_height'],
                    analysis_data['average_confidence']
                ))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error while storing analysis: {e}")
    
    def get_historical_data(self, start_time: datetime.datetime,
                          end_time: datetime.datetime,
                          location: Optional[str] = None) -> list:
        """
        Retrieve historical crowd data for a specific time period
        
        Args:
            start_time (datetime): Start of time period
            end_time (datetime): End of time period
            location (str, optional): Filter by location
        
        Returns:
            list: Historical crowd data
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT timestamp, location, density_level, people_count,
                           detection_boxes, frame_width, frame_height, average_confidence
                    FROM crowd_density
                    WHERE timestamp BETWEEN ? AND ?
                '''
                params = [start_time, end_time]
                
                if location:
                    query += ' AND location = ?'
                    params.append(location)
                
                cursor.execute(query, params)
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        'timestamp': datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'),
                        'location': row[1],
                        'density_level': row[2],
                        'people_count': row[3],
                        'detection_boxes': json.loads(row[4]),
                        'frame_width': row[5],
                        'frame_height': row[6],
                        'average_confidence': row[7]
                    })
                
                return results
        except sqlite3.Error as e:
            print(f"Database error while retrieving historical data: {e}")
            return []

def main():
    try:
        # Initialize the YOLO crowd analytics system
        crowd_analytics = YOLOCrowdAnalytics()
        
        # Initialize video capture (0 for webcam or provide video file path)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open video capture device")
            return
        
        print("Starting YOLO crowd analytics... Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
                
            # Process frame
            processed_frame, analysis = crowd_analytics.process_frame(frame, "Camera 1")
            
            if processed_frame is not None:
                # Display result
                cv2.imshow('YOLO Crowd Analytics', processed_frame)
            
            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()