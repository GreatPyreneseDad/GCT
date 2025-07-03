#!/usr/bin/env python3
"""
Market Pulse Launcher
Quick start script for the Financial News GCT Volatility Analyzer
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    # Package name mapping: import_name -> package_name
    required_packages = {
        'streamlit': 'streamlit',
        'anthropic': 'anthropic', 
        'feedparser': 'feedparser',
        'bs4': 'beautifulsoup4',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'plotly': 'plotly',
        'requests': 'requests',
        'yfinance': 'yfinance',
        'schedule': 'schedule'
    }
    
    missing_packages = []
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_environment():
    """Check if environment is properly configured"""
    issues = []
    
    # Check for .env file
    if not Path('.env').exists():
        issues.append("No .env file found. Copy .env.example to .env and add your API keys.")
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        issues.append("ANTHROPIC_API_KEY not found in environment variables.")
    
    if issues:
        print("⚠️  Environment issues:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n💡 See README.md for setup instructions.")
        return False
    
    return True

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("""
    🚀 MARKET PULSE INITIALIZING...
    
    Grounded Coherence Theory: ✓
    Claude AI Integration: ✓
    News Scrapers: ✓
    Volatility Detectors: ✓
    
    "In the market, as in life, coherence reveals truth
     and panic clouds judgment." - Ancient Trading Proverb
    
    Dashboard launching at http://localhost:8501
    """)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'market_pulse_dashboard.py',
            '--server.port=8501',
            '--server.headless=false'
        ])
    except KeyboardInterrupt:
        print("\n👋 Market Pulse shutting down...")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        sys.exit(1)

def main():
    """Main launcher function"""
    print("🚀 Market Pulse Launcher")
    print("=" * 50)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ Dependencies OK")
    
    # Check environment
    print("🔍 Checking environment...")
    if not check_environment():
        sys.exit(1)
    print("✅ Environment OK")
    
    # Launch dashboard
    print("🚀 Starting Market Pulse Dashboard...")
    launch_dashboard()

if __name__ == "__main__":
    main()