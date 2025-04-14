"""
Image generator module for creating images from text prompts using Gemini.
"""
import os
import mimetypes
from google import genai
from google.genai import types

from src.utils.config import load_api_key, get_output_paths


def generate_image(prompt, image_name="generated_image"):
    """
    Generate an image from a text prompt using Gemini model.
    
    Args:
        prompt (str): The description of the image to generate
        image_name (str): Base name for the saved image file
    
    Returns:
        str: Path to the saved image file
    """
    # Get the API key
    api_key = load_api_key()
    
    # Initialize the client
    client = genai.Client(
        api_key=api_key,
    )

    model = "gemini-2.0-flash-exp-image-generation"
    
    enhanced_prompt = f"""
    Create a high-quality, inspiring image for a self-improvement and motivation context:
    
    {prompt}
    
    Make the image vibrant, clear, and emotionally resonant. Include relevant visual elements 
    that communicate the meaning effectively. The style should be professional and inspirational.
    """
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=enhanced_prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "image",
            "text",
        ],
        response_mime_type="text/plain",
    )

    saved_files = []
    
    # Get the output directory for images
    _, images_dir = get_output_paths()
    
    # Stream the response
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
            
        if chunk.candidates[0].content.parts[0].inline_data:
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            file_extension = mimetypes.guess_extension(inline_data.mime_type) or ".jpg"
            file_path = os.path.join(images_dir, f"{image_name}{file_extension}")
            
            save_binary_file(file_path, inline_data.data)
            saved_files.append(file_path)
            
            print(
                f"File of mime type {inline_data.mime_type} saved to: {file_path}"
            )
        else:
            if chunk.text:
                print(chunk.text)
    
    return saved_files


def save_binary_file(file_name, data):
    """
    Save binary data to a file.
    
    Args:
        file_name (str): Name of the file to save
        data (bytes): Binary data to save
    """
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"Saved file: {file_name}")
