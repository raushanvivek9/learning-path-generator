"""
Main Streamlit application for the Learning Path Generator.
This is the entry point for the web UI.
"""

import streamlit as st
import json
from datetime import datetime
from src.config.config import Config
from src.utils.utils import (
    validate_learning_goal,
    validate_skill_level,
    format_milestone_for_display
)
from src.llm_generator import get_generator


# Configure Streamlit page
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="🎓",
    layout=Config.PAGE_LAYOUT,
    initial_sidebar_state=Config.INITIAL_SIDEBAR_STATE
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Global page style */
    .stApp {
        background: radial-gradient(circle at top left, #2d1f56 0%, transparent 35%),
                    radial-gradient(circle at top right, #3f6cff 0%, transparent 30%),
                    radial-gradient(circle at bottom left, #1f4a9a 0%, transparent 28%),
                    linear-gradient(180deg, #0b1120 0%, #111a33 100%);
        color: #f5f7ff;
    }

    .css-12oz5g7.egzxvld0 {
        padding-top: 0rem;
    }

    .main-header {
        color: #ffffff;
        font-size: 3.4rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
        line-height: 1.05;
    }

    .hero-subtitle {
        color: #d6dbff;
        font-size: 1.15rem;
        max-width: 760px;
        margin-bottom: 1.5rem;
    }

    .hero-card,
    .section-card,
    .result-card,
    .panel-card {
        background: rgba(19, 29, 54, 0.82);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 70px rgba(0, 0, 0, 0.20);
        border-radius: 32px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(18px);
    }

    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.7rem 1rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.08);
        color: #c9d4ff;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.2rem;
        min-height: 120px;
    }

    .feature-card h4 {
        margin: 0 0 0.65rem 0;
        color: #ffffff;
    }

    .feature-card p {
        margin: 0;
        color: #bec8ff;
        line-height: 1.6;
    }

    .input-card {
        background: rgba(23, 36, 67, 0.96);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
    }

    .result-card {
        padding: 1.75rem;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1rem;
        text-align: center;
        color: #e6ebff;
    }

    .metric-card .stMetricLabel {
        color: #b9c1ff;
    }

    .metric-card .stMetricValue {
        color: #ffffff;
        font-weight: 700;
    }

    .stButton>button {
        background: linear-gradient(90deg, #7c5cff 0%, #4dabf7 100%);
        color: #fff;
        font-size: 1rem;
        padding: 0.95rem 1.2rem;
        border-radius: 999px;
        border: none;
        box-shadow: 0 18px 40px rgba(124, 92, 255, 0.22);
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        background: linear-gradient(90deg, #8a66ff 0%, #61b4ff 100%);
    }

    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div>div {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #f0f6ff !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 18px !important;
    }

    .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #f7f9ff;
    }

    .stDivider {
        border-color: rgba(255, 255, 255, 0.12) !important;
    }

    .error-box, .warning-box, .success-box {
        border-left-width: 0px !important;
        padding: 1.25rem !important;
        border-radius: 24px !important;
    }

    .success-box {
        background: rgba(33, 105, 62, 0.18);
        color: #d9ffe5;
        border: 1px solid rgba(57, 191, 102, 0.25);
    }

    .error-box {
        background: rgba(180, 35, 55, 0.18);
        color: #ffdbe0;
        border: 1px solid rgba(234, 93, 118, 0.25);
    }

    .warning-box {
        background: rgba(180, 149, 35, 0.18);
        color: #fff4d6;
        border: 1px solid rgba(242, 196, 89, 0.25);
    }

    .stSidebar {
        background: rgba(7, 15, 35, 0.92);
        border-left: 1px solid rgba(255, 255, 255, 0.08);
        color: #f5f5ff;
    }

    .stSidebar .stMarkdown h3 {
        color: #ffffff;
    }

    .sidebar-content {
        padding: 0 1rem 1rem 1rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "learning_path" not in st.session_state:
        st.session_state.learning_path = None
    if "generated" not in st.session_state:
        st.session_state.generated = False
    if "goal" not in st.session_state:
        st.session_state.goal = ""
    if "skill_level" not in st.session_state:
        st.session_state.skill_level = "beginner"
    if "loading" not in st.session_state:
        st.session_state.loading = False


def display_header():
    """Display the main header and introduction"""
    st.markdown("""
    <div class="hero-card">
        <div style="display:grid; gap:1.2rem;">
            <div class="hero-pill">AI Learning Roadmaps</div>
            <h1 class="main-header">Build a smarter study plan in seconds.</h1>
            <div class="hero-subtitle">
                Enter your learning goal and current experience level, then let the AI generate a tailored roadmap with milestones, resources, and practical exercises.
            </div>
            <div style="display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.75rem;">
                <div class="feature-card">
                    <h4>Fast Setup</h4>
                    <p>Generate a complete study plan in under a minute.</p>
                </div>
                <div class="feature-card">
                    <h4>Personalized</h4>
                    <p>Roadmaps adapt to your level, goals, and learning preferences.</p>
                </div>
                <div class="feature-card">
                    <h4>Practical</h4>
                    <p>Includes projects, resources, and real-world skills.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_input_section():
    """Display the input form for user's learning goal"""
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('### 📝 Start Your Learning Journey')

    col1, col2 = st.columns([3, 1])
    
    with col1:
        goal = st.text_area(
            "Learning Goal",
            placeholder="E.g., 'I want to learn Machine Learning' or 'I want to become a full-stack web developer'",
            height=130,
            key="goal_input"
        )
    
    with col2:
        skill_level = st.selectbox(
            "Current Skill Level",
            ["beginner", "intermediate", "advanced"],
            key="skill_level_input"
        )
        st.markdown("<div style='margin-top: 1rem; color: #c7d3ff;'>Select your experience level to tailor the roadmap.</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    return goal, skill_level


def validate_inputs(goal: str, skill_level: str) -> tuple[bool, str]:
    """
    Validate user inputs
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    is_valid, error_msg = validate_learning_goal(goal)
    if not is_valid:
        return False, error_msg
    
    if not validate_skill_level(skill_level):
        return False, "Please select a valid skill level"
    
    return True, ""


def display_loading_state():
    """Display a loading message while generating the path"""
    with st.spinner("🤖 Generating your personalized learning path... This may take a moment."):
        st.info("Our AI is crafting a custom roadmap just for you. Please wait...")
        return True


def display_learning_path(learning_path: dict):
    """Display the generated learning path"""
    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    # Check for errors
    if learning_path.get("error"):
        st.markdown(
            f'<div class="error-box"><strong>Error:</strong> {learning_path.get("message", "Unknown error")}</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    if learning_path.get("fallback"):
        fallback_message = learning_path.get(
            "provider_error",
            "AI generation is unavailable, so an offline fallback path was created."
        )
        st.markdown(
            f'<div class="warning-box">{fallback_message}</div>',
            unsafe_allow_html=True
        )

    # Display success message
    generation_label = "created" if learning_path.get("fallback") else "generated"
    st.markdown(
        f'<div class="success-box">Your learning path for <strong>"{learning_path.get("goal", "")}"</strong> has been {generation_label}!</div>',
        unsafe_allow_html=True
    )
    
    # Display overview if available
    if learning_path.get("overview"):
        with st.expander("📋 Path Overview", expanded=True):
            st.write(learning_path["overview"])
    
    # Display basic info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Skill Level", learning_path.get("skill_level", "N/A").title())
    with col2:
        st.metric("Total Duration", learning_path.get("total_duration", "N/A"))
    with col3:
        st.metric("Hours per Week", learning_path.get("estimated_hours_per_week", "N/A"))
    
    st.divider()
    
    # Display milestones
    if learning_path.get("milestones"):
        st.subheader("📚 Learning Milestones")
        
        for idx, milestone in enumerate(learning_path["milestones"], 1):
            with st.expander(
                f"🎯 {milestone.get('week_or_phase', f'Phase {idx}')}: {milestone.get('title', 'Milestone')}",
                expanded=(idx == 1)  # First milestone expanded by default
            ):
                # Description
                if milestone.get("description"):
                    st.write(f"**What you'll learn:** {milestone['description']}")
                
                # Topics
                if milestone.get("topics"):
                    st.write("**Topics to cover:**")
                    for topic in milestone["topics"]:
                        st.write(f"• {topic}")
                
                # Resources
                if milestone.get("resources"):
                    st.write("**Resources:**")
                    for resource in milestone["resources"]:
                        resource_info = f"[{resource.get('title', 'Resource')}]({resource.get('url', '#')})"
                        meta = f"_{resource.get('type', 'resource').title()} • {resource.get('duration', 'TBD')}_"
                        st.write(f"• {resource_info} — {meta}")
                
                # Practical exercise
                if milestone.get("practical_exercise"):
                    st.info(f"🛠️ **Hands-on Exercise:** {milestone['practical_exercise']}")
    
    st.divider()
    
    # Display prerequisites
    if learning_path.get("prerequisites"):
        with st.expander("📌 Prerequisites"):
            for prereq in learning_path["prerequisites"]:
                st.write(f"• {prereq}")
    
    # Display tips
    if learning_path.get("tips_and_best_practices"):
        with st.expander("💡 Tips & Best Practices"):
            for tip in learning_path["tips_and_best_practices"]:
                st.write(f"• {tip}")
    
    # Display alternative resources
    if learning_path.get("alternative_resources"):
        with st.expander("🔄 Alternative Resources"):
            st.write(learning_path["alternative_resources"])
    
    # Export options
    st.divider()
    st.subheader("💾 Export & Share")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON export
        json_str = json.dumps(learning_path, indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name=f"learning_path_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # Markdown export
        markdown_str = _generate_markdown_export(learning_path)
        st.download_button(
            label="📥 Download as Markdown",
            data=markdown_str,
            file_name=f"learning_path_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

    st.markdown('</div>', unsafe_allow_html=True)


def _generate_markdown_export(learning_path: dict) -> str:
    """Generate markdown format of the learning path"""
    md = f"# {learning_path.get('goal', 'Learning Path')}\n\n"
    md += f"**Skill Level:** {learning_path.get('skill_level', 'N/A')}\n"
    md += f"**Duration:** {learning_path.get('total_duration', 'N/A')}\n"
    md += f"**Hours per Week:** {learning_path.get('estimated_hours_per_week', 'N/A')}\n\n"
    
    if learning_path.get("overview"):
        md += f"## Overview\n{learning_path['overview']}\n\n"
    
    if learning_path.get("milestones"):
        md += "## Milestones\n\n"
        for idx, milestone in enumerate(learning_path["milestones"], 1):
            md += f"### {milestone.get('week_or_phase', f'Phase {idx}')}: {milestone.get('title', 'Milestone')}\n\n"
            if milestone.get("description"):
                md += f"{milestone['description']}\n\n"
            if milestone.get("topics"):
                md += "**Topics:**\n"
                for topic in milestone["topics"]:
                    md += f"- {topic}\n"
                md += "\n"
            if milestone.get("resources"):
                md += "**Resources:**\n"
                for resource in milestone["resources"]:
                    md += f"- [{resource.get('title', 'Resource')}]({resource.get('url', '#')}) - {resource.get('type', 'resource')}\n"
                md += "\n"
            if milestone.get("practical_exercise"):
                md += f"**Exercise:** {milestone['practical_exercise']}\n\n"
    
    return md


def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    
    # Input section
    goal, skill_level = display_input_section()
    
    # Generate button
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_button = st.button(
            "✨ Generate Path",
            type="primary",
            use_container_width=True
        )
    
    # Process button click
    if generate_button:
        # Validate inputs
        is_valid, error_msg = validate_inputs(goal, skill_level)
        
        if not is_valid:
            st.error(f"❌ {error_msg}")
        else:
            # Generate learning path
            with st.spinner("🤖 Generating your personalized learning path..."):
                generator = get_generator()
                learning_path = generator.generate_learning_path(goal, skill_level)
                
                st.session_state.learning_path = learning_path
                st.session_state.generated = True
                st.session_state.goal = goal
                st.session_state.skill_level = skill_level
            
    
    # Display generated path if available
    if st.session_state.generated and st.session_state.learning_path:
        display_learning_path(st.session_state.learning_path)
        
        # Refinement section
        st.divider()
        st.subheader("🔄 Refine Your Path")
        refinement_text = st.text_area(
            "How would you like to modify the learning path?",
            placeholder="E.g., 'Add more practical projects' or 'Focus more on Python programming'",
            height=80,
            key="refinement_input"
        )
        
        if st.button("🔧 Refine Path", use_container_width=True):
            if not refinement_text.strip():
                st.warning("Please enter a refinement request")
            else:
                with st.spinner("🤖 Refining your learning path..."):
                    generator = get_generator()
                    refined_path = generator.refine_learning_path(
                        st.session_state.learning_path,
                        refinement_text
                    )
                    st.session_state.learning_path = refined_path
    
    # Sidebar information
    with st.sidebar:
        st.markdown("### 📖 About This Tool")
        st.info(
            """
            This **Learning Path Generator** uses AI to create personalized 
            learning roadmaps. It takes into account your:
            - 🎯 Learning goal
            - 📊 Current skill level
            
            And generates:
            - Week-by-week milestones
            - Real, curated resources
            - Hands-on exercises
            - Estimated timeline
            """
        )
        
        st.markdown("### 🚀 How to Use")
        st.markdown(
            """
            1. **Enter your goal** - Be specific! (e.g., "Learn React" instead of "Learn coding")
            2. **Select skill level** - Choose beginner, intermediate, or advanced
            3. **Click Generate** - Wait for AI to create your path
            4. **Review milestones** - Check topics and resources for each week
            5. **Refine** - Ask for adjustments if needed
            6. **Download** - Export as JSON or Markdown
            """
        )
        
        st.divider()
        st.markdown("### ℹ️ Version Info")
        st.caption(f"**{Config.APP_NAME}** v{Config.APP_VERSION}")
        st.caption(f"Powered by {Config.MODEL_NAME}")


if __name__ == "__main__":
    main()
