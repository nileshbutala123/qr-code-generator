#!/usr/bin/env python3
"""
Mock Test for Intelligent AI Agent
Tests basic functionality without needing API keys
"""

import os
import sys
from pathlib import Path

print("\n" + "="*70)
print("🤖 INTELLIGENT AI AGENT - SETUP VERIFICATION")
print("="*70)

# Check requirements file
print("\n📋 Requirements File:")
req_file = Path('requirements/features.txt')
if req_file.exists():
    print(f"   ✓ Found: {req_file}")
    with open(req_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    print(f"   ✓ Contains {len(lines)} requirements")
else:
    print(f"   ✗ NOT FOUND: {req_file}")

# Check AI Agent files
print("\n📁 AI Agent Modules:")
agent_dir = Path('ai-agent')
required_files = [
    'intelligent_agent.py',
    'codebase_analyzer.py',
    'claude_codegen.py',
    'enhanced_pr_creator.py',
]

for file in required_files:
    full_path = agent_dir / file
    if full_path.exists():
        size = full_path.stat().st_size
        print(f"   ✓ {file:30} ({size:,} bytes)")
    else:
        print(f"   ✗ {file:30} MISSING")

# Check git
print("\n🔗 Git Repository:")
git_dir = Path('.git')
if git_dir.exists():
    print(f"   ✓ Initialized")
else:
    print(f"   ✗ NO t initialized")

# Check API Key
print("\n🔑 Environment Variables:")
api_key = os.getenv('ANTHROPIC_API_KEY')
if api_key:
    print(f"   ✓ ANTHROPIC_API_KEY: {api_key[:7]}...{api_key.split('-')[-1]}")
else:
    print(f"   ✗ ANTHROPIC_API_KEY: NOT SET")
    print(f"      → Get from: https://console.anthropic.com/api_keys")
    print(f"      → Run: $env:ANTHROPIC_API_KEY='sk-ant-...'")

# Check documentation
print("\n📚 Documentation:")
docs = ['INTELLIGENT_AGENT.md', 'SETUP_COMPLETE.md', 'IMPLEMENTATION_SUMMARY.md']
for doc in docs:
    if Path(doc).exists():
        print(f"   ✓ {doc}")

print("\n" + "="*70)
print("✅ SETUP VERIFICATION COMPLETE")
print("="*70)

print("\n📖 TO RUN THE AGENT:")
print("""
1. Set your Claude API key:
   $env:ANTHROPIC_API_KEY='sk-ant-your-key-here'

2. Run the intelligent agent:
   python -m ai_agent.intelligent_agent

3. Or use quick start:
   python quickstart_agent.py

The agent will:
✓ Analyze your FastAPI QR code repository
✓ Use Claude AI to understand requirements
✓ Ask for your approval before making changes
✓ Create a GitHub PR automatically
""")

print("\n📚 For more info, read: INTELLIGENT_AGENT.md")
