#!/usr/bin/env python3
"""
Main application for the Viral Self-Improvement Content Generator
"""
import os
import time
import random
import sys
import argparse
import importlib.util
import subprocess

# First, perform a comprehensive check for MoviePy to ensure it's properly installed
def verify_moviepy_installation():
    """
    Verify that MoviePy is properly installed and functioning.
    Returns bool indicating whether MoviePy is available and working.
    """
    print("Checking MoviePy installation...")
    
    try:
        # First, attempt to import MoviePy
        import moviepy.editor
        # Try to access critical functionality to ensure it's working
        temp_clip = moviepy.editor.ColorClip((640, 480), color=(0,0,0), duration=1)
        
        # If we got here, MoviePy is working
        print("✅ MoviePy is properly installed and functioning")
        return True
    except ImportError:
        print("⚠️ MoviePy is not installed. Attempting to install...")
        try:
            # Attempt to install MoviePy and its dependencies
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", 
                                  "moviepy==1.0.3", "decorator==4.4.2", 
                                  "imageio==2.9.0", "tqdm==4.64.1", "proglog==0.1.10"])
            
            # Try importing after installation
            import moviepy.editor
            temp_clip = moviepy.editor.ColorClip((640, 480), color=(0,0,0), duration=1)
            
            print("✅ MoviePy was successfully installed")
            return True
        except Exception as e:
            print(f"❌ Failed to install MoviePy: {e}")
            print("Video generation will be disabled.")
            return False
    except Exception as e:
        print(f"⚠️ MoviePy is installed but not functioning correctly: {e}")
        print("Video generation will be disabled.")
        return False

# Check MoviePy at the very beginning
MOVIEPY_AVAILABLE = verify_moviepy_installation()

# Import from our new folder structure
from src.generators.script_generator import generate_motivation_script
from src.generators.image_generator import generate_image
from src.utils.topic_data import get_all_topics, get_random_topics

# Import video generator if MoviePy is available
if MOVIEPY_AVAILABLE:
    try:
        from src.generators.video_generator import create_video, find_generated_files
        print("Video generation capabilities loaded successfully")
    except ImportError as e:
        print(f"Warning: Video generator module could not be loaded: {e}")
        MOVIEPY_AVAILABLE = False

# Check if Kokoro is available and import audio generator if it is
KOKORO_AVAILABLE = importlib.util.find_spec("kokoro") is not None
SOUNDFILE_AVAILABLE = importlib.util.find_spec("soundfile") is not None

if KOKORO_AVAILABLE and SOUNDFILE_AVAILABLE:
    try:
        from src.generators.audio_generator import generate_audio, VOICE_OPTIONS
        print("Audio generation capabilities loaded successfully")
    except ImportError as e:
        print(f"Warning: Audio generator module could not be loaded: {e}")
        KOKORO_AVAILABLE = False
else:
    print("Note: Audio generation is disabled (kokoro or soundfile library not installed)")
    # Define empty VOICE_OPTIONS for compatibility
    VOICE_OPTIONS = {"Not Available": ["none"]}

