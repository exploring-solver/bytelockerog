from fastapi.responses import StreamingResponse
import io
import cv2
import base64
import numpy as np
import tensorflow as tf
from datetime import datetime
import pandas as pd
from sklearn.cluster import DBSCAN
import face_recognition
import threading
import queue
import logging
from typing import Dict, List, Tuple, Optional
import yaml
from dataclasses import dataclass
import torch
import pickle
import json
import asyncio
from torch import nn
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from datetime import time
# Configuration and logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SystemConfig:
    """System configuration parameters"""
    min_confidence: float = 0.6
    frame_skip: int = 3
    max_crowd_density: float = 0.75
    restricted_areas: List[List[Tuple[int, int]]] = None
    working_hours: Tuple[int, int] = (9, 17)
    enable_pose_detection: bool = False
    
class VideoStream:
    """Handles video stream capture and preprocessing"""
    def __init__(self, source: str, config: SystemConfig):
        self.source = source
        self.config = config
        self.capture = cv2.VideoCapture(source)
        
        # Check if camera opened successfully
        if not self.capture.isOpened():
            raise ValueError(f"Error opening video source {source}")
            
        # Set camera properties
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.frame_queue = queue.Queue(maxsize=30)
        self._running = False
        
    def start(self):
        """Start video capture thread"""
        self._running = True
        threading.Thread(target=self._capture_frames, daemon=True).start()
        
    def _capture_frames(self):
        """Continuously capture frames from the video source"""
        frame_count = 0
        consecutive_failures = 0
        
        while self._running:
            try:
                ret, frame = self.capture.read()
                
                if not ret:
                    consecutive_failures += 1
                    logger.warning(f"Failed to capture frame from {self.source}")
                    if consecutive_failures > 10:
                        logger.error("Too many consecutive capture failures")
                        break
                    time.sleep(0.1)
                    continue
                    
                consecutive_failures = 0
                
                if frame_count % self.config.frame_skip == 0:
                    # Preprocess frame
                    processed_frame = preprocess_frame(frame)
                    if processed_frame is not None:
                        if not self.frame_queue.full():
                            self.frame_queue.put(processed_frame)
                        else:
                            # Clear oldest frame if queue is full
                            try:
                                self.frame_queue.get_nowait()
                            except queue.Empty:
                                pass
                            self.frame_queue.put(processed_frame)
                            
                frame_count += 1
                
            except Exception as e:
                logger.error(f"Error in frame capture: {str(e)}")
                time.sleep(0.1)
                
    def stop(self):
        """Stop video capture"""
        self._running = False
        if self.capture:
            self.capture.release()

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
            # Check if face matches any known faces
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

class CrowdAnalyzer:
    """Analyzes crowd density and movement patterns"""
    def __init__(self, config: SystemConfig):
        self.config = config
        self.clustering = DBSCAN(eps=30, min_samples=3)
        
    def analyze_crowd(self, detections: List[Dict]) -> Dict:
        """Analyze crowd density and patterns"""
        if not detections:
            return {'density': 0.0, 'hotspots': []}
            
        points = np.array([[(d['bbox'][0] + d['bbox'][2])/2, 
                           (d['bbox'][1] + d['bbox'][3])/2] for d in detections])
        
        clusters = self.clustering.fit_predict(points)
        unique_clusters = np.unique(clusters[clusters != -1])
        
        density = len(detections) / (640 * 480)  # normalized by frame size
        hotspots = []
        
        for cluster_id in unique_clusters:
            cluster_points = points[clusters == cluster_id]
            center = np.mean(cluster_points, axis=0)
            hotspots.append({
                'center': tuple(map(int, center)),
                'size': len(cluster_points)
            })
            
        return {
            'density': density,
            'hotspots': hotspots
        }

