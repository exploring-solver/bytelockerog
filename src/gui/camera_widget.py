# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtGui import QImage, QPixmap
# import cv2

# class CameraWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         # Camera feed label
#         self.camera_label = QLabel()
#         self.camera_label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.camera_label)

#         # Initialize camera
#         self.capture = cv2.VideoCapture(0)
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(30)  # Update every 30ms
        
#         self.person_detector = None

#     def set_components(self, video_stream, person_detector):
#         self.video_stream = video_stream
#         self.person_detector = person_detector
    
#     def update_frame(self):
#         ret, frame = self.capture.read()
#         if ret and self.person_detector:
#             # Get detections from person detector
#             detections = self.person_detector.detect(frame)
            
#             # Draw detection boxes and labels
#             for detection in detections:
#                 left, top, right, bottom = detection['bbox']
#                 name = detection['name']
#                 confidence = detection['confidence']
                
#                 cv2.rectangle(frame, 
#                             (int(left), int(top)), 
#                             (int(right), int(bottom)), 
#                             (0, 255, 0), 2)
#                 cv2.putText(frame, 
#                           f'{name} {confidence:.2f}', 
#                           (int(left), int(top-10)), 
#                           cv2.FONT_HERSHEY_SIMPLEX, 
#                           0.5, 
#                           (0, 255, 0), 
#                           2)

#             # Convert frame to QImage
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             h, w, ch = rgb_frame.shape
#             bytes_per_line = ch * w
#             qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
#             # Scale image to fit label while maintaining aspect ratio
#             scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
#                 self.camera_label.size(), 
#                 Qt.KeepAspectRatio, 
#                 Qt.SmoothTransformation
#             )
#             self.camera_label.setPixmap(scaled_pixmap)

#     def stop_camera(self):
#         self.timer.stop()
#         self.capture.release()

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.camera_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30ms
        
        self.cctv_system = None
        self.camera_id = None

    def set_cctv_system(self, cctv_system, camera_id='main_camera'):
        self.cctv_system = cctv_system
        self.camera_id = camera_id

    # Main optimizations in update_frame method
    def update_frame(self):
        if not self.cctv_system or not self.camera_id:
            return

        stream = self.cctv_system.video_streams.get(self.camera_id)
        if not stream or stream.frame_queue.empty():
            return

        frame = stream.frame_queue.get()
        if frame is None:
            return

        # Only perform detection every N frames (e.g., every 3rd frame)
        if hasattr(self, '_frame_count'):
            self._frame_count += 1
        else:
            self._frame_count = 0

        # Draw previous detections if not processing this frame
        if self._frame_count % 3 != 0:
            if hasattr(self, '_last_detections'):
                self._draw_detections(frame, self._last_detections)
        else:
            # Get detections and cache them
            detections = self.cctv_system.person_detector.detect(frame)
            self._last_detections = detections
            self._draw_detections(frame, detections)

        # Convert frame to QImage more efficiently
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)  # Note: BGR888 instead of converting

        scaled_pixmap = QPixmap.fromImage(qt_image).scaled(
            self.camera_label.size(), 
            Qt.KeepAspectRatio, 
            Qt.FastTransformation  # Use FastTransformation instead of SmoothTransformation
        )
        self.camera_label.setPixmap(scaled_pixmap)

    def _draw_detections(self, frame, detections):
        for detection in detections:
            left, top, right, bottom = detection['bbox']
            name = detection['name']
            confidence = detection['confidence']

            cv2.rectangle(frame, 
                        (int(left), int(top)), 
                        (int(right), int(bottom)), 
                        (0, 255, 0), 2)
            cv2.putText(frame, 
                    f'{name} {confidence:.2f}', 
                    (int(left), int(top-10)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    (0, 255, 0), 
                    2)
