import base64
import os
import mimetypes
from google import genai
from google.genai import types
from dotenv import load_dotenv

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

def generate_image(prompt, image_name="generated_image"):
    """
    Generate an image from a text prompt using Gemini model.
    
    Args:
        prompt (str): The description of the image to generate
        image_name (str): Base name for the saved image file
    
    Returns:
        str: Path to the saved image file
    """
    # Load environment variables
    load_dotenv()
    
    # Initialize the client
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
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
    
    # Create an output directory if it doesn't exist
    os.makedirs("output_images", exist_ok=True)
    
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
            file_path = os.path.join("output_images", f"{image_name}{file_extension}")
            
            save_binary_file(file_path, inline_data.data)
            saved_files.append(file_path)
            
            print(
                f"File of mime type {inline_data.mime_type} saved to: {file_path}"
            )
        else:
            if chunk.text:
                print(chunk.text)
    
    return saved_files

if __name__ == "__main__":
    test_prompt = "A person climbing a mountain at sunrise, symbolizing personal growth and perseverance"
    generate_image(test_prompt, "test_image")
