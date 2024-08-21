import os
import base64
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Union
from config import SIZE, SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key: str = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key is not set in environment variables.")
client: OpenAI = OpenAI(api_key=api_key)

def run_api(
    messages: List[Dict[str, Union[str, List[Dict[str, str]]]]]
) -> Union[str, None]:
    """
    Run the OpenAI API with the given messages.

    Args:
        messages (List[Dict[str, Union[str, List[Dict[str, str]]]]]): The
            messages to send to the API.

    Returns:
        Union[str, None]: The generated caption, or None if an error occurs.
    """
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            max_tokens=500,
        )
        caption: str = response.choices[0].message.content
        return caption
    except Exception as e:
        print(f"Error while communicating with OpenAI API: {e}")
        return None

def img2text(path: str, subject_name: str=None) -> Union[str, None]:
    """
    Convert an image at the given path to text using the OpenAI API.

    Args:
        path (str): The path to the image file.
        subject_name (str, optional): The name of the subject in the image.

    Returns:
        Union[str, None]: The generated caption for the image, or None if an error occurs.
    """
    try:
        image = Image.open(path)
    except FileNotFoundError:
        print(f"Error: File not found at path {path}")
        return None
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file at path {path}")
        return None

    # Convert RGBA images to RGB to ensure consistency
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Resize the image to the specified size
    try:
        image = image.resize(SIZE)
    except ValueError as e:
        print(f"Error resizing image: {e}")
        return None

    # Convert the image to a base64-encoded string
    buffered = BytesIO()
    try:
        image.save(buffered, format="JPEG")
    except OSError as e:
        print(f"Error saving image to buffer: {e}")
        return None
    
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Prepare the data dictionary
    img_dict: Dict[str, Dict[str, str]] = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{image_base64}",
        }
    }

    # Create the message list for the API request
    messages: List[Dict[str, Union[str, List[Dict[str, str]]]]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": [img_dict]},
    ]

    if subject_name:
        subject_prompt = f"Whenever the main subject appears, explicitly use the name '{subject_name}' rather than generic terms like 'man,' 'girl,' 'person,' or similar descriptors."
        messages.append({"role": "user", "content": subject_prompt})

    # Get and return the caption
    return run_api(messages)