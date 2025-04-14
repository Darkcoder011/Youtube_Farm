"""
Video generator module for combining images and audio into a complete video.
"""
import os
import glob
import random
from datetime import datetime
from moviepy.editor import (
    ImageClip, 
    AudioFileClip, 
    concatenate_videoclips, 
    CompositeVideoClip,
    TextClip,
    ColorClip
)
from moviepy.video.fx import fadein, fadeout, resize

from src.utils.config import get_output_paths


def create_video(audio_file, image_files, output_name=None, duration_per_image=5.0, 
                 fade_duration=0.5, add_transitions=True, add_text_overlay=True):
    """
    Creates a video from a list of images and an audio file.
    
    Args:
        audio_file (str): Path to the audio file
        image_files (list): List of paths to image files
        output_name (str, optional): Name for the output video file (without extension)
        duration_per_image (float, optional): Duration in seconds for each image
        fade_duration (float, optional): Duration of fade effects in seconds
        add_transitions (bool, optional): Whether to add transition effects between images
        add_text_overlay (bool, optional): Whether to add text overlays to the video
        
    Returns:
        str: Path to the created video file
    """
    print("\n--- Starting Video Generation with MoviePy ---")
    
    # Get output paths
    scripts_dir, _ = get_output_paths()
    base_dir = os.path.dirname(scripts_dir)
    video_dir = os.path.join(base_dir, "videos")
    os.makedirs(video_dir, exist_ok=True)
    
    # Default output name with timestamp if not provided
    if not output_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"motivation_video_{timestamp}"
    
    video_path = os.path.join(video_dir, f"{output_name}.mp4")
    
    try:
        # Load audio file
        print(f"Loading audio file: {audio_file}")
        audio = AudioFileClip(audio_file)
        audio_duration = audio.duration
        
        # Calculate how many images we need to cover the audio duration
        num_images = len(image_files)
        if num_images == 0:
            raise ValueError("No image files provided for video generation")
        
        # Calculate how long each image should be displayed
        # If we have few images, we'll repeat them to cover the audio duration
        if num_images * duration_per_image < audio_duration:
            # We need to repeat images to cover the full audio
            cycles_needed = int(audio_duration / (num_images * duration_per_image)) + 1
            image_files = image_files * cycles_needed
            # Recalculate after repeating
            num_images = len(image_files)
        
        # Adjust duration_per_image to match audio length perfectly
        duration_per_image = audio_duration / num_images
        
        print(f"Creating video with {num_images} images, {duration_per_image:.2f}s per image")
        
        # Create video clips from images
        video_clips = []
        
        for i, img_path in enumerate(image_files):
            if i >= num_images:
                break  # Ensure we don't exceed the audio duration
                
            try:
                # Create image clip
                img_clip = ImageClip(img_path, duration=duration_per_image)
                
                # Ensure the image has a 16:9 aspect ratio (YouTube standard)
                target_width = 1920
                target_height = 1080
                img_clip = img_clip.resize(width=target_width, height=target_height)
                
                # Add fade in/out effects if requested
                if add_transitions:
                    if i == 0:  # First clip
                        img_clip = img_clip.fx(fadein, fade_duration)
                    elif i == num_images - 1:  # Last clip
                        img_clip = img_clip.fx(fadeout, fade_duration)
                    else:  # Middle clips
                        img_clip = img_clip.fx(fadein, fade_duration).fx(fadeout, fade_duration)
                
                # Add text overlay if requested
                if add_text_overlay:
                    # Extract filename without extension as the caption
                    base_filename = os.path.basename(img_path)
                    caption = os.path.splitext(base_filename)[0]
                    
                    # Try to make a better caption by removing timestamps and underscores
                    parts = caption.split('_')
                    if len(parts) > 2:
                        # Skip timestamp parts if they exist
                        clean_parts = [p for p in parts if not (p.isdigit() and len(p) >= 8)]
                        caption = " ".join(clean_parts).title()
                    
                    # Create text clip
                    txt_clip = TextClip(
                        caption, 
                        fontsize=48, 
                        color='white', 
                        bg_color='rgba(0,0,0,0.5)',
                        font='Arial-Bold',
                        kerning=-2,
                        method='caption',
                        size=(target_width, None),
                        align='center'
                    )
                    
                    # Position at bottom of frame
                    txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(duration_per_image)
                    
                    # Composite the text over the image
                    img_clip = CompositeVideoClip([img_clip, txt_clip])
                
                video_clips.append(img_clip)
                print(f"Added image {i+1}/{num_images}: {img_path}")
                
            except Exception as e:
                print(f"⚠️ Error processing image {img_path}: {e}")
                # Create a blank clip if image processing fails
                blank_clip = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=duration_per_image)
                video_clips.append(blank_clip)
        
        # Concatenate clips
        print("Concatenating video clips...")
        final_clip = concatenate_videoclips(video_clips, method="compose")
        
        # Add audio
        print("Adding audio to video...")
        final_clip = final_clip.set_audio(audio)
        
        # Write the final video file
        print(f"Writing video to {video_path}...")
        final_clip.write_videofile(
            video_path, 
            codec='libx264', 
            audio_codec='aac', 
            fps=24, 
            threads=4,
            preset='medium'  # Balance between quality and encoding speed
        )
        
        print(f"✅ Video successfully created: {video_path}")
        return video_path
        
    except Exception as e:
        print(f"❌ Error in video generation: {str(e)}")
        return None
    finally:
        # Clean up MoviePy clips to prevent memory leaks
        try:
            if 'audio' in locals():
                audio.close()
            if 'final_clip' in locals():
                final_clip.close()
            for clip in video_clips if 'video_clips' in locals() else []:
                clip.close()
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")


