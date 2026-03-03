#!/usr/bin/env python3
"""
Test script for Intelligent AI Agent
Verifies all components are working properly
"""

import os
import sys
from pathlib import Path

def test_dependencies():
    """Test if all dependencies are installed"""
    print("\n" + "="*60)
    print("🧪 TESTING INTELLIGENT AI AGENT")
    print("="*60)
    
    print("\n📦 Checking dependencies...\n")
    
    dependencies = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('qrcode', 'QRCode'),
        ('pydantic', 'Pydantic'),
        ('anthropic', 'Anthropic'),
        ('openpyxl', 'OpenPyXL'),
        ('git', 'GitPython'),
    ]
    
    all_ok = True
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"   ✓ {display_name:20} installed")
        except ImportError:
            print(f"   ✗ {display_name:20} MISSING")
            all_ok = False
    
    return all_ok

def test_api_key():
    """Test if API key is configured"""
    print("\n🔑 Checking API configuration...\n")
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    github_token = os.getenv('GITHUB_TOKEN')
    
    if api_key:
        print(f"   ✓ ANTHROPIC_API_KEY: {'set (first 10 chars: ' + api_key[:10] + '...)'}")
    else:
        print(f"   ✗ ANTHROPIC_API_KEY: NOT SET")
        print(f"      Get from: https://console.anthropic.com/api_keys")
        print(f"      Then run: export ANTHROPIC_API_KEY='sk-ant-...'")
    
    if github_token:
        print(f"   ✓ GITHUB_TOKEN: set (optional)")
    else:
        print(f"   ℹ️  GITHUB_TOKEN: not set (optional, for auto PR)")
    
    return bool(api_key)

def test_imports():
    """Test if AI Agent modules can be imported"""
    print("\n📚 Checking AI Agent modules...\n")
    
    modules = [
        ('requirements_reader', 'RequirementsReader'),
        ('codebase_analyzer', 'CodebaseAnalyzer'),
        ('claude_codegen', 'ClaudeCodeGen'),
        ('enhanced_pr_creator', 'EnhancedPRCreator'),
        ('intelligent_agent', 'IntelligentAgent'),
    ]
    
    all_ok = True
    for module_name, class_name in modules:
        try:
            exec(f"from ai_agent.{module_name} import {class_name}")
            print(f"   ✓ {class_name:25} loaded")
        except Exception as e:
            print(f"   ✗ {class_name:25} FAILED: {str(e)[:40]}")
            all_ok = False
    
    return all_ok

def test_requirements_file():
    """Test if requirements file exists"""
    print("\n📝 Checking requirements file...\n")
    
    req_file = Path('requirements/features.txt')
    if req_file.exists():
        print(f"   ✓ requirements/features.txt exists")
        with open(req_file, 'r') as f:
            lines = f.readlines()
        print(f"   ✓ Contains {len(lines)} feature(s)")
        for i, line in enumerate(lines[:3], 1):
            print(f"      {i}. {line.strip()[:50]}")
        if len(lines) > 3:
            print(f"      ... and {len(lines)-3} more")
        return True
    else:
        print(f"   ✗ requirements/features.txt NOT FOUND")
        print(f"\n   Creating sample requirements file...")
        req_file.parent.mkdir(exist_ok=True)
        
        sample = """User Authentication | JWT-based login system | High
Database Integration | PostgreSQL with SQLAlchemy | High
Analytics Dashboard | Usage statistics and charts | Medium
Email Notifications | Send QR codes via email | Low
"""
        with open(req_file, 'w') as f:
            f.write(sample)
        
        print(f"   ✓ Created requirements/features.txt with sample data")
        return True

def test_git_repo():
    """Test if git repository is initialized"""
    print("\n🔗 Checking Git repository...\n")
    
    try:
        import subprocess
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✓ Git repository initialized")
            return True
        else:
            print(f"   ✗ Git repository not initialized")
            return False
    except Exception as e:
        print(f"   ✗ Git not found: {e}")
        return False

def main():
    """Run all tests"""
    tests = [
        ("Dependencies", test_dependencies),
        ("API Configuration", test_api_key),
        ("Requirements File", test_requirements_file),
        ("Git Repository", test_git_repo),
        ("AI Agent Modules", test_imports),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓" if result else "✗"
        print(f"   {status} {name}")
    
    print(f"\n   Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED! Ready to run Intelligent Agent")
        print("\nNext step: python -m ai_agent.intelligent_agent")
        return 0
    else:
        print("\n⚠️  Some tests failed. Fix issues above before running.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