class BehaviorAnalyzer:
    """Analyzes behavior patterns and detects anomalies"""
    def __init__(self, config: SystemConfig):
        self.config = config
        self.movement_history = []
        
    def analyze_behavior(self, detections: List[Dict], 
                        restricted_areas: List[List[Tuple[int, int]]]) -> List[Dict]:
        """Analyze behavior and detect anomalies"""
        anomalies = []
        
        # Check for restricted area violations
        for detection in detections:
            bbox = detection['bbox']
            center = ((bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2)
            
            for area in restricted_areas:
                if self._point_in_polygon(center, area):
                    anomalies.append({
                        'type': 'restricted_area_violation',
                        'location': center,
                        'confidence': detection['confidence']
                    })
        
        # Analyze movement patterns
        if len(self.movement_history) > 10:
            current_positions = [(d['bbox'][0] + d['bbox'][2])/2 for d in detections]
            
            # Detect sudden movements
            for i, hist in enumerate(self.movement_history[-2:]):
                if abs(current_positions[i] - hist) > 100:  # threshold for sudden movement
                    anomalies.append({
                        'type': 'sudden_movement',
                        'location': (current_positions[i], detections[i]['bbox'][1]),
                        'confidence': detections[i]['confidence']
                    })
                    
            self.movement_history = self.movement_history[-10:]
        
        self.movement_history.extend([d['bbox'][0] for d in detections])
        return anomalies
    
    def _point_in_polygon(self, point: Tuple[float, float], 
                         polygon: List[Tuple[int, int]]) -> bool:
        """Check if point is inside polygon"""
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

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

class AlertSystem:
    """Handles alert generation and notification"""
    def __init__(self, config: SystemConfig):
        self.config = config
        self.alert_queue = queue.Queue()
        
    def generate_alert(self, alert_type: str, details: Dict):
        """Generate and queue an alert"""
        try:
            # Ensure details are JSON serializable
            serializable_details = {}
            for key, value in details.items():
                if isinstance(value, (int, float, str, bool, list, dict)):
                    serializable_details[key] = value
                else:
                    serializable_details[key] = str(value)
            
            alert = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': alert_type,
                'details': serializable_details
            }
            
            self.alert_queue.put(alert)
            logger.info(f"Alert generated: {alert_type}")
            
        except Exception as e:
            logger.error(f"Error generating alert: {str(e)}")
    
    def get_alerts(self) -> List[Dict]:
        """Get all current alerts as a list"""
        alerts = []
        while not self.alert_queue.empty():
            try:
                alert = self.alert_queue.get_nowait()
                alerts.append(alert)
            except queue.Empty:
                break
        return alerts

    async def send_alert(self, websocket: WebSocket):
        """Send alert to connected client"""
        while True:
            if not self.alert_queue.empty():
                try:
                    alert = self.alert_queue.get()
                    # Ensure alert is JSON serializable
                    json_alert = json.dumps(alert, default=str)
                    await websocket.send_text(json_alert)
                except Exception as e:
                    logger.error(f"Error sending alert: {str(e)}")
            await asyncio.sleep(0.1)

class DatabaseHandler:
    """Handles database operations with MySQL"""
    def __init__(self, config: dict):
        # Create MySQL connection string
        connection_string = (
            f"mysql+pymysql://{config.get('root', 'root')}:"
            f"{config.get('password', '')}@"
            f"{config.get('host', 'localhost')}/"
            f"{config.get('database', 'bytelocker')}"
        )
        
        try:
            self.engine = create_engine(connection_string)
            Base = declarative_base()
            
            class Event(Base):
                __tablename__ = 'events'
                id = Column(Integer, primary_key=True, autoincrement=True)
                timestamp = Column(DateTime, nullable=False)
                event_type = Column(String(255), nullable=False)
                details = Column(String(1000))
                confidence = Column(Float)
                
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.Event = Event
            
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def log_event(self, event_type: str, details: Dict, confidence: float):
        """Log event to database"""
        session = self.Session()
        try:
            event = self.Event(
                timestamp=datetime.now(),
                event_type=event_type,
                details=str(details),
                confidence=confidence
            )
            session.add(event)
            session.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

