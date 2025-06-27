from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
from datetime import datetime
import threading
import time
from scraper import AntiAgingScraper
from summarizer import Summarizer
from free_summarizer import FreeSummarizer
from config import OUTPUT_SETTINGS
import logging
import json

app = Flask(__name__)

# Global variable to track scraping status
scraping_status = {
    'is_running': False,
    'last_run': None,
    'articles_count': 0,
    'error': None
}

def run_scraper_background():
    """Run scraper in background thread"""
    global scraping_status
    
    try:
        logging.info("Background scraper started")
        scraping_status['is_running'] = True
        scraping_status['error'] = None
        
        logging.info("Initializing AntiAgingScraper")
        scraper = AntiAgingScraper()
        
        logging.info("Starting scrape_all_sources")
        articles = scraper.scrape_all_sources()
        logging.info(f"Scraping completed, found {len(articles)} articles")
        
        # Add summarization - use free summarizer by default
        if articles:
            logging.info("Starting summarization process")
            # Try OpenAI first if available, otherwise use free summarizer
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key:
                try:
                    logging.info("Using OpenAI summarizer")
                    summarizer = Summarizer(openai_key)
                    for article in articles:
                        if 'summary' in article and article['summary']:
                            article['summary'] = summarizer.summarize(article['summary'])
                except Exception as e:
                    logging.warning(f"OpenAI summarization failed, using free summarizer: {str(e)}")
                    free_summarizer = FreeSummarizer()
                    for article in articles:
                        if 'summary' in article and article['summary']:
                            article['summary'] = free_summarizer.summarize(article['summary'])
            else:
                logging.info("Using free summarizer")
                # Use free summarizer
                free_summarizer = FreeSummarizer()
                for article in articles:
                    if 'summary' in article and article['summary']:
                        article['summary'] = free_summarizer.summarize(article['summary'])
        
        logging.info("Saving results")
        scraper.save_results(articles)
        
        scraping_status['last_run'] = datetime.now().isoformat()
        scraping_status['articles_count'] = len(articles)
        scraping_status['is_running'] = False
        
        logging.info(f"Background scraper completed successfully. Articles: {len(articles)}")
        
    except Exception as e:
        logging.error(f"Error in background scraper: {str(e)}")
        import traceback
        logging.error(f"Background scraper traceback: {traceback.format_exc()}")
        scraping_status['error'] = str(e)
        scraping_status['is_running'] = False

@app.route('/')
def dashboard():
    """Main dashboard page"""
    try:
        # Load latest data
        if os.path.exists(OUTPUT_SETTINGS['output_file']):
            df = pd.read_csv(OUTPUT_SETTINGS['output_file'])
            articles = df.to_dict('records')
        else:
            articles = []
        
        return render_template('dashboard.html', 
                             articles=articles, 
                             status=scraping_status)
    except Exception as e:
        return render_template('dashboard.html', 
                             articles=[], 
                             status=scraping_status,
                             error=str(e))

