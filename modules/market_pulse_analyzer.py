"""
Market Pulse Analyzer - The Core Engine
Combines GCT analysis with market volatility detection and prediction
"""

import logging
import json
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from dataclasses import dataclass

from .gct_analyzer import EnhancedGCTAnalyzer
from .news_scraper import NewsArticle
from config import (
    VOLATILITY_WEIGHTS, 
    ALERT_CONDITIONS, 
    MARKET_MOVERS,
    PERFORMANCE_CONFIG
)

@dataclass
class MarketPulseResult:
    """Result of market pulse analysis"""
    article_id: str
    headline: str
    source: str
    published_date: datetime
    gct_scores: Dict[str, float]
    volatility_score: float
    panic_indicator: float
    herd_factor: float
    predicted_impact: str
    market_keywords_density: float
    emotional_intensity: float
    urgency_score: float
    alert_triggers: List[str]
    confidence_level: float

class MarketPulseAnalyzer(EnhancedGCTAnalyzer):
    """
    Main Market Pulse Analyzer Class
    Extends GCT analysis with market-specific volatility detection
    """
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.analysis_history = []
        self.market_data_cache = {}
        
    def analyze_financial_news(self, article: NewsArticle) -> MarketPulseResult:
        """
        Analyze financial news article for market volatility potential
        
        Args:
            article: NewsArticle object containing headline and content
            
        Returns:
            MarketPulseResult with comprehensive analysis
        """
        
        try:
            # Get base GCT scores
            gct_result = self.analyze_text(article.content, article.headline)
            
            # Calculate market-specific metrics
            emotional_intensity = self.calculate_emotional_intensity(article.content)
            urgency_score = self._calculate_urgency_score(article.headline, article.content)
            market_keywords_density = self.calculate_market_keywords_density(article.content)
            
            # Calculate recency multiplier
            recency_multiplier = self._calculate_recency_multiplier(article.published_date)
            
            # The Magic Formula: GCT meets Wall Street
            # High q (moral activation) in finance = urgency/panic/euphoria
            volatility_score = (
                gct_result['q'] * VOLATILITY_WEIGHTS['gct_moral_activation'] +
                emotional_intensity * VOLATILITY_WEIGHTS['emotional_intensity'] +
                urgency_score * VOLATILITY_WEIGHTS['urgency_score'] +
                market_keywords_density * VOLATILITY_WEIGHTS['market_keyword_density']
            ) * recency_multiplier
            
            # Ensure volatility_score is in 0-1 range
            volatility_score = min(1.0, max(0.0, volatility_score))
            
            # Wisdom paradox: Low ρ + High q = Panic selling
            panic_indicator = (1 - gct_result['rho']) * gct_result['q']
            
            # Social amplification: High f = Herd behavior
            herd_factor = gct_result['f'] * 1.2
            
            # Predict market impact
            predicted_impact = self._categorize_impact(volatility_score)
            
            # Check alert conditions
            alert_triggers = self._check_alert_conditions({
                'gct_scores': gct_result,
                'volatility_score': volatility_score,
                'panic_indicator': panic_indicator,
                'herd_factor': herd_factor
            })
            
            # Calculate confidence level
            confidence_level = self._calculate_confidence_level(
                gct_result, volatility_score, article
            )
            
            # Create result object
            result = MarketPulseResult(
                article_id=article.id,
                headline=article.headline,
                source=article.source,
                published_date=article.published_date,
                gct_scores=gct_result,
                volatility_score=volatility_score,
                panic_indicator=panic_indicator,
                herd_factor=herd_factor,
                predicted_impact=predicted_impact,
                market_keywords_density=market_keywords_density,
                emotional_intensity=emotional_intensity,
                urgency_score=urgency_score,
                alert_triggers=alert_triggers,
                confidence_level=confidence_level
            )
            
            # Store in history
            self.analysis_history.append(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error analyzing article {article.id}: {e}")
            raise
    
    def _calculate_urgency_score(self, headline: str, content: str) -> float:
        """Calculate urgency score based on time-sensitive language"""
        
        urgency_keywords = [
            'breaking', 'urgent', 'alert', 'just in', 'happening now',
            'developing', 'live', 'immediate', 'emergency', 'flash',
            'update', 'latest', 'now', 'today', 'this hour'
        ]
        
        # Check headline (more weight)
        headline_words = headline.lower().split()
        headline_urgency = sum(1 for word in headline_words if word in urgency_keywords)
        headline_score = min(1.0, headline_urgency / len(headline_words) * 5)
        
        # Check content
        content_words = content.lower().split()
        content_urgency = sum(1 for word in content_words if word in urgency_keywords)
        content_score = min(1.0, content_urgency / len(content_words) * 20)
        
        # Check for time references
        time_patterns = [
            r'\b(this|today|now|currently|just|moments ago|minutes ago)\b',
            r'\b(breaking|developing|happening now|live)\b',
            r'\b(urgent|immediate|emergency|critical)\b'
        ]
        
        import re
        time_score = 0
        for pattern in time_patterns:
            matches = re.findall(pattern, content.lower())
            time_score += len(matches) * 0.1
        
        time_score = min(1.0, time_score)
        
        # Combine scores
        urgency_score = headline_score * 0.5 + content_score * 0.3 + time_score * 0.2
        return min(1.0, max(0.0, urgency_score))
    
    def _calculate_recency_multiplier(self, published_date: datetime) -> float:
        """Calculate recency multiplier - more recent news has higher impact"""
        
        now = datetime.now()
        age_hours = (now - published_date).total_seconds() / 3600
        
        # Exponential decay with half-life of 6 hours
        half_life = 6
        multiplier = 2 ** (-age_hours / half_life)
        
        # Ensure minimum multiplier of 0.1 and maximum of 2.0
        return min(2.0, max(0.1, multiplier))
    
    def _categorize_impact(self, volatility_score: float) -> str:
        """Categorize predicted market impact"""
        
        if volatility_score >= 0.8:
            return "EXTREME"
        elif volatility_score >= 0.6:
            return "HIGH"
        elif volatility_score >= 0.4:
            return "MEDIUM"
        elif volatility_score >= 0.2:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _check_alert_conditions(self, analysis: Dict) -> List[str]:
        """Check which alert conditions are triggered"""
        
        triggered_alerts = []
        
        for alert_name, condition_func in ALERT_CONDITIONS.items():
            try:
                if condition_func(analysis):
                    triggered_alerts.append(alert_name)
            except Exception as e:
                self.logger.warning(f"Error checking alert condition {alert_name}: {e}")
        
        return triggered_alerts
    
    def _calculate_confidence_level(self, gct_result: Dict, volatility_score: float, 
                                   article: NewsArticle) -> float:
        """Calculate confidence level in the analysis"""
        
        # Factors that increase confidence
        confidence_factors = []
        
        # Content length (more content = higher confidence)
        content_length_factor = min(1.0, len(article.content) / 1000)
        confidence_factors.append(content_length_factor)
        
        # GCT method used (Claude AI = higher confidence)
        if gct_result.get('method') == 'claude':
            confidence_factors.append(0.9)
        elif gct_result.get('method') == 'combined':
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.6)
        
        # Source reliability (some sources are more reliable)
        source_reliability = self._get_source_reliability(article.source)
        confidence_factors.append(source_reliability)
        
        # Numerical data presence (financial articles should have numbers)
        import re
        numbers = re.findall(r'[\$€£¥]?\d+\.?\d*[%]?', article.content)
        numerical_factor = min(1.0, len(numbers) / 10)
        confidence_factors.append(numerical_factor)
        
        # Calculate overall confidence
        confidence = sum(confidence_factors) / len(confidence_factors)
        return min(1.0, max(0.0, confidence))
    
    def _get_source_reliability(self, source: str) -> float:
        """Get reliability score for news source"""
        
        reliability_scores = {
            'bloomberg': 0.95,
            'reuters': 0.95,
            'wall_street_journal': 0.90,
            'financial_times': 0.90,
            'cnbc': 0.85,
            'marketwatch': 0.80,
            'yahoo_finance': 0.75,
            'mock_': 0.50  # Mock sources for testing
        }
        
        for source_key, score in reliability_scores.items():
            if source_key in source.lower():
                return score
        
        return 0.70  # Default reliability
    
    def process_article_batch(self, articles: List[NewsArticle]) -> List[MarketPulseResult]:
        """Process a batch of articles and return ranked results"""
        
        results = []
        
        for article in articles:
            try:
                result = self.analyze_financial_news(article)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error processing article {article.id}: {e}")
                continue
        
        # Sort by volatility score (highest first)
        results.sort(key=lambda x: x.volatility_score, reverse=True)
        
        return results
    
    def find_contradictory_sentiments(self, results: List[MarketPulseResult]) -> List[Tuple[MarketPulseResult, MarketPulseResult]]:
        """Find articles with contradictory sentiments on similar topics"""
        
        contradictions = []
        
        for i, result1 in enumerate(results):
            for j, result2 in enumerate(results[i+1:], i+1):
                # Check if articles are about similar topics
                if self._are_similar_topics(result1, result2):
                    # Check if sentiments are contradictory
                    if self._are_contradictory_sentiments(result1, result2):
                        contradictions.append((result1, result2))
        
        return contradictions
    
    def _are_similar_topics(self, result1: MarketPulseResult, result2: MarketPulseResult) -> bool:
        """Check if two articles discuss similar topics"""
        
        # Simple keyword overlap approach
        words1 = set(result1.headline.lower().split())
        words2 = set(result2.headline.lower().split())
        
        # Calculate Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if len(union) == 0:
            return False
        
        similarity = len(intersection) / len(union)
        return similarity > 0.3  # Threshold for similar topics
    
    def _are_contradictory_sentiments(self, result1: MarketPulseResult, result2: MarketPulseResult) -> bool:
        """Check if two articles have contradictory sentiments"""
        
        # Compare emotional intensity and panic indicators
        emotion_diff = abs(result1.emotional_intensity - result2.emotional_intensity)
        panic_diff = abs(result1.panic_indicator - result2.panic_indicator)
        
        # If one is very positive and other is very negative
        return emotion_diff > 0.5 or panic_diff > 0.5
    
    def get_market_sentiment_snapshot(self) -> Dict:
        """Get current market sentiment snapshot"""
        
        if not self.analysis_history:
            return {
                'overall_sentiment': 'NEUTRAL',
                'average_volatility': 0.0,
                'panic_level': 0.0,
                'herd_activity': 0.0,
                'top_concerns': [],
                'article_count': 0
            }
        
        # Get recent articles (last 4 hours)
        recent_cutoff = datetime.now() - timedelta(hours=4)
        recent_results = [r for r in self.analysis_history 
                         if r.published_date >= recent_cutoff]
        
        if not recent_results:
            recent_results = self.analysis_history[-10:]  # Last 10 if no recent ones
        
        # Calculate metrics
        avg_volatility = sum(r.volatility_score for r in recent_results) / len(recent_results)
        avg_panic = sum(r.panic_indicator for r in recent_results) / len(recent_results)
        avg_herd = sum(r.herd_factor for r in recent_results) / len(recent_results)
        
        # Determine overall sentiment
        if avg_volatility > 0.7:
            sentiment = 'VERY_BEARISH'
        elif avg_volatility > 0.5:
            sentiment = 'BEARISH'
        elif avg_volatility > 0.3:
            sentiment = 'NEUTRAL'
        elif avg_volatility > 0.1:
            sentiment = 'BULLISH'
        else:
            sentiment = 'VERY_BULLISH'
        
        # Get top concerns (most mentioned keywords)
        all_headlines = ' '.join(r.headline for r in recent_results)
        from collections import Counter
        words = all_headlines.lower().split()
        top_concerns = [word for word, count in Counter(words).most_common(5) 
                       if len(word) > 3]
        
        return {
            'overall_sentiment': sentiment,
            'average_volatility': avg_volatility,
            'panic_level': avg_panic,
            'herd_activity': avg_herd,
            'top_concerns': top_concerns,
            'article_count': len(recent_results),
            'timestamp': datetime.now().isoformat()
        }
    
    def validate_predictions(self, symbol: str = 'SPY') -> Dict:
        """Validate volatility predictions against actual market movements"""
        
        try:
            # Get historical predictions
            if len(self.analysis_history) < 10:
                return {'error': 'Not enough historical data for validation'}
            
            # Get market data
            ticker = yf.Ticker(symbol)
            market_data = ticker.history(period='5d', interval='1h')
            
            # Calculate actual volatility
            market_data['returns'] = market_data['Close'].pct_change()
            market_data['volatility'] = market_data['returns'].rolling(4).std()
            
            # Match predictions with actual movements
            correlations = []
            for result in self.analysis_history[-50:]:  # Last 50 predictions
                # Find closest market data point
                closest_time = None
                min_time_diff = float('inf')
                
                for timestamp in market_data.index:
                    time_diff = abs((timestamp - result.published_date).total_seconds())
                    if time_diff < min_time_diff:
                        min_time_diff = time_diff
                        closest_time = timestamp
                
                if closest_time is not None and min_time_diff < 3600:  # Within 1 hour
                    actual_volatility = market_data.loc[closest_time, 'volatility']
                    if not np.isnan(actual_volatility):
                        correlations.append({
                            'predicted': result.volatility_score,
                            'actual': actual_volatility,
                            'time_diff': min_time_diff
                        })
            
            if not correlations:
                return {'error': 'No matching data points found'}
            
            # Calculate correlation
            predicted_vals = [c['predicted'] for c in correlations]
            actual_vals = [c['actual'] for c in correlations]
            
            correlation = np.corrcoef(predicted_vals, actual_vals)[0, 1]
            
            return {
                'correlation': correlation,
                'data_points': len(correlations),
                'avg_predicted': np.mean(predicted_vals),
                'avg_actual': np.mean(actual_vals),
                'symbol': symbol,
                'validation_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error validating predictions: {e}")
            return {'error': str(e)}

# Example usage and testing
if __name__ == "__main__":
    from news_scraper import NewsArticle
    
    # Create analyzer
    analyzer = MarketPulseAnalyzer()
    
    # Create sample article
    sample_article = NewsArticle(
        headline="Fed Signals Aggressive Rate Hikes as Market Volatility Spikes",
        content="""The Federal Reserve signaled today that it may raise interest rates more aggressively than expected, sending shockwaves through financial markets. Chairman Powell warned that the central bank is prepared to take dramatic action to combat inflation, even if it means triggering a recession. Tech stocks plunged in after-hours trading as investors fled to safer assets. Market analysts are predicting unprecedented volatility in the coming weeks as uncertainty about monetary policy continues to grow.""",
        source="sample_news",
        url="https://example.com/fed-rates",
        published_date=datetime.now()
    )
    
    # Analyze article
    result = analyzer.analyze_financial_news(sample_article)
    
    print(f"Analysis complete for: {result.headline}")
    print(f"Volatility Score: {result.volatility_score:.3f}")
    print(f"Predicted Impact: {result.predicted_impact}")
    print(f"Alert Triggers: {result.alert_triggers}")
    print(f"Confidence Level: {result.confidence_level:.3f}")
    
    # Get market sentiment snapshot
    sentiment = analyzer.get_market_sentiment_snapshot()
    print(f"\nMarket Sentiment: {sentiment}")