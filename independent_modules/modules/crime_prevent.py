import cv2
import numpy as np
import sqlite3
import datetime
import json
import face_recognition
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import queue
from PIL import Image
from PIL import ImageTk
class CrimePreventionSystem:
    def __init__(self, db_path='crime_prevention.db', known_faces_dir='known_faces'):
        """
        Initialize Crime Prevention Module with Enhanced Features
        
        Args:
            db_path (str): Path to SQLite database
            known_faces_dir (str): Directory to store known face encodings
        """
        self.db_path = db_path
        self.known_faces_dir = known_faces_dir
        
        # Ensure known faces directory exists
        os.makedirs(known_faces_dir, exist_ok=True)
        
        self._create_database()
        self.known_face_encodings = []
        self.known_face_names = []
        self._load_known_faces()
        
        # Camera and detection settings
        self.cameras = self._detect_available_cameras()
        self.active_cameras = []
        self.detection_queue = queue.Queue()
        
    def _detect_available_cameras(self):
        """
        Detect available cameras in the system
        
        Returns:
            list: List of available camera indices
        """
        available_cameras = []
        for i in range(5):  # Check up to 5 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras
    
    def _create_database(self):
        """Create database tables for crime prevention"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS suspicious_activities (
                    timestamp DATETIME,
                    location TEXT,
                    activity_type TEXT,
                    severity INTEGER,
                    details TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS known_identities (
                    name TEXT,
                    face_encoding_path TEXT,
                    last_seen DATETIME
                )
            ''')
            conn.commit()
    
    def _load_known_faces(self):
        """
        Load known face encodings from files
        """
        self.known_face_encodings.clear()
        self.known_face_names.clear()
        
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith('.npy'):
                encoding = np.load(os.path.join(self.known_faces_dir, filename))
                name = os.path.splitext(filename)[0].replace('_encoding', '')
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(name)
    
    def add_known_face(self, name: str, face_image: np.ndarray):
        """
        Add a new known face to the system
        
        Args:
            name (str): Name of the person
            face_image (numpy.ndarray): Face image to encode
        
        Returns:
            bool: Whether face was successfully added
        """
        # Detect face in the image
        face_locations = face_recognition.face_locations(face_image)
        
        if not face_locations:
            print(f"No face detected for {name}")
            return False
        
        # Compute face encoding
        face_encodings = face_recognition.face_encodings(face_image, face_locations)
        
        if not face_encodings:
            print(f"Could not compute face encoding for {name}")
            return False
        
        # Save face encoding
        encoding_filename = os.path.join(self.known_faces_dir, f"{name}_encoding.npy")
        np.save(encoding_filename, face_encodings[0])
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO known_identities 
                (name, face_encoding_path, last_seen) 
                VALUES (?, ?, ?)
            ''', (name, encoding_filename, datetime.datetime.now()))
            conn.commit()
        
        # Reload known faces to update the list
        self._load_known_faces()
        
        return True
    
    def detect_suspicious_behavior(self, frame, location: str):
        """
        Detect suspicious behaviors in the video frame with visual indicators
        
        Args:
            frame (numpy.ndarray): Input video frame
            location (str): Location of surveillance
        
        Returns:
            tuple: (suspicious behavior detection results, processed frame with annotations)
        """
        # Convert BGR to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        suspicious_results = {
            'timestamp': datetime.datetime.now(),
            'location': location,
            'suspicious_activities': [],
            'detected_faces': []
        }
        
        # Process each detected face
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare with known faces
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding, 
                tolerance=0.6
            )
            
            name = "Unknown"
            if any(matches):
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
            else:
                suspicious_results['suspicious_activities'].append({
                    'type': 'UNAUTHORIZED_ACCESS',
                    'severity': 4,
                    'details': 'Unknown face detected'
                })
            
            # Store detected face info
            suspicious_results['detected_faces'].append({
                'name': name,
                'location': (top, right, bottom, left)
            })
            
            # Draw rectangle and name
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw name with background
            label_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)[0]
            cv2.rectangle(frame, (left, top - 25), (left + label_size[0] + 10, top), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 5, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        # Loitering detection
        if len(face_locations) > 3:
            suspicious_results['suspicious_activities'].append({
                'type': 'LOITERING',
                'severity': 3,
                'details': f'Multiple faces detected: {len(face_locations)}'
            })
        
        # Store in database
        if suspicious_results['suspicious_activities']:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for activity in suspicious_results['suspicious_activities']:
                    cursor.execute('''
                        INSERT INTO suspicious_activities 
                        (timestamp, location, activity_type, severity, details) 
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        suspicious_results['timestamp'],
                        location,
                        activity['type'],
                        activity['severity'],
                        json.dumps(activity)
                    ))
                conn.commit()
        
        return suspicious_results, frame

    def detect_unattended_objects(self, frame, location: str):
        """
        Enhanced Unattended Object Detection with visualization
        
        Args:
            frame (numpy.ndarray): Input video frame
            location (str): Location of surveillance
        
        Returns:
            tuple: (unattended object results, frame with annotations)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Background subtractor
        if not hasattr(self, 'background_subtractor'):
            self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
                detectShadows=True
            )
        
        # Apply background subtraction
        foreground_mask = self.background_subtractor.apply(gray)
        
        # Threshold to remove shadows
        _, binary_mask = cv2.threshold(foreground_mask, 244, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter objects
        unattended_objects = [
            contour for contour in contours 
            if cv2.contourArea(contour) > 500
        ]
        
        # Draw rectangles around unattended objects
        for contour in unattended_objects:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        unattended_result = {
            'timestamp': datetime.datetime.now(),
            'location': location,
            'unattended_objects': len(unattended_objects)
        }
        
        # Store in database
        if unattended_objects:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO suspicious_activities 
                    (timestamp, location, activity_type, severity, details) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    unattended_result['timestamp'],
                    location,
                    'UNATTENDED_OBJECT',
                    4,
                    json.dumps({
                        'object_count': len(unattended_objects),
                        'object_sizes': [cv2.contourArea(obj) for obj in unattended_objects]
                    })
                ))
                conn.commit()
        
        return unattended_result, frame

