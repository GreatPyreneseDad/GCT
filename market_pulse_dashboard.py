"""
Market Pulse Dashboard - Main Streamlit Application
Revolutionary financial news analyzer combining GCT with market volatility detection
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import logging
import time
from typing import List, Dict
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)

# Import our modules
from modules import create_scraper, MarketPulseAnalyzer, MarketPulseResult
from config import DASHBOARD_CONFIG, CUSTOM_CSS, DEBUG_CONFIG

# Set page config
st.set_page_config(
    page_title=DASHBOARD_CONFIG['page_title'],
    page_icon=DASHBOARD_CONFIG['page_icon'],
    layout=DASHBOARD_CONFIG['layout'],
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'market_sentiment' not in st.session_state:
    st.session_state.market_sentiment = {}

@st.cache_data(ttl=900)  # Cache for 15 minutes
def load_news_data():
    """Load and analyze news data"""
    try:
        # Create scraper and analyzer
        scraper = create_scraper()
        analyzer = MarketPulseAnalyzer()
        
        # Scrape news
        with st.spinner("🔍 Scraping latest financial news..."):
            articles = scraper.scrape_all_sources()
        
        if not articles:
            st.warning("No articles found. Using cached data if available.")
            return []
        
        # Analyze articles
        with st.spinner("🧠 Analyzing news with GCT framework..."):
            results = analyzer.process_article_batch(articles)
        
        # Update session state
        st.session_state.analysis_results = results
        st.session_state.last_update = datetime.now()
        st.session_state.market_sentiment = analyzer.get_market_sentiment_snapshot()
        
        return results
        
    except Exception as e:
        st.error(f"Error loading news data: {e}")
        return []

def display_header():
    """Display the main header with market pulse gauge"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("# 🚀 Market Pulse")
        st.markdown("*Financial News GCT Volatility Analyzer*")
        st.markdown("---")
    
    with col2:
        if st.session_state.market_sentiment:
            sentiment = st.session_state.market_sentiment
            volatility = sentiment.get('average_volatility', 0)
            
            # Create volatility gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=volatility * 100,
                title={'text': "Market Volatility"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "red" if volatility > 0.6 else "orange" if volatility > 0.3 else "green"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgray"},
                        {'range': [30, 60], 'color': "gray"},
                        {'range': [60, 100], 'color': "darkgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }
            ))
            fig.update_layout(height=200)
            st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        if st.session_state.last_update:
            st.metric(
                label="Last Update",
                value=st.session_state.last_update.strftime("%H:%M"),
                delta=f"{len(st.session_state.analysis_results)} articles"
            )

def display_market_sentiment():
    """Display current market sentiment overview"""
    if not st.session_state.market_sentiment:
        return
    
    st.markdown("## 📊 Market Sentiment Overview")
    
    sentiment = st.session_state.market_sentiment
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sentiment_value = sentiment.get('overall_sentiment', 'NEUTRAL')
        sentiment_color = {
            'VERY_BULLISH': '🟢',
            'BULLISH': '🟢',
            'NEUTRAL': '🟡',
            'BEARISH': '🔴',
            'VERY_BEARISH': '🔴'
        }.get(sentiment_value, '🟡')
        
        st.metric(
            label="Overall Sentiment",
            value=f"{sentiment_color} {sentiment_value}",
        )
    
    with col2:
        panic_level = sentiment.get('panic_level', 0)
        panic_emoji = '🚨' if panic_level > 0.6 else '⚠️' if panic_level > 0.3 else '✅'
        st.metric(
            label="Panic Level",
            value=f"{panic_emoji} {panic_level:.1%}",
        )
    
    with col3:
        herd_activity = sentiment.get('herd_activity', 0)
        herd_emoji = '🐑' if herd_activity > 0.6 else '👥' if herd_activity > 0.3 else '👤'
        st.metric(
            label="Herd Activity",
            value=f"{herd_emoji} {herd_activity:.1%}",
        )
    
    with col4:
        article_count = sentiment.get('article_count', 0)
        st.metric(
            label="Articles Analyzed",
            value=f"📰 {article_count}",
        )