def find_generated_files(base_dir, timestamp=None):
    """
    Find matching generated files (images and audio) by timestamp.
    
    Args:
        base_dir (str): Base directory to search in
        timestamp (str, optional): Specific timestamp to match, if None will use latest files
        
    Returns:
        tuple: (audio_file, image_files) - Paths to audio file and list of image files
    """
    # Find all audio files
    audio_dir = os.path.join(base_dir, "audio")
    audio_files = glob.glob(os.path.join(audio_dir, "*.wav"))
    
    # Find all image files
    images_dir = os.path.join(base_dir, "images")
    image_files = glob.glob(os.path.join(images_dir, "*.*"))
    image_files = [f for f in image_files if not f.endswith('.gitkeep')]  # Filter out .gitkeep files
    
    if not audio_files or not image_files:
        print(f"⚠️ Could not find enough files: Audio files: {len(audio_files)}, Image files: {len(image_files)}")
        return None, []
    
    # If timestamp provided, filter files
    if timestamp:
        matching_audio = [f for f in audio_files if timestamp in os.path.basename(f)]
        matching_images = [f for f in image_files if timestamp in os.path.basename(f)]
        
        if matching_audio and matching_images:
            return matching_audio[0], sorted(matching_images)
    
    # Otherwise use the latest files
    latest_audio = max(audio_files, key=os.path.getctime)
    
    # Try to match images by extracting timestamp from audio filename
    audio_basename = os.path.basename(latest_audio)
    timestamp_parts = audio_basename.split('_')
    
    if len(timestamp_parts) > 1:
        # Try to extract timestamp by finding any parts that could be a timestamp
        potential_timestamps = [part for part in timestamp_parts if part.isdigit() and len(part) >= 8]
        
        if potential_timestamps:
            timestamp = potential_timestamps[0]
            matching_images = [f for f in image_files if timestamp in os.path.basename(f)]
            
            if matching_images:
                return latest_audio, sorted(matching_images)
    
    # Fall back to latest files if no timestamp match found
    print("⚠️ No timestamp match found, using latest files")
    latest_images = sorted(image_files, key=os.path.getctime, reverse=True)
    return latest_audio, latest_images[:min(5, len(latest_images))]  # Limit to at most 5 latest images


if __name__ == "__main__":
    # Test the video generator with sample files
    print("Testing video generator...")
    
    # Get output paths
    scripts_dir, _ = get_output_paths()
    base_dir = os.path.dirname(scripts_dir)
    
    # Find matching files
    audio_file, image_files = find_generated_files(base_dir)
    
    if audio_file and image_files:
        print(f"Found audio file: {audio_file}")
        print(f"Found {len(image_files)} image files")
        
        # Generate video
        create_video(audio_file, image_files, "test_video")
    else:
        print("Could not find matching audio and image files for testing.")
