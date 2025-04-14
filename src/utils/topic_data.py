"""
Database of self-improvement topics for content generation.
"""

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


def get_all_topics():
    """
    Get all available self-improvement topics.
    
    Returns:
        list: All available topics
    """
    return SELF_IMPROVEMENT_TOPICS


def get_random_topics(n=5):
    """
    Get a random selection of self-improvement topics.
    
    Args:
        n (int): Number of topics to return
        
    Returns:
        list: Random selection of topics
    """
    import random
    return random.sample(SELF_IMPROVEMENT_TOPICS, min(n, len(SELF_IMPROVEMENT_TOPICS)))


def get_topics_by_category():
    """
    Get self-improvement topics organized by category.
    
    Returns:
        dict: Topics organized by category
    """
    return {
        "Mindset & Psychology": SELF_IMPROVEMENT_TOPICS[0:20],
        "Productivity & Time Management": SELF_IMPROVEMENT_TOPICS[20:40],
        "Health & Wellness": SELF_IMPROVEMENT_TOPICS[40:60],
        "Fitness & Physical Development": SELF_IMPROVEMENT_TOPICS[60:80],
        "Emotional Intelligence & Relationships": SELF_IMPROVEMENT_TOPICS[80:100],
        "Career & Professional Development": SELF_IMPROVEMENT_TOPICS[100:120],
        "Financial Intelligence": SELF_IMPROVEMENT_TOPICS[120:140],
        "Personal Development": SELF_IMPROVEMENT_TOPICS[140:160],
        "Learning & Skill Acquisition": SELF_IMPROVEMENT_TOPICS[160:180],
        "Creativity & Expression": SELF_IMPROVEMENT_TOPICS[180:200],
        "Extra Topics": SELF_IMPROVEMENT_TOPICS[200:]
    }
