import base64
from io import BytesIO
from datetime import datetime

import openai
import requests
from PIL import Image
from openai import OpenAI

description_example = 'A man resting in the grass on a sunny day, enjoying receiving caresses from some enthusiastic friends. The scene portrays a relaxed and joyful atmosphere, with the man lying comfortably in the grass, surrounded by friends who are affectionately interacting with him. The friends are shown in a manner that reflects their enthusiasm and camaraderie. The setting is a peaceful outdoor scene, capturing the essence of a sunny day. '

def make_image(description, folder_dst):
    client = OpenAI(api_key="COMPLETE THIS")

    prompt = (
        "Subject: Illustration in Art Nouveau style. " + description.strip() + " "
        'Style: The illustration is depicted in the elegant, flowing Alphonse Mucha style. The color palette is harmonious and muted, focusing on pastel shades to create a playful yet ethereal atmosphere, typical of the art nouveau aesthetic. This serene and affectionate moment is highlighted by the use of soft, flowing lines and organic forms.'
    )


    image_params = {
    "model": "dall-e-3",
    "n": 1,               # Between 2 and 10 is only for DALL-E 2
    "size": "1024x1024",  # 256x256, 512x512 only for DALL-E 2 - not much cheaper
    "prompt": prompt,     # DALL-E 3: max 4000 characters, DALL-E 2: max 1000
    "user": "org-aC6zsZhh9ij6XMLlwAv9ttlf",     # pass a customer ID to OpenAI for abuse monitoring
    }

    image_params.update({"response_format": "b64_json"})  # defaults to "url" for separate download

    ## -- DALL-E 3 exclusive parameters --
    #image_params.update({"size": "1792x1024"})  # 1792x1024 or 1024x1792 available for DALL-E 3
    #image_params.update({"quality": "hd"})      # quality at 2x the price, defaults to "standard" 
    #image_params.update({"style": "natural"})   # defaults to "vivid"

    try:
        images_response = client.images.generate(**image_params)
    except openai.APIConnectionError as e:
        print("Server connection error: {e.__cause__}")  # from httpx.
        raise
    except openai.RateLimitError as e:
        print(f"OpenAI RATE LIMIT error {e.status_code}: (e.response)")
        raise
    except openai.APIStatusError as e:
        print(f"OpenAI STATUS error {e.status_code}: (e.response)")
        raise
    except openai.BadRequestError as e:
        print(f"OpenAI BAD REQUEST error {e.status_code}: (e.response)")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

    # make a file name prefix from date-time of response
    images_dt = datetime.utcfromtimestamp(images_response.created)
    img_filename = images_dt.strftime('DALLE-%Y%m%d_%H%M%S')  # like 'DALLE-20231111_144356'

    # get the prompt used if rewritten by dall-e-3, null if unchanged by AI
    revised_prompt = images_response.data[0].revised_prompt

    # get out all the images in API return, whether url or base64
    # note the use of pydantic "model.data" style reference and its model_dump() method
    image_url_list = []
    image_data_list = []
    for image in images_response.data:
        image_url_list.append(image.model_dump()["url"])
        image_data_list.append(image.model_dump()["b64_json"])

    # Initialize an empty list to store the Image objects
    image_objects = []

    # Check whether lists contain urls that must be downloaded or b64_json images
    if image_url_list and all(image_url_list):
        # Download images from the urls
        for i, url in enumerate(image_url_list):
            while True:
                try:
                    print(f"getting URL: {url}")
                    response = requests.get(url)
                    response.raise_for_status()  # Raises stored HTTPError, if one occurred.
                except requests.HTTPError as e:
                    print(f"Failed to download image from {url}. Error: {e.response.status_code}")
                    retry = input("Retry? (y/n): ")  # ask script user if image url is bad
                    if retry.lower() in ["n", "no"]:  # could wait a bit if not ready
                        raise
                    else:
                        continue
                break
            image_objects.append(Image.open(BytesIO(response.content)))  # Append the Image object to the list
            image_objects[i].save(f"{img_filename}_{i}.png")
            print(f"{img_filename}_{i}.png was saved")
    elif image_data_list and all(image_data_list):  # if there is b64 data
        # Convert "b64_json" data to png file
        for i, data in enumerate(image_data_list):
            image_objects.append(Image.open(BytesIO(base64.b64decode(data))))  # Append the Image object to the list
            image_objects[i].save(folder_dst + f"/{img_filename}_{i}.png")
            print(f"{img_filename}_{i}.png was saved")
    else:
        print("No image data was obtained. Maybe bad code?")

import pandas as pd
import os
from glob import glob

def process_csv_and_generate_images(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        sentence = row['Original Sentence']
        description = row['Visual Description']
        if type(description) != str or len(description) == 0:
            continue
        print(sentence)
        
        folder_name = sentence.replace(' ', '_')
        folder_dst = f"./images/{folder_name}"

        if os.path.exists(folder_dst.replace('_', ' ')):
            folder_dst = folder_dst.replace('_', ' ')
        if not os.path.exists(folder_dst):
            continue
        # Create the folder if it doesn't already exist
        #os.makedirs(folder_dst, exist_ok=True)

        files = glob(folder_dst + "/*")

        if len(files) == 0:            
            try:
                # Execute the make_image function with the description and folder destination
                make_image(description, folder_dst)
            except Exception as e:
                print(e)

csv_path = "cards.csv"
process_csv_and_generate_images(csv_path)