class CCTVSystem:
    """Main system class that coordinates all components"""
    def __init__(self, config_path: str):
        try:
            with open(config_path, 'r') as f:
                config_dict = yaml.safe_load(f)
            
            # Extract database config
            self.db_config = config_dict.pop('db_config', {})
            
            # Initialize system config
            self.config = SystemConfig(**config_dict)
            
            self.video_streams = {}
            self.person_detector = PersonDetector(self.config)
            self.crowd_analyzer = CrowdAnalyzer(self.config)
            self.behavior_analyzer = BehaviorAnalyzer(self.config)
            self.work_monitor = WorkMonitor(self.config)
            self.alert_system = AlertSystem(self.config)
            
            # Initialize database handler
            self.db_handler = DatabaseHandler(self.db_config)
            
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {config_path}")
            raise
        except Exception as e:
            logging.error(f"Initialization error: {e}")
            raise
        
    def add_camera(self, camera_id: str, source: str):
        """Add new camera stream"""
        stream = VideoStream(source, self.config)
        self.video_streams[camera_id] = stream
        stream.start()
        
    def process_frame(self, camera_id: str):
        """Process single frame from camera"""
        stream = self.video_streams.get(camera_id)
        if not stream or stream.frame_queue.empty():
            return
            
        frame = stream.frame_queue.get()
        
        # Detect persons
        detections = self.person_detector.detect(frame)
        
        # Analyze crowd
        crowd_analysis = self.crowd_analyzer.analyze_crowd(detections)
        if crowd_analysis['density'] > self.config.max_crowd_density:
            self.alert_system.generate_alert('high_crowd_density', crowd_analysis)
            
        # Analyze behavior
        anomalies = self.behavior_analyzer.analyze_behavior(
            detections, self.config.restricted_areas)
        for anomaly in anomalies:
            self.alert_system.generate_alert('behavior_anomaly', anomaly)
            
        # Monitor workplace safety
        if self._is_working_hours():
            violations = self.work_monitor.monitor_safety(frame, detections)
            for violation in violations:
                self.alert_system.generate_alert('safety_violation', violation)
                
        # Log events
        for detection in detections:
            self.db_handler.log_event('person_detected', detection, 
                                    detection['confidence'])
                                    
    def _is_working_hours(self) -> bool:
        """Check if current time is within working hours"""
        current_hour = datetime.now().hour
        return self.config.working_hours[0] <= current_hour <= self.config.working_hours[1]
        
    def run(self):
        """Main processing loop"""
        while True:
            for camera_id in self.video_streams:
                self.process_frame(camera_id)


# API Implementation
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Cache-Control"]
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {str(e)}")
                await self.disconnect(connection)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    try:
        # Create minimal config if file doesn't exist
        if not os.path.exists('config.yml'):
            default_config = {
                'min_confidence': 0.6,
                'frame_skip': 3,
                'max_crowd_density': 0.75,
                'restricted_areas': [],
                'working_hours': [9, 17],
                'enable_pose_detection': False,
                'db_config': {
                    'host': 'localhost',
                    'user': 'root',
                    'password': '',
                    'database': 'bytelocker'
                }
            }
            with open('config.yml', 'w') as f:
                yaml.dump(default_config, f)
        
        global system
        system = CCTVSystem('config.yml')
        
        # Add test camera (use 0 for webcam)
        system.add_camera('test_cam', 0)
        
    except Exception as e:
        logging.error(f"Startup error: {e}")
        raise

def inspect_frame(frame):
    """
    Inspect frame properties for debugging
    """
    if frame is None:
        logger.info("Frame is None")
        return None
        
    logger.info(f"Frame type: {type(frame)}")
    logger.info(f"Frame shape: {frame.shape if hasattr(frame, 'shape') else 'No shape attribute'}")
    logger.info(f"Frame dtype: {frame.dtype if hasattr(frame, 'dtype') else 'No dtype attribute'}")
    
    if isinstance(frame, np.ndarray):
        logger.info(f"Frame min value: {frame.min()}")
        logger.info(f"Frame max value: {frame.max()}")
        
    return frame

