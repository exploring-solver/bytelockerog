import moondream as md
from PIL import Image

model = md.vl(model="C:\\Users\\amane\\moondream-2b-int8.mf")

# Load and process image
image = Image.open("bedroom.png")
encoded_image = model.encode_image(image)

# Generate caption
caption = model.caption(encoded_image)["caption"]
print("Caption:", caption)

# Ask questions
answer = model.query(encoded_image, "What's in this image?")["answer"]
print("Answer:", answer)