"""
Core LLM integration module for generating learning paths.
Handles communication with OpenAI's ChatGPT API.
"""

from src.config.config import Config
from src.utils.utils import create_prompt, parse_json_response
import json
from typing import Dict, Any

try:
    from openai import OpenAI, APIStatusError, RateLimitError
    OPENAI_API_ERRORS = (RateLimitError, APIStatusError)
except ImportError:
    OpenAI = None
    APIStatusError = None
    RateLimitError = None
    OPENAI_API_ERRORS = ()


class LearningPathGenerator:
    """
    Generates personalized learning paths using OpenAI's API.
    """
    
    def __init__(self):
        """Initialize the LLM client with OpenAI API key"""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY) if OpenAI else None
        self.model = Config.MODEL_NAME
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        self.conversation_history = []
    
    def generate_learning_path(
        self, 
        goal: str, 
        skill_level: str = "beginner"
    ) -> Dict[str, Any]:
        """
        Generate a personalized learning path for the user.
        
        Args:
            goal: The user's learning goal
            skill_level: User's current skill level (beginner/intermediate/advanced)
            
        Returns:
            Dictionary containing the structured learning path
        """
        try:
            if self.client is None:
                return self._build_fallback_learning_path(
                    goal,
                    skill_level,
                    "The openai Python package is not installed in this environment."
                )

            # Create the initial prompt
            prompt = create_prompt(goal, skill_level)
            
            # Make API call to OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            
            # Parse the response into structured format
            learning_path = parse_json_response(response_text)
            
            # Add metadata
            learning_path["generated"] = True
            learning_path["goal"] = goal
            learning_path["skill_level"] = skill_level
            
            return learning_path
            
        except OPENAI_API_ERRORS as e:
            if self._is_quota_error(e):
                return self._build_fallback_learning_path(goal, skill_level, str(e))
            return self._build_error_response(
                "Error generating learning path",
                goal,
                skill_level,
                str(e)
            )
        except Exception as e:
            return self._build_error_response(
                "Error generating learning path",
                goal,
                skill_level,
                str(e)
            )
    
    def refine_learning_path(
        self,
        initial_path: Dict[str, Any],
        refinement_request: str
    ) -> Dict[str, Any]:
        """
        Refine an existing learning path based on user feedback.
        
        Args:
            initial_path: The initially generated learning path
            refinement_request: User's request for refinement
            
        Returns:
            Refined learning path
        """
        try:
            if self.client is None:
                fallback = self._build_fallback_learning_path(
                    initial_path.get("goal", "your learning goal"),
                    initial_path.get("skill_level", "beginner"),
                    "The openai Python package is not installed in this environment."
                )
                fallback["refined"] = False
                fallback["refinement_request"] = refinement_request
                return fallback

            goal = initial_path.get("goal", "")
            skill_level = initial_path.get("skill_level", "beginner")
            
            # Create refinement prompt
            refinement_prompt = f"""
Based on the learning path for: "{goal}" (skill level: {skill_level})

User's refinement request: {refinement_request}

Please provide an updated learning path that addresses this request. 
Return the updated path in the same JSON format as before, making sure to adjust:
- The milestones if needed
- The resources if needed
- The timeline if needed
- Any other relevant sections

{json.dumps(initial_path, indent=2)}

Updated learning path:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": refinement_prompt
                    }
                ]
            )
            
            response_text = response.choices[0].message.content
            refined_path = parse_json_response(response_text)
            refined_path["refined"] = True
            refined_path["refinement_request"] = refinement_request
            
            return refined_path
            
        except OPENAI_API_ERRORS as e:
            if self._is_quota_error(e):
                fallback = self._build_fallback_learning_path(
                    initial_path.get("goal", "your learning goal"),
                    initial_path.get("skill_level", "beginner"),
                    str(e)
                )
                fallback["refined"] = False
                fallback["refinement_request"] = refinement_request
                return fallback
            return {
                "error": True,
                "message": f"Error refining learning path: {str(e)}"
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Error refining learning path: {str(e)}"
            }
    
    def get_resource_alternatives(
        self,
        topic: str,
        skill_level: str,
        resource_type: str = "all"
    ) -> Dict[str, Any]:
        """
        Get alternative resources for a specific topic.
        
        Args:
            topic: The topic to find resources for
            skill_level: The skill level
            resource_type: Type of resources (video, article, course, documentation, all)
            
        Returns:
            Dictionary with alternative resources
        """
        try:
            if self.client is None:
                return {
                    "topic": topic,
                    "resources": self._default_resources(topic, skill_level),
                    "recommendations": (
                        "OpenAI generation is unavailable because the openai "
                        "Python package is not installed in this environment."
                    ),
                    "generated": False,
                    "fallback": True,
                    "provider_error": (
                        "Install project dependencies with pip install -r "
                        "requirements.txt to re-enable AI resource generation."
                    )
                }

            prompt = f"""Find {resource_type} resources for learning about "{topic}" 
