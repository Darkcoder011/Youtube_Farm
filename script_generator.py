import os
import random
from google import genai
from google.genai import types
from dotenv import load_dotenv

# List of 200+ self-improvement topics
SELF_IMPROVEMENT_TOPICS = [
    # Mindset & Psychology
    "Growth mindset development", "Overcoming limiting beliefs", "Positive psychology techniques", 
    "Mental resilience building", "Cognitive behavioral strategies", "Mindfulness practices", 
    "Self-compassion development", "Emotional intelligence mastery", "Impostor syndrome overcoming",
    "Comfort zone expansion", "Decision-making improvement", "Focus and concentration enhancement",
    "Belief system transformation", "Identity development", "Self-perception improvement",
    "Psychological triggers understanding", "Mind-body connection", "Neuroplasticity utilization",
    "Mental clarity techniques", "Ego transcendence",
    
    # Productivity & Time Management
    "Deep work strategies", "Procrastination elimination", "Time blocking methods", 
    "Priority management", "Goal setting frameworks", "Habit stacking", "Task batching", 
    "Productivity systems", "Efficiency optimization", "Energy management", 
    "Morning routine optimization", "Decision fatigue reduction", "Attention management",
    "Productivity journaling", "Time tracking methods", "Digital minimalism",
    "Work environment optimization", "Single-tasking mastery", "Focus blocks implementation",
    "Planning systems",
    
    # Health & Wellness
    "Micronutrient optimization", "Sleep quality improvement", "Mobility enhancement", 
    "Longevity protocols", "Dietary habit transformation", "Gut health optimization", 
    "Stress management techniques", "Healing breathwork", "Movement optimization", 
    "Immune system strengthening", "Cold exposure benefits", "Sauna protocols",
    "Fasting methods", "Posture improvement", "Hydration optimization",
    "Muscle recovery techniques", "Inflammation reduction", "Joint health protocols",
    "Metabolic health optimization", "Hormone balance strategies",
    
    # Fitness & Physical Development
    "Progressive overload principles", "Functional movement patterns", "Strength training frameworks", 
    "Endurance building", "Mobility enhancement", "Flexibility development", 
    "Athletic performance optimization", "Body composition improvement", "Movement efficiency", 
    "Training consistency strategies", "Injury prevention protocols", "Workout intensity optimization",
    "Exercise sequencing", "Recovery optimization", "Movement variation importance",
    "Training frequency balance", "Body awareness development", "Mind-muscle connection",
    "Fitness tracking methods", "Specialized training techniques",
    
    # Emotional Intelligence & Relationships
    "Emotional regulation", "Active listening skills", "Empathy development", 
    "Relationship boundary setting", "Conflict resolution strategies", "Vulnerability cultivation", 
    "Trust building methods", "Communication enhancement", "Social skills development", 
    "Authentic connection creation", "Love languages understanding", "Attachment style awareness",
    "Forgiveness practice", "Emotional awareness", "Social intelligence development",
    "Interpersonal effectiveness", "Rejection resilience", "Difficult conversation navigation",
    "Loneliness overcoming", "Deep relationship cultivation",
    
    # Career & Professional Development
    "Career capital building", "Professional networking", "Personal branding", 
    "Leadership development", "Public speaking mastery", "Negotiation skills", 
    "Professional reinvention", "Remote work optimization", "Workplace effectiveness", 
    "Job crafting strategies", "Industry pivot techniques", "Career planning frameworks",
    "Professional boundary setting", "Workplace politics navigation", "Skill stacking",
    "Professional confidence development", "Resume optimization", "Interview preparation",
    "Professional relationship cultivation", "Workplace communication enhancement",
    
    # Financial Intelligence
    "Personal finance fundamentals", "Investment strategies", "Money mindset transformation", 
    "Income diversification", "Financial independence roadmaps", "Debt elimination strategies", 
    "Saving optimization", "Wealth building principles", "Financial literacy development", 
    "Retirement planning", "Tax optimization strategies", "Financial risk management",
    "Money management systems", "Budgeting frameworks", "Financial goal setting",
    "Investment psychology", "Financial decision making", "Economic trend awareness",
    "Financial freedom strategies", "Wealth preservation techniques",
    
    # Personal Development
    "Self-awareness deepening", "Personal value clarification", "Life purpose discovery", 
    "Personal mission statement creation", "Character strength development", "Integrity building", 
    "Authenticity cultivation", "Personal philosophy development", "Self-reflection practices", 
    "Identity alignment", "Life design frameworks", "Personal vision creation",
    "Core value integration", "Personal transformation catalysts", "Meaning creation",
    "Life balance optimization", "Personal growth measurement", "Self-actualization journey",
    "Perspective expansion", "Life experiment design",
    
    # Learning & Skill Acquisition
    "Learning acceleration techniques", "Deliberate practice methods", "Skill acquisition frameworks", 
    "Knowledge management systems", "Memory enhancement", "Information processing optimization", 
    "Critical thinking development", "Creative problem solving", "Analytical reasoning", 
    "Pattern recognition improvement", "Mental model building", "Reading retention strategies",
    "Note-taking systems", "Knowledge synthesis", "Input-to-output ratios",
    "Self-education roadmaps", "Learning transfer maximization", "Depth vs breadth balance",
    "Learning environment optimization", "Specialized skill development",
    
    # Creativity & Expression
    "Creative thinking enhancement", "Idea generation methods", "Inspiration cultivation", 
    "Creative process optimization", "Artistic expression development", "Writing improvement", 
    "Creative block overcoming", "Divergent thinking practice", "Personal style development", 
    "Creative courage building", "Self-expression methods", "Creative mindset cultivation",
    "Idea connection frameworks", "Creative constraint utilization", "Flow state accessing",
    "Creative consistency development", "Feedback integration", "Originality cultivation",
    "Creative risk-taking", "Creative identity formation",
    
    # Extra Topics
    "Digital detox strategies", "Travel as personal development", "Environmental wellness",
    "Cultural intelligence development", "Community building", "Legacy creation",
    "Spiritual growth practices", "Lifestyle design", "Minimalism adoption",
    "Adventure mindset cultivation", "Life transition navigation", "Courage building",
    "Resilience development", "Failure recovery strategies", "Personal renaissance engineering"
]

def generate_motivation_script(topic=None):
    """
    Generates a viral motivational script along with image prompts using Gemini.
    
    Args:
        topic (str, optional): Specific self-improvement topic to focus on. If None, a random topic is selected.
    
    Returns:
        tuple: (script, image_prompts) - The motivational script and a list of image prompts
    """
    # Load environment variables
    load_dotenv()
    
    # Initialize the client
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash-thinking-exp-01-21"
    
    # Select a topic if not provided
    if not topic:
        topic = random.choice(SELF_IMPROVEMENT_TOPICS)
    
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

def get_available_topics():
    """Returns the list of available self-improvement topics"""
    return SELF_IMPROVEMENT_TOPICS

def get_random_topics(n=5):
    """Returns a random selection of n self-improvement topics"""
    return random.sample(SELF_IMPROVEMENT_TOPICS, min(n, len(SELF_IMPROVEMENT_TOPICS)))

if __name__ == "__main__":
    # Pick a random topic to demonstrate
    random_topic = random.choice(SELF_IMPROVEMENT_TOPICS)
    
    print(f"Selected topic: {random_topic}\n")
    script, prompts = generate_motivation_script(random_topic)
    
    print("\n\nExtracted Image Prompts:")
    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. {prompt}")
        
    print("\n\nAvailable Topics:")
    for i, topic in enumerate(get_random_topics(10), 1):
        print(f"{i}. {topic}")
