# Replit Setup Guide

## Fixing the lxml.html.clean Import Error

The error you're encountering is due to the `newspaper` library requiring `lxml[html_clean]` instead of just `lxml`. Here's how to fix it:

### Method 1: Run the Setup Script (Recommended)

1. In your Replit shell, run:
   ```bash
   python setup_replit.py
   ```

This script will:
- Install `lxml[html_clean]` properly
- Install all other required dependencies
- Test the imports to ensure everything works

### Method 2: Manual Installation

If the setup script doesn't work, try these commands in the Replit shell:

```bash
# Update pip first
python -m pip install --upgrade pip

# Install lxml with html_clean support
pip install 'lxml[html_clean]'

# If that fails, try this alternative:
pip install lxml
pip install lxml_html_clean

# Install other dependencies
pip install requests>=2.25.1
pip install feedparser>=6.0.0
pip install pandas>=1.3.0
pip install beautifulsoup4>=4.9.3
pip install newspaper3k>=0.2.8
pip install schedule>=1.1.0
pip install openai>=0.27.0
pip install python-dotenv>=0.19.0
```

### Method 3: Using requirements.txt

You can also install from the requirements.txt file:

```bash
pip install -r requirements.txt
```

### Testing the Fix

After installation, test that everything works:

```python
# Test the imports
import newspaper
from newspaper import Article
print("✓ newspaper library imported successfully")
```

### Running the Application

Once the dependencies are installed correctly, you can run:

```bash
python main.py
```

### Troubleshooting

If you still get the lxml error:

1. **Try a different lxml version:**
   ```bash
   pip uninstall lxml
   pip install lxml==4.9.3
   ```

2. **Use an alternative approach:**
   The scraper can work without the `newspaper` library's full functionality. The basic RSS feed parsing and web scraping will still work.

3. **Check Replit's Python version:**
   Make sure you're using Python 3.8+ in your Replit environment.

### Environment Variables

Don't forget to set your `OPENAI_API_KEY` in Replit's Secrets tab if you want to use the summarization feature.

### Files Created

- `requirements.txt` - Standard Python dependencies
- `pyproject.toml` - Alternative dependency specification
- `setup_replit.py` - Automated setup script
- `.replit` - Replit configuration
- `install_dependencies.py` - Alternative installation script 