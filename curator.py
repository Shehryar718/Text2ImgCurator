import os
import argparse
from utils import img2text
from config import IMAGE_FOLDER, CAPTION_FOLDER, VALID_EXTENSIONS

def process_images(image_folder, caption_folder, subject_name=None):
    # Get all image paths with valid extensions
    image_paths = [
        os.path.join(image_folder, image)
        for image in os.listdir(image_folder)
        if os.path.splitext(image)[-1].lower() in VALID_EXTENSIONS
    ]

    # Ensure the caption folder exists
    os.makedirs(caption_folder, exist_ok=True)

    # Process each image in the list
    for image_path in image_paths:
        # Generate caption from the image, passing subject_name if the function supports it
        caption = img2text(image_path, subject_name) if subject_name else img2text(image_path)
        
        # Handle the case where no caption is generated
        if not caption:
            caption = 'No caption found'
        
        # Prepare the caption file path
        file_name = os.path.basename(image_path)
        caption_file = os.path.splitext(file_name)[0] + '.txt'
        caption_path = os.path.join(caption_folder, caption_file)
        
        # Write the caption to a text file with error handling
        try:
            with open(caption_path, 'w') as f:
                f.write(caption)
        except IOError as e:
            print(f"Error writing caption for {file_name}: {e}")

if __name__ == '__main__':
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Process images to generate captions.')
    parser.add_argument('--image_folder', type=str, default=IMAGE_FOLDER, help='Path to the folder containing images.')
    parser.add_argument('--caption_folder', type=str, default=CAPTION_FOLDER, help='Path to the folder to save captions.')
    parser.add_argument('--subject_name', type=str, default=None, help='Name to use for the subject in the captions (optional).')

    # Parse arguments
    args = parser.parse_args()

    # Process images with provided arguments
    process_images(args.image_folder, args.caption_folder, args.subject_name)