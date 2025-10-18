#!/usr/bin/env python3
"""
CollegiumAI Ollama Test Suite
===========================

Comprehensive test script for CollegiumAI Ollama integration.
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd, description):
    """Run a CLI command and display results"""
    print(f"\n🧪 {description}")
    print("=" * 60)
    print(f"Command: {cmd}")
    print("-" * 40)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🎓✨ CollegiumAI Ollama Integration Test Suite")
    print("=" * 80)
    
    base_cmd = "python ollama_integration.py"
    tests = [
        # Basic CLI tests
        (f"{base_cmd}", "Main CLI Interface"),
        (f"{base_cmd} --help", "Help System"),
        (f"{base_cmd} --version", "Version Info"),
        
        # Ollama service tests
        (f"{base_cmd} ollama status", "Ollama Service Status"),
        (f"{base_cmd} ollama models", "Available Models"),
        
        # Agent chat tests
        (f'{base_cmd} agent chat -a student_services -m "Hello"', "Student Services Chat"),
        (f'{base_cmd} agent chat -a bologna_process -m "Convert 60 ECTS"', "Bologna Process Chat"),
        
        # Student services tests
        (f'{base_cmd} student advise -n "Alice" -q "What is AI?"', "Academic Advising"),
        
        # Demo test
        (f"{base_cmd} demo", "Interactive Demo"),
        
        # Error handling test
        (f'{base_cmd} agent chat -a student_services -m "Test" --model "invalid"', "Error Handling"),
    ]
    
    passed = 0
    total = len(tests)
    
    for cmd, description in tests:
        success = run_command(cmd, description)
        if success:
            passed += 1
            print("✅ PASSED")
        else:
            print("❌ FAILED")
        
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 80)
    print(f"🎯 Test Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests PASSED! CollegiumAI Ollama integration is fully functional.")
    else:
        print(f"⚠️  {total-passed} tests failed. Review the output above.")
    
    print("=" * 80)

if __name__ == "__main__":
    main()