"""
Enhanced GCT Analyzer for Financial News Analysis
Extends the original GCT analyzer with market-specific volatility detection
"""

import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter
import anthropic

from config import (
    ANTHROPIC_API_KEY, 
    VOLATILITY_KEYWORDS, 
    GCT_ANALYSIS_PROMPT,
    MARKET_MOVERS,
    DEBUG_CONFIG
)

class EnhancedGCTAnalyzer:
    """Enhanced GCT Analyzer with Claude AI integration and financial focus"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.logger = logging.getLogger(__name__)
        
        # Financial-specific word lists
        self.financial_keywords = self._build_financial_keywords()
        
    def _build_financial_keywords(self) -> Dict[str, List[str]]:
        """Build comprehensive financial keyword dictionary"""
        return {
            'market_emotions': {
                'panic': ['crash', 'plunge', 'collapse', 'fear', 'panic', 'selloff', 'rout'],
                'euphoria': ['surge', 'soar', 'rocket', 'boom', 'rally', 'moon', 'explode'],
                'uncertainty': ['volatility', 'uncertainty', 'risk', 'doubt', 'concern', 'worry']
            },
            'institutions': [
                'fed', 'federal reserve', 'fomc', 'ecb', 'boj', 'bank of england',
                'treasury', 'sec', 'cftc', 'finra', 'fdic'
            ],
            'market_indicators': [
                'gdp', 'inflation', 'cpi', 'ppi', 'unemployment', 'jobs report',
                'yield curve', 'vix', 'dxy', 'oil prices', 'gold'
            ],
            'trading_terms': [
                'bull', 'bear', 'long', 'short', 'puts', 'calls', 'options',
                'futures', 'derivatives', 'margin', 'leverage'
            ],
            'urgency_indicators': [
                'breaking', 'urgent', 'alert', 'just in', 'happening now',
                'developing', 'live', 'immediate', 'emergency'
            ]
        }
    
    def analyze_text(self, text: str, headline: str) -> Dict:
        """Analyze text using both heuristic and Claude AI methods"""
        
        # Basic preprocessing
        words = re.findall(r'\b\w+\b', text.lower())
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Heuristic analysis (fast)
        heuristic_analysis = self._analyze_heuristic(text, headline, words, sentences)
        
        # Claude AI analysis (comprehensive)
        claude_analysis = self._analyze_with_claude(text, headline)
        
        # Combine results
        combined_analysis = self._combine_analyses(heuristic_analysis, claude_analysis)
        
        return combined_analysis
    
    def _analyze_heuristic(self, text: str, headline: str, words: List[str], sentences: List[str]) -> Dict:
        """Fast heuristic analysis using keyword matching"""
        
        # Financial-specific Ψ (Internal Consistency)
        psi = self._calculate_financial_psi(words, sentences, text)
        
        # Financial-specific ρ (Accumulated Wisdom)
        rho = self._calculate_financial_rho(text, sentences, words)
        
        # Financial-specific q (Moral Activation Energy)
        q = self._calculate_financial_q(text, words, headline)
        
        # Financial-specific f (Social Belonging)
        f = self._calculate_financial_f(words, text)
        
        # Calculate coherence
        coherence = self._calculate_coherence(psi, rho, q, f)
        
        return {
            'psi': psi,
            'rho': rho, 
            'q': q,
            'f': f,
            'coherence': coherence,
            'method': 'heuristic'
        }
    
    def _analyze_with_claude(self, text: str, headline: str) -> Dict:
        """Comprehensive analysis using Claude AI"""
        
        if DEBUG_CONFIG['mock_news_data']:
            # Return mock analysis for testing
            return {
                'psi': 0.7,
                'rho': 0.6,
                'q': 0.8,
                'f': 0.5,
                'coherence': 2.3,
                'method': 'claude_mock',
                'explanation': 'Mock analysis for testing purposes'
            }
        
        try:
            # Prepare prompt
            prompt = GCT_ANALYSIS_PROMPT.format(
                article_text=text[:2000],  # Limit text length
                headline=headline
            )
            
            # Call Claude
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            analysis = self._parse_claude_response(response.content[0].text)
            analysis['method'] = 'claude'
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Claude analysis failed: {e}")
            # Fallback to heuristic if Claude fails
            return self._analyze_heuristic(text, headline, 
                                         re.findall(r'\b\w+\b', text.lower()),
                                         re.split(r'[.!?]+', text))
    
    def _parse_claude_response(self, response_text: str) -> Dict:
        """Parse Claude's response into structured data"""
        
        # Initialize default values
        analysis = {
            'psi': 0.5,
            'rho': 0.5,
            'q': 0.5,
            'f': 0.5,
            'coherence': 2.0,
            'explanation': response_text
        }
        
        # Extract numerical scores using regex
        score_patterns = {
            'psi': r'(?:grounding|γ|gamma).*?(\d+\.?\d*)',
            'rho': r'(?:coherence|ρ|rho).*?(\d+\.?\d*)',
            'q': r'(?:moral|activation|q).*?(\d+\.?\d*)',
            'f': r'(?:dialectical|feedback|f).*?(\d+\.?\d*)'
        }
        
        for metric, pattern in score_patterns.items():
            matches = re.findall(pattern, response_text.lower())
            if matches:
                try:
                    score = float(matches[0])
                    # Normalize to 0-1 range if needed
                    if score > 1.0:
                        score = score / 10.0
                    analysis[metric] = min(1.0, max(0.0, score))
                except ValueError:
                    continue
        
        # Calculate coherence
        analysis['coherence'] = self._calculate_coherence(
            analysis['psi'], analysis['rho'], 
            analysis['q'], analysis['f']
        )
        
        return analysis
    
    def _calculate_financial_psi(self, words: List[str], sentences: List[str], text: str) -> float:
        """Financial-specific internal consistency calculation"""
        
        # Market terminology consistency
        market_terms = self.financial_keywords['trading_terms'] + self.financial_keywords['market_indicators']
        market_term_count = sum(1 for word in words if word in market_terms)
        market_consistency = min(1.0, market_term_count / len(words) * 50)
        
        # Numerical data consistency (prices, percentages, etc.)
        numerical_patterns = re.findall(r'[\$€£¥]?\d+\.?\d*[%]?', text)
        numerical_consistency = min(1.0, len(numerical_patterns) / max(len(sentences), 1) * 2)
        
        # Stock symbol consistency
        stock_symbols = re.findall(r'\b[A-Z]{2,5}\b', text)
        symbol_consistency = min(1.0, len(stock_symbols) / 10)
        
        # Combine metrics
        psi = (market_consistency * 0.4 + numerical_consistency * 0.3 + symbol_consistency * 0.3)
        return min(1.0, max(0.0, psi))
    
    def _calculate_financial_rho(self, text: str, sentences: List[str], words: List[str]) -> float:
        """Financial-specific wisdom/depth calculation"""
        
        # Market analysis depth
        analysis_words = ['analysis', 'forecast', 'projection', 'estimate', 'outlook', 
                         'trend', 'pattern', 'correlation', 'fundamental', 'technical']
        analysis_count = sum(1 for word in analysis_words if word in text.lower())
        analysis_depth = min(1.0, analysis_count / 10)
        
        # Causal reasoning in finance
        financial_causal = ['due to', 'because of', 'driven by', 'caused by', 'results from',
                           'leads to', 'triggers', 'impacts', 'affects', 'influences']
        causal_count = sum(1 for phrase in financial_causal if phrase in text.lower())
        causal_score = min(1.0, causal_count / 5)
        
        # Historical context
        time_references = ['historically', 'previously', 'last quarter', 'year-over-year',
                          'compared to', 'since', 'following', 'after', 'before']
        historical_count = sum(1 for phrase in time_references if phrase in text.lower())
        historical_score = min(1.0, historical_count / 5)
        
        # Expert citations
        expert_indicators = ['analyst', 'economist', 'ceo', 'cfo', 'expert', 'strategist',
                           'according to', 'says', 'notes', 'expects', 'believes']
        expert_count = sum(1 for phrase in expert_indicators if phrase in text.lower())
        expert_score = min(1.0, expert_count / 5)
        
        # Combine metrics
        rho = (analysis_depth * 0.3 + causal_score * 0.3 + historical_score * 0.2 + expert_score * 0.2)
        return min(1.0, max(0.0, rho))
    
    def _calculate_financial_q(self, text: str, words: List[str], headline: str) -> float:
        """Financial-specific moral activation (urgency/emotion) calculation"""
        
        # Market emotion intensity
        panic_words = VOLATILITY_KEYWORDS['panic_words']
        euphoria_words = VOLATILITY_KEYWORDS['euphoria_words']
        
        panic_count = sum(1 for word in words if word in panic_words)
        euphoria_count = sum(1 for word in words if word in euphoria_words)
        emotion_intensity = min(1.0, (panic_count + euphoria_count) / len(words) * 20)
        
        # Urgency indicators
        urgency_words = VOLATILITY_KEYWORDS['urgency_words']
        urgency_count = sum(1 for word in words if word in urgency_words)
        urgency_score = min(1.0, urgency_count / 5)
        
        # Federal Reserve / Policy urgency
        fed_words = VOLATILITY_KEYWORDS['fed_words']
        fed_count = sum(1 for phrase in fed_words if phrase in text.lower())
        fed_urgency = min(1.0, fed_count / 3)
        
        # Magnitude words
        magnitude_words = VOLATILITY_KEYWORDS['magnitude_words']
        magnitude_count = sum(1 for word in words if word in magnitude_words)
        magnitude_score = min(1.0, magnitude_count / 5)
        
        # Headline urgency (headlines are more impactful)
        headline_words = headline.lower().split()
        headline_emotion = sum(1 for word in headline_words 
                              if word in panic_words or word in euphoria_words or word in urgency_words)
        headline_urgency = min(1.0, headline_emotion / max(len(headline_words), 1) * 3)
        
        # Combine metrics
        q = (emotion_intensity * 0.25 + urgency_score * 0.25 + fed_urgency * 0.2 + 
             magnitude_score * 0.15 + headline_urgency * 0.15)
        return min(1.0, max(0.0, q))
    
    def _calculate_financial_f(self, words: List[str], text: str) -> float:
        """Financial-specific social belonging calculation"""
        
        # Market participant language
        participant_words = ['investors', 'traders', 'market', 'wall street', 'retail',
                           'institutional', 'hedge funds', 'mutual funds', 'pension funds']
        participant_count = sum(1 for phrase in participant_words if phrase in text.lower())
        participant_score = min(1.0, participant_count / 5)
        
        # Collective market sentiment
        sentiment_words = ['sentiment', 'mood', 'confidence', 'optimism', 'pessimism',
                         'fear', 'greed', 'risk appetite', 'risk aversion']
        sentiment_count = sum(1 for phrase in sentiment_words if phrase in text.lower())
        sentiment_score = min(1.0, sentiment_count / 5)
        
        # Economic community references
        community_words = ['economy', 'markets', 'industry', 'sector', 'global',
                         'worldwide', 'international', 'domestic']
        community_count = sum(1 for word in words if word in community_words)
        community_score = min(1.0, community_count / 10)
        
        # Combine metrics
        f = (participant_score * 0.4 + sentiment_score * 0.4 + community_score * 0.2)
        return min(1.0, max(0.0, f))
    
    def _calculate_coherence(self, psi: float, rho: float, q: float, f: float) -> float:
        """Calculate overall coherence using GCT formula"""
        
        # Biological optimization for q (urgency has diminishing returns)
        q_max = 1.0
        K_m = 0.2
        K_i = 0.8
        q_optimal = (q_max * q) / (K_m + q + (q**2 / K_i))
        
        # Core coherence equation
        coherence = psi + (rho * psi) + q_optimal + (f * psi)
        
        return coherence
    
    def _combine_analyses(self, heuristic: Dict, claude: Dict) -> Dict:
        """Combine heuristic and Claude analyses"""
        
        # Weight the analyses (Claude gets more weight if available)
        if claude['method'] == 'claude':
            heuristic_weight = 0.3
            claude_weight = 0.7
        else:
            heuristic_weight = 1.0
            claude_weight = 0.0
        
        combined = {
            'psi': heuristic['psi'] * heuristic_weight + claude['psi'] * claude_weight,
            'rho': heuristic['rho'] * heuristic_weight + claude['rho'] * claude_weight,
            'q': heuristic['q'] * heuristic_weight + claude['q'] * claude_weight,
            'f': heuristic['f'] * heuristic_weight + claude['f'] * claude_weight,
            'method': 'combined',
            'heuristic_analysis': heuristic,
            'claude_analysis': claude
        }
        
        # Recalculate coherence
        combined['coherence'] = self._calculate_coherence(
            combined['psi'], combined['rho'], combined['q'], combined['f']
        )
        
        return combined
    
    def calculate_market_keywords_density(self, text: str) -> float:
        """Calculate density of market-moving keywords"""
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Count all market-related keywords
        total_keywords = 0
        for category in VOLATILITY_KEYWORDS.values():
            for keyword in category:
                total_keywords += text_lower.count(keyword)
        
        # Add market movers (stock symbols)
        for symbol in MARKET_MOVERS:
            total_keywords += text_lower.count(symbol.lower())
        
        # Calculate density
        density = total_keywords / max(len(words), 1)
        return min(1.0, density * 10)  # Scale up for visibility
    
    def calculate_emotional_intensity(self, text: str) -> float:
        """Calculate emotional intensity of financial text"""
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Combine all emotional keywords
        all_emotional_words = (
            VOLATILITY_KEYWORDS['panic_words'] +
            VOLATILITY_KEYWORDS['euphoria_words'] +
            VOLATILITY_KEYWORDS['magnitude_words'] +
            VOLATILITY_KEYWORDS['uncertainty_words']
        )
        
        emotional_count = sum(1 for word in words if word in all_emotional_words)
        intensity = emotional_count / max(len(words), 1)
        
        return min(1.0, intensity * 15)  # Scale up for visibility

# Example usage
if __name__ == "__main__":
    analyzer = EnhancedGCTAnalyzer()
    
    # Test with sample financial news
    sample_headline = "Fed Signals Aggressive Rate Hikes as Inflation Soars"
    sample_text = """
    The Federal Reserve signaled today that it may need to raise interest rates more aggressively 
    than previously anticipated as inflation continues to surge above target levels. Chairman Powell 
    noted that the central bank is prepared to take decisive action to combat rising prices, 
    even if it means risking a recession. Market analysts are warning that this hawkish stance 
    could trigger significant volatility in equity markets, with tech stocks particularly vulnerable 
    to higher borrowing costs.
    """
    
    result = analyzer.analyze_text(sample_text, sample_headline)
    print(f"Analysis result: {json.dumps(result, indent=2)}")