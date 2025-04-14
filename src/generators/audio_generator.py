"""
Audio generator module for creating speech from text using Kokoro TTS.
"""
import os
import numpy as np
import soundfile as sf
import warnings
from kokoro import KPipeline

from src.utils.media_utils import collect_complete_story
from src.utils.config import get_output_paths

# Suppress specific warnings
warnings.filterwarnings("ignore", message="dropout option adds dropout after all but last recurrent layer")
warnings.filterwarnings("ignore", message="`torch.nn.utils.weight_norm` is deprecated")

# Voice options available in Kokoro
VOICE_OPTIONS = {
    'American English': ['af', 'af_bella', 'af_sarah', 'am_adam', 'am_michael'],
    'British English': ['bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis'],
    'Custom': ['af_nicole', 'af_sky', 'af_heart']
}

# Default voices for different content types
DEFAULT_VOICES = {
    'motivation': 'af_bella',  # Clear, professional female voice
    'storytelling': 'af_heart',  # Warm, engaging voice
    'instruction': 'am_michael',  # Authoritative male voice
    'default': 'af_bella'  # Default fallback
}

def generate_audio(script_text, audio_name="motivation_audio", voice_type=None, max_retries=3):
    """
    Generates audio from a motivational script using Kokoro TTS.
    
    Args:
        script_text (str): The text of the script to convert to speech
        audio_name (str): Base name for the saved audio file
        voice_type (str, optional): The specific voice to use from VOICE_OPTIONS
        max_retries (int): Maximum number of retry attempts if generation fails
        
    Returns:
        dict: Information about the generated audio including path and data
    """
    print("\n--- Starting Text-to-Speech Generation with Kokoro ---")
    
    # Get output paths
    scripts_dir, _ = get_output_paths()
    audio_dir = os.path.join(os.path.dirname(scripts_dir), "audio")
    os.makedirs(audio_dir, exist_ok=True)
    
    # Set up the voice to use
    if not voice_type or voice_type not in [v for voices in VOICE_OPTIONS.values() for v in voices]:
        voice_type = DEFAULT_VOICES['motivation']
        print(f"Using default voice: {voice_type}")
    else:
        print(f"Using selected voice: {voice_type}")
    
    try:
        # First collect and clean the complete script
        complete_script = collect_complete_story(script_text)
        
        print("⏳ Converting complete script to speech...")
        print(f"Script preview (first 100 chars): {complete_script[:100]}...")
        print(f"Total script length: {len(complete_script)} characters")
        
        # Initialize Kokoro pipeline with explicit repo_id to suppress warning
        attempt = 0
        success = False
        
        while attempt < max_retries and not success:
            attempt += 1
            
            try:
                pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
                
                # Generate audio for the complete script
                generator = pipeline(complete_script, voice=voice_type)
                
                # Save the complete audio file
                audio_path = os.path.join(audio_dir, f"{audio_name}.wav")
                
                # Process all audio chunks, combining them into a single file
                all_audio = []
                total_segments = 0
                total_duration = 0
                
                print("Processing script segments:")
                for i, (gs, ps, audio) in enumerate(generator):
                    total_segments += 1
                    # Ensure ps is a float before adding to total_duration
                    try:
                        segment_duration = float(ps)
                        total_duration += segment_duration
                        print(f"  Segment {i+1}: {gs} phonemes, {segment_duration:.2f} seconds")
                    except (ValueError, TypeError):
                        print(f"  Segment {i+1}: {gs} phonemes, duration unknown (non-numeric value)")
                    all_audio.append(audio)
                
                # Combine ALL audio chunks into ONE single file
                if all_audio:
                    print(f"\nCombining {total_segments} segments into a SINGLE audio file...")
                    combined_audio = np.concatenate(all_audio)
                    sf.write(audio_path, combined_audio, 24000)
                    print(f"✅ COMPLETE SCRIPT saved as ONE audio file: {audio_path}")
                    print(f"   - Total duration: {total_duration:.2f} seconds")
                    print(f"   - File format: WAV (24kHz mono)")
                    
                    success = True
                    return {
                        "audio_path": audio_path,
                        "combined_audio": combined_audio,
                        "sample_rate": 24000
                    }
                else:
                    print("⚠️ No audio chunks were generated")
                    
            except Exception as e:
                print(f"⚠️ Error in text-to-speech generation (attempt {attempt}/{max_retries}): {e}")
                if attempt >= max_retries:
                    print(f"Failed after {max_retries} attempts. Last error: {str(e)}")
                    return None
                    
        return None
            
    except Exception as e:
        print(f"⚠️ Error in audio generation: {e}")
        return None
