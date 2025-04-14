# Viral Self-Improvement Content Generator

This project uses Google's Gemini API to generate viral-worthy motivational self-improvement scripts and accompanying inspirational images.

## Project Structure

```
├── main.py                 # Main application entry point
├── requirements.txt        # Project dependencies
├── src/                    # Source code package
│   ├── generators/         # Content generation modules
│   │   ├── script_generator.py   # Creates viral self-improvement scripts
│   │   └── image_generator.py    # Generates images from prompts
│   └── utils/              # Utility modules
│       ├── config.py       # Configuration utilities
│       └── topic_data.py   # Database of 200+ self-improvement topics
├── data/                   # Data storage directory
└── output/                 # Output storage directories
    ├── scripts/            # Generated motivational scripts
    └── images/             # Generated images
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

   Note: API keys are already configured in `src/utils/config.py`

## Development

This project follows standard Python package structure for better organization:

- **src/** - Contains all source code in a proper Python package structure
- **data/** - Reserved for any data files needed by the application
- **output/** - Organized storage for generated content

## How It Works

1. Select from 200+ self-improvement topics or let the system choose one randomly
2. The script generator creates viral, highly shareable motivational content with image prompts using Gemini's text generation capabilities
3. The image generator takes those prompts and creates visual representations using Gemini's image generation model
4. All outputs are saved with timestamps for easy tracking

## Output

- Motivational scripts are saved as markdown files in the `output/scripts` directory
- Generated images are saved in the `output/images` directory with timestamps

## Models Used

- Text Generation: `gemini-2.0-flash-thinking-exp-01-21`
- Image Generation: `gemini-2.0-flash-exp-image-generation`

## Note

You need a valid Google API key with access to Gemini models to use this application.