@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    """API endpoint to trigger scraping"""
    try:
        logging.info("Scrape endpoint called")
        
        if scraping_status['is_running']:
            logging.info("Scraping already in progress")
            return jsonify({'status': 'error', 'message': 'Scraping already in progress'})
        
        logging.info("Starting scraping in background thread")
        
        # Start scraping in background thread
        thread = threading.Thread(target=run_scraper_background)
        thread.daemon = True
        thread.start()
        
        logging.info("Scraping thread started successfully")
        return jsonify({'status': 'success', 'message': 'Scraping started'})
        
    except Exception as e:
        logging.error(f"Error in trigger_scrape: {str(e)}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'})

@app.route('/api/status')
def get_status():
    """API endpoint to get scraping status"""
    return jsonify(scraping_status)

@app.route('/api/articles')
def get_articles():
    """API endpoint to get articles data"""
    try:
        output_file = OUTPUT_SETTINGS['output_file']
        logging.info(f"Checking for articles file: {output_file}")
        logging.info(f"Current working directory: {os.getcwd()}")
        logging.info(f"File exists: {os.path.exists(output_file)}")
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            logging.info(f"File size: {file_size} bytes")
            
            df = pd.read_csv(output_file)
            logging.info(f"DataFrame shape: {df.shape}")
            logging.info(f"DataFrame columns: {list(df.columns)}")
            
            # Clean the data before converting to JSON
            df = df.replace({pd.NA: None, pd.NaT: None})
            df = df.fillna('')  # Replace NaN with empty strings
            
            # Convert to records and clean each article
            articles = df.to_dict('records')
            cleaned_articles = []
            
            for article in articles:
                cleaned_article = {}
                for key, value in article.items():
                    # Handle different types of invalid values
                    if pd.isna(value) or value == 'nan' or value == 'NaN' or value == 'None':
                        cleaned_article[key] = ''
                    elif isinstance(value, (int, float)) and (pd.isna(value) or str(value) == 'nan'):
                        cleaned_article[key] = ''
                    else:
                        cleaned_article[key] = str(value) if value is not None else ''
                cleaned_articles.append(cleaned_article)
            
            logging.info(f"Converted to {len(cleaned_articles)} articles")
            
            # Log first few articles for debugging
            if cleaned_articles:
                logging.info(f"First article keys: {list(cleaned_articles[0].keys())}")
                logging.info(f"First article title: {cleaned_articles[0].get('title', 'NO_TITLE')}")
            
            return jsonify(cleaned_articles)
        else:
            logging.info(f"Output file {output_file} does not exist")
            return jsonify([])
    except Exception as e:
        logging.error(f"Error loading articles: {str(e)}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)})

@app.route('/api/debug')
def debug_info():
    """Debug endpoint to check file system and data"""
    try:
        import os
        import glob
        
        debug_info = {
            'current_directory': os.getcwd(),
            'files_in_directory': os.listdir('.'),
            'csv_files': glob.glob('*.csv'),
            'output_file': OUTPUT_SETTINGS['output_file'],
            'output_file_exists': os.path.exists(OUTPUT_SETTINGS['output_file']),
            'backup_file_exists': os.path.exists(OUTPUT_SETTINGS['backup_file']),
            'scraping_status': scraping_status
        }
        
        if os.path.exists(OUTPUT_SETTINGS['output_file']):
            file_size = os.path.getsize(OUTPUT_SETTINGS['output_file'])
            debug_info['output_file_size'] = file_size
            
            try:
                df = pd.read_csv(OUTPUT_SETTINGS['output_file'])
                debug_info['dataframe_shape'] = df.shape
                debug_info['dataframe_columns'] = list(df.columns)
                
                # Clean the data before showing first row
                df_clean = df.replace({pd.NA: None, pd.NaT: None})
                df_clean = df_clean.fillna('')
                
                if len(df_clean) > 0:
                    first_row = df_clean.iloc[0].to_dict()
                    # Convert all values to strings to avoid JSON issues
                    cleaned_first_row = {}
                    for key, value in first_row.items():
                        if pd.isna(value) or value == 'nan' or value == 'NaN' or value == 'None':
                            cleaned_first_row[key] = ''
                        else:
                            cleaned_first_row[key] = str(value) if value is not None else ''
                    debug_info['first_row'] = cleaned_first_row
                else:
                    debug_info['first_row'] = None
            except Exception as e:
                debug_info['csv_read_error'] = str(e)
        
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({'error': str(e)})

def schedule_daily_scrape():
    """Background function to schedule daily scraping"""
    while True:
        now = datetime.now()
        # Run at 7 AM daily
        if now.hour == 7 and now.minute == 0:
            if not scraping_status['is_running']:
                thread = threading.Thread(target=run_scraper_background)
                thread.daemon = True
                thread.start()
        time.sleep(60)  # Check every minute

@app.route('/api/test')
def test_imports():
    """Test endpoint to verify all imports work"""
    try:
        # Test scraper import
        scraper = AntiAgingScraper()
        scraper_status = "✓ AntiAgingScraper imported successfully"
        
        # Test summarizer imports
        try:
            summarizer = Summarizer("test")
            summarizer_status = "✓ Summarizer imported successfully"
        except Exception as e:
            summarizer_status = f"⚠ Summarizer import issue: {str(e)}"
        
        try:
            free_summarizer = FreeSummarizer()
            free_summarizer_status = "✓ FreeSummarizer imported successfully"
        except Exception as e:
            free_summarizer_status = f"⚠ FreeSummarizer import issue: {str(e)}"
        
        return jsonify({
            'status': 'success',
            'scraper': scraper_status,
            'summarizer': summarizer_status,
            'free_summarizer': free_summarizer_status,
            'python_version': os.sys.version,
            'working_directory': os.getcwd()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        })

if __name__ == '__main__':
    # Start background scheduler
    scheduler_thread = threading.Thread(target=schedule_daily_scrape)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 