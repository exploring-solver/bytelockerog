# main.py
import sys
import yaml
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.core.video_stream import VideoStream
from src.core.person_detector import PersonDetector
from src.core.crowd_analyzer import CrowdAnalyzer
from src.core.alert_system import AlertSystem
from src.core.cctv_system import CCTVSystem

def load_config():
    try:
        with open('config/config.yml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {
            'min_confidence': 0.4,
            'frame_skip': 3,
            'max_crowd_density': 0.75,
            'restricted_areas': [],
            'working_hours': [9, 17],
            'enable_pose_detection': False,
            'db_config': {
                'host': 'localhost',
                'port': 3306,
                'database': 'bytelocker',
                'user': 'root',
                'password': ''
            }
        }

def initialize_system(config):
    # Initialize CCTV system first
    cctv_system = CCTVSystem('config/config.yml')
    
    # Initialize core components
    video_stream = VideoStream(source=0, config=config)
    person_detector = cctv_system.person_detector
    crowd_analyzer = cctv_system.crowd_analyzer
    alert_system = cctv_system.alert_system
    
    # Add default camera to CCTV system
    cctv_system.add_camera('main_camera', 0)  # 0 for webcam
    
    return {
        'cctv_system': cctv_system,
        'video_stream': video_stream,
        'person_detector': person_detector,
        'crowd_analyzer': crowd_analyzer,
        'alert_system': alert_system
    }

def main():
    # Initialize application
    app = QApplication(sys.argv)
    
    # Load configuration
    config = load_config()
    
    # Initialize system components
    system_components = initialize_system(config)
    
    # Create main window with system components
    window = MainWindow()
    
    # Set up camera widget
    # window.camera_widget.set_components(
    #     video_stream=system_components['video_stream'],
    #     person_detector=system_components['person_detector']
    # )
    
    # Start video stream and CCTV system
    # system_components['video_stream'].start()
    # Set up analytics widget
    # window.analytics_widget.set_components(
    #     person_detector=system_components['person_detector'],
    #     crowd_analyzer=system_components['crowd_analyzer'],
    #     alert_system=system_components['alert_system']
    # )
    cctv_system = system_components['cctv_system']
    # window.analytics_widget.set_cctv_system(system_components['cctv_system'])
    window.camera_widget.set_cctv_system(cctv_system, 'main_camera')
    window.analytics_widget.set_cctv_system(cctv_system, 'main_camera')

    # # Print statements to display data being fetched frame by frame
    # def process_frames():
    #     while True:
    #         frame = system_components['video_stream'].get_frame()
    #         if frame is not None:
    #             print("New frame fetched.")
    #             detections = system_components['person_detector'].detect(frame)
    #             print(f"Detections: {detections}")
    #             crowd_data = system_components['crowd_analyzer'].analyze_crowd(detections)
    #             print(f"Crowd Analysis: {crowd_data}")
    #             alerts = system_components['alert_system'].check_alerts(crowd_data)
    #             print(f"Alerts: {alerts}")
    
    # Start processing frames in a separate thread or in the main loop
    # Here it's shown in a separate function for clarity
    # process_frames()
    
    # Show window
    window.show()
    
    # Start application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore', category=FutureWarning, message=r".*torch.cuda.amp.autocast.*")
    main()
