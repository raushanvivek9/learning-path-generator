# 🎓 Quick Start Guide - Learning Path Generator

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Your API Key
Create a `.env` file in the project root:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key from: https://console.anthropic.com

### Step 3: Run the Application
```bash
streamlit run app.py
```

Your browser will open to `http://localhost:8501`

---

## 🎯 Using the Web Interface

1. **Enter your learning goal**
   - Example: "I want to learn React.js for web development"
   
2. **Select your skill level**
   - Beginner / Intermediate / Advanced

3. **Click "Generate Path"**
   - Wait for AI to create your personalized roadmap
   
4. **Review the milestones**
   - Check week-by-week breakdown
   - See recommended resources
   - View practical exercises

5. **Refine if needed**
   - Ask for adjustments (e.g., "Add more projects")
   - System will update the path
   
6. **Export your path**
   - Download as JSON or Markdown

---

## 💻 Using the Python Script

```python
from src.llm_generator import get_generator

# Initialize generator
generator = get_generator()

# Generate learning path
path = generator.generate_learning_path(
    goal="Learn Python for Data Science",
    skill_level="intermediate"
)

# Print the path
import json
print(json.dumps(path, indent=2))
```

Run with: `python example_usage.py`

---

## 🔍 Example Learning Goals

### Beginner
- "I want to learn Python programming from scratch"
- "I want to learn HTML and CSS for web design"
- "I want to understand JavaScript basics"

### Intermediate
- "I want to build a REST API with Python and Flask"
- "I want to learn React.js for web development"
- "I want to master SQL databases"

### Advanced
- "I want to learn Kubernetes and containerization"
- "I want to master system design and architecture"
- "I want to learn cloud computing with AWS"

---

## 📁 Project Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit web application |
| `src/llm_generator.py` | Core LLM integration logic |
| `src/config/config.py` | Configuration management |
| `src/utils/utils.py` | Helper functions |
| `example_usage.py` | Example Python scripts |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variables template |

---

## 🆘 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Run `pip install -r requirements.txt`

### Issue: "ANTHROPIC_API_KEY not found"
**Solution:** 
1. Create `.env` file in project root
2. Add: `ANTHROPIC_API_KEY=your_key_here`
3. Get key from: https://console.anthropic.com

### Issue: Streamlit won't start
**Solution:** 
```bash
# Kill any running Streamlit process
# Then try again with verbose output
streamlit run app.py --logger.level=debug
```

### Issue: Response is too short or incomplete
**Solution:** Increase `MAX_TOKENS` in `.env`:
```env
MAX_TOKENS=4096
```

---

## 📚 What the AI Generates

For each learning path, you get:

✅ **Structured Milestones**
- Week-by-week or phase-wise breakdown
- Clear learning objectives
- Time estimates

✅ **Curated Resources**
- Free YouTube videos
- Articles and documentation
- Paid courses (when valuable)
- Official documentation links

✅ **Practical Exercises**
- Hands-on coding projects
- Real-world applications
- Skill verification tasks

✅ **Timeline & Effort**
- Total duration estimate
- Hours per week required
- Prerequisites

---

## 🚀 Next Steps

1. **Generate a path** for something you want to learn
2. **Review the milestones** and resources
3. **Refine** if you want different focus areas
4. **Export** your path for offline reference
5. **Start learning** from the first milestone!

---

## 💡 Pro Tips

- Be specific in your learning goal (not just "coding", but "Python for Web Development")
- Intermediate learners get more advanced resources
- Use the refinement feature to adjust the path
- Download as JSON to programmatically process the path
- Export as Markdown to share with others or print

---

**Happy Learning!** 🎓✨

For more details, see [README.md](README.md)
