import os
import random
from glob import glob

from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont

def getsize(font, text):
    left, top, right, bottom = font.getbbox(text)
    return right - left, bottom - top

def wrap_text(text, font, max_width):
    """
    Wrap text to fit within a specified width.
    """
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and getsize(font,line + words[0])[0] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return lines


def create_tarot_card(image_path, card_name, output_path, description=None):
    # Load the frame and the image
    if description is None:
        frame_path = "frames/frame.png"
    else:
        frame_path = "frames/frame_description.png"

    frame = Image.open(frame_path).convert("RGBA")
    image = Image.open(image_path).convert("RGBA")
    
    # Calculate new size for the image
    new_width = int(frame.size[0] * 0.98)
    new_height = int(frame.size[1] * 0.97)
    image = image.resize((new_width, new_height))
    
    # Create a new image for the base (same size as the frame) with transparency
    base = Image.new("RGBA", frame.size, (255, 255, 255, 0))
    
    # Calculate the position to place the resized image (centered horizontally at the top)
    x_position = (frame.size[0] - new_width) // 2
    y_position = 15  # At the top
    
    # Paste the resized image onto the base image
    base.paste(image, (x_position, y_position), image)
    
    # Overlay the frame on top of the base image (with the image)
    combined = Image.alpha_composite(base, frame)
    
    # Add text
    draw = ImageDraw.Draw(combined)
    font_size = 100  # Adjust the size to fit your design
    font = ImageFont.truetype("fonts/Montserrat-Light.ttf", font_size)

    # Calculate text width and height to center it
    text_x = (combined.width - getsize(font, card_name)[0]) / 2
    if description is None:
        text_y = combined.height - 200
    else:
        text_y = combined.height - 610
    # Draw the text
    draw.text((text_x, text_y), card_name, fill="black", font=font)
    
    if description:
        # Add text
        font_size = 75  # Adjust the size to fit your design
        font = ImageFont.truetype("fonts/Montserrat-Light.ttf", font_size)
        
        max_width = combined.width - 200  # Adjust as needed

        # Starting position for the text
        text_y = combined.height - 390  # Adjust as needed
        line_height = getsize(font,'A')[1] + 10  # Calculate line height (adjust spacing as needed)
        
        lines = wrap_text(description, font, max_width)

        for line in lines:
            text_x = 100
            draw.text((text_x, text_y), line, fill="black", font=font)
            text_y += line_height
        
    combined.save(output_path)


if __name__ == "__main__":
    import pandas as pd

    title2description = {}

    for d in pd.read_csv("cards.csv").to_dict("records"):
        if type(d["Description"]) == str:
            name = d["Original Sentence"].replace("_"," ").title()
            title2description[name] = d["Description"]


    for folder in tqdm(glob("images/*")):
        try:
            name = folder.split("/")[-1].replace("_", " ").title()
            image = random.choice(glob(os.path.join(folder,"*")))

            create_tarot_card(image, name, f"deck/{name}.png", description=title2description.get(name))
        except Exception as e:
            print(e)