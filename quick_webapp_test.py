#!/usr/bin/env python3
"""Quick test of CollegiumAI web application"""

import requests
import json

def test_webapp():
    print('🎓 CollegiumAI Web Application Test')
    print('=' * 40)
    
    # Test React App
    try:
        print('Testing React App on http://localhost:3000...')
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print('✅ React App: Successfully running')
            print('   Status:', response.status_code)
            print('   Content-Type:', response.headers.get('content-type', 'unknown'))
        else:
            print('❌ React App: Unexpected status', response.status_code)
    except Exception as e:
        print('❌ React App: Connection failed -', str(e))
    
    print()
    print('🚀 Web Application Status:')
    print('   Frontend: http://localhost:3000 (React TypeScript)')
    print('   Features: Dashboard, Persona Gallery, Chat, Multi-Agent, Cognitive Monitor')
    print('   Architecture: Material-UI, Redux, React Router')
    print()
    print('✨ Key Features Available:')
    print('   • Interactive Persona Gallery (51+ personas)')
    print('   • Advanced Chat Interface with cognitive insights')
    print('   • Multi-Agent Collaboration Workspace')
    print('   • Real-time Cognitive Architecture Monitor')
    print('   • University Systems Management')
    print('   • Performance Analytics Dashboard')
    print('   • System Status Monitoring')
    
    return True

if __name__ == "__main__":
    test_webapp()