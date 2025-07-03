"""
News Scraper Module for Market Pulse
Scrapes financial news from multiple RSS feeds and web sources
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import hashlib
import time
import json
from urllib.parse import urljoin, urlparse
import re

from config import NEWS_SOURCES, SCRAPING_CONFIG, DEBUG_CONFIG

class NewsArticle:
    """Represents a single news article with metadata"""
    
    def __init__(self, headline: str, content: str, source: str, 
                 url: str, published_date: datetime, author: str = None):
        self.headline = headline
        self.content = content
        self.source = source
        self.url = url
        self.published_date = published_date
        self.author = author
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique ID based on headline and URL"""
        content_hash = hashlib.md5(f"{self.headline}{self.url}".encode()).hexdigest()
        return f"{self.source}_{content_hash[:8]}"
    
    def to_dict(self) -> Dict:
        """Convert article to dictionary"""
        return {
            'id': self.id,
            'headline': self.headline,
            'content': self.content,
            'source': self.source,
            'url': self.url,
            'published_date': self.published_date.isoformat(),
            'author': self.author,
            'scraped_at': datetime.now().isoformat()
        }

class FinancialNewsScraper:
    """Main news scraper class"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(SCRAPING_CONFIG['headers'])
        self.logger = logging.getLogger(__name__)
        
    def scrape_rss_feed(self, source_name: str, feed_url: str) -> List[NewsArticle]:
        """Scrape articles from RSS feed"""
        articles = []
        
        try:
            # Parse RSS feed
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                self.logger.warning(f"RSS feed parsing issues for {source_name}: {feed.bozo_exception}")
            
            for entry in feed.entries:
                try:
                    # Extract article data
                    headline = entry.title
                    url = entry.link
                    published_date = self._parse_date(entry.get('published', entry.get('updated')))
                    
                    # Get full article content
                    content = self._extract_article_content(url)
                    
                    if content and len(content) > 100:  # Minimum content length
                        article = NewsArticle(
                            headline=headline,
                            content=content,
                            source=source_name,
                            url=url,
                            published_date=published_date,
                            author=entry.get('author')
                        )
                        articles.append(article)
                        
                except Exception as e:
                    self.logger.error(f"Error processing article from {source_name}: {e}")
                    continue
            
            self.logger.info(f"Scraped {len(articles)} articles from {source_name}")
            
        except Exception as e:
            self.logger.error(f"Error scraping RSS feed {source_name}: {e}")
        
        return articles
    
    def _extract_article_content(self, url: str) -> Optional[str]:
        """Extract full article content from URL"""
        try:
            response = self.session.get(
                url, 
                timeout=SCRAPING_CONFIG['timeout'],
                allow_redirects=True
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try different content selectors based on common patterns
            content_selectors = [
                'article',
                '[data-module="ArticleBody"]',
                '.article-body',
                '.story-body',
                '.content-body',
                '.article-content',
                '.post-content',
                '.entry-content',
                'main p',
                '.text p'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = ' '.join([elem.get_text(strip=True) for elem in elements])
                    break
            
            # Fallback: get all paragraph text
            if not content:
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text(strip=True) for p in paragraphs])
            
            # Clean up content
            content = re.sub(r'\s+', ' ', content).strip()
            
            return content if len(content) > 50 else None
            
        except Exception as e:
            self.logger.error(f"Error extracting content from {url}: {e}")
            return None
    
    def _parse_date(self, date_string: str) -> datetime:
        """Parse date string to datetime object"""
        if not date_string:
            return datetime.now()
        
        try:
            # Try feedparser's parsing first
            parsed = feedparser._parse_date(date_string)
            if parsed:
                return datetime(*parsed[:6])
        except:
            pass
        
        # Fallback to current time
        return datetime.now()
    
    def scrape_all_sources(self) -> List[NewsArticle]:
        """Scrape all configured news sources"""
        all_articles = []
        
        for source_name, feed_url in NEWS_SOURCES.items():
            try:
                articles = self.scrape_rss_feed(source_name, feed_url)
                all_articles.extend(articles)
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error scraping {source_name}: {e}")
                continue
        
        # Remove duplicates
        unique_articles = self._deduplicate_articles(all_articles)
        
        # Filter recent articles (last 24 hours)
        recent_articles = self._filter_recent_articles(unique_articles)
        
        self.logger.info(f"Total articles scraped: {len(all_articles)}")
        self.logger.info(f"Unique articles: {len(unique_articles)}")
        self.logger.info(f"Recent articles (24h): {len(recent_articles)}")
        
        return recent_articles
    
    def _deduplicate_articles(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        """Remove duplicate articles based on content similarity"""
        seen_ids = set()
        unique_articles = []
        
        for article in articles:
            # Simple deduplication by headline similarity
            headline_hash = hashlib.md5(article.headline.lower().encode()).hexdigest()
            
            if headline_hash not in seen_ids:
                seen_ids.add(headline_hash)
                unique_articles.append(article)
        
        return unique_articles
    
    def _filter_recent_articles(self, articles: List[NewsArticle], hours: int = 24) -> List[NewsArticle]:
        """Filter articles from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        return [
            article for article in articles 
            if article.published_date >= cutoff_time
        ]
    
    def save_articles_to_json(self, articles: List[NewsArticle], filepath: str):
        """Save articles to JSON file"""
        try:
            articles_data = [article.to_dict() for article in articles]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved {len(articles)} articles to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving articles to JSON: {e}")
    
    def load_articles_from_json(self, filepath: str) -> List[NewsArticle]:
        """Load articles from JSON file"""
        articles = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
            
            for article_dict in articles_data:
                article = NewsArticle(
                    headline=article_dict['headline'],
                    content=article_dict['content'],
                    source=article_dict['source'],
                    url=article_dict['url'],
                    published_date=datetime.fromisoformat(article_dict['published_date']),
                    author=article_dict.get('author')
                )
                articles.append(article)
            
            self.logger.info(f"Loaded {len(articles)} articles from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error loading articles from JSON: {e}")
        
        return articles

