"""
Image generator module for creating images from text prompts using Gemini.
"""
import os
import time
import mimetypes
import random
import logging
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

from src.utils.config import load_api_key, get_output_paths

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def generate_image(prompt, image_name="generated_image", max_retries=100, retry_delay=20):
    """
    Generate an image from a text prompt using Gemini model with retry mechanism.
    
    Args:
        prompt (str): The description of the image to generate
        image_name (str): Base name for the saved image file
        max_retries (int): Maximum number of retry attempts if generation fails
        retry_delay (int): Delay in seconds between retry attempts
    
    Returns:
        list: Paths to the saved image files
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
    
    # Retry loop
    attempt = 0
    success = False
    last_error = None
    
    while attempt < max_retries and not success:
        attempt += 1
        
        if attempt > 1:
            # This is a retry attempt
            retry_msg = f"Retry attempt {attempt}/{max_retries} after {retry_delay} seconds delay..."
            print(retry_msg)
            logging.info(retry_msg)
        
        try:
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
                    
                    success_msg = f"File of mime type {inline_data.mime_type} saved to: {file_path}"
                    print(success_msg)
                    logging.info(success_msg)
                    
                    # Mark as successful
                    success = True
                else:
                    if chunk.text:
                        print(chunk.text)
            
            # If we made it here with no saved files but no exception, mark as success to avoid retry
            if not saved_files and not success:
                logging.warning("No images were generated but no error occurred.")
                success = True
                
        except genai_errors.ServerError as e:
            # Handle server overload and other server errors
            error_msg = f"Server error on attempt {attempt}/{max_retries}: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            last_error = e
            
            # If we've reached max retries, re-raise the error
            if attempt >= max_retries:
                print(f"Failed after {max_retries} attempts. Last error: {str(e)}")
                raise
            
            # Add some jitter to the retry delay to avoid synchronized retries
            jitter = random.uniform(0.8, 1.2)  
            adjusted_delay = retry_delay * jitter
            time.sleep(adjusted_delay)
            
        except Exception as e:
            # Handle other unexpected errors
            error_msg = f"Unexpected error on attempt {attempt}/{max_retries}: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            last_error = e
            
            # If we've reached max retries, re-raise the error
            if attempt >= max_retries:
                print(f"Failed after {max_retries} attempts. Last error: {str(e)}")
                raise
            
            # Add some jitter to the retry delay
            jitter = random.uniform(0.8, 1.2)  
            adjusted_delay = retry_delay * jitter
            time.sleep(adjusted_delay)
    
    if not success:
        error_msg = f"Failed to generate image after {max_retries} attempts. Last error: {str(last_error)}"
        print(error_msg)
        logging.error(error_msg)
    elif attempt > 1:
        print(f"Successfully generated image after {attempt} attempts")
        logging.info(f"Successfully generated image after {attempt} attempts")
    
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
