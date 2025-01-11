from .logging_setup import logger
import numpy as np
import cv2

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
        print("Error: Received None frame")
        return None
        
    try:
        # Convert to numpy array if needed
        if not isinstance(frame, np.ndarray):
            logger.error(f"Invalid frame type: {type(frame)}")
            print(f"Error: Invalid frame type: {type(frame)}")
            return None
            
        # Make a copy to avoid modifying original
        frame = frame.copy()
        print("Frame copied for preprocessing.")
        
        # Check frame dimensions
        if len(frame.shape) < 2:
            logger.error(f"Invalid frame shape: {frame.shape}")
            print(f"Error: Invalid frame shape: {frame.shape}")
            return None
            
        # Handle different color spaces
        if len(frame.shape) == 2:  # Grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            print("Converted grayscale frame to RGB.")
        elif len(frame.shape) == 3:
            if frame.shape[2] == 4:  # RGBA
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                print("Converted RGBA frame to RGB.")
            elif frame.shape[2] == 3:  # BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                print("Converted BGR frame to RGB.")
                
        # Ensure uint8 dtype
        if frame.dtype != np.uint8:
            if frame.max() <= 1.0:
                frame = (frame * 255).astype(np.uint8)
                print("Normalized frame values to uint8.")
            else:
                frame = frame.astype(np.uint8)
                print("Converted frame dtype to uint8.")
        
        # Verify final frame properties
        if not (frame.dtype == np.uint8 and len(frame.shape) == 3 and frame.shape[2] == 3):
            logger.error(f"Invalid processed frame: dtype={frame.dtype}, shape={frame.shape}")
            print(f"Error: Invalid processed frame: dtype={frame.dtype}, shape={frame.shape}")
            return None
        
        print(f"Frame preprocessed successfully: dtype={frame.dtype}, shape={frame.shape}")
        return frame
        
    except Exception as e:
        logger.error(f"Frame preprocessing error: {str(e)}")
        print(f"Error: Frame preprocessing error: {str(e)}")
        return None
