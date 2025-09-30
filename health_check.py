#!/usr/bin/env python3
"""
SnapChef Health Check Script
Monitors the health of all services
"""

import requests
import time
import json
from datetime import datetime

def check_service_health():
    """Check health of all services"""
    services = {
        "frontend": "http://localhost:3000",
        "backend": "http://localhost:8000/health",
        "redis": "http://localhost:6379",
        "elasticsearch": "http://localhost:9200/_cluster/health"
    }
    
    health_status = {}
    
    for service, url in services.items():
        try:
            if service == "redis":
                # Redis doesn't have HTTP endpoint, skip for now
                health_status[service] = {"status": "unknown", "message": "Redis check not implemented"}
                continue
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                health_status[service] = {
                    "status": "healthy",
                    "response_time": response.elapsed.total_seconds(),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                health_status[service] = {
                    "status": "unhealthy",
                    "status_code": response.status_code,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            health_status[service] = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    return health_status

def main():
    """Main health check function"""
    print(f"🏥 SnapChef Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    health = check_service_health()
    
    for service, status in health.items():
        if status["status"] == "healthy":
            print(f"✅ {service.upper()}: {status['status']} ({status['response_time']:.2f}s)")
        elif status["status"] == "unhealthy":
            print(f"❌ {service.upper()}: {status['status']} (HTTP {status['status_code']})")
        else:
            print(f"⚠️  {service.upper()}: {status['status']} - {status.get('error', 'Unknown error')}")
    
    # Save health status to file
    with open('health_status.json', 'w') as f:
        json.dump(health, f, indent=2)
    
    print(f"\n📊 Health status saved to health_status.json")

if __name__ == "__main__":
    main()
