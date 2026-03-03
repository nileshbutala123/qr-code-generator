#!/usr/bin/env python3
"""
Quick Start Guide for Intelligent AI Agent
==========================================

Run this script to get started with AI-powered code generation!
"""

import os
import sys
from pathlib import Path


def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment...\n")
    
    checks = {
        "Python 3.8+": sys.version_info >= (3, 8),
        "ANTHROPIC_API_KEY set": bool(os.getenv('ANTHROPIC_API_KEY')),
        "Git installed": os.system('git --version > /dev/null 2>&1') == 0,
        "requirements/features.txt exists": Path('requirements/features.txt').exists(),
    }
    
    all_good = True
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
        if not passed:
            all_good = False
    
    print()
    return all_good


def setup_instructions():
    """Show setup instructions"""
    print("📋 Setup Instructions\n")
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt\n")
    
    print("2. Set your Anthropic API key:")
    print("   export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxx'")
    print("   (Get from: https://console.anthropic.com/api_keys)\n")
    
    print("3. Create a requirements file (requirements/features.txt):")
    print("   Feature Name | Description | Priority\n")
    
    print("4. Run the agent:")
    print("   python -m ai_agent.intelligent_agent\n")


def run_demo():
    """Run a demo"""
    print("🚀 Running Intelligent Agent...\n")
    
    try:
        from ai_agent.intelligent_agent import IntelligentAgent
        
        # Check requirements file
        if not Path('requirements/features.txt').exists():
            print("⚠️  requirements/features.txt not found!")
            print("Creating sample file...\n")
            
            sample_content = """User Authentication | Implement JWT-based login | High
Database Integration | Store QR codes in database | High
Analytics Dashboard | Display usage statistics | Medium
API Rate Limiting | Prevent abuse with rate limits | Medium
"""
            
            Path('requirements').mkdir(exist_ok=True)
            with open('requirements/features.txt', 'w') as f:
                f.write(sample_content)
            print("✓ Created sample requirements/features.txt")
        
        # Run agent
        agent = IntelligentAgent(
            requirements_file="requirements/features.txt"
        )
        
        result = agent.run(interactive=True)
        
        if result['success']:
            print(f"\n✅ Success!")
            print(f"   Session: {result['session_id']}")
            print(f"   Requirements: {result['requirements_processed']}")
            print(f"   Changes: {result['changes_generated']}")
        else:
            print(f"\n❌ Error: {result.get('error')}")
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure requirements are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🤖 INTELLIGENT AI AGENT - Quick Start")
    print("="*60 + "\n")
    
    # Check environment
    if not check_environment():
        print("⚠️  Some checks failed. See setup instructions below.\n")
        setup_instructions()
        return
    
    print("✅ Environment looks good!\n")
    
    # Ask user
    response = input("Would you like to run the agent now? (yes/no): ").strip().lower()
    
    if response in ['y', 'yes']:
        run_demo()
    else:
        print("\nFor more information, see INTELLIGENT_AGENT.md")


if __name__ == "__main__":
    main()
