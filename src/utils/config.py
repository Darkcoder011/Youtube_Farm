"""
Configuration utilities for the self-improvement content generator.
"""
import os

# List of available API keys
GEMINI_API_KEYS = [
    "AIzaSyDt4vsxhiXUC-M4aC5tZCkmxw02kvOIbLc",
    "AIzaSyDC-w6giUXQV3cCSs2BGCMRUWnCfXdETBQ",
    "AIzaSyCbWk0dSGqYFgrjdE5IsuirqZowSw8FQLM",
    "AIzaSyBQxoT97-AGqmCoS9YbQLh1KlOqCDIITz0",
    "AIzaSyD-JWNeXoa2gVyHOXi9-D3QXN7LQrH90cY",
    "AIzaSyDOEDegu4gtr7y92DrqBZvzg59Mhvtummw"
]

# Primary API key to use
PRIMARY_API_KEY = GEMINI_API_KEYS[2]  # Using the third key in the list

def load_api_key():
    """
    Get the Gemini API key.
    
    Returns:
        str: The Gemini API key
    """
    return PRIMARY_API_KEY

def get_output_paths():
    """
    Get paths for output files.
    
    Returns:
        tuple: (scripts_dir, images_dir) - Paths to output directories
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    scripts_dir = os.path.join(base_dir, "output", "scripts")
    images_dir = os.path.join(base_dir, "output", "images")
    
    # Ensure directories exist
    os.makedirs(scripts_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    return scripts_dir, images_dir
