"""
Utility functions for the Learning Path Generator.
Handles text processing, formatting, and validation.
"""

import json
from typing import Dict, List, Any


def validate_learning_goal(goal: str) -> tuple[bool, str]:
    """
    Validate user's learning goal input.
    
    Args:
        goal: The learning goal text
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not goal or not isinstance(goal, str):
        return False, "Learning goal must be a non-empty string"
    
    if len(goal.strip()) < 5:
        return False, "Learning goal must be at least 5 characters long"
    
    if len(goal) > 500:
        return False, "Learning goal must not exceed 500 characters"
    
    return True, ""


def validate_skill_level(level: str) -> bool:
    """
    Validate user's skill level input.
    
    Args:
        level: The skill level (beginner, intermediate, advanced)
        
    Returns:
        True if valid, False otherwise
    """
    valid_levels = ["beginner", "intermediate", "advanced"]
    return level.lower() in valid_levels


def format_learning_path(raw_response: str) -> Dict[str, Any]:
    """
    Parse and format the LLM response into a structured learning path.
    
    Args:
        raw_response: The raw response from the LLM
        
    Returns:
        Dictionary containing the formatted learning path
    """
    try:
        # Try to parse as JSON first
        if raw_response.startswith('{'):
            return json.loads(raw_response)
    except json.JSONDecodeError:
        pass
    
    # If not JSON, structure the response
    return {
        "structured": False,
        "raw_content": raw_response,
        "milestones": []
    }


def create_prompt(goal: str, skill_level: str) -> str:
    """
    Create a structured prompt for the LLM.
    
    Args:
        goal: The user's learning goal
        skill_level: User's current skill level
        
    Returns:
        The formatted prompt string
    """
    prompt = f"""Create a detailed, personalized learning path for someone who wants to: "{goal}"

Current skill level: {skill_level}

Please provide a comprehensive learning roadmap in the following JSON format:
{{
    "goal": "{goal}",
    "skill_level": "{skill_level}",
    "total_duration": "estimated duration (e.g., 3-6 months)",
    "overview": "brief overview of the learning path",
    "milestones": [
        {{
            "week_or_phase": "Week 1 / Phase 1",
            "title": "title of this milestone",
            "description": "what you'll learn",
            "topics": ["topic1", "topic2", "topic3"],
            "resources": [
                {{
                    "type": "video/article/course/documentation",
                    "title": "resource title",
                    "url": "resource url or 'Search: [keyword]' if no specific url",
                    "duration": "estimated time to complete",
                    "difficulty": "easy/medium/hard"
                }}
            ],
            "practical_exercise": "hands-on project or exercise for this week"
        }}
    ],
    "prerequisites": ["any prerequisites you should know before starting"],
    "tips_and_best_practices": ["tip1", "tip2", "tip3"],
    "estimated_hours_per_week": estimated number,
    "alternative_resources": "suggestions for alternative learning paths or resources"
}}

Make sure the resources are real, practical, and accessible. Include a mix of free resources (YouTube, Medium, official docs) and paid courses when valuable. The learning path should be realistic and achievable for someone at the {skill_level} level."""
    
    return prompt


def parse_json_response(response_text: str) -> Dict[str, Any]:
    """
    Extract and parse JSON from LLM response.
    
    Args:
        response_text: The response text from the LLM
        
    Returns:
        Parsed JSON dictionary or structured fallback
    """
    # Try to find JSON object in the response
    start_idx = response_text.find('{')
    end_idx = response_text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = response_text[start_idx:end_idx+1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    # Fallback: structure the plain text response
    return {
        "raw_content": response_text,
        "structured": False,
        "note": "Response was not in JSON format, displayed as plain text"
    }


def format_milestone_for_display(milestone: Dict[str, Any]) -> str:
    """
    Format a single milestone for pretty display.
    
    Args:
        milestone: The milestone data dictionary
        
    Returns:
        Formatted string for display
    """
    output = f"\n## {milestone.get('week_or_phase', 'Phase')}: {milestone.get('title', 'Untitled')}\n"
    output += f"\n**Description:** {milestone.get('description', 'N/A')}\n"
    
    if milestone.get('topics'):
        output += f"\n**Topics to Cover:**\n"
        for topic in milestone['topics']:
            output += f"- {topic}\n"
    
    if milestone.get('resources'):
        output += f"\n**Resources:**\n"
        for resource in milestone['resources']:
            output += f"- [{resource.get('title', 'Resource')}]({resource.get('url', '#')}) "
            output += f"({resource.get('type', 'resource')}) - {resource.get('duration', 'TBD')}\n"
    
    if milestone.get('practical_exercise'):
        output += f"\n**Practical Exercise:** {milestone['practical_exercise']}\n"
    
    return output
