import schedule
import time
import os
from scraper import AntiAgingScraper
from summarizer import Summarizer

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Set this in your environment

# Set to True to enable summarization
ENABLE_SUMMARIZATION = True if OPENAI_API_KEY else False

def run_scraper():
    scraper = AntiAgingScraper()
    articles = scraper.scrape_all_sources()

    if ENABLE_SUMMARIZATION and articles:
        summarizer = Summarizer(OPENAI_API_KEY)
        for article in articles:
            if 'summary' in article and article['summary']:
                article['summary'] = summarizer.summarize(article['summary'])

    scraper.save_results(articles)

if __name__ == "__main__":
    # Run once immediately
    run_scraper()
    # Schedule to run daily at 7am
    schedule.every().day.at("07:00").do(run_scraper)
    print("Scheduled scraper to run daily at 7:00 AM.")
    while True:
        schedule.run_pending()
        time.sleep(60) 