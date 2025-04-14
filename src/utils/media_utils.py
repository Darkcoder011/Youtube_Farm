"""
Utility functions for media processing (text, audio, etc.)
"""
import re
import os

def collect_complete_story(story_text):
    """
    Collects and cleans the full story text from the markdown format,
    removing markdown formatting and image prompts.
    
    Args:
        story_text (str): The raw markdown text of the story
        
    Returns:
        str: The cleaned story text ready for TTS processing
    """
    # Split the text into lines
    lines = story_text.split('\n')
    
    # Initialize variables
    cleaned_lines = []
    skip_line = False
    
    # Process each line
    for line in lines:
        # Skip image prompts
        if line.strip().startswith('IMAGE PROMPT:'):
            skip_line = True
            continue
        
        # Reset skip flag after an empty line following an image prompt
        if skip_line and not line.strip():
            skip_line = False
            continue
            
        # Skip lines we're flagged to skip
        if skip_line:
            continue
            
        # Skip markdown heading markers but keep the text
        if line.strip().startswith('#'):
            # Remove the heading markers
            clean_line = re.sub(r'^#+\s+', '', line).strip()
            cleaned_lines.append(clean_line)
            continue
            
        # Add regular lines
        cleaned_lines.append(line)
    
    # Join the cleaned lines
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Remove excessive newlines (more than 2 in a row)
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    # Remove any remaining markdown formatting
    # Remove bold/italic
    cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_text)
    cleaned_text = re.sub(r'\*(.*?)\*', r'\1', cleaned_text)
    
    # Remove links
    cleaned_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', cleaned_text)
    
    return cleaned_text.strip()

def ensure_directory(directory_path):
    """
    Ensures that a directory exists, creating it if necessary.
    
    Args:
        directory_path (str): Path to the directory
        
    Returns:
        str: The path to the directory
    """
    os.makedirs(directory_path, exist_ok=True)
    return directory_path
