import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QSplitter
from PyQt5.QtCore import Qt
from .camera_widget import CameraWidget
from .analytics_widget import AnalyticsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI CCTV Monitoring System")
        self.setGeometry(100, 100, 1280, 720)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        # Left panel - Camera feeds
        self.camera_widget = CameraWidget()
        self.camera_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Right panel - Analytics
        self.analytics_widget = AnalyticsWidget()
        self.analytics_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add widgets to splitter for adjustable sizing
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.camera_widget)
        splitter.addWidget(self.analytics_widget)
        
        # Set initial sizes (e.g., 60% camera, 40% analytics)
        splitter.setSizes([int(self.width() * 0.6), int(self.width() * 0.4)])
        
        # Add splitter to layout
        layout.addWidget(splitter)
    
    def set_cctv_system(self, cctv_system):
        self.cctv_system = cctv_system
        
    def closeEvent(self, event):
        self.camera_widget.stop_camera()
        event.accept()