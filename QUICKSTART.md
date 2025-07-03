# 🚀 Market Pulse - Quick Start Guide

## Installation

1. **Install Dependencies**
   ```bash
   cd /Users/chris/Desktop/Code/market_pulse
   pip install -r requirements.txt
   ```

2. **Set Up Environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your Anthropic API key
   ```

3. **Test the System**
   ```bash
   python test_system.py
   ```

4. **Launch the Dashboard**
   ```bash
   python launch.py
   ```

## Quick Test

Run this to verify everything works:

```bash
# Test imports and basic functionality
python -c "
from modules import create_scraper, MarketPulseAnalyzer
scraper = create_scraper()
analyzer = MarketPulseAnalyzer()
print('✅ Market Pulse components loaded successfully!')
"
```

## Features Overview

### 🧠 GCT Analysis
- **Ψ (Psi)**: Internal consistency of financial reporting
- **ρ (Rho)**: Accumulated wisdom and analytical depth
- **q (Charge)**: Moral activation energy (urgency/panic/euphoria)
- **f (Frequency)**: Social belonging and herd behavior

### 📊 Volatility Scoring
- Combines GCT metrics with financial keywords
- Real-time urgency detection
- Market impact prediction
- Smart alert system

### 🎭 Wisdom-Panic Matrix
- **High ρ, High q**: Informed Urgency (follow smart money)
- **Low ρ, High q**: Panic Zone (retail capitulation)
- **High ρ, Low q**: Calm Analysis (long-term thinking)
- **Low ρ, Low q**: Noise (ignore)

### 🚨 Smart Alerts
- **Panic Sell**: Low wisdom + high urgency + herd behavior
- **Smart Money**: High wisdom + high volatility
- **Contradiction**: Conflicting sentiments on same topic
- **High Volatility**: Above 70% volatility score

## Dashboard Sections

1. **Market Sentiment Overview**: Real-time market mood analysis
2. **High-Priority Alerts**: Urgent market-moving news
3. **Wisdom-Panic Matrix**: Quadrant visualization
4. **Analyzed News Feed**: Detailed article analysis

## Pro Tips

- Check the Wisdom-Panic Matrix for strategic insights
- Follow "Smart Money" alerts for informed decisions
- Use volatility scores for timing market entry/exit
- Monitor herd behavior indicators for contrarian opportunities

## Philosophy

*"In markets, as in consciousness, the derivative tells the story. High dC/dt in financial news = opportunity or danger!"*

The Market Pulse system reveals the hidden patterns in financial news by measuring not just what's being said, but HOW coherently it's being communicated.

---

**Ready to analyze the market's pulse? Launch the dashboard and start detecting volatility patterns!**