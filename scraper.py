import requests
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
from newspaper import Article
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
import re
from config import TARGET_WEBSITES, KEYWORDS, SCRAPING_SETTINGS, OUTPUT_SETTINGS
import os

class AntiAgingScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': SCRAPING_SETTINGS['user_agent']
        })
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(OUTPUT_SETTINGS['log_file']),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def fetch_rss_feed(self, feed_url: str) -> List[Dict]:
        """Fetch articles from RSS feed"""
        try:
            self.logger.info(f"Fetching RSS feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:SCRAPING_SETTINGS['max_articles_per_site']]:
                article = {
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'published_date': entry.get('published', ''),
                    'summary': entry.get('summary', ''),
                    'source': feed.feed.get('title', 'Unknown')
                }
                articles.append(article)
                
            self.logger.info(f"Found {len(articles)} articles from RSS feed")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching RSS feed {feed_url}: {str(e)}")
            return []
    
    def scrape_website(self, url: str, site_name: str) -> List[Dict]:
        """Scrape articles from website directly"""
        try:
            self.logger.info(f"Scraping website: {url}")
            response = self.session.get(url, timeout=SCRAPING_SETTINGS['timeout'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Look for article links (this is a generic approach)
            article_links = soup.find_all('a', href=True)
            
            for link in article_links[:SCRAPING_SETTINGS['max_articles_per_site']]:
                href = link.get('href')
                if href and self._is_article_url(href):
                    article = {
                        'title': link.get_text(strip=True),
                        'url': href if href.startswith('http') else f"{url.rstrip('/')}/{href.lstrip('/')}",
                        'published_date': '',
                        'summary': '',
                        'source': site_name
                    }
                    articles.append(article)
            
            self.logger.info(f"Found {len(articles)} articles from website")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error scraping website {url}: {str(e)}")
            return []
    
    def _is_article_url(self, url: str) -> bool:
        """Check if URL looks like an article"""
        article_patterns = [
            r'/article/',
            r'/news/',
            r'/research/',
            r'/study/',
            r'/publication/',
            r'/paper/',
            r'/journal/'
        ]
        return any(re.search(pattern, url, re.IGNORECASE) for pattern in article_patterns)
    
    def filter_articles_by_keywords(self, articles: List[Dict]) -> List[Dict]:
        """Filter articles based on keywords"""
        filtered_articles = []
        
        for article in articles:
            title = article.get('title', '').lower()
            summary = article.get('summary', '').lower()
            
            # Check if any keyword is in title or summary
            if any(keyword.lower() in title or keyword.lower() in summary 
                   for keyword in KEYWORDS):
                filtered_articles.append(article)
        
        self.logger.info(f"Filtered {len(filtered_articles)} relevant articles from {len(articles)} total")
        return filtered_articles
    
    def extract_article_details(self, article: Dict) -> Dict:
        """Extract detailed information from article URL"""
        try:
            url = article.get('url')
            if not url:
                return article
            
            self.logger.info(f"Extracting details from: {url}")
            
            # Use newspaper3k for article extraction
            news_article = Article(url)
            news_article.download()
            news_article.parse()
            
            # Update article with extracted information
            article.update({
                'title': news_article.title or article.get('title', ''),
                'summary': news_article.text[:500] if news_article.text else article.get('summary', ''),
                'published_date': news_article.publish_date.isoformat() if news_article.publish_date else article.get('published_date', ''),
                'authors': ', '.join(news_article.authors) if news_article.authors else '',
                'keywords': ', '.join(news_article.keywords) if news_article.keywords else ''
            })
            
            time.sleep(SCRAPING_SETTINGS['request_delay'])
            
        except Exception as e:
            self.logger.error(f"Error extracting details from {url}: {str(e)}")
        
        return article
    
    def scrape_all_sources(self) -> List[Dict]:
        """Scrape all configured sources"""
        all_articles = []
        
        for website in TARGET_WEBSITES:
            self.logger.info(f"Processing {website['name']}")
            
            if website['type'] == 'rss':
                articles = self.fetch_rss_feed(website['rss_feed'])
            elif website['type'] == 'scrape':
                articles = self.scrape_website(website['url'], website['name'])
            elif website['type'] == 'search':
                # For search-based sites, we'll implement a search scraper
                articles = self.scrape_search_results(website['search_url'], website['name'])
            else:
                continue
            
            # Filter articles by keywords
            filtered_articles = self.filter_articles_by_keywords(articles)
            
            # Extract detailed information for filtered articles
            for article in filtered_articles:
                detailed_article = self.extract_article_details(article)
                all_articles.append(detailed_article)
            
            time.sleep(SCRAPING_SETTINGS['request_delay'])
        
        return all_articles
    
    def scrape_search_results(self, search_url: str, site_name: str) -> List[Dict]:
        """Scrape search results from sites like ScienceDirect"""
        try:
            self.logger.info(f"Scraping search results: {search_url}")
            response = self.session.get(search_url, timeout=SCRAPING_SETTINGS['timeout'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Look for search result links
            result_links = soup.find_all('a', href=True)
            
            for link in result_links[:SCRAPING_SETTINGS['max_articles_per_site']]:
                href = link.get('href')
                if href and '/science/article/' in href:
                    article = {
                        'title': link.get_text(strip=True),
                        'url': href if href.startswith('http') else f"https://www.sciencedirect.com{href}",
                        'published_date': '',
                        'summary': '',
                        'source': site_name
                    }
                    articles.append(article)
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error scraping search results {search_url}: {str(e)}")
            return []
    
    def save_results(self, articles: List[Dict]):
        """Save results to CSV file"""
        if not articles:
            self.logger.warning("No articles to save")
            return
        
        try:
            df = pd.DataFrame(articles)
            
            # Add timestamp
            df['scraped_date'] = datetime.now().isoformat()
            
            # Get absolute paths
            output_path = os.path.abspath(OUTPUT_SETTINGS['output_file'])
            backup_path = os.path.abspath(OUTPUT_SETTINGS['backup_file'])
            
            self.logger.info(f"Saving {len(articles)} articles to {output_path}")
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            self.logger.info(f"Successfully saved {len(articles)} articles to {output_path}")
            
            # Create backup
            df.to_csv(backup_path, index=False)
            self.logger.info(f"Created backup at {backup_path}")
            
            # Verify file was created
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                self.logger.info(f"File exists with size: {file_size} bytes")
            else:
                self.logger.error(f"File was not created at {output_path}")
                
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")
            raise
    
    def run(self):
        """Main method to run the scraper"""
        self.logger.info("Starting anti-aging research scraper")
        
        try:
            articles = self.scrape_all_sources()
            self.save_results(articles)
            
            self.logger.info(f"Scraping completed. Found {len(articles)} relevant articles")
            
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")

if __name__ == "__main__":
    scraper = AntiAgingScraper()
    scraper.run() 