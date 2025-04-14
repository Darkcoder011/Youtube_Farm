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
    Create a high-quality, inspiring image for a self-improvement and motivation context with YOUTUBE VIDEO DIMENSIONS (16:9 aspect ratio, 1920x1080 pixels):
    
    {prompt}
    
    Make the image vibrant, clear, and emotionally resonant. Include relevant visual elements 
    that communicate the meaning effectively. The style should be professional and inspirational.
    
    IMPORTANT: The image MUST be in landscape YouTube format (16:9 aspect ratio), suitable for YouTube thumbnails
    and video content. Ensure the image has high resolution (1920x1080) with the main subject positioned
    properly for a YouTube video. Leave space on the right side for potential text overlay.
    """
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=enhanced_prompt),
            ],
        ),
    ]
    
    # Configure for YouTube-sized image generation
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "image",
            "text",
        ],
        response_mime_type="text/plain",
        # Adding generation parameters for better quality
        temperature=0.4,  # Lower temperature for more consistent results
        top_k=32,
        top_p=0.95,
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
                    # Name the file with a YouTube-specific format
                    file_path = os.path.join(images_dir, f"{image_name}_youtube{file_extension}")
                    
                    # Save and potentially post-process the image
                    processed_path = save_binary_file(file_path, inline_data.data)
                    saved_files.append(processed_path)
                    
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
        
    Returns:
        str: The full path to the saved file
    """
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"Saved file: {file_name}")
    
    # Attempt to post-process the image if PIL is available
    try:
        from PIL import Image
        # Open the image file
        img = Image.open(file_name)
        
        # Check if the image is not already 16:9
        width, height = img.size
        aspect_ratio = width / height
        target_ratio = 16 / 9
        
        if abs(aspect_ratio - target_ratio) > 0.1:  # If aspect ratio is significantly different
            print(f"Image aspect ratio ({aspect_ratio:.2f}) is not 16:9 ({target_ratio:.2f}). Adjusting...")
            
            # Calculate new dimensions
            if aspect_ratio > target_ratio:  # Too wide
                new_width = width
                new_height = int(width / target_ratio)
            else:  # Too tall
                new_height = height
                new_width = int(height * target_ratio)
            
            # Create a new image with YouTube dimensions (black background)
            youtube_img = Image.new('RGB', (new_width, new_height), (0, 0, 0))
            
            # Calculate position to paste (centered)
            paste_x = (new_width - width) // 2
            paste_y = (new_height - height) // 2
            
            # Paste original image
            youtube_img.paste(img, (paste_x, paste_y))
            
            # Save as YouTube optimized image
            youtube_file = file_name.replace('.', '_youtube.')
            youtube_img.save(youtube_file, quality=95)
            print(f"Created YouTube-optimized version: {youtube_file}")
            return youtube_file
    except ImportError:
        print("PIL not available for image post-processing. Using original image.")
    except Exception as e:
        print(f"Error during image post-processing: {str(e)}. Using original image.")
    
    return file_name
