#!/usr/bin/env python3
"""
SnapChef Setup Test Script
Tests if all components are properly configured and running
"""

import requests
import time
import sys
import json
from urllib.parse import urljoin

def test_service(url, service_name, timeout=10):
    """Test if a service is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {service_name} is running at {url}")
            return True
        else:
            print(f"❌ {service_name} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name} is not responding: {e}")
        return False

def test_api_endpoint(url, endpoint, service_name):
    """Test specific API endpoint"""
    try:
        full_url = urljoin(url, endpoint)
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {service_name} endpoint {endpoint} is working")
            return True
        else:
            print(f"❌ {service_name} endpoint {endpoint} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name} endpoint {endpoint} failed: {e}")
        return False

def test_recipe_search():
    """Test recipe search functionality"""
    try:
        search_url = "http://localhost:8000/search"
        search_data = {
            "dish_name": "biryani",
            "filters": None
        }
        
        response = requests.post(search_url, json=search_data, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recipe search is working - found {data.get('total_found', 0)} results")
            return True
        else:
            print(f"❌ Recipe search failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Recipe search failed: {e}")
        return False

def main():
    """Main test function"""
    print("🍳 SnapChef Setup Test")
    print("=" * 50)
    
    # Test services
    services = [
        ("http://localhost:3000", "Frontend"),
        ("http://localhost:8000", "Backend API"),
        ("http://localhost:6379", "Redis"),
        ("http://localhost:9200", "Elasticsearch")
    ]
    
    all_services_running = True
    
    for url, name in services:
        if not test_service(url, name):
            all_services_running = False
    
    if not all_services_running:
        print("\n❌ Some services are not running. Please check Docker containers.")
        print("Run: docker-compose ps")
        sys.exit(1)
    
    # Test API endpoints
    print("\n🔍 Testing API Endpoints...")
    api_endpoints = [
        ("http://localhost:8000", "/health", "Health Check"),
        ("http://localhost:8000", "/docs", "API Documentation"),
        ("http://localhost:8000", "/recipes/popular", "Popular Recipes"),
        ("http://localhost:8000", "/stats", "System Stats")
    ]
    
    for base_url, endpoint, name in api_endpoints:
        test_api_endpoint(base_url, endpoint, name)
    
    # Test recipe search
    print("\n🔍 Testing Recipe Search...")
    if test_recipe_search():
        print("\n🎉 All tests passed! SnapChef is ready to use.")
        print("\n📱 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📊 API Docs: http://localhost:8000/docs")
    else:
        print("\n❌ Recipe search test failed. Check the logs for more details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
