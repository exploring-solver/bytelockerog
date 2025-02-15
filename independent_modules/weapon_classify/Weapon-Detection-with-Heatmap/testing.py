from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import os
import numpy as np

def load_and_preprocess_images(path, target_size=(64, 64)):
    """Load and preprocess images to match the model's requirements"""
    images = []
    files = os.listdir(path)
    
    for filename in files:
        # Construct full path
        image_path = os.path.join(path, filename)
        
        # Load and preprocess image
        img = load_img(image_path, target_size=target_size)
        img_array = img_to_array(img)
        img_array = img_array / 255.0  # Rescale to match training
        images.append(img_array)
    
    return np.array(images)

def predict_images():
    # Parameters matching the original training configuration
    IMG_SIZE = (64, 64)  # Original model was trained on 64x64 images
    MODEL_PATH = "classifier1.h5"  # Use the saved model from training
    TEST_PATH = 'test'  # Your test directory

    try:
        # Load and preprocess test images
        x = load_and_preprocess_images(TEST_PATH, IMG_SIZE)
        print("Input shape:", x.shape)
        
        # Load the model
        model = load_model(MODEL_PATH)
        
        # Print model summary
        model.summary()
        
        # Make predictions
        predictions = model.predict(x)
        
        # Process predictions
        for i, pred in enumerate(predictions):
            # For binary classification
            probability = pred[0] if pred.shape else pred
            class_prediction = 1 if probability > 0.5 else 0
            print(f"Image {i+1}: Probability = {probability:.4f}, Class = {class_prediction}")
            
        return predictions

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    predictions = predict_images()