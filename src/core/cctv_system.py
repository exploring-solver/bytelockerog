from config.config import SystemConfig
from datetime import datetime
import logging
from config.config import SystemConfig
import yaml
from .person_detector import PersonDetector
from .crowd_analyzer import CrowdAnalyzer
from .behavior_analyzer import BehaviorAnalyzer
from .work_monitor import WorkMonitor
from .alert_system import AlertSystem
from ..database.handlers import DatabaseHandler
from .video_stream import VideoStream

class CCTVSystem:
    """Main system class that coordinates all components"""
    def __init__(self, config_path: str):
        print(f"Loading configuration from {config_path}...")
        
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
            print("CCTV System initialized successfully.")
            
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {config_path}")
            raise
        except Exception as e:
            logging.error(f"Initialization error: {e}")
            raise
        
    def add_camera(self, camera_id: str, source: str):
        """Add new camera stream"""
        print(f"Adding camera '{camera_id}' with source '{source}'...")
        stream = VideoStream(source, self.config)
        self.video_streams[camera_id] = stream
        stream.start()
        print(f"Camera '{camera_id}' added and stream started.")
        
    def process_frame(self, camera_id: str):
        """Process single frame from camera"""
        stream = self.video_streams.get(camera_id)
        if not stream or stream.frame_queue.empty():
            return
            
        frame = stream.frame_queue.get()
        print(f"Processing frame from camera '{camera_id}'...")
        
        # Detect persons
        detections = self.person_detector.detect(frame)
        print(f"Detections: {len(detections)} persons detected.")
        
        # Analyze crowd
        crowd_analysis = self.crowd_analyzer.analyze_crowd(detections)
        print(f"Crowd Density: {crowd_analysis['density']:.2f}")
        if crowd_analysis['density'] > self.config.max_crowd_density:
            print("High crowd density detected. Generating alert.")
            self.alert_system.generate_alert('high_crowd_density', crowd_analysis)
            
        # Analyze behavior
        anomalies = self.behavior_analyzer.analyze_behavior(
            detections, self.config.restricted_areas)
        for anomaly in anomalies:
            print("Behavior anomaly detected. Generating alert.")
            self.alert_system.generate_alert('behavior_anomaly', anomaly)
            
        # Monitor workplace safety
        if self._is_working_hours():
            violations = self.work_monitor.monitor_safety(frame, detections)
            for violation in violations:
                print("Safety violation detected. Generating alert.")
                self.alert_system.generate_alert('safety_violation', violation)
                
        # Log events
        for detection in detections:
            self.db_handler.log_event('person_detected', detection, 
                                    detection['confidence'])
            print(f"Event logged for detection with confidence {detection['confidence']:.2f}.")
            
                                    
    def _is_working_hours(self) -> bool:
        """Check if current time is within working hours"""
        current_hour = datetime.now().hour
        return self.config.working_hours[0] <= current_hour <= self.config.working_hours[1]
        
    def run(self):
        """Main processing loop"""
        print("Running CCTV system...")
        while True:
            for camera_id in self.video_streams:
                self.process_frame(camera_id)