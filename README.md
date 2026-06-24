# Learning Path Generator

A powerful, AI-driven system that generates personalized learning roadmaps for any topic. Users input their learning goals and current skill level, and the system creates a structured, actionable learning path with:

- **Weekly/Phase-based milestones**
- **Curated resources** (free and paid)
- **Practical hands-on exercises**
- **Estimated timeline** for completion
- **Alternative learning paths** and resources

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd learning_path_generator
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and replace `your_openai_api_key_here` with your actual OpenAI API key
   - Or set it as an environment variable:
     ```bash
     # On Windows (PowerShell)
     $env:OPENAI_API_KEY = "your_api_key_here"
     
     # On macOS/Linux
     export OPENAI_API_KEY="your_api_key_here"
     ```

### Running the Application

#### Option 1: Web UI with Streamlit (Recommended)
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

#### Live Deployment
The app is also deployed at:

https://learning-path-generator-raushanvivek.streamlit.app/

#### Option 2: Command-line Script
```bash
python example_usage.py
```

## 📋 Project Structure

```
learning_path_generator/
├── app.py                          # Main Streamlit application
├── example_usage.py                # Example usage scripts
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # This file
└── src/
    ├── config/
    │   └── config.py              # Configuration management
    ├── utils/
    │   └── utils.py               # Utility functions
    └── llm_generator.py           # Core LLM integration
```

## 🎯 How It Works

### 1. **User Input**
   - Learning goal (e.g., "I want to learn Machine Learning")
   - Current skill level (beginner/intermediate/advanced)

### 2. **AI Processing**
   - Sends structured prompt to OpenAI ChatGPT
   - ChatGPT generates a comprehensive learning path
   - Response is parsed and formatted

### 3. **Structured Output**
   - Milestones (weeks or phases)
   - Topics for each milestone
   - Resources with descriptions and links
   - Practical exercises
   - Estimated duration and effort

### 4. **Interactive Refinement**
   - Users can request modifications
   - System refines the path based on feedback
   - Export to JSON or Markdown

## 💻 API Reference

### LearningPathGenerator Class

#### `generate_learning_path(goal: str, skill_level: str) -> Dict`
Generates a complete learning path for the given goal.

**Parameters:**
- `goal` (str): The learning goal (5-500 characters)
- `skill_level` (str): One of "beginner", "intermediate", "advanced"

**Returns:**
- Dictionary containing the structured learning path with milestones, resources, and metadata

**Example:**
```python
from src.llm_generator import get_generator

generator = get_generator()
path = generator.generate_learning_path(
    goal="Learn Python for Web Development",
    skill_level="beginner"
)
```

#### `refine_learning_path(initial_path: Dict, refinement_request: str) -> Dict`
Refines an existing learning path based on user feedback.

**Parameters:**
- `initial_path` (Dict): The initially generated path
- `refinement_request` (str): User's refinement request

**Returns:**
- Dictionary containing the refined learning path

**Example:**
```python
refined = generator.refine_learning_path(
    initial_path=path,
    refinement_request="Add more frontend frameworks like React"
)
```

#### `get_resource_alternatives(topic: str, skill_level: str, resource_type: str) -> Dict`
Finds alternative resources for a specific topic.

**Parameters:**
- `topic` (str): The topic to find resources for
- `skill_level` (str): One of "beginner", "intermediate", "advanced"
- `resource_type` (str): One of "video", "article", "course", "documentation", "all"

**Returns:**
- Dictionary containing alternative resources

**Example:**
```python
resources = generator.get_resource_alternatives(
    topic="Neural Networks",
    skill_level="intermediate",
    resource_type="video"
)
```

## 🔧 Configuration

All configuration is managed through environment variables in `.env`:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
MODEL_NAME=gpt-4o-mini
MAX_TOKENS=2048
TEMPERATURE=0.7
```

### Configuration Options

- **OPENAI_API_KEY**: Your OpenAI API key (required)
- **MODEL_NAME**: ChatGPT model to use (default: gpt-4o-mini)
- **MAX_TOKENS**: Maximum tokens in responses (default: 2048)
- **TEMPERATURE**: Response creativity (0.0-1.0, default: 0.7)

### Common Issue: Quota Errors
If you see a `429` insufficient quota error, your OpenAI account has run out of free credits. Visit [https://platform.openai.com/usage](https://platform.openai.com/usage) to check your quota, or sign up for a plan to continue using the API.

## 📤 Export Formats

### JSON Export
```json
{
  "goal": "Learn Machine Learning",
  "skill_level": "beginner",
  "total_duration": "3-6 months",
  "milestones": [
    {
      "week_or_phase": "Week 1",
      "title": "Python Basics",
      "topics": ["Variables", "Data Types", "Functions"],
      "resources": [...]
    }
  ]
}
```

### Markdown Export
```markdown
# Learn Machine Learning

**Skill Level:** Beginner
**Duration:** 3-6 months

## Milestones

### Week 1: Python Basics
...
```

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you have a `.env` file in the project root
- Verify the OpenAI API key is set correctly
- Or set it as an environment variable before running

### "Module not found: openai"
- Make sure you've installed dependencies: `pip install -r requirements.txt`
- Verify you're in the correct virtual environment

### Insufficient quota / 429 errors
- Check your OpenAI usage dashboard: https://platform.openai.com/usage
- If your free credits are exhausted, sign up for a paid plan or wait until more quota is available
- Use a smaller model or lower `MAX_TOKENS` to reduce usage

### LLM responses are incomplete or malformed
- Try increasing `MAX_TOKENS` in `.env`
- Adjust `TEMPERATURE` for different response styles
- Check your API rate limits

## 📚 Example Use Cases

### Web Development Beginner
```
Goal: "I want to learn full-stack web development"
Skill Level: Beginner
```

### Data Science Intermediate
```
Goal: "Master machine learning with Python and TensorFlow"
Skill Level: Intermediate
```

### Advanced DevOps
```
Goal: "Learn Kubernetes and container orchestration"
Skill Level: Advanced
```

## 🤝 Contributing

Feel free to fork, modify, or improve this project! Some ideas:

- Add support for other LLM providers (OpenAI, Gemini)
- Create a database to store learning paths
- Add progress tracking functionality
- Implement user accounts and history
- Add interactive quiz generation
- Integrate with real APIs for course recommendations

## 📄 License

This project is open source and available for educational use.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web UI
- Powered by [OpenAI ChatGPT](https://platform.openai.com/)
- Inspired by the need for personalized learning in the AI era

## 📞 Support

If you encounter any issues:

1. Check the **Troubleshooting** section above
2. Review the **example_usage.py** for usage patterns
3. Check your API key and rate limits
4. Ensure all dependencies are installed correctly

---

**Made with ❤️ for learners everywhere** 🌍
