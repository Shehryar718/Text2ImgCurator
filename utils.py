import os
import base64
from PIL import Image
from io import BytesIO
from config import SIZE
from config import SYSTEM_PROMPT
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key: str = os.environ.get('OPENAI_API_KEY')
client: OpenAI = OpenAI(api_key=api_key)

def run_api(messages):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        max_tokens=500,
    )
    caption = response.choices[0].message.content
    return caption


def img2text(path: str):
    image = Image.open(path)

    # Convert RGBA images to RGB to ensure consistency
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    image = image.resize(SIZE)

    # Convert the image to a base64-encoded string
    buffered = BytesIO()
    image.save(buffered, format="JPEG")

    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Prepare the data dictionary
    img_dict = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{image_base64}",
        }
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": [img_dict]})

    return run_api(messages)