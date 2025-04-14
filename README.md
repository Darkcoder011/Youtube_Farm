# Viral Self-Improvement Content Generator

This project uses Google's Gemini API to generate viral-worthy motivational self-improvement scripts with accompanying inspirational images, audio narration using Kokoro TTS, and complete videos combining all elements.

## Project Structure

```
├── main.py                 # Main application entry point
├── requirements.txt        # Project dependencies
├── src/                    # Source code package
│   ├── generators/         # Content generation modules
│   │   ├── script_generator.py   # Creates viral self-improvement scripts
│   │   ├── image_generator.py    # Generates images from prompts
│   │   ├── audio_generator.py    # Converts scripts to speech using Kokoro TTS
│   │   └── video_generator.py    # Combines images and audio into videos
│   └── utils/              # Utility modules
│       ├── config.py       # Configuration utilities
│       ├── topic_data.py   # Database of 200+ self-improvement topics
│       └── media_utils.py  # Media processing utilities
├── data/                   # Data storage directory
└── output/                 # Output storage directories
    ├── scripts/            # Generated motivational scripts
    ├── images/             # Generated images (YouTube 16:9 format)
    ├── audio/              # Generated audio narrations
    └── videos/             # Complete videos with images and audio
```

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python main.py
   ```

   Additional command line options:
   ```
   python main.py --auto             # Run in automatic mode
   python main.py --list-voices      # Display available TTS voices
   python main.py --voice af_bella   # Specify a TTS voice
   python main.py --skip-audio       # Skip audio generation
   python main.py --skip-video       # Skip video generation
   ```

   Note: API keys are already configured in `src/utils/config.py`

## Development

This project follows standard Python package structure for better organization:

- **src/** - Contains all source code in a proper Python package structure
- **data/** - Reserved for any data files needed by the application
- **output/** - Organized storage for generated content

## How It Works

1. Select from 200+ self-improvement topics or let the system choose one randomly
2. The script generator creates viral, highly shareable motivational content with image prompts using Gemini's text generation capabilities
3. The image generator takes those prompts and creates visual representations in YouTube 16:9 format using Gemini's image generation model
4. The audio generator converts the script into natural-sounding speech using Kokoro TTS
5. The video generator combines the images and audio into a complete video with transitions and text overlays
6. All outputs are saved with timestamps for easy tracking

## Output

- Motivational scripts are saved as markdown files in the `output/scripts` directory
- YouTube-optimized images (16:9 aspect ratio) are saved in the `output/images` directory
- Audio narrations are saved as WAV files in the `output/audio` directory
- Complete videos are saved as MP4 files in the `output/videos` directory
- All outputs use matching timestamps for easy correlation

## Models Used

- Text Generation: `gemini-2.0-flash-thinking-exp-01-21` (Google Gemini)
- Image Generation: `gemini-2.0-flash-exp-image-generation` (Google Gemini)
- Audio Generation: `Kokoro-82M` (Kokoro TTS)
- Video Creation: `MoviePy` (Python video editing library)

## Note

API keys are already configured in the code, so you can run the application immediately without additional setup.

## Run on Google Colab

You can run this project directly in Google Colab without any local setup. Just copy and paste this code cell:

```python
# Clone the repository
!git clone https://github.com/motivationai/motivation-ai-.git
%cd motivation-ai-

# Install required packages for audio and video generation without version conflicts
# Note: We avoid specifying versions for packages already in Colab
!pip install -q kokoro>=0.9.2 soundfile==0.12.1
!pip install -q moviepy==1.0.3 decorator==4.4.2 imageio==2.9.0 tqdm==4.64.1 proglog==0.1.10
!apt-get -qq -y install espeak-ng > /dev/null 2>&1

# Verify that MoviePy is properly installed
import importlib
if importlib.util.find_spec("moviepy") is None:
    raise ImportError("MoviePy installation failed. Please try running this cell again.")
else:
    print("✅ MoviePy successfully installed")

# Create necessary directories
!mkdir -p output/scripts output/images output/audio

# Run the application in automatic mode with audio generation
!python main.py --auto --voice af_bella

# Display generated images (if any)
import glob
from IPython.display import Image, display, Markdown

# Display the generated script
script_files = sorted(glob.glob('output/scripts/*.md'))
if script_files:
    with open(script_files[-1], 'r') as f:
        script_content = f.read()
    display(Markdown(script_content))

# Display any generated images
image_files = sorted(glob.glob('output/images/*.*'))
for img_file in image_files:
    if not img_file.endswith('.gitkeep'):
        display(Image(img_file))
        print(f"Image: {img_file}")

# Display info about generated video
video_files = sorted(glob.glob('output/videos/*.*'))
if video_files:
    print("\nGenerated video:")
    for video_file in video_files:
        print(f"Video: {video_file}")
    # For Colab, you could use HTML to display the video
    from IPython.display import HTML
    if video_files:
        display(HTML(f"""
        <video width="640" height="360" controls>
          <source src="{video_files[-1]}" type="video/mp4">
        </video>
        """))
```

This code will:
1. Clone the repository
2. Install dependencies
3. Run the application
4. Display the generated script and images directly in the notebook
