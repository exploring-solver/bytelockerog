import cv2
import numpy as np
import face_recognition
import os

# Directory containing known face encodings
KNOWN_FACES_DIR = "./known_faces"

def load_known_faces():
    known_faces = {}
    for file in os.listdir(KNOWN_FACES_DIR):
        if file.endswith("_encoding.npy"):
            name = file.replace("_encoding.npy", "")
            encoding = np.load(os.path.join(KNOWN_FACES_DIR, file))
            known_faces[name] = encoding
    return known_faces

# Load known face encodings
known_faces = load_known_faces()

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect face locations
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = {name: face_recognition.compare_faces([encoding], face_encoding)[0] for name, encoding in known_faces.items()}
        
        name = "Unknown"
        for person, match in matches.items():
            if match:
                name = person
                break

        # Draw rectangle around face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Display frame
    cv2.imshow("Face Recognition", frame)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
