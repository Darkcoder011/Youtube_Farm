#!/usr/bin/env python3
"""
Continuous Runner for the Viral Self-Improvement Content Generator

This script continuously runs the content generation process, creating new
motivational videos one after another until the user manually stops it.
"""
import os
import sys
import time
import signal
import random
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('ContinuousRunner')

# Import main script functions
try:
    from main import (
        generate_script, 
        create_images, 
        generate_audio, 
        create_video,
        process_arguments,
        verify_api_key,
        verify_moviepy_installation
    )
    logger.info("Successfully imported functions from main module")
except ImportError as e:
    logger.error(f"Failed to import required functions from main module: {e}")
    sys.exit(1)

# Global flag to track if we should exit
should_exit = False

def signal_handler(sig, frame):
    """Handle interrupt signals to gracefully exit the continuous loop."""
    global should_exit
    logger.info("Interrupt received. Finishing current video and exiting...")
    should_exit = True

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def generate_random_topic():
    """Generate a random motivational topic."""
    topics = [
        "perseverance", "success", "growth mindset", "overcoming obstacles", 
        "self-discipline", "positive thinking", "goal setting", "resilience",
        "personal growth", "mindfulness", "confidence", "leadership",
        "courage", "inspiration", "passion", "productivity", "focus",
        "gratitude", "determination", "consistency", "ambition", "excellence"
    ]
    return random.choice(topics)

def get_delay_between_videos():
    """Get the delay between video generations in seconds."""
    # Default: wait 2 minutes between videos
    default_delay = 2 * 60
    
    try:
        delay_str = os.environ.get('VIDEO_GEN_DELAY_SECONDS')
        if delay_str:
            delay = int(delay_str)
            if delay < 60:
                logger.warning(f"Delay is very short ({delay}s). Setting minimum of 60s.")
                return max(60, delay)  # Minimum 60 seconds
            return delay
        return default_delay
    except (ValueError, TypeError):
        logger.warning(f"Invalid delay value. Using default {default_delay}s.")
        return default_delay

def run_continuous():
    """Run the video generation process continuously."""
    logger.info("Starting continuous video generation")
    
    # Verify requirements first
    if not verify_api_key():
        logger.error("API key verification failed. Exiting.")
        return
    
    if not verify_moviepy_installation():
        logger.warning("MoviePy installation verification failed. Video generation may not work.")
    
    # Get delay between videos
    delay_seconds = get_delay_between_videos()
    logger.info(f"Will generate videos continuously with {delay_seconds}s delay between generations")
    
    # Print instructions for stopping
    logger.info("Press Ctrl+C to stop the continuous generation after current video completes")
    
    video_count = 0
    
    try:
        while not should_exit:
            video_count += 1
            generation_start = datetime.now()
            
            logger.info(f"\n{'='*80}\nStarting video generation #{video_count} at {generation_start.strftime('%Y-%m-%d %H:%M:%S')}\n{'='*80}")
            
            # Generate a random topic
            topic = generate_random_topic()
            logger.info(f"Selected random topic: {topic}")
            
            try:
                # We'll use the same flow as in main.py but with our random topic in auto mode
                # Always use auto mode for continuous generation
                args = process_arguments(['--topic', topic, '--auto'])
                
                # Generate script
                logger.info(f"Generating script on topic: {topic}")
                script_path, script_segments = generate_script(args.topic, args.script_only)
                if not script_path:
                    logger.error("Script generation failed. Skipping to next iteration.")
                    continue
                
                # Create images
                logger.info("Generating images based on script")
                image_files = create_images(script_segments, args.skip_images)
                if not image_files:
                    logger.error("Image generation failed. Skipping to next iteration.")
                    continue
                
                # Generate audio
                logger.info("Generating audio narration")
                audio_file = generate_audio(script_path, script_segments, args.voice, args.skip_audio)
                if not audio_file:
                    logger.error("Audio generation failed. Skipping to next iteration.")
                    continue
                
                # Create video
                logger.info("Creating final video")
                video_path = create_video(audio_file, image_files, args.skip_video)
                if not video_path:
                    logger.error("Video creation failed. Skipping to next iteration.")
                    continue
                
                # Record completion time and duration
                generation_end = datetime.now()
                duration = (generation_end - generation_start).total_seconds()
                logger.info(f"\nVideo #{video_count} completed in {duration:.1f} seconds")
                logger.info(f"Video saved to: {video_path}")
                
                if should_exit:
                    logger.info("Exit flag detected. Stopping after this video.")
                    break
                
                # Wait before starting next video
                wait_until = datetime.now().timestamp() + delay_seconds
                logger.info(f"Waiting {delay_seconds} seconds before starting next video...")
                
                # Use a small loop to check for exit flag during the wait
                while datetime.now().timestamp() < wait_until and not should_exit:
                    time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error during video generation cycle: {str(e)}")
                # Still wait before trying again
                if not should_exit:
                    logger.info(f"Waiting {delay_seconds} seconds before retrying...")
                    time.sleep(delay_seconds)
    
    except Exception as e:
        logger.error(f"Fatal error in continuous runner: {str(e)}")
    
    finally:
        logger.info(f"\n{'='*80}\nContinuous generation stopped after creating {video_count} videos\n{'='*80}")

if __name__ == "__main__":
    # Parse any specific arguments for the continuous runner
    import argparse
    parser = argparse.ArgumentParser(description="Continuously generate motivational videos")
    parser.add_argument("--delay", type=int, help="Delay between videos in seconds (default: 120)")
    continuous_args = parser.parse_args()
    
    # Set delay from arguments if provided
    if continuous_args.delay:
        os.environ['VIDEO_GEN_DELAY_SECONDS'] = str(continuous_args.delay)
    
    # Run the continuous generation
    run_continuous()
