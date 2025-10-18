#!/usr/bin/env python3
"""
Quick Web App Test
Test if CollegiumAI web app is working
"""

import requests
import json
import time

def test_web_app():
    """Test the CollegiumAI web app"""
    
    base_url = "http://localhost:8080"
    
    print("🌐 Testing CollegiumAI Web App")
    print("=" * 40)
    
    # Test endpoints
    endpoints = [
        "/health",
        "/docs",  # FastAPI auto-generated documentation
        "/openapi.json"  # OpenAPI schema
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\n🧪 Testing: {url}")
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Status: {response.status_code} OK")
                
                # Try to parse JSON response
                try:
                    data = response.json()
                    if endpoint == "/health":
                        print(f"📊 Health: {data.get('status', 'Unknown')}")
                        print(f"⚡ Server: {data.get('server', 'CollegiumAI')}")
                        print(f"📅 Timestamp: {data.get('timestamp', 'N/A')}")
                    elif endpoint == "/openapi.json":
                        print(f"📚 API Title: {data.get('info', {}).get('title', 'N/A')}")
                        print(f"🔢 API Version: {data.get('info', {}).get('version', 'N/A')}")
                    else:
                        print(f"📄 Response length: {len(str(data))} characters")
                except:
                    print(f"📄 Response length: {len(response.text)} characters")
                    
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"📄 Response: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection failed - Server not running on {base_url}")
            return False
        except requests.exceptions.Timeout:
            print(f"⏰ Request timeout")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def check_server_running():
    """Check if server is running"""
    try:
        response = requests.get("http://localhost:8080/health", timeout=2)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🔍 Checking if CollegiumAI server is running...")
    
    if check_server_running():
        print("✅ Server is running!")
        test_web_app()
        
        print("\n" + "=" * 40)
        print("🎉 WEB APP IS WORKING! 🎉")
        print("=" * 40)
        print("🌐 Access your CollegiumAI web app at:")
        print("   http://localhost:8080")
        print("📚 API Documentation:")
        print("   http://localhost:8080/docs")
        print("🔗 Interactive API:")
        print("   http://localhost:8080/redoc")
        print("=" * 40)
        
    else:
        print("❌ Server is not running.")
        print("\n💡 To start the server:")
        print("   python api/server.py --port 8080")
        print("\n🐳 Or use Docker:")
        print("   docker-compose up -d")