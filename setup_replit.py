#!/usr/bin/env python3
"""
Setup script for Replit environment
Handles the lxml.html.clean dependency issue
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("Setting up Replit environment for Anti-Aging Scraper...")
    
    # Update pip first
    run_command("python -m pip install --upgrade pip", "Updating pip")
    
    # Install lxml with html_clean support
    print("\nInstalling lxml with html_clean support...")
    success = run_command("pip install 'lxml[html_clean]'", "Installing lxml[html_clean]")
    
    if not success:
        print("Trying alternative lxml installation...")
        run_command("pip install lxml", "Installing lxml")
        run_command("pip install lxml_html_clean", "Installing lxml_html_clean")
    
    # Install other dependencies
    print("\nInstalling other dependencies...")
    dependencies = [
        "requests>=2.25.1",
        "feedparser>=6.0.0",
        "pandas>=1.3.0", 
        "beautifulsoup4>=4.9.3",
        "newspaper3k>=0.2.8",
        "schedule>=1.1.0",
        "openai>=0.27.0",
        "python-dotenv>=0.19.0"
    ]
    
    for dep in dependencies:
        run_command(f"pip install '{dep}'", f"Installing {dep}")
    
    # Test the import
    print("\nTesting imports...")
    try:
        import newspaper
        from newspaper import Article
        print("✓ newspaper library imported successfully")
    except ImportError as e:
        print(f"✗ newspaper import failed: {e}")
        return False
    
    try:
        import lxml.html.clean
        print("✓ lxml.html.clean imported successfully")
    except ImportError as e:
        print(f"✗ lxml.html.clean import failed: {e}")
        print("This might still work with newspaper3k...")
    
    print("\nSetup completed! You can now run: python main.py")
    return True

if __name__ == "__main__":
    main() 