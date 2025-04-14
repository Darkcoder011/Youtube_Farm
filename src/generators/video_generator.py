"""
Video generator module for combining images and audio into a complete video with advanced visual effects.
"""
import os
import glob
import random
from datetime import datetime
import numpy as np
from moviepy.editor import (
    ImageClip, 
    AudioFileClip, 
    concatenate_videoclips, 
    CompositeVideoClip,
    TextClip,
    ColorClip
)
from moviepy.video.fx import (
    fadein, fadeout, resize, lum_contrast, painting, 
    colorx, mirror_x, invert_colors, accel_decel, 
    blackwhite, crop, vfx_frame
)

from src.utils.config import get_output_paths


def apply_image_effects(clip, effect_name, **kwargs):
    """
    Apply various visual effects to an image clip based on effect name.
    
    Args:
        clip (ImageClip): The clip to apply effects to
        effect_name (str): The name of the effect to apply
        **kwargs: Additional parameters for the effect
        
    Returns:
        ImageClip: The modified clip with effects applied
    """
    clip_duration = clip.duration
    
    if effect_name == "ken_burns_zoom":
        # Ken Burns Zoom Effect
        zoom_factor = kwargs.get('zoom_factor', 1.08)
        zoom_direction = kwargs.get('zoom_direction', 'in')  # 'in' or 'out'
        
        if zoom_direction == 'in':
            # Zoom in effect (start small, end large)
            return clip.resize(lambda t: max(1.0, zoom_factor**(t/clip_duration)))
        else:
            # Zoom out effect (start large, end small)
            return clip.resize(lambda t: max(1.0, zoom_factor**(1-t/clip_duration)))
            
    elif effect_name == "slow_pan":
        # Slow Pan Effect (left/right or up/down)
        direction = kwargs.get('direction', random.choice(['left', 'right', 'up', 'down']))
        pan_factor = kwargs.get('pan_factor', 0.1)
        
        w, h = clip.size
        
        # Create a larger clip to allow for panning
        clip_large = clip.resize(1.1)  # Make it 10% larger
        
        if direction == 'left':
            # Pan from right to left
            return clip_large.set_position(lambda t: ('right', 'center')).crop(
                x1=lambda t: w * pan_factor * (1-t/clip_duration),
                y1=0,
                width=w,
                height=h
            )
        elif direction == 'right':
            # Pan from left to right
            return clip_large.set_position(lambda t: ('left', 'center')).crop(
                x1=lambda t: w * pan_factor * (t/clip_duration),
                y1=0,
                width=w,
                height=h
            )
        elif direction == 'up':
            # Pan from bottom to top
            return clip_large.set_position(lambda t: ('center', 'bottom')).crop(
                x1=0,
                y1=lambda t: h * pan_factor * (1-t/clip_duration),
                width=w,
                height=h
            )
        else:  # 'down'
            # Pan from top to bottom
            return clip_large.set_position(lambda t: ('center', 'top')).crop(
                x1=0,
                y1=lambda t: h * pan_factor * (t/clip_duration),
                width=w,
                height=h
            )
            
    elif effect_name == "background_blur_center_text":
        # Background Blur with Center Text
        # Text should be added separately in the main function
        # Here we just blur the background a bit
        # This is a simplified version as true gaussian blur is complex in moviepy
        return clip.fx(painting, saturation=1.2, black=0.001)
        
    elif effect_name == "color_boost":
        # Color Boost (Contrast + Warm Tone)
        contrast = kwargs.get('contrast', 50)
        colorx_factor = kwargs.get('colorx_factor', 1.3)
        
        # First boost colors then adjust contrast
        return clip.fx(colorx, colorx_factor).fx(lum_contrast, 0, contrast, 255)
        
    elif effect_name == "dark_overlay":
        # Dark Overlay Effect
        opacity = kwargs.get('opacity', 0.3)
        
        # Create a black color clip with the same size and duration
        overlay = ColorClip(size=clip.size, color=(0, 0, 0), duration=clip.duration).set_opacity(opacity)
        return CompositeVideoClip([clip, overlay])
        
    elif effect_name == "glow_effect":
        # Glow / Light Leak Effect
        # Simplified version: increase brightness and add a slight color tint
        glow_color = kwargs.get('glow_color', 'warm')  # 'warm' or 'cool'
        
        if glow_color == 'warm':
            # Warm glow (yellowish tint)
            return clip.fx(colorx, 1.2).fx(lum_contrast, 20, 0, 255)
        else:
            # Cool glow (bluish tint) - simplified version without image_transform
            return clip.fx(colorx, 1.1).fx(lum_contrast, 10, 0, 255)
        
    elif effect_name == "cinematic_crop":
        # Cinematic Crop (21:9 aspect ratio)
        w, h = clip.size
        
        # Calculate the height for 21:9 aspect ratio
        target_h = int(w * 9 / 21)
        crop_amount = (h - target_h) // 2
        
        return clip.crop(y1=crop_amount, y2=h-crop_amount)
        
    elif effect_name == "vignette":
        # Vignette Effect - simplified version without custom transforms
        # Return a darker version with lum_contrast as a simplified alternative
        return clip.fx(lum_contrast, -20, 20, 128)
        
    elif effect_name == "subtle_grain":
        # Subtle Grain / Texture - simplified version without custom transforms
        # Return a slightly higher contrast version as an alternative
        return clip.fx(lum_contrast, 0, 10, 255)
        
    elif effect_name == "mirror_effect":
        # Mirror effect (flip horizontally)
        return clip.fx(mirror_x)
        
    elif effect_name == "bw_partial":
        # Partial black and white effect - simplified to standard blackwhite filter
        return clip.fx(blackwhite)
    
    # If no effect matches, return the original clip
    return clip