def preprocess_frame(frame):
    """
    Preprocess frame to ensure it's in the correct format for YOLOv5 and face_recognition
    
    Args:
        frame: Input frame from video stream
        
    Returns:
        numpy.ndarray: Processed frame in RGB format with uint8 dtype
    """
    if frame is None:
        logger.error("Received None frame")
        return None
        
    try:
        # Convert to numpy array if needed
        if not isinstance(frame, np.ndarray):
            logger.error(f"Invalid frame type: {type(frame)}")
            return None
            
        # Make a copy to avoid modifying original
        frame = frame.copy()
        
        # Check frame dimensions
        if len(frame.shape) < 2:
            logger.error(f"Invalid frame shape: {frame.shape}")
            return None
            
        # Handle different color spaces
        if len(frame.shape) == 2:  # Grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif len(frame.shape) == 3:
            if frame.shape[2] == 4:  # RGBA
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
            elif frame.shape[2] == 3:  # BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
        # Ensure uint8 dtype
        if frame.dtype != np.uint8:
            if frame.max() <= 1.0:
                frame = (frame * 255).astype(np.uint8)
            else:
                frame = frame.astype(np.uint8)
        
        # Verify final frame properties
        if not (frame.dtype == np.uint8 and len(frame.shape) == 3 and frame.shape[2] == 3):
            logger.error(f"Invalid processed frame: dtype={frame.dtype}, shape={frame.shape}")
            return None
            
        return frame
        
    except Exception as e:
        logger.error(f"Frame preprocessing error: {str(e)}")
        return None

@app.get("/video-feed")
async def video_feed():
    async def generate_frames():
        while True:
            try:
                # Get frame from the video stream
                frame = system.video_streams['test_cam'].frame_queue.get()
                if frame is not None:
                    # Convert frame to JPEG format
                    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    frame_bytes = base64.b64encode(buffer.tobytes()).decode('utf-8')
                    # Yield the frame with proper format
                    yield f"data: data:image/jpeg;base64,{frame_bytes}\n\n"
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in video feed: {str(e)}")
                continue

    return StreamingResponse(
        generate_frames(),
        media_type='text/event-stream'
    )

@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            try:
                # Get frame with timeout
                try:
                    frame = await asyncio.wait_for(
                        asyncio.to_thread(
                            system.video_streams['test_cam'].frame_queue.get
                        ),
                        timeout=1.0
                    )
                except (asyncio.TimeoutError, queue.Empty):
                    # Send heartbeat if no frame available
                    await websocket.send_json({
                        "status": "active",
                        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    continue
                
                # Skip if frame is None
                if frame is None:
                    logger.warning("Received None frame")
                    continue
                
                # Process frame
                try:
                    detected_people = system.person_detector.detect(frame)
                    people_count = len(detected_people) if detected_people is not None else 0
                    
                    crowd_analysis = system.crowd_analyzer.analyze_crowd(detected_people)
                    density = crowd_analysis.get('density', 0) if crowd_analysis else 0
                    
                    current_time = datetime.now()
                    
                    # Convert queue to list for alerts
                    alerts = []
                    while not system.alert_system.alert_queue.empty():
                        try:
                            alert = system.alert_system.alert_queue.get_nowait()
                            if isinstance(alert, dict):
                                # Ensure datetime objects are converted to strings
                                if 'timestamp' in alert and isinstance(alert['timestamp'], datetime):
                                    alert['timestamp'] = alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                                alerts.append(alert)
                        except queue.Empty:
                            break
                    
                    # Prepare response data
                    stats = {
                        'peopleCount': people_count,
                        'crowdDensity': [{
                            'time': current_time.strftime('%H:%M:%S'),
                            'density': float(density)  # Ensure density is JSON serializable
                        }],
                        'alerts': alerts,
                        'violations': [],  # Add actual violations here if needed
                        'status': 'success',
                        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Ensure all data is JSON serializable
                    json_stats = json.dumps(stats, default=str)
                    await websocket.send_text(json_stats)
                    
                except Exception as e:
                    logger.error(f"Frame processing error: {str(e)}")
                    error_response = {
                        'error': str(e),
                        'status': 'error',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    await websocket.send_json(error_response)
                
            except WebSocketDisconnect:
                logger.info("Client disconnected")
                break
                
            except Exception as e:
                logger.error(f"WebSocket error: {str(e)}")
                try:
                    error_response = {
                        'error': str(e),
                        'status': 'error',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    await websocket.send_json(error_response)
                except:
                    break
                    
            await asyncio.sleep(0.1)
            
    finally:
        manager.disconnect(websocket)
        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)