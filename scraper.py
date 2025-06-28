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
                # Use getattr for safer attribute access
                article = {
                    'title': getattr(entry, 'title', ''),
                    'url': getattr(entry, 'link', ''),
                    'published_date': getattr(entry, 'published', ''),
                    'summary': getattr(entry, 'summary', ''),
                    'source': getattr(feed.feed, 'title', 'Unknown')
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
                # Use getattr for safer attribute access
                href = getattr(link, 'href', '')
                
                if isinstance(href, str) and self._is_article_url(href):
                    article = {
                        'title': link.get_text(strip=True) if hasattr(link, 'get_text') else '',
                        'url': href if href.startswith('http') else f"{url.rstrip('/')}/{href.lstrip('/')}" if isinstance(href, str) else '',
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
        """Filter articles based on keywords with intelligent content-based filtering"""
        filtered_articles = []
        
        # Get target year for filtering
        target_year = SCRAPING_SETTINGS.get('date_filter_year', 2025)
        
        for article in articles:
            if isinstance(article, dict):
                article['title'] = self.clean_html(article.get('title', ''))
                article['summary'] = self.clean_html(article.get('summary', ''))
                published_date = article.get('published_date', '')
            else:
                published_date = ''
            
            # DATE FILTERING - Only include articles from 2025 (but be flexible with missing dates)
            if SCRAPING_SETTINGS.get('require_recent_articles', True) and published_date:
                try:
                    # Try to parse the published date
                    if isinstance(published_date, str):
                        # Handle different date formats
                        if 'T' in published_date:
                            # ISO format: 2025-01-15T10:30:00
                            article_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                        else:
                            # Simple date format: 2025-01-15
                            article_date = datetime.strptime(published_date[:10], '%Y-%m-%d')
                        
                        if article_date.year != target_year:
                            self.logger.info(f"Article '{article['title'][:50]}...' filtered out (wrong year: {article_date.year})")
                            continue
                except Exception as e:
                    self.logger.warning(f"Could not parse date '{published_date}' for article '{article['title'][:50]}...': {str(e)}")
                    # If we can't parse the date, include the article (don't filter out)
            
            # INTELLIGENT CONTENT FILTERING
            if SCRAPING_SETTINGS.get('content_filtering', True):
                # Check for relevance using a scoring system
                relevance_score = self.calculate_relevance_score(article)
                
                # Only include articles with sufficient relevance
                if relevance_score < 2:  # Minimum score threshold
                    self.logger.info(f"Article '{article['title'][:50]}...' filtered out (low relevance score: {relevance_score})")
                    continue
                
                self.logger.info(f"Article '{article['title'][:50]}...' passed content filter (score: {relevance_score})")
            
            # Include the article
            filtered_articles.append(article)
        
        # Sort articles by published date (most recent first)
        filtered_articles.sort(key=lambda x: x.get('published_date', ''), reverse=True)
        
        self.logger.info(f"Filtered {len(filtered_articles)} relevant articles from {len(articles)} total (content filtering: {SCRAPING_SETTINGS.get('content_filtering', True)}, year filtering: {target_year})")
        return filtered_articles
    
    def calculate_relevance_score(self, article: Dict) -> int:
        """Calculate relevance score for anti-aging research"""
        score = 0
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        source = article.get('source', '').lower()
        
        # Primary keywords (high weight)
        primary_keywords = ['anti-aging', 'longevity', 'senescence', 'aging research', 'life extension']
        for keyword in primary_keywords:
            if keyword in title:
                score += 3
            if keyword in summary:
                score += 2
        
        # Secondary keywords (medium weight)
        secondary_keywords = ['telomere', 'sirtuin', 'rapamycin', 'metformin', 'nad+', 'mitochondria', 
                            'autophagy', 'cellular aging', 'biological age', 'epigenetic clock', 
                            'senolytics', 'gerontology', 'oxidative stress', 'inflammation']
        for keyword in secondary_keywords:
            if keyword in title:
                score += 2
            if keyword in summary:
                score += 1
        
        # Tertiary keywords (low weight)
        tertiary_keywords = ['health', 'medicine', 'research', 'study', 'clinical trial', 'treatment', 
                           'therapy', 'drug', 'molecule', 'protein', 'gene', 'dna', 'cell']
        for keyword in tertiary_keywords:
            if keyword in title:
                score += 1
            if keyword in summary:
                score += 0.5
        
        # Bonus for relevant sources
        relevant_sources = ['nature', 'cell', 'science', 'aging', 'longevity', 'gerontology']
        for source_keyword in relevant_sources:
            if source_keyword in source:
                score += 1
        
        # Penalty for clearly irrelevant content
        irrelevant_keywords = ['covid', 'vaccine', 'politics', 'election', 'sports', 'entertainment', 
                             'celebrity', 'weather', 'traffic', 'crime', 'accident']
        for keyword in irrelevant_keywords:
            if keyword in title:
                score -= 2
            if keyword in summary:
                score -= 1
        
        return max(0, int(score))  # Ensure non-negative score
    
    def extract_article_details(self, article: Dict) -> Dict:
        """Extract detailed information from article URL"""
        try:
            url = article.get('url') if isinstance(article, dict) else ''
            if not url:
                return article
            
            self.logger.info(f"Extracting details from: {url}")
            
            # Use newspaper3k for article extraction
            news_article = Article(url)
            news_article.download()
            news_article.parse()
            
            # Update article with extracted information
            article.update({
                'title': self.clean_html(news_article.title) if hasattr(news_article, 'title') else (article.get('title', '') if isinstance(article, dict) else ''),
                'summary': self.clean_html(news_article.text[:500]) if hasattr(news_article, 'text') and news_article.text else (article.get('summary', '') if isinstance(article, dict) else ''),
                'published_date': news_article.publish_date.isoformat() if hasattr(news_article, 'publish_date') and news_article.publish_date and hasattr(news_article.publish_date, 'isoformat') and hasattr(news_article.publish_date, 'year') else (article.get('published_date', '') if isinstance(article, dict) else ''),
                'authors': ', '.join(news_article.authors) if hasattr(news_article, 'authors') and news_article.authors else '',
                'keywords': ', '.join(news_article.keywords) if hasattr(news_article, 'keywords') and news_article.keywords else ''
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
            
            # Skip detailed extraction for now to speed up scraping
            # for article in filtered_articles:
            #     detailed_article = self.extract_article_details(article)
            #     all_articles.append(detailed_article)
            
            # Add filtered articles directly
            all_articles.extend(filtered_articles)
            
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
                # Use getattr for safer attribute access
                href = getattr(link, 'href', '')
                
                if isinstance(href, str) and '/science/article/' in href:
                    article = {
                        'title': link.get_text(strip=True) if hasattr(link, 'get_text') else '',
                        'url': href if href.startswith('http') else f"https://www.sciencedirect.com{href}" if isinstance(href, str) else '',
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
            cleaned_articles = []
            for article in articles:
                cleaned_article = {}
                for key, value in article.items():
                    if key in ('title', 'summary'):
                        text = self.clean_html(value)
                        if not text.strip():
                            text = 'Untitled' if key == 'title' else 'No summary available'
                        cleaned_article[key] = text
                    else:
                        cleaned_article[key] = value if value is not None else ''
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

    def clean_html(self, raw_html):
        if not isinstance(raw_html, str):
            return str(raw_html)
        cleanr = re.compile('<.*?>')
        return re.sub(cleanr, '', raw_html)

if __name__ == "__main__":
    scraper = AntiAgingScraper()
    scraper.run() 