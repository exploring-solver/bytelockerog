import face_recognition
import pickle
import os
from typing import List
import numpy as np
from pathlib import Path

def generate_face_encodings(name: str, images_dir: str) -> List[np.ndarray]:
    """
    Generate face encodings for multiple images of a person
    
    Args:
        name: Person's name
        images_dir: Directory containing the person's face images
    """
    encodings = []
    
    # Create face_data directory if it doesn't exist
    Path('face_data').mkdir(exist_ok=True)
    
    # Process each image in the directory
    for image_file in os.listdir(images_dir):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(images_dir, image_file)
            
            # Load and encode face
            try:
                image = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(image)
                
                if face_locations:
                    # Get encodings for all faces found
                    face_encodings = face_recognition.face_encodings(image, face_locations)
                    
                    # Assume the first face is the target person
                    if face_encodings:
                        encodings.append(face_encodings[0])
                        print(f"Successfully encoded face from {image_file}")
                else:
                    print(f"No face found in {image_file}")
                    
            except Exception as e:
                print(f"Error processing {image_file}: {e}")
    
    if encodings:
        # Save encodings to pickle file
        output_file = f'face_data/{name}_encodings.pkl'
        with open(output_file, 'wb') as f:
            pickle.dump(encodings, f)
        print(f"\nSaved {len(encodings)} encodings to {output_file}")
    else:
        print(f"\nNo valid face encodings found for {name}")
    
    return encodings

if __name__ == "__main__":
    person_name = "aman"
    # person_name = "ansh"
    images_folder = "face_images/aman"
    generate_face_encodings(person_name, images_folder)