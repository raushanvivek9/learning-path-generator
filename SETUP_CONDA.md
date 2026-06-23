# Setup Instructions (Using Conda)

This guide sets up the Learning Path Generator in a compatible Conda environment.

## Quick Setup

### 1. Activate the Pre-Built Conda Environment

The application has been tested and works in the `ai_intern_lp` Conda environment with Python 3.12:

```bash
conda activate ai_intern_lp
```

If this is your first time, the environment should already exist. To verify:
```bash
conda env list
```

### 2. Run the Application

From the project directory:

```bash
streamlit run app.py
```

By default, Streamlit will start on `http://localhost:8501`.

If port `8501` is in use, specify an alternate port:

```bash
streamlit run app.py --server.port 8502
```

---

## Environment Details

The `ai_intern_lp` environment includes:

- **Python**: 3.12.13
- **Streamlit**: 1.28.1
- **Anthropic SDK**: 0.111.0+ (with Messages API)
- **httpx**: 0.27.0 (compatible with Anthropic SDK)
- **Other dependencies**: pandas, requests, python-dotenv, etc.

---

## Why This Environment?

**Problem**: The system Python (3.13) has an incompatible `numpy` wheel that causes crashes.

**Solution**: Python 3.12 environment avoids the numpy issue and ensures all dependencies work together.

---

## Creating a Fresh Environment (Optional)

If you need to recreate the environment:

```bash
# Create the environment
conda create -y -n ai_intern_lp python=3.12 pip

# Activate it
conda activate ai_intern_lp

# Install dependencies
pip install -r requirements.txt
```

---

## Troubleshooting

### Port Already in Use
If you get "Port 8501 is already in use", use:
```bash
streamlit run app.py --server.port 8502
```

### Missing Environment
If the `ai_intern_lp` environment doesn't exist, create it with the commands above.

### Module Import Errors
Ensure the environment is activated:
```bash
conda activate ai_intern_lp
```

Then verify packages are installed:
```bash
pip show streamlit anthropic
```

---

## API Key Configuration

Set your Anthropic API key before running:

```bash
# Option 1: Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Option 2: Set environment variable
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# Option 3: Export (on macOS/Linux)
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

For more details, see [README.md](README.md).
