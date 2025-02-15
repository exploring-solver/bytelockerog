import cv2
import numpy as np
import sqlite3
import datetime
import json
import torch
import warnings
from typing import Tuple, Dict, Optional

# Filter out the specific deprecation warning
warnings.filterwarnings("ignore", category=FutureWarning, 
                      message=".*torch.cuda.amp.autocast.*")

class CrowdAnalytics:
    def __init__(self, db_path='crowd_analytics.db'):
        """
        Initialize Crowd Analytics module with YOLO model and database
        """
        self.db_path = db_path
        
        # Load YOLOv5 model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        # Set model parameters
        self.model.conf = 0.3  # Confidence threshold
        self.model.classes = [0]  # Only detect people (class 0 in COCO)
        self.model.to('cpu')  # Ensure CPU usage
        
        # Create database
        self._create_database()
        
    def _create_database(self):
        """Create database tables for crowd analytics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
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
                        frame_height INTEGER
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
    
    def process_frame(self, frame: np.ndarray, location: str) -> Tuple[np.ndarray, Dict]:
        """
        Process a video frame using YOLO to detect people
        """
        try:
            # Make a copy for visualization
            display_frame = frame.copy()
            height, width = frame.shape[:2]
            
            # Run YOLO detection
            results = self.model(frame)
            detections = results.xyxy[0].cpu().numpy()  # Get detection boxes
            
            # Create heatmap layer
            heatmap = np.zeros((height, width), dtype=np.float32)
            processed_boxes = []
            
            # Process detected people
            people_count = 0
            for detection in detections:
                if detection[5] == 0:  # Class 0 is person
                    people_count += 1
                    x1, y1, x2, y2 = map(int, detection[:4])
                    confidence = detection[4]
                    
                    # Store detection data
                    processed_boxes.append({
                        'x': int(x1),
                        'y': int(y1),
                        'width': int(x2 - x1),
                        'height': int(y2 - y1),
                        'confidence': float(confidence)
                    })
                    
                    # Draw rectangle around person
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Add to heatmap - fixed circle color value
                    center_x = int((x1 + x2) // 2)
                    center_y = int((y1 + y2) // 2)
                    radius = int((y2 - y1) // 3)  # Use height for radius
                    cv2.circle(heatmap, (center_x, center_y), radius, 1.0, -1)  # Fixed numeric value
            
            # Process heatmap if people were detected
            if people_count > 0:
                # Normalize and colorize heatmap
                heatmap = cv2.GaussianBlur(heatmap, (99, 99), 0)
                heatmap_normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
                heatmap_colored = cv2.applyColorMap(heatmap_normalized.astype(np.uint8), cv2.COLORMAP_JET)
                
                # Blend heatmap with original frame
                overlay = cv2.addWeighted(display_frame, 0.7, heatmap_colored, 0.3, 0)
            else:
                overlay = display_frame.copy()
            
            # Calculate density metrics
            density_per_area = people_count / (width * height) * 10000  # per 10000 pixels
            
            # Prepare analysis data
            analysis_data = {
                'timestamp': datetime.datetime.now(),
                'location': location,
                'people_count': people_count,
                'density_level': people_count,
                'density_per_area': density_per_area,
                'detection_boxes': processed_boxes,
                'frame_width': width,
                'frame_height': height
            }
            
            # Store in database
            self._store_analysis(analysis_data)
            
            # Add text overlay
            cv2.putText(overlay, f"People: {people_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(overlay, f"Density per 10k px: {density_per_area:.2f}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            return overlay, analysis_data
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            import traceback
            traceback.print_exc()
            return frame, None
    
    def _store_analysis(self, analysis_data: Dict):
        """Store analysis data in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO crowd_density 
                    (timestamp, location, density_level, people_count, detection_boxes,
                     frame_width, frame_height)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    analysis_data['timestamp'],
                    analysis_data['location'],
                    analysis_data['density_level'],
                    analysis_data['people_count'],
                    json.dumps(analysis_data['detection_boxes']),
                    analysis_data['frame_width'],
                    analysis_data['frame_height']
                ))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error while storing analysis: {e}")
    
    def get_historical_data(self, start_time: datetime.datetime,
                          end_time: datetime.datetime,
                          location: Optional[str] = None) -> list:
        """Retrieve historical crowd data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT timestamp, location, density_level, people_count,
                           detection_boxes, frame_width, frame_height
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
                        'frame_height': row[6]
                    })
                
                return results
        except sqlite3.Error as e:
            print(f"Database error while retrieving historical data: {e}")
            return []

def main():
    try:
        print("Starting YOLO crowd analytics... Press 'q' to quit")
        crowd_analytics = CrowdAnalytics()
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open video capture device")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            processed_frame, analysis = crowd_analytics.process_frame(frame, "Camera 1")
            
            if processed_frame is not None:
                cv2.imshow('Crowd Analytics', processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWiwndows()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()