def main(auto_mode=False, voice=None, skip_audio=False, skip_video=False):
    """
    Main application function that:
    1. Allows selection of a self-improvement topic or randomly chooses one
    2. Generates viral motivational script with image prompts
    3. Generates images based on those prompts
    4. Saves results to output directory
    
    Args:
        auto_mode (bool): If True, automatically select a random topic without user input
    """
    print("=" * 80)
    print("🌟 VIRAL SELF-IMPROVEMENT CONTENT GENERATOR 🌟")
    print("=" * 80)
    
    # Get available topics
    all_topics = get_all_topics()
    
    selected_topic = None
    
    if auto_mode:
        # Automatically select a random topic
        selected_topic = random.choice(all_topics)
        print(f"\nAUTO MODE: Randomly selected topic: {selected_topic}\n")
    else:
        random_topics = get_random_topics(10)
        
        # Display topic options
        print("\nChoose a self-improvement topic or let us pick one for you!")
        print("\nRandom Topic Suggestions:")
        for i, topic in enumerate(random_topics, 1):
            print(f"{i}. {topic}")
        print("\n0. Let the system choose randomly from 200+ topics")
        print("or type 'custom' to enter your own topic")
        
        # Get user choice
        choice = input("\nEnter your choice (0-10 or 'custom'): ")
        
        if choice.lower() == 'custom':
            custom_topic = input("Enter your custom self-improvement topic: ")
            selected_topic = custom_topic
        elif choice.isdigit():
            choice_num = int(choice)
            if choice_num == 0:
                # Random choice from all topics
                selected_topic = random.choice(all_topics)
            elif 1 <= choice_num <= len(random_topics):
                # User selected from the displayed topics
                selected_topic = random_topics[choice_num-1]
        
        if not selected_topic:
            print("Invalid choice - selecting a random topic")
            selected_topic = random.choice(all_topics)
        
    print(f"\nGenerating VIRAL content on: {selected_topic}\n")
    print("Creating content that's designed to be shared and go viral...\n")
    
    # Generate the motivational script and image prompts
    script, image_prompts = generate_motivation_script(selected_topic)
    
    # Get output paths from config
    from src.utils.config import get_output_paths
    scripts_dir, _ = get_output_paths()
    
    # Save the script to a file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    script_file = os.path.join(scripts_dir, f"motivation_script_{timestamp}.md")
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script)
    
    print("\n" + "=" * 80)
    print(f"✅ Script saved to {script_file}")
    print("=" * 80)
    
    # Generate images for each prompt
    print("\nNow generating inspirational images based on the script...\n")
    
    generated_images = []
    for i, prompt in enumerate(image_prompts, 1):
        print(f"Generating image {i}/{len(image_prompts)}...")
        print(f"Prompt: {prompt}")
        
        try:
            # Generate image with a unique name and retry logic
            image_name = f"motivation_{timestamp}_{i}"
            # Use 100 retry attempts with 20 second delay between each attempt
            image_files = generate_image(prompt, image_name, max_retries=100, retry_delay=20)
            
            if image_files:
                generated_images.extend(image_files)
                print(f"✅ Image {i} generated successfully\n")
            else:
                print(f"⚠️ Image {i} was not generated, but no error occurred\n")
        except Exception as e:
            # Catch any exceptions to prevent the whole process from failing
            print(f"❌ Failed to generate image {i} after multiple attempts: {str(e)}\n")
            print("Continuing with the next image...\n")
        
        # Short pause to avoid rate limiting
        # Only pause if not the last image
        if i < len(image_prompts):
            # Adding a random jitter to the pause to avoid API rate pattern detection
            jitter_seconds = random.uniform(1.5, 3.0)
            time.sleep(jitter_seconds)
    
    # Generate audio from the script if audio generation is enabled and available
    audio_result = None
    if not skip_audio and KOKORO_AVAILABLE and SOUNDFILE_AVAILABLE:
        print("\nNow generating audio narration of the script...\n")
        try:
            audio_name = f"motivation_{timestamp}"
            audio_result = generate_audio(script, audio_name, voice)
            
            if audio_result:
                print(f"✅ Audio generated successfully\n")
            else:
                print(f"⚠️ Failed to generate audio\n")
        except Exception as e:
            print(f"❌ Error during audio generation: {str(e)}\n")
    elif not skip_audio:
        print("\nAudio generation skipped - required libraries not installed\n")
        print("To enable audio generation, install required packages:")
        print("  pip install kokoro>=0.9.2 soundfile==0.12.1 numpy>=1.20.0")
        print("  On Linux/Colab: apt-get install espeak-ng")
    else:
        print("\nAudio generation skipped as requested\n")
    
    # Generate video from images and audio if enabled
    video_result = None
    if not skip_video and audio_result and generated_images:
        print("\nNow generating video from images and audio...\n")
        
        # At this point, we've already verified MOVIEPY_AVAILABLE at the beginning
        
        if MOVIEPY_AVAILABLE:
            try:
                # Use the same timestamp for the video
                video_name = f"motivation_{timestamp}"
                # Get the base directory for finding files
                from src.utils.config import get_output_paths
                scripts_dir, _ = get_output_paths()
                base_dir = os.path.dirname(scripts_dir)
                
                # Get paths to audio and image files
                audio_file = audio_result['audio_path']
                image_files = generated_images
                
                # Generate video
                video_result = create_video(audio_file, image_files, video_name)
                
                if video_result:
                    print(f"✅ Video generated successfully\n")
                else:
                    print(f"⚠️ Failed to generate video\n")
            except Exception as e:
                print(f"❌ Error during video generation: {str(e)}\n")
        else:
            print("\nVideo generation skipped - required library not installed\n")
            print("To enable video generation, install required packages:")
            print("  pip install moviepy==1.0.3 decorator==4.4.2 imageio==2.9.0 tqdm==4.64.1 proglog==0.1.10")
    elif not skip_video and (not audio_result or not generated_images):
        print("\nVideo generation skipped - missing audio or images\n")
    else:
        print("\nVideo generation skipped as requested\n")
    
    # Final summary
    print("\n" + "=" * 80)
    print("🎉 GENERATION COMPLETE 🎉")
    print("=" * 80)
    print(f"📝 Motivational script saved to: {script_file}")
    print(f"🖼️ Generated {len(generated_images)} images in the output/images directory")
    if audio_result:
        print(f"🎙️ Audio narration saved to: {audio_result['audio_path']}")
    if video_result:
        print(f"🎬 Complete video saved to: {video_result}")
    print("\nThank you for using the Viral Self-Improvement Content Generator!")

def display_available_voices():
    """Display all available voices for TTS"""
    if not KOKORO_AVAILABLE:
        print("\nAudio generation is not available - Kokoro TTS library is not installed")
        print("To install: pip install kokoro>=0.9.2 soundfile==0.12.1")
        return
        
    print("\nAvailable voices for text-to-speech:\n")
    for category, voices in VOICE_OPTIONS.items():
        print(f"{category}:")
        for voice in voices:
            print(f"  - {voice}")
    print()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Viral Self-Improvement Content Generator")
    parser.add_argument("-a", "--auto", action="store_true", help="Run in automatic mode without user interaction")
    parser.add_argument("--voice", type=str, help="Specify voice for TTS (use --list-voices to see options)")
    parser.add_argument("--list-voices", action="store_true", help="Display available voices and exit")
    parser.add_argument("--skip-audio", action="store_true", help="Skip audio generation")
    parser.add_argument("--skip-video", action="store_true", help="Skip video generation")
    
    args = parser.parse_args()
    
    # If user requested to list voices, show them and exit
    if args.list_voices:
        display_available_voices()
        sys.exit(0)
    
    # Run the main application
    main(auto_mode=args.auto, voice=args.voice, skip_audio=args.skip_audio, skip_video=args.skip_video)