for someone with {skill_level} level knowledge.

Please provide a JSON response with this format:
{{
    "topic": "{topic}",
    "resources": [
        {{
            "title": "resource title",
            "type": "video/article/course/documentation",
            "url": "resource URL or 'Search: [keyword]'",
            "description": "brief description",
            "duration": "estimated time",
            "difficulty": "easy/medium/hard",
            "cost": "free/paid"
        }}
    ],
    "recommendations": "which resources are best for {skill_level} learners"
}}"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=1024,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response_text = response.choices[0].message.content
            return parse_json_response(response_text)
            
        except OPENAI_API_ERRORS as e:
            if self._is_quota_error(e):
                return {
                    "topic": topic,
                    "resources": self._default_resources(topic, skill_level),
                    "recommendations": (
                        "OpenAI quota is currently unavailable, so these are "
                        "offline fallback resources. Start with official docs, "
                        "then use project-based practice to validate progress."
                    ),
                    "generated": False,
                    "fallback": True,
                    "provider_error": self._friendly_quota_message()
                }
            return {
                "error": True,
                "message": f"Error fetching resources: {str(e)}"
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Error fetching resources: {str(e)}"
            }

    def _is_quota_error(self, error: Exception) -> bool:
        """Return True when OpenAI reports exhausted quota or billing limits."""
        body = getattr(error, "body", None)
        if isinstance(body, dict):
            error_info = body.get("error", {})
            if error_info.get("code") == "insufficient_quota":
                return True

        message = str(error).lower()
        quota_markers = [
            "insufficient_quota",
            "exceeded your current quota",
            "check your plan and billing",
        ]
        return any(marker in message for marker in quota_markers)

    def _build_error_response(
        self,
        prefix: str,
        goal: str,
        skill_level: str,
        message: str
    ) -> Dict[str, Any]:
        return {
            "error": True,
            "message": f"{prefix}: {message}",
            "goal": goal,
            "skill_level": skill_level
        }

    def _friendly_quota_message(self) -> str:
        return (
            "OpenAI could not generate this response because the configured API "
            "key has no available quota. Add billing/credits in the OpenAI "
            "dashboard or use a different API key to re-enable AI generation."
        )

    def _build_fallback_learning_path(
        self,
        goal: str,
        skill_level: str,
        provider_error: str = ""
    ) -> Dict[str, Any]:
        """Create a useful local roadmap when the OpenAI account has no quota."""
        duration_by_level = {
            "beginner": ("8-10 weeks", 6),
            "intermediate": ("6-8 weeks", 8),
            "advanced": ("4-6 weeks", 10),
        }
        total_duration, hours_per_week = duration_by_level.get(
            skill_level,
            duration_by_level["beginner"]
        )

        milestones = [
            {
                "week_or_phase": "Phase 1",
                "title": "Map the Fundamentals",
                "description": f"Build a clear foundation for {goal} and define what success looks like.",
                "topics": [
                    "Core terminology",
                    "Prerequisite concepts",
                    "Tooling and setup",
                    "Simple examples"
                ],
                "resources": self._default_resources(goal, skill_level),
                "practical_exercise": (
                    "Create a one-page concept map and complete a tiny starter "
                    "exercise that proves your setup works."
                )
            },
            {
                "week_or_phase": "Phase 2",
                "title": "Practice the Core Skills",
                "description": "Turn the fundamentals into repeatable habits through guided practice.",
                "topics": [
                    "Common workflows",
                    "Worked examples",
                    "Debugging mistakes",
                    "Short daily drills"
                ],
                "resources": self._default_resources(f"{goal} practice", skill_level),
                "practical_exercise": (
                    "Build three small exercises, each focused on one important "
                    "skill, and write down what broke and how you fixed it."
                )
            },
            {
                "week_or_phase": "Phase 3",
                "title": "Build a Portfolio Project",
                "description": "Apply what you learned in a realistic project with a clear outcome.",
                "topics": [
                    "Project planning",
                    "Implementation",
                    "Testing and validation",
                    "Documentation"
                ],
                "resources": self._default_resources(f"{goal} project tutorial", skill_level),
                "practical_exercise": (
                    "Ship one complete project, document your decisions, and collect "
                    "feedback from a peer or community."
                )
            },
            {
                "week_or_phase": "Phase 4",
                "title": "Review and Specialize",
                "description": "Fill gaps, strengthen weak areas, and choose a focused next step.",
                "topics": [
                    "Knowledge gaps",
                    "Advanced patterns",
                    "Performance or quality improvements",
                    "Next specialization"
                ],
                "resources": self._default_resources(f"advanced {goal}", skill_level),
                "practical_exercise": (
                    "Improve your portfolio project using feedback, then write a "
                    "short roadmap for the next month."
                )
            }
        ]

        return {
            "generated": False,
            "fallback": True,
            "goal": goal,
            "skill_level": skill_level,
            "total_duration": total_duration,
            "overview": (
                f"This offline fallback roadmap helps you start learning {goal} "
                "while OpenAI API quota is unavailable. It is intentionally "
                "general, so refine the topics and resources once billing or API "
                "access is restored."
            ),
            "milestones": milestones,
            "prerequisites": [
                "A reliable study schedule",
                "A notes system for questions and discoveries",
                "Access to official documentation and project examples"
            ],
            "tips_and_best_practices": [
                "Prefer small projects over passive watching.",
                "Keep a weekly review log with wins, blockers, and next actions.",
                "Use official documentation when tutorials disagree.",
                "Ask for feedback before moving to more advanced material."
            ],
            "estimated_hours_per_week": hours_per_week,
            "alternative_resources": (
                "Search for official documentation, freeCodeCamp, Coursera, edX, "
                "YouTube crash courses, and GitHub example projects related to "
                f"{goal}."
            ),
            "provider_error": self._friendly_quota_message(),
            "raw_provider_error": provider_error
        }

    def _default_resources(
        self,
        topic: str,
        skill_level: str
    ) -> list[Dict[str, str]]:
        return [
            {
                "type": "documentation",
                "title": f"Official documentation for {topic}",
                "url": f"Search: official documentation {topic}",
                "duration": "2-4 hours",
                "difficulty": "easy" if skill_level == "beginner" else "medium",
                "description": "Use the primary docs as the source of truth.",
                "cost": "free"
            },
            {
                "type": "video",
                "title": f"Beginner-friendly overview of {topic}",
                "url": f"Search: {topic} tutorial {skill_level}",
                "duration": "1-3 hours",
                "difficulty": "easy",
                "description": "Watch a guided overview before practicing.",
                "cost": "free"
            },
            {
                "type": "course",
                "title": f"Project-based course for {topic}",
                "url": f"Search: project based {topic} course",
                "duration": "1-2 weeks",
                "difficulty": "medium",
                "description": "Choose a course with exercises and a final project.",
                "cost": "free/paid"
            }
        ]


# Singleton instance for use across the application
_generator = None


def get_generator() -> LearningPathGenerator:
    """
    Get or create a singleton instance of the generator.
    
    Returns:
        LearningPathGenerator instance
    """
    global _generator
    if _generator is None:
        _generator = LearningPathGenerator()
    return _generator
