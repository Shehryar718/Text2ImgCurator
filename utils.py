import os
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Union
from config import SIZE, SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key: str = os.environ.get('OPENAI_API_KEY')
client: OpenAI = OpenAI(api_key=api_key)

def run_api(
    messages: List[Dict[str, Union[str, List[Dict[str, str]]]]]
) -> str:
    """
    Run the OpenAI API with the given messages.

    Args:
        messages (List[Dict[str, Union[str, List[Dict[str, str]]]]]): The
            messages to send to the API.

    Returns:
        str: The generated caption.
    """
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        max_tokens=500,
    )
    caption: str = response.choices[0].message.content
    return caption

def img2text(path: str) -> str:
    """
    Convert an image at the given path to text using the OpenAI API.

    Args:
        path (str): The path to the image file.

    Returns:
        str: The generated caption for the image.
    """
    image = Image.open(path)

    # Convert RGBA images to RGB to ensure consistency
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Resize the image to the specified size
    image = image.resize(SIZE)

    # Convert the image to a base64-encoded string
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
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
        {"role": "user", "content": [img_dict]}
    ]

    # Get and return the caption
    return run_api(messages)
