"""
Example script demonstrating how to use the Learning Path Generator
without the Streamlit UI.
"""

from src.llm_generator import get_generator
from src.utils.utils import validate_learning_goal, validate_skill_level
import json


def example_basic_usage():
    """Basic example of generating a learning path"""
    print("=" * 60)
    print("Learning Path Generator - Basic Usage Example")
    print("=" * 60)
    
    # User inputs
    goal = "I want to learn Machine Learning and AI"
    skill_level = "beginner"
    
    print(f"\n📝 Learning Goal: {goal}")
    print(f"📊 Skill Level: {skill_level}")
    
    # Validate inputs
    is_valid, error_msg = validate_learning_goal(goal)
    if not is_valid:
        print(f"❌ Invalid goal: {error_msg}")
        return
    
    # Generate learning path
    print("\n🤖 Generating learning path...")
    generator = get_generator()
    learning_path = generator.generate_learning_path(goal, skill_level)
    
    # Display results
    if learning_path.get("error"):
        print(f"❌ Error: {learning_path.get('message')}")
    else:
        print("\n✅ Learning path generated successfully!\n")
        
        # Display overview
        print(f"📋 Overview: {learning_path.get('overview', 'N/A')}\n")
        
        # Display milestones
        if learning_path.get("milestones"):
            print("📚 Milestones:\n")
            for idx, milestone in enumerate(learning_path["milestones"], 1):
                print(f"\n{idx}. {milestone.get('week_or_phase', f'Phase {idx}')}: {milestone.get('title', 'Milestone')}")
                print(f"   Description: {milestone.get('description', 'N/A')}")
                
                if milestone.get("topics"):
                    print("   Topics:")
                    for topic in milestone["topics"]:
                        print(f"     - {topic}")
                
                if milestone.get("resources"):
                    print("   Resources:")
                    for resource in milestone["resources"]:
                        print(f"     - {resource.get('title', 'Resource')} ({resource.get('type', 'resource')})")
        
        # Print full JSON
        print("\n" + "=" * 60)
        print("Full JSON Response:")
        print("=" * 60)
        print(json.dumps(learning_path, indent=2))


def example_with_refinement():
    """Example showing how to refine a generated learning path"""
    print("\n" + "=" * 60)
    print("Learning Path Generator - With Refinement")
    print("=" * 60)
    
    goal = "Learn Python for Data Science"
    skill_level = "intermediate"
    
    print(f"\n📝 Initial Goal: {goal}")
    print(f"📊 Skill Level: {skill_level}")
    
    # Generate initial path
    print("\n🤖 Generating initial learning path...")
    generator = get_generator()
    initial_path = generator.generate_learning_path(goal, skill_level)
    
    if not initial_path.get("error"):
        print("✅ Initial path generated!\n")
        
        # Refine based on user feedback
        refinement = "Add more practical projects and real-world datasets"
        print(f"🔄 Refinement Request: {refinement}\n")
        
        print("🤖 Refining learning path...")
        refined_path = generator.refine_learning_path(initial_path, refinement)
        
        if not refined_path.get("error"):
            print("✅ Path refined successfully!")
            print(f"\n📋 Updated Overview: {refined_path.get('overview', 'N/A')}")
        else:
            print(f"❌ Refinement failed: {refined_path.get('message')}")
    else:
        print(f"❌ Error generating initial path: {initial_path.get('message')}")


def example_get_alternatives():
    """Example showing how to get alternative resources for a topic"""
    print("\n" + "=" * 60)
    print("Learning Path Generator - Alternative Resources")
    print("=" * 60)
    
    topic = "Neural Networks"
    skill_level = "intermediate"
    
    print(f"\n📝 Topic: {topic}")
    print(f"📊 Skill Level: {skill_level}")
    
    print("\n🤖 Finding alternative resources...")
    generator = get_generator()
    resources = generator.get_resource_alternatives(topic, skill_level)
    
    if not resources.get("error"):
        print("✅ Resources found!\n")
        
        if resources.get("resources"):
            print("📚 Available Resources:")
            for resource in resources["resources"]:
                print(f"\n- {resource.get('title', 'Resource')}")
                print(f"  Type: {resource.get('type', 'N/A')}")
                print(f"  Duration: {resource.get('duration', 'N/A')}")
                print(f"  Difficulty: {resource.get('difficulty', 'N/A')}")
                print(f"  Cost: {resource.get('cost', 'N/A')}")
    else:
        print(f"❌ Error: {resources.get('message')}")


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    # Uncomment to run additional examples:
    # example_with_refinement()
    # example_get_alternatives()
