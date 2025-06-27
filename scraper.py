import requests
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
from newspaper import Article
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
from config import TARGET_WEBSITES, TITLE_KEYWORDS, CONTENT_KEYWORDS, SCRAPING_SETTINGS, OUTPUT_SETTINGS
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
        """Filter articles based on keywords with strict title filtering and date filtering"""
        filtered_articles = []
        
        # Calculate date threshold (30 days ago)
        date_threshold = datetime.now() - timedelta(days=SCRAPING_SETTINGS.get('date_filter_days', 30))
        
        for article in articles:
            title = article.get('title', '').lower()
            summary = article.get('summary', '').lower()
            published_date = article.get('published_date', '')
            
            # DATE FILTERING - Only include recent articles (last 30 days)
            if SCRAPING_SETTINGS.get('require_recent_articles', True) and published_date:
                try:
                    # Try to parse the published date
                    if isinstance(published_date, str):
                        # Handle different date formats
                        if 'T' in published_date:
                            # ISO format: 2024-01-15T10:30:00
                            article_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                        else:
                            # Simple date format: 2024-01-15
                            article_date = datetime.strptime(published_date[:10], '%Y-%m-%d')
                        
                        if article_date < date_threshold:
                            self.logger.info(f"Article '{title[:50]}...' filtered out (too old: {published_date})")
                            continue
                except Exception as e:
                    self.logger.warning(f"Could not parse date '{published_date}' for article '{title[:50]}...': {str(e)}")
                    # If we can't parse the date, include the article (don't filter out)
            
            # STRICT TITLE FILTERING - Only include articles with title keywords
            if SCRAPING_SETTINGS.get('strict_title_filtering', True):
                title_matches = any(keyword.lower() in title for keyword in TITLE_KEYWORDS)
                
                if not title_matches:
                    # Skip articles that don't have required title keywords
                    continue
                
                self.logger.info(f"Article '{title[:50]}...' passed title filter")
            
            # Additional content filtering (optional)
            content_matches = any(keyword.lower() in title or keyword.lower() in summary 
                                 for keyword in CONTENT_KEYWORDS)
            
            if content_matches:
                filtered_articles.append(article)
        
        self.logger.info(f"Filtered {len(filtered_articles)} relevant articles from {len(articles)} total (strict title filtering: {SCRAPING_SETTINGS.get('strict_title_filtering', True)}, date filtering: {SCRAPING_SETTINGS.get('require_recent_articles', True)})")
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
            # Clean the articles data before creating DataFrame
            cleaned_articles = []
            for article in articles:
                cleaned_article = {}
                for key, value in article.items():
                    # Handle None, NaN, and empty values
                    if value is None or (isinstance(value, str) and value.lower() in ['nan', 'none', '']):
                        cleaned_article[key] = ''
                    elif isinstance(value, (int, float)) and (pd.isna(value) or str(value) == 'nan'):
                        cleaned_article[key] = ''
                    else:
                        cleaned_article[key] = str(value) if value is not None else ''
                cleaned_articles.append(cleaned_article)
            
            df = pd.DataFrame(cleaned_articles)
            
            # Add timestamp
            df['scraped_date'] = datetime.now().isoformat()
            
            # Get absolute paths
            output_path = os.path.abspath(OUTPUT_SETTINGS['output_file'])
            backup_path = os.path.abspath(OUTPUT_SETTINGS['backup_file'])
            
            self.logger.info(f"Saving {len(cleaned_articles)} articles to {output_path}")
            
            # Save to CSV
            df.to_csv(output_path, index=False)
            self.logger.info(f"Successfully saved {len(cleaned_articles)} articles to {output_path}")
            
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