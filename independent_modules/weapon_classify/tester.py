from keras.preprocessing.image import img_to_array
import os
import numpy as np
import tensorflow as tf
from PIL import Image
from keras.layers import Input

def load_and_preprocess_images(path, target_size=(50, 50)):
    images = []
    files = os.listdir(path)
    
    for filename in files:
        image_path = os.path.join(path, filename)
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img = img.resize(target_size)
        img_array = img_to_array(img)
        
        # Transpose the dimensions to match the model's expected input
        # From (height, width, channels) to (channels, height, width)
        img_array = np.transpose(img_array, (2, 0, 1))
        
        # Normalize
        img_array = img_array / 255.0
        images.append(img_array)
    
    # Stack arrays and add batch dimension
    return np.stack(images)

# Parameters
IMG_SIZE = (50, 50)
MODEL_PATH = "models/model_latest.h5"
TEST_PATH = 'test'

try:
    # Create input layer with explicit shape
    input_shape = (3, 50, 50)  # channels_first format
    inputs = Input(shape=input_shape)
    
    # Load and preprocess images
    x = load_and_preprocess_images(TEST_PATH, IMG_SIZE)
    print("Input shape:", x.shape)
    
    # Load model with custom configuration
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects=None,
        compile=True,
        options=tf.saved_model.LoadOptions(
            experimental_io_device='/job:localhost'
        )
    )
    
    # Print model architecture
    model.summary()
    
    # Make predictions
    predictions = model.predict(x)
    print("\nPredictions:", predictions)

except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()