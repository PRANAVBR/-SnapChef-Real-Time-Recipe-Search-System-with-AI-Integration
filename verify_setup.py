#!/usr/bin/env python3
"""
SnapChef Setup Verification Script
Comprehensive verification of all components
"""

import requests
import time
import json
import sys
import os
from datetime import datetime
from urllib.parse import urljoin

class SnapChefVerifier:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "endpoints": {},
            "overall_status": "unknown"
        }
    
    def verify_docker_containers(self):
        """Verify Docker containers are running"""
        print("🐳 Checking Docker containers...")
        
        try:
            import subprocess
            result = subprocess.run(['docker-compose', 'ps'], capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                running_containers = [line for line in lines if 'Up' in line]
                
                expected_containers = ['snapchef-backend', 'snapchef-frontend', 'redis', 'elasticsearch', 'pathway-pipeline']
                
                for container in expected_containers:
                    if any(container in line for line in running_containers):
                        print(f"✅ {container} is running")
                        self.results["services"][container] = "running"
                    else:
                        print(f"❌ {container} is not running")
                        self.results["services"][container] = "not_running"
                
                return len([c for c in expected_containers if any(c in line for line in running_containers)]) == len(expected_containers)
            else:
                print("❌ Failed to check Docker containers")
                return False
                
        except Exception as e:
            print(f"❌ Error checking Docker containers: {e}")
            return False
    
    def verify_service(self, url, name, timeout=10):
        """Verify a service is responding"""
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                print(f"✅ {name} is responding at {url}")
                self.results["services"][name] = {
                    "status": "healthy",
                    "url": url,
                    "response_time": response.elapsed.total_seconds()
                }
                return True
            else:
                print(f"❌ {name} returned status {response.status_code}")
                self.results["services"][name] = {
                    "status": "unhealthy",
                    "url": url,
                    "status_code": response.status_code
                }
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ {name} is not responding: {e}")
            self.results["services"][name] = {
                "status": "error",
                "url": url,
                "error": str(e)
            }
            return False
    
    def verify_api_endpoints(self):
        """Verify API endpoints are working"""
        print("\n🔍 Verifying API endpoints...")
        
        base_url = "http://localhost:8000"
        endpoints = [
            ("/health", "Health Check"),
            ("/docs", "API Documentation"),
            ("/recipes/popular", "Popular Recipes"),
            ("/stats", "System Statistics")
        ]
        
        all_working = True
        
        for endpoint, name in endpoints:
            try:
                url = urljoin(base_url, endpoint)
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ {name} endpoint is working")
                    self.results["endpoints"][endpoint] = {
                        "status": "working",
                        "response_time": response.elapsed.total_seconds()
                    }
                else:
                    print(f"❌ {name} endpoint returned status {response.status_code}")
                    self.results["endpoints"][endpoint] = {
                        "status": "error",
                        "status_code": response.status_code
                    }
                    all_working = False
                    
            except Exception as e:
                print(f"❌ {name} endpoint failed: {e}")
                self.results["endpoints"][endpoint] = {
                    "status": "error",
                    "error": str(e)
                }
                all_working = False
        
        return all_working
    
    def test_recipe_search(self):
        """Test recipe search functionality"""
        print("\n🍳 Testing recipe search...")
        
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
                
                if data.get('results'):
                    print("📋 Sample results:")
                    for i, recipe in enumerate(data['results'][:2], 1):
                        print(f"  {i}. {recipe.get('title', 'Unknown')} ({recipe.get('source', 'Unknown')})")
                
                self.results["recipe_search"] = {
                    "status": "working",
                    "results_found": data.get('total_found', 0),
                    "response_time": response.elapsed.total_seconds()
                }
                return True
            else:
                print(f"❌ Recipe search failed with status {response.status_code}")
                self.results["recipe_search"] = {
                    "status": "error",
                    "status_code": response.status_code
                }
                return False
                
        except Exception as e:
            print(f"❌ Recipe search failed: {e}")
            self.results["recipe_search"] = {
                "status": "error",
                "error": str(e)
            }
            return False
    
    def check_environment(self):
        """Check environment configuration"""
        print("\n⚙️ Checking environment configuration...")
        
        env_file = ".env"
        if os.path.exists(env_file):
            print("✅ .env file exists")
            
            with open(env_file, 'r') as f:
                env_content = f.read()
                
            if "HUGGINGFACE_API_KEY" in env_content:
                if "your_huggingface_api_key_here" in env_content:
                    print("⚠️  Hugging Face API key not configured")
                    return False
                else:
                    print("✅ Hugging Face API key is configured")
                    return True
            else:
                print("❌ Hugging Face API key not found in .env")
                return False
        else:
            print("❌ .env file not found")
            return False
    
    def save_results(self):
        """Save verification results"""
        with open('verification_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📊 Verification results saved to verification_results.json")
    
    def run_verification(self):
        """Run complete verification"""
        print("🍳 SnapChef Setup Verification")
        print("=" * 50)
        
        # Check environment
        env_ok = self.check_environment()
        
        # Check Docker containers
        docker_ok = self.verify_docker_containers()
        
        if not docker_ok:
            print("\n❌ Docker containers are not running properly.")
            print("Please run: docker-compose up -d")
            self.results["overall_status"] = "failed"
            self.save_results()
            return False
        
        # Wait a bit for services to fully start
        print("\n⏳ Waiting for services to fully initialize...")
        time.sleep(10)
        
        # Verify services
        services = [
            ("http://localhost:3000", "Frontend"),
            ("http://localhost:8000", "Backend API"),
            ("http://localhost:9200", "Elasticsearch")
        ]
        
        all_services_ok = True
        for url, name in services:
            if not self.verify_service(url, name):
                all_services_ok = False
        
        # Verify API endpoints
        api_ok = self.verify_api_endpoints()
        
        # Test recipe search
        search_ok = self.test_recipe_search()
        
        # Determine overall status
        if all_services_ok and api_ok and search_ok:
            self.results["overall_status"] = "success"
            print("\n🎉 All verifications passed! SnapChef is ready to use.")
            print("\n📱 Frontend: http://localhost:3000")
            print("🔧 Backend API: http://localhost:8000")
            print("📊 API Docs: http://localhost:8000/docs")
            return True
        else:
            self.results["overall_status"] = "failed"
            print("\n❌ Some verifications failed. Check the details above.")
            return False

def main():
    verifier = SnapChefVerifier()
    success = verifier.run_verification()
    verifier.save_results()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
