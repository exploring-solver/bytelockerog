import time
import queue
from ..utils.logging_setup import logger
import threading
import cv2
from ..utils.preprocessing import preprocess_frame
from config.config import SystemConfig
import datetime

class VideoStream:
    """Handles video stream capture and preprocessing"""
    def __init__(self, source: str, config: SystemConfig):
        self.source = source
        self.config = config
        self.capture = cv2.VideoCapture(source)
        
        # Check if camera opened successfully
        if not self.capture.isOpened():
            raise ValueError(f"Error opening video source {source}")
        print(f"Video source {source} opened successfully.")
            
        # Set camera properties
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        print("Camera properties set: width=640, height=480.")
        
        self.frame_queue = queue.Queue(maxsize=30)
        self._running = False
        
    def start(self):
        """Start video capture thread"""
        self._running = True
        print("Starting video capture thread.")
        threading.Thread(target=self._capture_frames, daemon=True).start()
        
    def _capture_frames(self):
        """Continuously capture frames from the video source"""
        frame_count = 0
        consecutive_failures = 0
        
        # Set camera buffer size
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        while self._running:
            try:
                ret, frame = self.capture.read()
                
                if not ret:
                    consecutive_failures += 1
                    if consecutive_failures > 10:
                        break
                    time.sleep(0.1)
                    continue
                    
                consecutive_failures = 0
                
                # Only process every Nth frame
                if frame_count % self.config.frame_skip == 0:
                    processed_frame = preprocess_frame(frame)
                    if processed_frame is not None and not self.frame_queue.full():
                        # Clear queue if full
                        while self.frame_queue.full():
                            self.frame_queue.get_nowait()
                        self.frame_queue.put(processed_frame)
                        
                frame_count += 1
                    
            except Exception as e:
                logger.error(f"Error in frame capture: {str(e)}")
                time.sleep(0.1)
                
    def stop(self):
        """Stop video capture"""
        self._running = False
        print("Stopping video capture.")
        if self.capture:
            self.capture.release()
            print("Video capture released.")
