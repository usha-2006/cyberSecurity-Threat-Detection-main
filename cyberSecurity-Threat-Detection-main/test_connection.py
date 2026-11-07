#!/usr/bin/env python3
"""
Test script to verify both API and dashboard servers are working.
"""

import requests
import time

def test_api_connection():
    """Test if the API server is responding."""
    print("🔍 Testing API Connection...")
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ API Server is running and responding!")
            return True
        else:
            print(f"❌ API Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API Server is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        return False

def test_dashboard_connection():
    """Test if the dashboard server is responding."""
    print("\n🌐 Testing Dashboard Connection...")
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard Server is running and responding!")
            return True
        else:
            print(f"❌ Dashboard Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Dashboard Server is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Dashboard: {e}")
        return False

def test_detection_endpoint():
    """Test the detection endpoint."""
    print("\n🎯 Testing Detection Endpoint...")
    try:
        test_data = {
            "data": {
                "source_ip": "192.168.1.100",
                "destination_ip": "10.0.0.50",
                "protocol": "TCP",
                "port": 80
            },
            "request_id": f"test_{int(time.time())}"
        }
        
        response = requests.post('http://localhost:8000/detect', json=test_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            threats = result.get('threats', [])
            if threats:
                threat = threats[0]
                print(f"✅ Detection working! Found: {threat.get('name', 'Unknown')}")
                print(f"   Solutions: {len(threat.get('solutions', []))} steps")
            else:
                print("✅ Detection working! No threats detected (clean traffic)")
            return True
        else:
            print(f"❌ Detection endpoint error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing detection: {e}")
        return False

def main():
    """Run all connection tests."""
    print("🧪 Testing Enhanced Threat Detection System Connections")
    print("=" * 60)
    
    api_ok = test_api_connection()
    dashboard_ok = test_dashboard_connection()
    
    if api_ok:
        detection_ok = test_detection_endpoint()
    else:
        detection_ok = False
    
    print("\n" + "=" * 60)
    print("📊 Connection Test Results:")
    print(f"   API Server (port 8000): {'✅ OK' if api_ok else '❌ FAILED'}")
    print(f"   Dashboard Server (port 3000): {'✅ OK' if dashboard_ok else '❌ FAILED'}")
    print(f"   Detection Endpoint: {'✅ OK' if detection_ok else '❌ FAILED'}")
    
    if api_ok and dashboard_ok:
        print("\n🎉 Both servers are running!")
        print("🌐 Open your browser to: http://localhost:3000")
        print("🎲 Try the 'Analyze Threat' button to see random detection!")
    else:
        print("\n💡 Troubleshooting:")
        if not api_ok:
            print("   - Start API server: python -m src.api.main")
        if not dashboard_ok:
            print("   - Start Dashboard server: python serve_dashboard.py")

if __name__ == "__main__":
    main()
