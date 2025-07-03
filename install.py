#!/usr/bin/env python3
"""
Market Pulse Installation Script
Automated setup for the Financial News GCT Volatility Analyzer
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("⚠️  Not in a virtual environment. Creating one...")
        try:
            # Create virtual environment
            subprocess.check_call([sys.executable, '-m', 'venv', 'market_pulse_env'])
            print("✅ Virtual environment created")
            print("🔄 Please run the following commands:")
            print("   source market_pulse_env/bin/activate")
            print("   python install.py")
            return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating virtual environment: {e}")
            return False
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup_environment():
    """Set up environment configuration"""
    print("🔧 Setting up environment...")
    
    # Copy .env.example to .env if it doesn't exist
    if not Path('.env').exists():
        if Path('.env.example').exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("⚠️  Please edit .env and add your Anthropic API key")
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✅ .env file already exists")
    
    # Create data and logs directories
    for directory in ['data', 'logs']:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")
    
    return True

def verify_installation():
    """Verify that installation was successful"""
    print("🔍 Verifying installation...")
    
    try:
        # Test imports
        from modules import create_scraper, MarketPulseAnalyzer
        print("✅ Core modules can be imported")
        
        # Test basic functionality
        scraper = create_scraper()
        analyzer = MarketPulseAnalyzer()
        print("✅ Components can be instantiated")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Market Pulse Installation")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    steps = [
        ("Installing Dependencies", install_dependencies),
        ("Setting up Environment", setup_environment),
        ("Verifying Installation", verify_installation)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ {step_name} failed")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Installation completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your Anthropic API key")
    print("2. Run: python test_system.py")
    print("3. Run: python launch.py")
    print("\nFor detailed instructions, see QUICKSTART.md")

if __name__ == "__main__":
    main()