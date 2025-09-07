#!/usr/bin/env python3
"""
Simple API test script for Agent Mira
Tests the core functionality of the property recommendation system
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_model_info():
    """Test ML model info endpoint"""
    print("🔍 Testing ML model info...")
    try:
        response = requests.get(f"{API_BASE}/api/ml/model-info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model info retrieved: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Model info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model info error: {str(e)}")
        return False

def test_properties():
    """Test properties endpoint"""
    print("🔍 Testing properties endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/properties")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {len(data)} properties")
            return True
        else:
            print(f"❌ Properties failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Properties error: {str(e)}")
        return False

def test_preferences():
    """Test preferences submission"""
    print("🔍 Testing preferences submission...")
    try:
        preferences = {
            "session_id": "test_session_123",
            "budget": 500000,
            "location": "New York, NY",
            "min_bedrooms": 2,
            "max_commute_time": 30,
            "min_school_rating": 7.0,
            "preferred_amenities": ["Gym", "Pool", "Parking"]
        }
        
        response = requests.post(
            f"{API_BASE}/api/preferences",
            json=preferences
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Preferences submitted: {data.get('message', 'Success')}")
            return data.get('session_id')
        else:
            print(f"❌ Preferences failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Preferences error: {str(e)}")
        return None

def test_recommendations(session_id):
    """Test recommendations endpoint"""
    print("🔍 Testing recommendations...")
    try:
        response = requests.get(
            f"{API_BASE}/api/recommendations",
            params={"session_id": session_id, "top_n": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {len(data)} recommendations")
            
            # Show top recommendation
            if data:
                top_rec = data[0]
                print(f"   Top recommendation: {top_rec['property']['title']}")
                print(f"   Score: {top_rec['total_score']}")
                print(f"   Reasoning: {top_rec['reasoning']}")
            
            return True
        else:
            print(f"❌ Recommendations failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Recommendations error: {str(e)}")
        return False

def test_price_prediction():
    """Test price prediction endpoint"""
    print("🔍 Testing price prediction...")
    try:
        features = {
            "bedrooms": 3,
            "bathrooms": 2,
            "size_sqft": 1500,
            "year_built": 2020,
            "location": "New York, NY",
            "amenities": ["Gym", "Pool"]
        }
        
        response = requests.post(
            f"{API_BASE}/api/ml/predict-price",
            json=features
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Price predicted: ${data.get('predicted_price', 0):,.2f}")
            return True
        else:
            print(f"❌ Price prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Price prediction error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Agent Mira API Test Suite")
    print("=" * 40)
    
    # Wait a moment for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(3)
    
    tests_passed = 0
    total_tests = 6
    
    # Run tests
    if test_health():
        tests_passed += 1
    
    if test_model_info():
        tests_passed += 1
    
    if test_properties():
        tests_passed += 1
    
    session_id = test_preferences()
    if session_id:
        tests_passed += 1
        
        if test_recommendations(session_id):
            tests_passed += 1
    else:
        print("⚠️  Skipping recommendations test due to preferences failure")
    
    if test_price_prediction():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
        print("   Make sure the backend is running: docker-compose up -d")
        print("   Check logs: docker-compose logs backend")

if __name__ == "__main__":
    main()
