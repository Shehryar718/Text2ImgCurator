# Text2ImgCurator

**Text2ImgCurator** is a Python-based tool designed to streamline the process of generating high-quality captions for images, which can then be used to fine-tune text-to-image models. This project leverages the OpenAI API to produce precise, descriptive, and contextually relevant captions, ideal for curating datasets in machine learning projects.

## Features

- **Automated Caption Generation**: Uses OpenAI's API to produce high-quality captions.
- **Custom Subject Naming**: Optionally specify the name of the subject in the images.
- **Supports Multiple Image Formats**: Handles `.jpg`, `.png`, `.jpeg`, and `.JPG` file extensions.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Shehryar718/Text2ImgCurator.git
   cd Text2ImgCurator
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key by creating a `.env` file in the project root:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

To generate captions for images in a folder, use the following command:

```bash
python curator.py --image_folder path/to/images --caption_folder path/to/captions --subject_name "Optional Subject Name"
```

- `--image_folder`: Path to the folder containing images. Defaults to `"imgs"`.
- `--caption_folder`: Path to the folder where captions will be saved. Defaults to `"captions"`.
- `--subject_name`: (Optional) Specify a subject name to be used in the captions instead of generic terms.

### Example

```bash
python curator.py --image_folder imgs --caption_folder captions --subject_name "John Doe"
```

## Configuration

You can adjust various settings in the `config.py` file:

- **SIZE**: Image dimensions for processing (default is `(512, 512)`).
- **IMAGE_FOLDER**: Default folder for images.
- **CAPTION_FOLDER**: Default folder for captions.
- **VALID_EXTENSIONS**: List of valid image file extensions.

## File Structure

- **src/config.py**: Configuration settings.
- **src/utils.py**: Utility functions for processing images and interacting with the OpenAI API.
- **curator.py**: Main script for generating captions.
- **requirements.txt**: List of Python dependencies.
