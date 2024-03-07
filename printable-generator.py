import os
from glob import glob

from PIL import Image

# Function to resize and place images in a 3x3 grid on an A4 page
def create_a4_collage(folder_path):

    if not os.path.exists("printables"):
        os.makedirs("printables")

    # A4 dimensions in pixels at 300 PPI
    a4_width_px = int((210/25.4)*300)
    a4_height_px = int((297/25.4)*300)
    
    # Create a blank A4 image
    a4_image = Image.new('RGB', (a4_width_px, a4_height_px), 'white')
    
    # Image resize dimensions
    resize_width = 800
    resize_height = 1118
    
    # Read all image filenames in the specified folder
    image_files = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    
    
    for i in range(0,len(image_files),9):
        image_files_i = image_files[i:i+9]
    
        # Load, resize, and place each image on the A4 canvas
        for index, file_name in enumerate(image_files_i):
            image_path = os.path.join(folder_path, file_name)

            # Calculate position
            x_offset = (index % 3) * (a4_width_px // 3) + (a4_width_px // 3 - resize_width) // 2
            y_offset = (index // 3) * (a4_height_px // 3) + (a4_height_px // 3 - resize_height) // 2

            with Image.open(image_path) as img:
                # Resize image
                img = img.resize((resize_width, resize_height))                            
                # Paste image onto A4 canvas
                a4_image.paste(img, (x_offset, y_offset))

        # Save the final collage
        a4_image.save(f'printables/a4_collage_{i}.jpg')

    a4_image_back = Image.new('RGB', (a4_width_px, a4_height_px), 'white')

    # Load, resize, and place each image on the A4 canvas
    for index in range(9):
        with Image.open("backs/back1.png") as img_back:
            # Resize image
            img_back = img_back.resize((resize_width, resize_height))
            
            # Calculate position
            x_offset = (index % 3) * (a4_width_px // 3) + (a4_width_px // 3 - resize_width) // 2
            y_offset = (index // 3) * (a4_height_px // 3) + (a4_height_px // 3 - resize_height) // 2
            
            a4_image_back.paste(img_back, (x_offset, y_offset))
    # Save the final collage
    a4_image_back.save(f'printables/a4_backs.jpg')

    print("A4 collage created successfully!")

def images_to_pdf_with_backs(image_paths, back_image_path, output_pdf_path):
    """
    Converts a list of images to a PDF file, intercalating each image with a specific back image.
    
    Parameters:
    - image_paths: List of paths to the images to be included in the PDF.
    - back_image_path: Path to the back image to be added after each image in the list.
    - output_pdf_path: Path where the output PDF will be saved.
    """
    
    images = []
    for image_path in image_paths:
        img = Image.open(image_path)
        img = img.convert('RGB')  # Convert images to RGB to ensure compatibility
        images.append(img)
        
        # Add the back image after each original image
        back_img = Image.open(back_image_path)
        back_img = back_img.convert('RGB')
        images.append(back_img)

    # Save the images as a PDF
    if images:
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
    print("PDF Created!")

folder_path = 'deck'
create_a4_collage(folder_path)

image_paths = glob("printables/a4_collage*.jpg")
back_image_path = 'printables/back.jpg'  # Path to your back image
output_pdf_path = 'output.pdf'  # Desired output PDF path

images_to_pdf_with_backs(image_paths, back_image_path, output_pdf_path)
