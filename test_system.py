#!/usr/bin/env python3
"""
Market Pulse System Test
Test script to verify all components are working correctly
"""

import sys
import os
from datetime import datetime

# Add the current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from modules import create_scraper, MarketPulseAnalyzer, NewsArticle
        from config import NEWS_SOURCES, ANTHROPIC_API_KEY
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_news_scraper():
    """Test the news scraper functionality"""
    print("🔍 Testing news scraper...")
    
    try:
        from modules import create_scraper
        scraper = create_scraper()
        
        # Test with mock data if configured
        articles = scraper.scrape_all_sources()
        
        if articles:
            print(f"✅ News scraper working - found {len(articles)} articles")
            
            # Show sample article
            sample = articles[0]
            print(f"   Sample headline: {sample.headline[:60]}...")
            return True
        else:
            print("⚠️  No articles found (might be using mock data)")
            return True
            
    except Exception as e:
        print(f"❌ News scraper error: {e}")
        return False

def test_gct_analyzer():
    """Test the GCT analyzer functionality"""
    print("🔍 Testing GCT analyzer...")
    
    try:
        from modules import MarketPulseAnalyzer, NewsArticle
        
        analyzer = MarketPulseAnalyzer()
        
        # Create test article
        test_article = NewsArticle(
            headline="Fed Signals Aggressive Rate Hikes as Market Volatility Spikes",
            content="The Federal Reserve announced today that it will raise interest rates more aggressively than expected, causing significant market volatility. Investors are concerned about the impact on economic growth.",
            source="test_source",
            url="https://example.com/test",
            published_date=datetime.now()
        )
        
        # Analyze article
        result = analyzer.analyze_financial_news(test_article)
        
        print(f"✅ GCT analyzer working")
        print(f"   Volatility score: {result.volatility_score:.3f}")
        print(f"   Predicted impact: {result.predicted_impact}")
        print(f"   Alert triggers: {result.alert_triggers}")
        
        return True
        
    except Exception as e:
        print(f"❌ GCT analyzer error: {e}")
        return False

def test_dashboard_components():
    """Test that dashboard components can be loaded"""
    print("🔍 Testing dashboard components...")
    
    try:
        import streamlit as st
        import plotly.graph_objects as go
        import plotly.express as px
        import pandas as pd
        
        print("✅ Dashboard dependencies available")
        return True
        
    except Exception as e:
        print(f"❌ Dashboard component error: {e}")
        return False

def test_config():
    """Test configuration settings"""
    print("🔍 Testing configuration...")
    
    try:
        from config import NEWS_SOURCES, ANTHROPIC_API_KEY, VOLATILITY_KEYWORDS
        
        # Check news sources
        if NEWS_SOURCES:
            print(f"✅ News sources configured: {len(NEWS_SOURCES)} sources")
        else:
            print("⚠️  No news sources configured")
        
        # Check API key (don't print the actual key)
        if ANTHROPIC_API_KEY and len(ANTHROPIC_API_KEY) > 10:
            print("✅ Anthropic API key configured")
        else:
            print("⚠️  Anthropic API key not configured or too short")
        
        # Check volatility keywords
        if VOLATILITY_KEYWORDS:
            total_keywords = sum(len(words) for words in VOLATILITY_KEYWORDS.values())
            print(f"✅ Volatility keywords configured: {total_keywords} keywords")
        else:
            print("⚠️  No volatility keywords configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def run_full_test():
    """Run a full end-to-end test"""
    print("🔍 Running full end-to-end test...")
    
    try:
        from modules import create_scraper, MarketPulseAnalyzer
        
        # Create components
        scraper = create_scraper()
        analyzer = MarketPulseAnalyzer()
        
        # Get articles
        articles = scraper.scrape_all_sources()
        
        if not articles:
            print("⚠️  No articles available for full test")
            return True
        
        # Analyze first few articles
        test_articles = articles[:3]
        results = analyzer.process_article_batch(test_articles)
        
        # Get market sentiment
        sentiment = analyzer.get_market_sentiment_snapshot()
        
        print(f"✅ Full test complete")
        print(f"   Processed {len(results)} articles")
        print(f"   Market sentiment: {sentiment.get('overall_sentiment', 'Unknown')}")
        print(f"   Average volatility: {sentiment.get('average_volatility', 0):.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Full test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Market Pulse System Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("News Scraper", test_news_scraper),
        ("GCT Analyzer", test_gct_analyzer),
        ("Dashboard Components", test_dashboard_components),
        ("Full End-to-End", run_full_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Market Pulse is ready to launch.")
        print("Run 'python launch.py' to start the dashboard.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("See README.md for troubleshooting steps.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)