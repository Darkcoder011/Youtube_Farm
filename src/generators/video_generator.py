"""
Video generator module for combining images and audio into a complete video.
Maximum compatibility version for Google Colab.
"""
import os
import glob
import random
from datetime import datetime

# Minimal imports for maximum compatibility
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# Import only the most reliable effects
try:
    # These are the most basic effects that should work across versions
    from moviepy.video.fx.all import blackwhite, colorx
    EFFECTS_AVAILABLE = True
except ImportError:
    print("Basic effects not available, videos will be generated without filters")
    EFFECTS_AVAILABLE = False

from src.utils.config import get_output_paths

# Import the Drive uploader module (will be used only after successful video creation)
try:
    from src.utils import drive_uploader
    DRIVE_UPLOAD_AVAILABLE = True
except ImportError:
    print("Google Drive upload functionality not available. Will skip uploading.")
    DRIVE_UPLOAD_AVAILABLE = False


def create_video(audio_file, image_files, output_name=None, duration_per_image=5.0, 
                 fade_duration=0.5, add_transitions=False, add_text_overlay=False, add_basic_filters=True,
                 upload_to_drive=True, video_title=None, video_description=None, video_tags=None):
    """
    Creates a basic video from a list of images and an audio file.
    Simplified version for maximum Colab compatibility with optional basic filters.
    
    Args:
        audio_file (str): Path to the audio file
        image_files (list): List of paths to image files
        output_name (str, optional): Name for the output video file (without extension)
        duration_per_image (float, optional): Duration in seconds for each image
        fade_duration (float, optional): Duration of fade transitions if enabled
        add_transitions (bool, optional): Whether to add basic fade transitions
        add_text_overlay (bool, optional): Not used in simplified version
        add_basic_filters (bool, optional): Whether to add very basic video filters
        upload_to_drive (bool, optional): Whether to upload the video to Google Drive
        video_title (str, optional): Title for the video (for metadata)
        video_description (str, optional): Description for the video (for metadata)
        video_tags (list/str, optional): Tags for the video (for metadata)
        
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
                # Ultra-simple image clip creation with no effects or transformations
                img_clip = ImageClip(img_path)
                img_clip = img_clip.set_duration(duration_per_image)
                
                # No text overlay for maximum compatibility
                
                video_clips.append(img_clip)
                print(f"Added image {i+1}/{num_images}: {img_path}")
                
            except Exception as e:
                print(f"⚠️ Error processing image {img_path}: {e}")
                # Skip failed images instead of trying to create a blank clip
        
        # Concatenate clips with simplest method
        print("Concatenating video clips...")
        final_clip = concatenate_videoclips(video_clips)
        
        # Apply very basic filters that work across most versions if requested and available
        if add_basic_filters and EFFECTS_AVAILABLE and len(video_clips) > 0:
            try:
                # Choose a random basic filter to apply
                print("Applying a simple filter to enhance video quality...")
                filter_choice = random.choice(["none", "light_contrast", "black_and_white", "warm_tint"])
                
                if filter_choice == "black_and_white":
                    final_clip = final_clip.fx(blackwhite)
                    print("Applied black and white filter")
                elif filter_choice == "warm_tint":
                    # Very slight color enhancement (1.2 = 20% color boost)
                    final_clip = final_clip.fx(colorx, 1.2)
                    print("Applied warm color tint")
                elif filter_choice == "light_contrast":
                    # Apply both for a more vibrant look
                    final_clip = final_clip.fx(colorx, 1.1)
                    print("Applied light contrast enhancement")
                else:
                    print("No filter applied - using original colors")
            except Exception as e:
                print(f"⚠️ Could not apply filter: {e}")
                print("Continuing with unfiltered video...")
        
        # Add audio
        print("Adding audio to video...")
        final_clip = final_clip.set_audio(audio)
        
        # Write the final video file - simplest possible settings
        print(f"Writing video to {video_path}...")
        final_clip.write_videofile(
            video_path, 
            codec='libx264', 
            audio_codec='aac', 
            fps=24,
            threads=2,
            preset='ultrafast'  # Prioritize compatibility and speed over quality
        )
        
        print(f"✅ Video successfully created: {video_path}")
        
        # Upload to Google Drive if requested and available
        if upload_to_drive and DRIVE_UPLOAD_AVAILABLE:
            try:
                print("\n--- Starting Google Drive Upload ---")
                
                # Use video name as title if not provided
                if not video_title:
                    video_title = os.path.basename(video_path).split('.')[0]
                    # Clean up the title a bit
                    video_title = video_title.replace('_', ' ').title()
                
                # Generate a simple description if not provided
                if not video_description:
                    video_description = f"Motivational video generated on {datetime.now().strftime('%Y-%m-%d')}\n"
                    video_description += f"Duration: {audio_duration:.2f} seconds\n"
                    video_description += f"Contains {num_images} images\n"
                
                # Generate some default tags if not provided
                if not video_tags:
                    video_tags = ["motivation", "inspiration", "success", "personal development"]
                
                # Find the first image to use as thumbnail
                thumbnail_path = None
                if image_files and len(image_files) > 0:
                    thumbnail_path = image_files[0]
                
                # Upload to Drive
                folder_id = drive_uploader.upload_video_with_metadata(
                    video_path=video_path,
                    title=video_title,
                    description=video_description,
                    tags=video_tags,
                    thumbnail_path=thumbnail_path,
                    video_duration=audio_duration
                )
                
                if folder_id:
                    print(f"✅ Video and metadata successfully uploaded to Google Drive")
                else:
                    print(f"⚠️ Failed to upload to Google Drive")
            except Exception as e:
                print(f"❌ Error during Google Drive upload: {str(e)}")
                print("Continuing without uploading...")
        
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
