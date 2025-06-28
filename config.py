# Configuration for Anti-Aging Research Webscraper

# Target websites to scrape
TARGET_WEBSITES = [
    {
        "name": "Medical News Today",
        "url": "https://www.medicalnewstoday.com",
        "rss_feed": "https://www.medicalnewstoday.com/rss.xml",
        "type": "rss"
    },
    {
        "name": "JAMA Network",
        "url": "https://jamanetwork.com",
        "rss_feed": "https://jamanetwork.com/rss/site_3/67.xml",
        "type": "rss"
    },
    {
        "name": "Science Daily",
        "url": "https://www.sciencedaily.com",
        "rss_feed": "https://www.sciencedaily.com/rss/health_medicine.xml",
        "type": "rss"
    },
    {
        "name": "Cell",
        "url": "https://www.cell.com",
        "rss_feed": "https://www.cell.com/rss/current.xml",
        "type": "rss"
    },
    {
        "name": "Nature",
        "url": "https://www.nature.com",
        "rss_feed": "https://www.nature.com/nature.rss",
        "type": "rss"
    },
    {
        "name": "ScienceDirect",
        "url": "https://www.sciencedirect.com",
        "search_url": "https://www.sciencedirect.com/search?query=anti-aging%20longevity%20senescence",
        "type": "search"
    },
    {
        "name": "News Medical",
        "url": "https://www.news-medical.net",
        "rss_feed": "https://www.news-medical.net/rss/feed.aspx",
        "type": "rss"
    },
    {
        "name": "Yale Medicine",
        "url": "https://medicine.yale.edu/news/",
        "type": "scrape"
    },
    {
        "name": "Nature Aging",
        "url": "https://www.nature.com/nataging",
        "rss_feed": "https://www.nature.com/nataging.rss",
        "type": "rss"
    },
    {
        "name": "Wiley Aging Cell",
        "url": "https://onlinelibrary.wiley.com/journal/14749726",
        "rss_feed": "https://onlinelibrary.wiley.com/rss/journal/14749726",
        "type": "rss"
    },
    {
        "name": "SciTech Daily",
        "url": "https://scitechdaily.com",
        "rss_feed": "https://scitechdaily.com/feed/",
        "type": "rss"
    },
    {
        "name": "Science Alert",
        "url": "https://www.sciencealert.com",
        "rss_feed": "https://www.sciencealert.com/feed",
        "type": "rss"
    }
]

# Keywords to filter articles - STRICT TITLE FILTERING
TITLE_KEYWORDS = [
    "anti-aging",
    "longevity", 
    "senescence"
]

# Additional keywords for broader content filtering (optional)
CONTENT_KEYWORDS = [
    "anti-aging",
    "longevity", 
    "senescence",
    "aging",
    "gerontology",
    "telomere",
    "sirtuin",
    "rapamycin",
    "metformin",
    "NAD+",
    "mitochondria",
    "autophagy",
    "inflammation",
    "oxidative stress",
    "cellular aging",
    "biological age",
    "epigenetic clock",
    "senolytics"
]

# Scraping settings
SCRAPING_SETTINGS = {
    "max_articles_per_site": 50,
    "request_delay": 1,  # seconds between requests
    "timeout": 30,  # seconds
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "strict_title_filtering": False,  # Use content-based filtering instead
    "title_filter_required": False,    # Don't require title keyword match
    "content_filtering": True,         # Enable content-based filtering
    "date_filter_year": 2025,        # Only include articles from 2025
    "require_recent_articles": True   # Enable date filtering
}

# Output settings
OUTPUT_SETTINGS = {
    "output_file": "anti_aging_research.csv",
    "backup_file": "anti_aging_research_backup.csv",
    "log_file": "scraper.log"
}

# OpenAI settings (for summarization)
OPENAI_SETTINGS = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 150,
    "temperature": 0.7
} 