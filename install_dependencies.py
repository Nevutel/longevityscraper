#!/usr/bin/env python3
"""
Installation script for dependencies, especially handling lxml[html_clean] requirement
"""
import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False
    return True

def main():
    print("Installing dependencies...")
    
    # First install lxml with html_clean support
    print("Installing lxml[html_clean]...")
    if not install_package("lxml[html_clean]"):
        print("Trying alternative installation...")
        install_package("lxml")
        install_package("lxml_html_clean")
    
    # Install other dependencies
    packages = [
        "requests>=2.25.1",
        "feedparser>=6.0.0", 
        "pandas>=1.3.0",
        "beautifulsoup4>=4.9.3",
        "newspaper3k>=0.2.8",
        "schedule>=1.1.0",
        "openai>=0.27.0",
        "python-dotenv>=0.19.0"
    ]
    
    for package in packages:
        install_package(package)
    
    print("\nDependencies installation completed!")

if __name__ == "__main__":
    main() 