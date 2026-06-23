#!/usr/bin/env python3
"""
Test script to verify the Learning Path Generator is set up correctly.
Run this to diagnose any configuration issues.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - FAIL (requires 3.8+)")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print("\n🔍 Checking dependencies...")
    required_packages = {
        'streamlit': 'Streamlit (UI framework)',
        'anthropic': 'Anthropic (Claude API)',
        'dotenv': 'python-dotenv (Environment variables)',
        'requests': 'Requests (HTTP library)',
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {description} - OK")
        except ImportError:
            print(f"   ❌ {description} - MISSING")
            all_installed = False
    
    if not all_installed:
        print("\n   💡 Install missing packages with:")
        print("      pip install -r requirements.txt")
    
    return all_installed


def check_env_file():
    """Check if .env file exists and has API key"""
    print("\n🔍 Checking environment configuration...")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("   ❌ .env file not found")
        print("   💡 Create one using: cp .env.example .env")
        return False
    
    print("   ✅ .env file exists")
    
    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'your_anthropic_api_key_here':
        print("   ❌ ANTHROPIC_API_KEY not configured")
        print("   💡 Edit .env and add your API key from https://console.anthropic.com")
        return False
    
    print("   ✅ ANTHROPIC_API_KEY configured")
    return True


def check_project_structure():
    """Check if all required directories and files exist"""
    print("\n🔍 Checking project structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'src/llm_generator.py',
        'src/config/config.py',
        'src/utils/utils.py',
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist


def test_llm_integration():
    """Test if LLM integration works"""
    print("\n🔍 Testing LLM integration...")
    
    try:
        from src.llm_generator import get_generator
        from src.config.config import Config
        
        print("   ✅ Imports successful")
        
        if not Config.ANTHROPIC_API_KEY:
            print("   ❌ API key not configured")
            return False
        
        print("   ✅ API key loaded")
        
        # Try to create a generator (doesn't make API call)
        generator = get_generator()
        print("   ✅ Generator initialized")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False


def run_all_checks():
    """Run all diagnostic checks"""
    print("\n" + "="*60)
    print("Learning Path Generator - Setup Verification")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Environment Configuration", check_env_file),
        ("LLM Integration", test_llm_integration),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error in {name}: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! You're ready to go!")
        print("\nTo start the application, run:")
        print("   streamlit run app.py")
        return True
    else:
        print("\n⚠️  Some checks failed. See above for details.")
        return False


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    success = run_all_checks()
    sys.exit(0 if success else 1)
