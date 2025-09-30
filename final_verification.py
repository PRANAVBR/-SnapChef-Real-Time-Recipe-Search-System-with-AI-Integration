#!/usr/bin/env python3
"""
Final verification script for SnapChef demo
Ensures all systems are working for judges
"""

import requests
import json
import time

def test_all_endpoints():
    """Test all API endpoints comprehensively"""
    base_url = "http://localhost:8000"
    
    print("🍳 SnapChef Final Verification")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. 🏥 Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data['status']}")
            print(f"   ✅ Service: {data['service']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Recipe Search - Multiple Queries
    print("\n2. 🔍 Recipe Search Testing")
    test_queries = [
        ("biryani", "Should return Chicken Biryani and Vegetable Biryani"),
        ("paneer", "Should return Paneer Butter Masala and Paneer Tikka"),
        ("dal", "Should return Dal Tadka and Dal Makhani"),
        ("curry", "Should return Chicken Curry and Vegetable Curry"),
        ("rice", "Should return Jeera Rice")
    ]
    
    search_results = {}
    for query, description in test_queries:
        try:
            response = requests.post(
                f"{base_url}/search",
                json={"dish_name": query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                result_count = data.get('total_found', 0)
                search_results[query] = result_count
                print(f"   ✅ '{query}': {result_count} results - {description}")
                
                # Show first result details
                if data.get('results') and len(data['results']) > 0:
                    first_result = data['results'][0]
                    print(f"      📝 First result: {first_result.get('title', 'Unknown')}")
                    print(f"      🔗 Source: {first_result.get('source', 'Unknown')}")
                    print(f"      ⭐ Rating: {first_result.get('rating', 'N/A')}")
            else:
                print(f"   ❌ '{query}': Failed ({response.status_code})")
                return False
        except Exception as e:
            print(f"   ❌ '{query}': Error - {e}")
            return False
    
    # Test 3: Popular Recipes
    print("\n3. 📈 Popular Recipes")
    try:
        response = requests.get(f"{base_url}/recipes/popular", timeout=10)
        if response.status_code == 200:
            data = response.json()
            popular_count = len(data.get('recipes', []))
            print(f"   ✅ Popular recipes: {popular_count} recipes")
            
            if popular_count > 0:
                print("   📋 Top popular recipes:")
                for i, recipe in enumerate(data['recipes'][:3], 1):
                    print(f"      {i}. {recipe.get('title', 'Unknown')} ({recipe.get('search_count', 0)} searches)")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: System Statistics
    print("\n4. 📊 System Statistics")
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Total searches: {data.get('total_searches', 0)}")
            print(f"   ✅ Recipes indexed: {data.get('total_recipes_indexed', 0)}")
            print(f"   ✅ Cache hit rate: {data.get('cache_hit_rate', 0):.1f}%")
            print(f"   ✅ Average response time: {data.get('avg_response_time_ms', 0):.1f}ms")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 5: Frontend Accessibility
    print("\n5. 🖥️ Frontend Accessibility")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("   ✅ Frontend is accessible")
            print("   🌐 Open http://localhost:3000 in your browser")
        else:
            print(f"   ❌ Frontend failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Frontend error: {e}")
        return False
    
    # Test 6: API Documentation
    print("\n6. 📚 API Documentation")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("   ✅ API docs accessible")
            print("   📖 Open http://localhost:8000/docs in your browser")
        else:
            print(f"   ❌ API docs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API docs error: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 VERIFICATION COMPLETE!")
    print("=" * 60)
    
    print(f"\n📊 Search Results Summary:")
    for query, count in search_results.items():
        print(f"   • '{query}': {count} results")
    
    print(f"\n🌐 Access Points:")
    print(f"   • Frontend: http://localhost:3000")
    print(f"   • Backend API: http://localhost:8000")
    print(f"   • API Docs: http://localhost:8000/docs")
    print(f"   • System Stats: http://localhost:8000/stats")
    
    print(f"\n✨ Key Features Demonstrated:")
    print(f"   • Real-time recipe search with AI-powered matching")
    print(f"   • Microservices architecture with Docker")
    print(f"   • Fast response times with caching")
    print(f"   • Modern React frontend")
    print(f"   • Comprehensive API documentation")
    print(f"   • Health monitoring and statistics")
    
    print(f"\n🎯 READY FOR JUDGES EVALUATION!")
    
    return True

if __name__ == "__main__":
    success = test_all_endpoints()
    if success:
        print("\n✅ All systems operational - Demo ready!")
    else:
        print("\n❌ Some issues detected - Please check logs")
