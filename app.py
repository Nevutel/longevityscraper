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
    
    scraping_status['is_running'] = True
    scraping_status['error'] = None
    
    try:
        scraper = AntiAgingScraper()
        articles = scraper.scrape_all_sources()
        
        # Add summarization - use free summarizer by default
        if articles:
            # Try OpenAI first if available, otherwise use free summarizer
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key:
                try:
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
                # Use free summarizer
                free_summarizer = FreeSummarizer()
                for article in articles:
                    if 'summary' in article and article['summary']:
                        article['summary'] = free_summarizer.summarize(article['summary'])
        
        scraper.save_results(articles)
        
        scraping_status['last_run'] = datetime.now().isoformat()
        scraping_status['articles_count'] = len(articles)
        scraping_status['is_running'] = False
        
    except Exception as e:
        scraping_status['error'] = str(e)
        scraping_status['is_running'] = False
        logging.error(f"Scraping error: {str(e)}")

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
    if scraping_status['is_running']:
        return jsonify({'status': 'error', 'message': 'Scraping already in progress'})
    
    # Start scraping in background thread
    thread = threading.Thread(target=run_scraper_background)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'success', 'message': 'Scraping started'})

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
            
            articles = df.to_dict('records')
            logging.info(f"Converted to {len(articles)} articles")
            
            # Log first few articles for debugging
            if articles:
                logging.info(f"First article keys: {list(articles[0].keys())}")
                logging.info(f"First article title: {articles[0].get('title', 'NO_TITLE')}")
            
            return jsonify(articles)
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
                debug_info['first_row'] = df.iloc[0].to_dict() if len(df) > 0 else None
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

if __name__ == '__main__':
    # Start background scheduler
    scheduler_thread = threading.Thread(target=schedule_daily_scrape)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 