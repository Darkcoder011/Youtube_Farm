import os
import random
from google import genai
from google.genai import types
from dotenv import load_dotenv

# List of 200+ AI, Future Tech & Digital Trends topics
SELF_IMPROVEMENT_TOPICS = [
    # AI Fundamentals & Development
    "Machine learning fundamentals", "Neural network architectures", "Natural language processing", 
    "Computer vision advancements", "Reinforcement learning techniques", "AI ethics frameworks", 
    "Deep learning innovations", "AI research frontiers", "Generative AI evolution",
    "Multimodal AI systems", "AI alignment strategies", "AGI development pathways",
    "Foundation model architectures", "AI interpretability methods", "Explainable AI techniques",
    "AI augmentation approaches", "Human-AI collaboration", "Federated learning advances",
    "AI training methodologies", "Transformer architecture innovations",
    
    # Future Computing & Infrastructure
    "Quantum computing advances", "Cloud computing evolution", "Edge computing applications", 
    "Neuromorphic computing", "Blockchain technologies", "Decentralized networks", "Web3 infrastructure", 
    "Green computing innovations", "High-performance computing", "Serverless architectures", 
    "Spatial computing systems", "Advanced cybersecurity frameworks", "Distributed systems design",
    "Mesh network technologies", "6G communication systems", "Computing sustainability",
    "Infrastructure optimization", "Computational efficiency", "Exascale computing challenges",
    "Zero-trust architectures",
    
    # Digital Transformation & Business
    "Industry 4.0 implementation", "Digital twin technology", "Business AI integration", 
    "IoT enterprise solutions", "RPA and business automation", "Digital innovation strategies", 
    "API economy evolution", "Platform business models", "Hyper-personalization techniques", 
    "Data-driven decision making", "Digital marketing transformation", "Customer experience technologies",
    "Digital employee experience", "Virtual collaboration tools", "Enterprise knowledge systems",
    "Organizational AI adoption", "Digital leadership development", "Change management for technology",
    "Digital ecosystem building", "Technology governance frameworks",
    
    # Emerging Technology Trends
    "Extended reality (XR) evolution", "Metaverse development", "Spatial computing applications", 
    "Brain-computer interfaces", "Synthetic biology advances", "Nanotechnology innovations", 
    "Advanced robotics systems", "Autonomous vehicle technologies", "Smart city infrastructures", 
    "Sustainable technology solutions", "Space technology commercialization", "Precision medicine technologies",
    "Advanced materials science", "Biotechnology convergence", "Energy storage breakthroughs",
    "Sensory augmentation devices", "Human enhancement technologies", "Carbon capture innovations",
    "Vertical farming technologies", "Alternative protein technologies",
    
    # Data Science & Analytics
    "Big data architectures", "Data engineering pipelines", "Predictive analytics models", 
    "Real-time analytics systems", "Data visualization techniques", "Natural language querying", 
    "Automated machine learning", "Data mesh architecture", "Decision intelligence frameworks", 
    "Synthetic data generation", "Data governance strategies", "Time-series analysis methods",
    "Geospatial analytics", "Graph database applications", "Behavioral analytics systems",
    "Prescriptive analytics models", "Analytics democratization", "MLOps best practices",
    "Data storytelling techniques", "Knowledge graph applications",
    
    # Digital Society & Future Work
    "Remote work evolution", "Digital nomad infrastructure", "Future skills development", 
    "AI-human workforce integration", "Digital inclusion strategies", "Technology education transformation", 
    "Universal basic income models", "Platform cooperative systems", "Digital public goods", 
    "Creator economy platforms", "Digital identity frameworks", "Online community building",
    "Digital citizenship development", "Virtual learning environments", "Work automation adaptation",
    "Knowledge worker augmentation", "Gig economy platforms", "Digital wellness practices",
    "Technological unemployment solutions", "Human-centered technology design",
    
    # Immersive Technologies
    "Virtual reality innovations", "Augmented reality platforms", "Mixed reality development", 
    "Spatial audio technologies", "Haptic feedback systems", "Volumetric capture methods", 
    "Digital twin environments", "Immersive storytelling techniques", "Metaverse ecosystems", 
    "Avatar technology development", "Social VR platforms", "Extended reality interfaces",
    "Immersive learning environments", "Spatial computing applications", "Virtual production techniques",
    "Augmented workplace solutions", "Immersive collaboration tools", "Digital fashion innovations",
    "Virtual architecture design", "Synthetic media creation",
    
    # Digital Ethics & Security
    "AI ethics frameworks", "Algorithmic bias mitigation", "Digital privacy protection", 
    "Cybersecurity resilience", "Ethical data collection", "Digital rights frameworks", 
    "Technology governance models", "Misinformation countermeasures", "Quantum cryptography", 
    "Zero-knowledge protocols", "Secure multiparty computation", "Ethical design practices",
    "Trust frameworks for technology", "Explainable AI methods", "Digital well-being strategies",
    "Data sovereignty principles", "Responsible innovation frameworks", "Technology impact assessment",
    "Digital inclusion practices", "Sustainable technology development",
    
    # Internet Evolution & Networks
    "Web3 infrastructure development", "Decentralized web protocols", "IoT network architectures", 
    "5G & 6G applications", "Mesh network innovations", "Network virtualization", 
    "Low-orbit satellite networks", "Edge intelligence systems", "Distributed ledger technologies", 
    "Interoperability frameworks", "Protocol innovation", "Content delivery evolution",
    "Semantic web technologies", "Ambient connectivity", "Machine-to-machine communication",
    "Network security architectures", "Digital infrastructure resilience", "Information discovery systems",
    "Personal area networks", "Ultra-wideband applications",
    
    # Human-Tech Interaction
    "Conversational interface design", "Ambient computing systems", "Gesture recognition technologies", 
    "Voice computing advances", "Brain-computer interfaces", "Affective computing methods", 
    "Wearable technology evolution", "Ambient intelligence environments", "Human-centered AI design", 
    "Digital twin interfaces", "Multimodal interaction systems", "Adaptive interfaces",
    "Spatial computing interaction", "Zero UI approaches", "Human augmentation interfaces",
    "Smart environment interaction", "Inclusive design methodologies", "Cognitive load optimization",
    "Tangible computing interfaces", "Multisensory digital experiences",
    
    # Extra Technology Trends
    "Digital sustainability practices", "Synthetic media evolution", "Low-code/no-code platforms",
    "FinTech infrastructure innovations", "Circular economy technologies", "Smart contract applications",
    "Regenerative technology approaches", "Computational creativity", "Personalized manufacturing",
    "Open source infrastructure", "Digital commons development", "Cross-reality systems",
    "Biodigital convergence", "Autonomous systems governance", "Technology sovereignty frameworks"
]

