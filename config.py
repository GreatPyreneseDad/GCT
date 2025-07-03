"""
Market Pulse Configuration Module
Central configuration for the Financial News GCT Volatility Analyzer
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# News Sources Configuration
NEWS_SOURCES = {
    'yahoo_finance': 'https://finance.yahoo.com/rss/topfinstories',
    'bloomberg': 'https://feeds.bloomberg.com/markets/news.rss',
    'reuters': 'https://feeds.reuters.com/reuters/businessNews',
    'cnbc': 'https://www.cnbc.com/id/10001147/device/rss/rss.html',
    'marketwatch': 'https://feeds.marketwatch.com/marketwatch/topstories',
    'financial_times': 'https://www.ft.com/rss/home',
    'wall_street_journal': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml'
}

# Volatility Keywords Configuration
VOLATILITY_KEYWORDS = {
    'panic_words': ['crash', 'plunge', 'collapse', 'crisis', 'panic', 'fear', 'selloff', 'tumble', 'nosedive'],
    'euphoria_words': ['surge', 'soar', 'rocket', 'boom', 'rally', 'explode', 'skyrocket', 'moon', 'breakout'],
    'fed_words': ['federal reserve', 'fed', 'powell', 'fomc', 'interest rates', 'monetary policy', 'hawkish', 'dovish'],
    'magnitude_words': ['unprecedented', 'historic', 'massive', 'shocking', 'dramatic', 'extreme', 'wild'],
    'urgency_words': ['breaking', 'urgent', 'alert', 'just in', 'happening now', 'live', 'developing'],
    'uncertainty_words': ['volatility', 'uncertainty', 'risk', 'fear', 'doubt', 'concern', 'worry', 'tension']
}

# Market Movers - Top stocks that move markets
MARKET_MOVERS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META', 'SPY', 'QQQ', 'BTC-USD']

# GCT Analysis Configuration
GCT_ANALYSIS_PROMPT = """
You are analyzing financial news through the lens of Grounded Coherence Theory (GCT).

For the following financial news article, provide a GCT analysis focusing on:

1. **Grounding (γ)**: How well-grounded are the claims in observable market data, financial metrics, or verified sources?
2. **Coherence (ρ)**: How internally consistent and logically structured is the narrative?
3. **Moral Activation (q)**: What is the emotional urgency, fear, or excitement level in the language?
4. **Dialectical Feedback (f)**: How much does this represent collective market sentiment vs. individual analysis?

Please respond with numerical scores (0-1) and brief explanations for each dimension.

Article: {article_text}
Headline: {headline}
"""

# Volatility Scoring Configuration
VOLATILITY_WEIGHTS = {
    'gct_moral_activation': 0.35,  # q score - urgency/panic/euphoria
    'emotional_intensity': 0.25,   # Raw emotional language detection
    'urgency_score': 0.20,         # Breaking news, time-sensitive language
    'market_keyword_density': 0.20 # Concentration of market-moving keywords
}

# Alert Configuration
ALERT_THRESHOLDS = {
    'high_volatility': 0.7,     # Above this = high volatility alert
    'panic_zone': 0.6,          # Low wisdom + high urgency
    'smart_money': 0.7,         # High wisdom + high volatility
    'contradiction': 0.5        # Conflicting sentiment threshold
}

# Alert conditions
ALERT_CONDITIONS = {
    'panic_sell': lambda analysis: (
        analysis['panic_indicator'] > ALERT_THRESHOLDS['panic_zone'] and 
        analysis['herd_factor'] > 0.6
    ),
    'smart_money': lambda analysis: (
        analysis['gct_scores']['rho'] > 0.7 and 
        analysis['volatility_score'] > ALERT_THRESHOLDS['smart_money']
    ),
    'contradiction': lambda analysis: (
        analysis.get('is_contradictory', False) and 
        analysis['volatility_score'] > ALERT_THRESHOLDS['contradiction']
    ),
    'high_volatility': lambda analysis: (
        analysis['volatility_score'] > ALERT_THRESHOLDS['high_volatility']
    )
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'page_title': 'Market Pulse - GCT Financial News Analyzer',
    'page_icon': '📈',
    'layout': 'wide',
    'update_interval': int(os.getenv('UPDATE_INTERVAL_MINUTES', 15)),
    'max_articles_display': 50,
    'chart_height': 400
}

# Streamlit Custom CSS
CUSTOM_CSS = """
<style>
    .high-volatility {
        background-color: #ff4444;
        color: white;
        padding: 10px;
        border-radius: 5px;
        animation: pulse 2s infinite;
        font-weight: bold;
    }
    
    .medium-volatility {
        background-color: #ffaa44;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .low-volatility {
        background-color: #44ff44;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
    
    .gct-score {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
    }
    
    .volatility-gauge {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
"""

# Data Storage Configuration
DATA_CONFIG = {
    'articles_db': 'data/articles.json',
    'analysis_db': 'data/analysis_results.json',
    'alerts_db': 'data/alerts.json',
    'performance_db': 'data/performance_metrics.json'
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'handlers': ['console', 'file'],
    'log_file': 'logs/market_pulse.log'
}

# Performance Tracking
PERFORMANCE_CONFIG = {
    'track_predictions': True,
    'correlation_window_hours': 24,
    'min_articles_for_correlation': 10,
    'performance_update_interval': 60  # minutes
}

# Web Scraping Configuration
SCRAPING_CONFIG = {
    'timeout': 30,
    'max_retries': 3,
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'headers': {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
}

# Development/Debug Configuration
DEBUG_CONFIG = {
    'enable_debug': os.getenv('DEBUG', 'false').lower() == 'true',
    'mock_news_data': os.getenv('MOCK_NEWS', 'false').lower() == 'true',
    'save_api_responses': os.getenv('SAVE_API_RESPONSES', 'false').lower() == 'true',
    'verbose_logging': os.getenv('VERBOSE_LOGGING', 'false').lower() == 'true'
}