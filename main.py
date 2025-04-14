#!/usr/bin/env python3
"""
Main application for the Viral Self-Improvement Content Generator
"""
import os
import time
import random

# Import from our new folder structure
from src.generators.script_generator import generate_motivation_script
from src.generators.image_generator import generate_image
from src.utils.topic_data import get_all_topics, get_random_topics

def main():
    """
    Main application function that:
    1. Allows selection of a self-improvement topic or randomly chooses one
    2. Generates viral motivational script with image prompts
    3. Generates images based on those prompts
    4. Saves results to output directory
    """
    print("=" * 80)
    print("🌟 VIRAL SELF-IMPROVEMENT CONTENT GENERATOR 🌟")
    print("=" * 80)
    
    # Get available topics
    all_topics = get_all_topics()
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
    selected_topic = None
    
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
        
        # Generate image with a unique name
        image_name = f"motivation_{timestamp}_{i}"
        image_files = generate_image(prompt, image_name)
        
        if image_files:
            generated_images.extend(image_files)
            print(f"✅ Image {i} generated successfully\n")
        else:
            print(f"❌ Failed to generate image {i}\n")
        
        # Short pause to avoid rate limiting
        if i < len(image_prompts):
            time.sleep(2)
    
    # Final summary
    print("\n" + "=" * 80)
    print("🎉 GENERATION COMPLETE 🎉")
    print("=" * 80)
    print(f"📝 Motivational script saved to: {script_file}")
    print(f"🖼️ Generated {len(generated_images)} images in the output/images directory")
    print("\nThank you for using the Viral Self-Improvement Content Generator!")

if __name__ == "__main__":
    main()