def generate_motivation_script(topic=None):
    """
    Generates a viral script on AI, Future Tech & Digital Trends along with image prompts using Gemini.
    
    Args:
        topic (str, optional): Specific technology topic to focus on. If None, a random topic is selected.
    
    Returns:
        tuple: (script, image_prompts) - The generated script and a list of image prompts
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
    
    # Create the prompt for generating a script on AI & Future Tech with image prompts
    prompt = f"""

    Create a VIRAL, highly engaging script focused on the AI/technology topic of "{topic}".
    
    Make this content EXTREMELY compelling and shareable - the kind that would get millions of views
    on social media platforms. It should have these characteristics:
    
    1. An attention-grabbing, future-focused introduction that hooks the reader instantly
    2. Use technology insights and recent advancements that feel cutting-edge and novel
    3. Include 3-5 counterintuitive or surprising insights/predictions related to "{topic}"
    4. Use powerful storytelling elements that create a sense of wonder and possibility
    5. Include viral-worthy phrases and quotes about technology that are highly shareable
    6. Have a conclusion that creates excitement about future possibilities
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
    Additional instructions for this specific technology topic:
    
    1. For the topic "{topic}", focus on the most surprising and counterintuitive aspects that most people don't know.
    2. Include at least one recent technological breakthrough or research finding that feels cutting-edge.
    3. Create a powerful "future vision" - something that challenges the reader's existing understanding of {topic}.
    4. Highlight a common misconception about {topic} and replace it with a more accurate technological perspective.
    5. Make the content feel exclusive, as if revealing insider knowledge from the tech industry.
    
    The image prompts should be extremely detailed and visually striking - designed to stop scrolling on social media.
    They should use futuristic visual elements, high-tech aesthetics, and compelling technological imagery related to {topic}.
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
    """Returns the list of available AI, Future Tech & Digital Trends topics"""
    return SELF_IMPROVEMENT_TOPICS

def get_random_topics(n=5):
    """Returns a random selection of n AI, Future Tech & Digital Trends topics"""
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
