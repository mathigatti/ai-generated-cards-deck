from PIL import Image
import os
from tqdm import tqdm

def resize_images(source_path, destination_path, max_width=800):
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    for filename in tqdm(os.listdir(source_path)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for common image formats
            img_path = os.path.join(source_path, filename)
            img = Image.open(img_path)
            width_percent = (max_width / float(img.size[0]))
            height_size = int((float(img.size[1]) * float(width_percent)))
            img = img.resize((max_width, height_size))
            
            # Change the file extension to .jpg
            new_filename = os.path.splitext(filename)[0] + '.jpg'
            new_file_path = os.path.join(destination_path, new_filename)
            img = img.convert("RGB")  # Ensure compatibility with JPEG
            img.save(new_file_path, 'JPEG', optimize=True, quality=85)

source_path = 'deck'
destination_path = 'deck_light'
resize_images(source_path, destination_path)