class CrimePreventionUI:
    def __init__(self, master):
        """
        Create Tkinter UI for Crime Prevention System
        
        Args:
            master (tk.Tk): Tkinter root window
        """
        self.master = master
        self.master.title("Crime Prevention Surveillance System")
        self.master.geometry("1200x800")
        
        # Create Crime Prevention System
        self.crime_system = CrimePreventionSystem()
        
        # Create main frames
        self.create_frames()
        
        # Camera handling
        self.camera_threads = {}
        self.camera_frames = {}
        
        # Setup camera selection
        self.setup_camera_selection()
    
    def create_frames(self):
        """Create UI frames for different sections"""
        # Left frame for camera selection and known faces
        self.left_frame = tk.Frame(self.master, width=300, bd=1, relief=tk.RAISED)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Right frame for camera feeds
        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        # Known Faces section
        self.known_faces_label = tk.Label(
            self.left_frame, 
            text="Known Faces", 
            font=("Arial", 12, "bold")
        )
        self.known_faces_label.pack(pady=10)
        
        # Listbox to show known faces
        self.known_faces_listbox = tk.Listbox(
            self.left_frame, 
            width=30, 
            height=10
        )
        self.known_faces_listbox.pack(pady=10)
        
        # Refresh known faces list
        self.refresh_known_faces()
        
        # Add Face Button
        self.add_face_button = tk.Button(
            self.left_frame, 
            text="Add New Face", 
            command=self.add_new_face
        )
        self.add_face_button.pack(pady=10)
    
    def setup_camera_selection(self):
        """Setup camera selection UI"""
        # Camera Selection Label
        camera_label = tk.Label(
            self.left_frame, 
            text="Available Cameras", 
            font=("Arial", 12, "bold")
        )
        camera_label.pack(pady=10)
        
        # Camera Selection Checkboxes
        self.camera_vars = {}
        for camera_index in self.crime_system.cameras:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(
                self.left_frame, 
                text=f"Camera {camera_index}", 
                variable=var,
                command=lambda idx=camera_index, v=var: self.toggle_camera(idx, v)
            )
            cb.pack(anchor=tk.W)
            self.camera_vars[camera_index] = var
    
    def refresh_known_faces(self):
        """Refresh the known faces listbox"""
        self.known_faces_listbox.delete(0, tk.END)
        for name in self.crime_system.known_face_names:
            self.known_faces_listbox.insert(tk.END, name)
    
    def add_new_face(self):
        """Add a new known face to the system"""
        # Open file dialog to select image
        filename = filedialog.askopenfilename(
            title="Select Face Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png"),
                ("All files", "*.*")
            ]
        )
        
        if not filename:
            return
        
        # Read image
        face_image = cv2.imread(filename)
        
        # Prompt for name
        name = tk.simpledialog.askstring(
            "Add Face", 
            "Enter name for this face:"
        )
        
        if name:
            # Add face
            success = self.crime_system.add_known_face(name, face_image)
            
            if success:
                messagebox.showinfo(
                    "Success", 
                    f"Face for {name} added successfully!"
                )
                self.refresh_known_faces()
            else:
                messagebox.showerror(
                    "Error", 
                    "Could not add face. Ensure a clear face is visible."
                )
    
    def toggle_camera(self, camera_index, var):
        """Start or stop camera feed"""
        if var.get():
            # Start camera
            thread = threading.Thread(
                target=self.start_camera_feed, 
                args=(camera_index,)
            )
            thread.daemon = True
            thread.start()
            self.camera_threads[camera_index] = thread
        else:
            # Stop camera
            if camera_index in self.camera_frames:
                del self.camera_frames[camera_index]
    
    def start_camera_feed(self, camera_index):
        """
        Capture and process camera feed with proper frame conversion
        
        Args:
            camera_index (int): Index of camera to capture
        """
        cap = cv2.VideoCapture(camera_index)
        
        # Set reasonable frame size
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Create label for camera feed
        frame_label = tk.Label(self.right_frame)
        frame_label.pack(side=tk.TOP, padx=5, pady=5)
        self.camera_frames[camera_index] = frame_label
        
        while camera_index in self.camera_frames:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            try:
                # Process frame with detections
                display_frame = frame.copy()
                
                # Detect suspicious behavior and draw face rectangles
                suspicious_result, frame_with_faces = self.crime_system.detect_suspicious_behavior(
                    display_frame,
                    f"Camera {camera_index}"
                )
                
                # Detect unattended objects and draw object rectangles
                unattended_result, final_frame = self.crime_system.detect_unattended_objects(
                    frame_with_faces,
                    f"Camera {camera_index}"
                )
                
                # Draw additional detection results
                self.draw_detection_results(final_frame, suspicious_result, unattended_result)
                
                # Convert to RGB for tkinter
                rgb_frame = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)
                
                # Convert to ImageTk format
                image = Image.fromarray(rgb_frame)
                photo = ImageTk.PhotoImage(image=image)
                
                # Update label
                frame_label.configure(image=photo)
                frame_label.image = photo  # Keep a reference!
                
            except Exception as e:
                print(f"Detection error: {e}")
            
            # Update the window
            self.master.update_idletasks()
            self.master.update()
        
        # Cleanup
        cap.release()

    
    def draw_detection_results(self, frame, suspicious_result, unattended_result):
        """
        Draw enhanced detection results on frame
        
        Args:
            frame (numpy.ndarray): Video frame
            suspicious_result (dict): Suspicious behavior detection results
            unattended_result (dict): Unattended object detection results
        """
        # Draw suspicious activities alert
        if suspicious_result['suspicious_activities']:
            alert_text = "SUSPICIOUS ACTIVITY DETECTED"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            color = (0, 0, 255)
            
            # Get text size for background rectangle
            (text_width, text_height), baseline = cv2.getTextSize(
                alert_text, font, font_scale, thickness
            )
            
            # Draw background rectangle
            cv2.rectangle(
                frame,
                (10, 10),
                (10 + text_width, 40),
                color,
                cv2.FILLED
            )
            
            # Draw alert text
            cv2.putText(
                frame,
                alert_text,
                (10, 30),
                font,
                font_scale,
                (255, 255, 255),
                thickness
            )
        
        # Draw unattended object count
        if unattended_result['unattended_objects'] > 0:
            object_text = f"Unattended Objects: {unattended_result['unattended_objects']}"
            cv2.putText(
                frame,
                object_text,
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )
    

def main():
    """
    Main function to launch the Crime Prevention System UI
    """
    root = tk.Tk()
    
    try:
        import tkinter.simpledialog
        import tkinter.messagebox
    except ImportError:
        print("Critical: Required Tkinter modules not found!")
        return
    
    app = CrimePreventionUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()