def create_video(audio_file, image_files, output_name=None, duration_per_image=5.0, 
                 fade_duration=0.5, add_transitions=True, add_text_overlay=True,
                 apply_effects=True, min_effects=7):
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
                
                # We'll apply effects to the whole video later, not to individual images
                
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
        
        # Apply visual effects to the entire video if requested
        if apply_effects:
            # List of all available effects
            all_effects = [
                "ken_burns_zoom", "slow_pan", "background_blur_center_text", 
                "color_boost", "dark_overlay", "glow_effect", 
                "cinematic_crop", "vignette", "subtle_grain", "mirror_effect", "bw_partial"
            ]
            
            # Randomly choose how many effects to apply (at least min_effects, up to length of all_effects)
            num_effects = random.randint(min_effects, min(len(all_effects), min_effects + 2))
            
            # Randomly select effects to apply
            selected_effects = random.sample(all_effects, num_effects)
            print(f"\nApplying {num_effects} effects to the entire video: {', '.join(selected_effects)}")
            
            # Apply each selected effect with random parameters to the entire video
            for effect in selected_effects:
                # Random parameters based on effect type
                if effect == "ken_burns_zoom":
                    params = {
                        'zoom_factor': random.uniform(1.05, 1.1),
                        'zoom_direction': random.choice(['in', 'out'])
                    }
                elif effect == "slow_pan":
                    params = {
                        'direction': random.choice(['left', 'right', 'up', 'down']),
                        'pan_factor': random.uniform(0.05, 0.15)
                    }
                elif effect == "color_boost":
                    params = {
                        'contrast': random.randint(30, 60),
                        'colorx_factor': random.uniform(1.1, 1.4)
                    }
                elif effect == "dark_overlay":
                    params = {'opacity': random.uniform(0.2, 0.4)}
                elif effect == "glow_effect":
                    params = {'glow_color': random.choice(['warm', 'cool'])}
                elif effect == "vignette":
                    params = {'intensity': random.uniform(0.6, 0.9)}
                elif effect == "subtle_grain":
                    params = {'intensity': random.uniform(0.05, 0.1)}
                else:
                    params = {}
                    
                # Apply the effect to the entire video
                print(f"  Applying {effect} effect to the entire video...")
                final_clip = apply_image_effects(final_clip, effect, **params)
        
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
