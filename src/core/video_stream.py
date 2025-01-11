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
        
        while self._running:
            try:
                ret, frame = self.capture.read()
                
                if not ret:
                    consecutive_failures += 1
                    logger.warning(f"Failed to capture frame from {self.source}")
                    print(f"Failed to capture frame. Consecutive failures: {consecutive_failures}")
                    if consecutive_failures > 10:
                        logger.error("Too many consecutive capture failures")
                        print("Too many consecutive capture failures. Stopping capture.")
                        break
                    time.sleep(0.1)
                    continue
                    
                consecutive_failures = 0
                print(f"Captured frame {frame_count} from {self.source}.")
                
                if frame_count % self.config.frame_skip == 0:
                    # Preprocess frame
                    processed_frame = preprocess_frame(frame)
                    print(f"Processed frame {frame_count}.")
                    if processed_frame is not None:
                        if not self.frame_queue.full():
                            self.frame_queue.put(processed_frame)
                            print(f"Frame {frame_count} added to queue.")
                        else:
                            # Clear oldest frame if queue is full
                            try:
                                self.frame_queue.get_nowait()
                                print("Queue full. Oldest frame removed.")
                            except queue.Empty:
                                pass
                            self.frame_queue.put(processed_frame)
                            print(f"Frame {frame_count} added to queue.")
                            
                frame_count += 1
                
            except Exception as e:
                logger.error(f"Error in frame capture: {str(e)}")
                print(f"Error in frame capture: {str(e)}")
                time.sleep(0.1)
                
    def stop(self):
        """Stop video capture"""
        self._running = False
        print("Stopping video capture.")
        if self.capture:
            self.capture.release()
            print("Video capture released.")
