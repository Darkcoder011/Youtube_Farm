#!/usr/bin/env python3
"""
Main application for the Viral Self-Improvement Content Generator
"""
import os
import time
import random
import sys

# Import from our new folder structure
from src.generators.script_generator import generate_motivation_script
from src.generators.image_generator import generate_image
from src.utils.topic_data import get_all_topics, get_random_topics

def main(auto_mode=False):
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
    
    # Final summary
    print("\n" + "=" * 80)
    print("🎉 GENERATION COMPLETE 🎉")
    print("=" * 80)
    print(f"📝 Motivational script saved to: {script_file}")
    print(f"🖼️ Generated {len(generated_images)} images in the output/images directory")
    print("\nThank you for using the Viral Self-Improvement Content Generator!")

if __name__ == "__main__":
    # Check if auto mode flag is provided
    auto_mode = False
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['-a', '--auto']:
        auto_mode = True
    
    main(auto_mode)