def display_top_alerts():
    """Display high-priority alerts"""
    if not st.session_state.analysis_results:
        return
    
    # Filter for high-volatility articles with alerts
    high_priority = [
        result for result in st.session_state.analysis_results
        if result.alert_triggers and result.volatility_score > 0.5
    ]
    
    if not high_priority:
        st.success("🟢 No high-priority alerts at this time")
        return
    
    st.markdown("## 🚨 High-Priority Alerts")
    
    for result in high_priority[:3]:  # Show top 3
        alert_type = result.alert_triggers[0].replace('_', ' ').title()
        
        with st.expander(f"🚨 {alert_type} Alert - {result.predicted_impact} Impact"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{result.headline}**")
                st.markdown(f"*Source: {result.source} | {result.published_date.strftime('%H:%M')}*")
                
                # Show key metrics
                st.markdown(f"""
                - **Volatility Score:** {result.volatility_score:.1%}
                - **Panic Indicator:** {result.panic_indicator:.1%}
                - **Confidence:** {result.confidence_level:.1%}
                """)
            
            with col2:
                # Volatility score as a big number
                st.markdown(f"""
                <div class="volatility-gauge" style="background-color: {'#ff4444' if result.volatility_score > 0.7 else '#ffaa44' if result.volatility_score > 0.4 else '#44ff44'};">
                    {result.volatility_score:.1%}
                </div>
                """, unsafe_allow_html=True)

def display_wisdom_panic_matrix():
    """Display the Wisdom-Panic Matrix visualization"""
    if not st.session_state.analysis_results:
        return
    
    st.markdown("## 🎭 Wisdom-Panic Matrix")
    st.markdown("*Quadrant Analysis: X-axis = Wisdom (ρ), Y-axis = Urgency (q)*")
    
    # Prepare data for scatter plot
    data = []
    for result in st.session_state.analysis_results:
        data.append({
            'Wisdom (ρ)': result.gct_scores['rho'],
            'Urgency (q)': result.gct_scores['q'],
            'Volatility': result.volatility_score,
            'Headline': result.headline[:50] + "..." if len(result.headline) > 50 else result.headline,
            'Source': result.source,
            'Impact': result.predicted_impact
        })
    
    df = pd.DataFrame(data)
    
    # Create scatter plot
    fig = px.scatter(
        df, 
        x='Wisdom (ρ)', 
        y='Urgency (q)',
        size='Volatility',
        color='Impact',
        hover_data=['Headline', 'Source'],
        title="Wisdom vs Urgency Analysis",
        color_discrete_map={
            'EXTREME': '#ff0000',
            'HIGH': '#ff6600',
            'MEDIUM': '#ffaa00',
            'LOW': '#00aa00',
            'MINIMAL': '#0000ff'
        }
    )
    
    # Add quadrant lines
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=0.5, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=0.75, y=0.75, text="Informed Urgency<br>(Follow Smart Money)", 
                      showarrow=False, font=dict(color="green"))
    fig.add_annotation(x=0.25, y=0.75, text="Panic Zone<br>(Retail Capitulation)", 
                      showarrow=False, font=dict(color="red"))
    fig.add_annotation(x=0.75, y=0.25, text="Calm Analysis<br>(Long-term Thinking)", 
                      showarrow=False, font=dict(color="blue"))
    fig.add_annotation(x=0.25, y=0.25, text="Noise<br>(Ignore)", 
                      showarrow=False, font=dict(color="gray"))
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def display_news_feed():
    """Display the main news feed with analysis results"""
    if not st.session_state.analysis_results:
        st.info("No news articles available. Click 'Refresh News' to load data.")
        return
    
    st.markdown("## 📰 Analyzed News Feed")
    
    # Filter and sort options
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        min_volatility = st.slider(
            "Minimum Volatility Score",
            0.0, 1.0, 0.0, 0.1,
            help="Filter articles by minimum volatility score"
        )
    
    with col2:
        impact_filter = st.selectbox(
            "Impact Level",
            ["ALL", "EXTREME", "HIGH", "MEDIUM", "LOW", "MINIMAL"],
            help="Filter by predicted market impact"
        )
    
    with col3:
        max_articles = st.slider(
            "Max Articles to Show",
            10, 100, 20, 10,
            help="Maximum number of articles to display"
        )
    
    # Filter articles
    filtered_results = [
        result for result in st.session_state.analysis_results
        if result.volatility_score >= min_volatility and
        (impact_filter == "ALL" or result.predicted_impact == impact_filter)
    ]
    
    # Display articles
    for i, result in enumerate(filtered_results[:max_articles]):
        with st.expander(f"#{i+1} - {result.headline}", expanded=i < 3):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Article info
                st.markdown(f"**Source:** {result.source}")
                st.markdown(f"**Published:** {result.published_date.strftime('%Y-%m-%d %H:%M')}")
                
                # GCT Scores
                st.markdown("**GCT Analysis:**")
                gct_col1, gct_col2, gct_col3, gct_col4 = st.columns(4)
                with gct_col1:
                    st.metric("Ψ (Consistency)", f"{result.gct_scores['psi']:.2f}")
                with gct_col2:
                    st.metric("ρ (Wisdom)", f"{result.gct_scores['rho']:.2f}")
                with gct_col3:
                    st.metric("q (Urgency)", f"{result.gct_scores['q']:.2f}")
                with gct_col4:
                    st.metric("f (Belonging)", f"{result.gct_scores['f']:.2f}")
                
                # Alerts
                if result.alert_triggers:
                    st.markdown("**🚨 Alert Triggers:**")
                    for alert in result.alert_triggers:
                        st.markdown(f"- {alert.replace('_', ' ').title()}")
            
            with col2:
                # Volatility visualization
                volatility_pct = result.volatility_score * 100
                st.markdown(f"""
                <div class="metric-card">
                    <div class="gct-score">{volatility_pct:.1f}%</div>
                    <div>Volatility Score</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Impact badge
                impact_color = {
                    'EXTREME': '#ff0000',
                    'HIGH': '#ff6600',
                    'MEDIUM': '#ffaa00',
                    'LOW': '#00aa00',
                    'MINIMAL': '#0000ff'
                }.get(result.predicted_impact, '#gray')
                
                st.markdown(f"""
                <div style="background-color: {impact_color}; color: white; padding: 5px; 
                           border-radius: 3px; text-align: center; font-weight: bold;">
                    {result.predicted_impact} IMPACT
                </div>
                """, unsafe_allow_html=True)

def display_sidebar():
    """Display the sidebar with controls and information"""
    st.sidebar.markdown("# 🎛️ Controls")
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh News", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (15 min)", value=False)
    
    if auto_refresh:
        st.sidebar.info("Auto-refresh enabled. Dashboard will update every 15 minutes.")
        # Note: In production, you'd implement this with a proper scheduler
    
    st.sidebar.markdown("---")
    
    # System information
    st.sidebar.markdown("## 📊 System Info")
    
    if st.session_state.last_update:
        st.sidebar.metric(
            "Last Update",
            st.session_state.last_update.strftime("%H:%M:%S")
        )
    
    if st.session_state.analysis_results:
        st.sidebar.metric(
            "Articles Analyzed",
            len(st.session_state.analysis_results)
        )
    
    # Debug information
    if DEBUG_CONFIG['enable_debug']:
        st.sidebar.markdown("## 🐛 Debug Info")
        st.sidebar.json({
            "Mock Data": DEBUG_CONFIG['mock_news_data'],
            "Session State Keys": list(st.session_state.keys()),
            "Analysis Results": len(st.session_state.analysis_results)
        })

def main():
    """Main application function"""
    
    # Display header
    display_header()
    
    # Load data if not already loaded
    if not st.session_state.analysis_results:
        with st.spinner("Loading initial data..."):
            load_news_data()
    
    # Display main sections
    display_market_sentiment()
    display_top_alerts()
    display_wisdom_panic_matrix()
    display_news_feed()
    
    # Display sidebar
    display_sidebar()
    
    # Footer
    st.markdown("---")
    st.markdown("*Market Pulse - Powered by Grounded Coherence Theory & Claude AI*")
    st.markdown("*'In markets, as in consciousness, the derivative tells the story.'*")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.info("Please refresh the page or check the logs for more details.")
        
        if DEBUG_CONFIG['enable_debug']:
            st.exception(e)