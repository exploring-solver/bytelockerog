import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
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
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        self.camera_widget = CameraWidget()
        left_layout.addWidget(self.camera_widget)
        
        # Right panel - Analytics
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        self.analytics_widget = AnalyticsWidget()
        right_layout.addWidget(self.analytics_widget)

        # Add panels to main layout
        layout.addWidget(left_panel, stretch=2)
        layout.addWidget(right_panel, stretch=1)
    
    def set_cctv_system(self, cctv_system):
        self.cctv_system = cctv_system
        
    def closeEvent(self, event):
        self.camera_widget.stop_camera()
        event.accept()