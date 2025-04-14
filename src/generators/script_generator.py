"""
Script generator module for creating viral self-improvement content.
"""
import random
from google import genai
from google.genai import types

from src.utils.config import load_api_key
from src.utils.topic_data import get_all_topics


def generate_motivation_script(topic=None):
    """
    Generates a viral motivational script along with image prompts using Gemini.
    
    Args:
        topic (str, optional): Specific self-improvement topic to focus on. If None, a random topic is selected.
    
    Returns:
        tuple: (script, image_prompts) - The motivational script and a list of image prompts
    """
    # Get the API key
    api_key = load_api_key()
    
    # Initialize the client
    client = genai.Client(
        api_key=api_key,
    )

    model = "gemini-2.0-flash-thinking-exp-01-21"
    
    # Select a topic if not provided
    if not topic:
        all_topics = get_all_topics()
        topic = random.choice(all_topics)
    
    print(f"Generating viral content on topic: {topic}")
    
    # Create the prompt for generating a motivational script with image prompts
    prompt = f"""
    Create a VIRAL, highly engaging self-improvement script focused on the topic of "{topic}".
    
    Make this content EXTREMELY compelling and shareable - the kind that would get millions of views
    on social media platforms. It should have these characteristics:
    
    1. An attention-grabbing, emotionally resonant introduction that hooks the reader instantly
    2. Use psychology-backed insights and techniques that feel fresh and novel
    3. Include 3-5 counterintuitive or surprising insights/steps related to "{topic}"
    4. Use powerful storytelling elements that create emotional impact
    5. Include viral-worthy phrases and quotes that are highly shareable
    6. Have a conclusion that creates urgency and motivates immediate action
    7. For each section, generate a detailed image prompt that would create a stunning visual
       representation perfect for social media sharing
    
    Format your response as follows:
    
    # [VIRAL-WORTHY TITLE WITH EMOTIONAL IMPACT]
    
    ## The Hook
    [Attention-grabbing opening that creates immediate emotional impact]
    
    IMAGE PROMPT: [Detailed, visually striking image description that captures the essence of the hook]
    
    ## Mind-Shift #1: [Counterintuitive Insight Title]
    [Content that challenges conventional wisdom and offers fresh perspective]
    
    IMAGE PROMPT: [Detailed image description that visualizes this counterintuitive concept dramatically]
    
    ## Mind-Shift #2: [Surprising Strategy Title]
    [Content that reveals an unexpected approach or insight]
    
    IMAGE PROMPT: [Detailed image description for stunning visual representation]
    
    [Continue for all insights/steps...]
    
    ## The Transformation
    [Emotionally powerful conclusion that creates urgency and desire for change]
    
    IMAGE PROMPT: [Detailed image description that portrays the transformational outcome]
    
    ## Viral Quote
    [A single, powerful, shareable quote that encapsulates the main message]
    
    IMAGE PROMPT: [Detailed image description for quote visualization perfect for sharing]
    """
    
    # Add specific instructions based on the selected topic
    topic_specific_instructions = f"""
    Additional instructions for this specific topic:
    
    1. For the topic "{topic}", focus on the most surprising and counterintuitive aspects that most people don't know.
    2. Include at least one science-backed insight that feels novel and enlightening.
    3. Create a powerful "pattern interrupt" - something that challenges the reader's existing beliefs about {topic}.
    4. Highlight a common misconception about {topic} and replace it with a more effective perspective.
    5. Make the content feel exclusive, as if revealing insider secrets.
    
    The image prompts should be extremely detailed and visually striking - designed to stop scrolling on social media.
    They should use powerful visual elements, contrasts, and emotionally resonant imagery related to {topic}.
    """
    
    # Combine the prompts
    full_prompt = prompt + "\n\n" + topic_specific_instructions
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=full_prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        # Add temperature for more creative responses
        temperature=0.8, 
        # Add top_k for better creativity
        top_k=40, 
        # Add top_p for more diverse outputs
        top_p=0.95,
    )
    
    # Store the complete response
    full_response = ""
    
    # Stream the response
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:
            full_response += chunk.text
            print(chunk.text, end="")
    
    # Extract image prompts from the response
    image_prompts = []
    for line in full_response.split('\n'):
        if line.strip().startswith("IMAGE PROMPT:"):
            prompt = line.replace("IMAGE PROMPT:", "").strip()
            image_prompts.append(prompt)
    
    return full_response, image_prompts