class MockNewsScraper(FinancialNewsScraper):
    """Mock scraper for testing purposes"""
    
    def scrape_all_sources(self) -> List[NewsArticle]:
        """Return mock articles for testing"""
        mock_articles = [
            NewsArticle(
                headline="Fed Signals Rate Hike Amid Inflation Concerns",
                content="The Federal Reserve indicated today that interest rates may need to rise faster than previously anticipated due to persistent inflation pressures. Chairman Powell noted that the central bank is prepared to take aggressive action if necessary.",
                source="mock_fed_news",
                url="https://example.com/fed-rates",
                published_date=datetime.now() - timedelta(hours=2)
            ),
            NewsArticle(
                headline="Tech Stocks Surge on AI Breakthrough",
                content="Major technology companies saw their shares soar after a breakthrough in artificial intelligence capabilities was announced. The development is expected to revolutionize multiple industries and create new market opportunities.",
                source="mock_tech_news",
                url="https://example.com/tech-surge",
                published_date=datetime.now() - timedelta(hours=1)
            ),
            NewsArticle(
                headline="Market Volatility Spikes as Geopolitical Tensions Rise",
                content="Global markets experienced significant volatility today as geopolitical tensions escalated. Investors fled to safe-haven assets while equity markets tumbled across multiple regions.",
                source="mock_market_news",
                url="https://example.com/market-volatility",
                published_date=datetime.now() - timedelta(minutes=30)
            )
        ]
        
        return mock_articles

def create_scraper() -> FinancialNewsScraper:
    """Factory function to create appropriate scraper"""
    if DEBUG_CONFIG['mock_news_data']:
        return MockNewsScraper()
    else:
        return FinancialNewsScraper()

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    scraper = create_scraper()
    articles = scraper.scrape_all_sources()
    
    print(f"Scraped {len(articles)} articles")
    
    for article in articles[:3]:  # Show first 3
        print(f"\nHeadline: {article.headline}")
        print(f"Source: {article.source}")
        print(f"Published: {article.published_date}")
        print(f"Content preview: {article.content[:200]}...")