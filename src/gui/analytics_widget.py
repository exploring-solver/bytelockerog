# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
# from PyQt5.QtCore import Qt, QTimer
# import pyqtgraph as pg
# from datetime import datetime
# from ..utils.logging_setup import logger
# class AnalyticsWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         # People count section
#         self.people_count_label = QLabel("People Count: 0")
#         self.people_count_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
#         self.layout.addWidget(self.people_count_label)

#         # Crowd density graph
#         self.graph_widget = pg.PlotWidget()
#         self.graph_widget.setBackground('w')
#         self.graph_widget.setTitle("Crowd Density Over Time")
#         self.graph_widget.setLabel('left', 'Density')
#         self.graph_widget.setLabel('bottom', 'Time (s)')
#         self.graph_widget.showGrid(x=True, y=True)
#         self.layout.addWidget(self.graph_widget)

#         # Alert section
#         self.alert_label = QLabel("Recent Alerts:")
#         self.alert_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
#         self.alert_label.setWordWrap(True)
#         self.layout.addWidget(self.alert_label)
        
#         # Initialize data
#         self.time_data = []
#         self.density_data = []
#         self.curve = self.graph_widget.plot(pen='b')
        
#         # Update timer
#         self.update_timer = QTimer()
#         self.update_timer.timeout.connect(self.fetch_and_update)
#         self.update_timer.start(1000)  # Update every second

#     def set_components(self, crowd_analyzer, alert_system, person_detector):
#         self.crowd_analyzer = crowd_analyzer
#         self.alert_system = alert_system
#         self.person_detector = person_detector

#     def set_cctv_system(self, cctv_system):
#         self.cctv_system = cctv_system
        
#     def fetch_and_update(self):
#         if not hasattr(self, 'crowd_analyzer') or not hasattr(self, 'alert_system'):
#             return

#         try:
#             # Get crowd analysis data
#             crowd_data = self.crowd_analyzer.get_current_analysis()
#             if crowd_data:
#                 people_count = crowd_data.get('count', 0)
#                 density = crowd_data.get('density', 0.0)
#                 hotspots = crowd_data.get('hotspots', [])
#             else:
#                 people_count = 0
#                 density = 0.0
#                 hotspots = []

#             # Get recent alerts
#             alerts = self.alert_system.get_alerts()
            
#             # Update the display
#             self.update_analytics(people_count, density, hotspots, alerts)

#         except Exception as e:
#             print(f"Error updating analytics: {str(e)}")
#             logger.error(f"Analytics update error: {str(e)}")

#     def update_analytics(self, people_count, density, hotspots, alerts):
#         # Update people count
#         self.people_count_label.setText(f"People Count: {people_count}")
        
#         # Update density graph
#         current_time = len(self.time_data)
#         self.time_data.append(current_time)
#         self.density_data.append(density)
        
#         # Keep last 50 points
#         if len(self.time_data) > 50:
#             self.time_data = self.time_data[-50:]
#             self.density_data = self.density_data[-50:]
            
#         self.curve.setData(self.time_data, self.density_data)

#         # Update alerts
#         alert_text = "Recent Alerts:\n\n"
#         for alert in alerts[-5:]:  # Show last 5 alerts
#             timestamp = alert.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#             alert_type = alert.get('type', 'Unknown')
#             details = alert.get('details', {})
            
#             alert_text += f"[{timestamp}] {alert_type}\n"
#             for key, value in details.items():
#                 alert_text += f"  - {key}: {value}\n"
#             alert_text += "\n"
            
#         self.alert_label.setText(alert_text)

#     def closeEvent(self, event):
#         self.update_timer.stop()
#         super().closeEvent(event)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
from datetime import datetime

class AnalyticsWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Use QVBoxLayout for vertical stacking
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Set size policy for widget to be expandable
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Initialize data for graphs
        self.time_data = []
        self.density_data = []
        self.violation_data = []
        
        # Create analytics displays
        self.setup_crowd_section()
        self.setup_density_graph()
        self.setup_behavior_section()
        self.setup_safety_section()
        self.setup_alerts_section()
        
        # Initialize timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_analytics)
        self.timer.start(1000)  # Update every second
        
        self.cctv_system = None
        self.camera_id = None

    def set_cctv_system(self, cctv_system, camera_id='main_camera'):
        self.cctv_system = cctv_system
        self.camera_id = camera_id

    def setup_crowd_section(self):
        # Crowd analysis section
        self.crowd_label = QLabel("Crowd Analysis")
        self.crowd_label.setStyleSheet("font-size: 12pt; font-weight: bold; padding: 5px;")
        self.layout.addWidget(self.crowd_label)
        
        self.crowd_table = QTableWidget()
        self.crowd_table.setMinimumHeight(100)
        self.crowd_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.crowd_table.setColumnCount(2)
        self.crowd_table.setHorizontalHeaderLabels(['Metric', 'Value'])
        self.crowd_table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.crowd_table)

    def setup_density_graph(self):
        # Crowd density graph
        self.density_graph = pg.PlotWidget()
        self.density_graph.setBackground('w')
        self.density_graph.setTitle("Crowd Density Over Time")
        self.density_graph.setLabel('left', 'Density')
        self.density_graph.setLabel('bottom', 'Time (s)')
        self.density_graph.showGrid(x=True, y=True)
        self.density_graph.setMinimumHeight(200)
        self.density_graph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.density_curve = self.density_graph.plot(pen='b')
        self.layout.addWidget(self.density_graph)

    def setup_behavior_section(self):
        # Behavior analysis section
        self.behavior_label = QLabel("Behavior Analysis")
        self.behavior_label.setStyleSheet("font-size: 12pt; font-weight: bold; padding: 5px;")
        self.layout.addWidget(self.behavior_label)
        
        self.behavior_table = QTableWidget()
        self.behavior_table.setMinimumHeight(100)
        self.behavior_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.behavior_table.setColumnCount(2)
        self.behavior_table.setHorizontalHeaderLabels(['Anomaly Type', 'Count'])
        self.behavior_table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.behavior_table)

    def setup_safety_section(self):
        # Safety monitoring section
        self.safety_label = QLabel("Safety Monitoring")
        self.safety_label.setStyleSheet("font-size: 12pt; font-weight: bold; padding: 5px;")
        self.layout.addWidget(self.safety_label)
        
        self.safety_table = QTableWidget()
        self.safety_table.setMinimumHeight(100)
        self.safety_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.safety_table.setColumnCount(2)
        self.safety_table.setHorizontalHeaderLabels(['Violation Type', 'Count'])
        self.safety_table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.safety_table)

    def setup_alerts_section(self):
        # Recent alerts section
        self.alerts_label = QLabel("Recent Alerts")
        self.alerts_label.setStyleSheet("font-size: 12pt; font-weight: bold; padding: 5px;")
        self.layout.addWidget(self.alerts_label)
        
        self.alerts_table = QTableWidget()
        self.alerts_table.setMinimumHeight(150)
        self.alerts_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.alerts_table.setColumnCount(3)
        self.alerts_table.setHorizontalHeaderLabels(['Time', 'Type', 'Details'])
        self.alerts_table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.alerts_table)

    def resizeEvent(self, event):
        """Handle resize events to adjust table column widths"""
        super().resizeEvent(event)
        
        # Adjust table column widths
        for table in [self.crowd_table, self.behavior_table, self.safety_table]:
            width = table.width()
            table.setColumnWidth(0, int(width * 0.4))
            table.setColumnWidth(1, int(width * 0.6))
        
        # Adjust alerts table columns
        width = self.alerts_table.width()
        self.alerts_table.setColumnWidth(0, int(width * 0.2))  # Time
        self.alerts_table.setColumnWidth(1, int(width * 0.3))  # Type
        self.alerts_table.setColumnWidth(2, int(width * 0.5))  # Details
        
        

    def update_analytics(self):
        try:
            if not self.cctv_system or not self.camera_id:
                return
                
            stream = self.cctv_system.video_streams.get(self.camera_id)
            if not stream or stream.frame_queue.empty():
                return

            frame = stream.frame_queue.get()
            if frame is None:
                return

            # Get detections and various analytics
            detections = self.cctv_system.person_detector.detect(frame)
            crowd_analysis = self.cctv_system.crowd_analyzer.analyze_crowd(detections)
            behavior_anomalies = self.cctv_system.behavior_analyzer.analyze_behavior(
                detections, self.cctv_system.config.restricted_areas
            )
            safety_violations = self.cctv_system.work_monitor.monitor_safety(frame, detections)
            
            # Update crowd analysis
            self.update_crowd_analysis(crowd_analysis)
            
            # Update behavior analysis
            self.update_behavior_analysis(behavior_anomalies)
            
            # Update safety monitoring
            self.update_safety_monitoring(safety_violations)
            
            # Update density graph
            self.update_density_graph(crowd_analysis['density'])
            
            # Update alerts
            recent_alerts = self.cctv_system.db_handler.get_recent_alerts(limit=5)
            self.update_alerts(recent_alerts)
                
        except Exception as e:
            print(f"Error updating analytics: {e}")

    def update_crowd_analysis(self, crowd_data):
        self.crowd_table.setRowCount(len(crowd_data))
        for i, (metric, value) in enumerate(crowd_data.items()):
            self.crowd_table.setItem(i, 0, QTableWidgetItem(str(metric)))
            self.crowd_table.setItem(i, 1, QTableWidgetItem(self.format_value(value)))

    def update_behavior_analysis(self, anomalies):
        anomaly_counts = {}
        for anomaly in anomalies:
            anomaly_type = anomaly['type']
            anomaly_counts[anomaly_type] = anomaly_counts.get(anomaly_type, 0) + 1
        
        self.behavior_table.setRowCount(len(anomaly_counts))
        for i, (anomaly_type, count) in enumerate(anomaly_counts.items()):
            self.behavior_table.setItem(i, 0, QTableWidgetItem(str(anomaly_type)))
            self.behavior_table.setItem(i, 1, QTableWidgetItem(str(count)))

    def update_safety_monitoring(self, violations):
        violation_counts = {}
        for violation in violations:
            violation_type = violation['type']
            violation_counts[violation_type] = violation_counts.get(violation_type, 0) + 1
        
        self.safety_table.setRowCount(len(violation_counts))
        for i, (violation_type, count) in enumerate(violation_counts.items()):
            self.safety_table.setItem(i, 0, QTableWidgetItem(str(violation_type)))
            self.safety_table.setItem(i, 1, QTableWidgetItem(str(count)))

    def update_density_graph(self, density):
        current_time = len(self.time_data)
        self.time_data.append(current_time)
        self.density_data.append(density)
        
        # Keep last 50 points
        if len(self.time_data) > 50:
            self.time_data = self.time_data[-50:]
            self.density_data = self.density_data[-50:]
            
        self.density_curve.setData(self.time_data, self.density_data)

    def update_alerts(self, alerts):
        self.alerts_table.setRowCount(len(alerts))
        for i, alert in enumerate(alerts):
            self.alerts_table.setItem(i, 0, QTableWidgetItem(self.format_value(alert['timestamp'])))
            self.alerts_table.setItem(i, 1, QTableWidgetItem(alert['type']))
            self.alerts_table.setItem(i, 2, QTableWidgetItem(str(alert['details'])))

    def format_value(self, value):
        """Format different types of values for display"""
        try:
            if isinstance(value, (float, int)):
                return f"{value:.2f}"
            elif isinstance(value, list):
                if not value:
                    return "None"
                return ", ".join(map(str, value))
            elif isinstance(value, datetime):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return str(value)
        except Exception as e:
            print(f"Error formatting value {value}: {e}")
            return str(value)