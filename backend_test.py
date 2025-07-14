#!/usr/bin/env python3
"""
Backend API Testing for EnviroIntel KE Environmental Monitoring Platform
Tests all API endpoints using the public URL from frontend/.env
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any

class EnviroIntelAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.tests_run = 0
        self.tests_passed = 0
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'EnviroIntel-API-Tester/1.0'
        })

    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}: PASSED {details}")
        else:
            print(f"❌ {test_name}: FAILED {details}")

    def test_endpoint(self, endpoint: str, expected_status: int = 200, method: str = "GET") -> tuple[bool, Dict[Any, Any]]:
        """Test a single API endpoint"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = self.session.get(url, timeout=10)
            else:
                response = self.session.request(method, url, timeout=10)
            
            success = response.status_code == expected_status
            data = {}
            
            if response.headers.get('content-type', '').startswith('application/json'):
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    data = {"error": "Invalid JSON response"}
            
            return success, data, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}, 0

    def test_root_endpoint(self):
        """Test root endpoint"""
        success, data, status = self.test_endpoint("/")
        expected_message = "EnviroIntel KE API - Environmental Cyber Intelligence Platform"
        
        if success and data.get("message") == expected_message:
            self.log_test("Root Endpoint", True, f"- Status: {status}")
            return True
        else:
            self.log_test("Root Endpoint", False, f"- Status: {status}, Data: {data}")
            return False

    def test_threats_endpoint(self):
        """Test /api/threats endpoint"""
        success, data, status = self.test_endpoint("/api/threats")
        
        if success and "threats" in data and isinstance(data["threats"], list):
            threats_count = len(data["threats"])
            self.log_test("All Threats Endpoint", True, f"- Status: {status}, Count: {threats_count}")
            
            # Validate threat structure
            if threats_count > 0:
                threat = data["threats"][0]
                required_fields = ["id", "type", "title", "description", "location", "severity", "confidence", "timestamp", "source", "status"]
                missing_fields = [field for field in required_fields if field not in threat]
                
                if not missing_fields:
                    self.log_test("Threat Data Structure", True, "- All required fields present")
                else:
                    self.log_test("Threat Data Structure", False, f"- Missing fields: {missing_fields}")
            
            return True, data["threats"]
        else:
            self.log_test("All Threats Endpoint", False, f"- Status: {status}, Data: {data}")
            return False, []

    def test_threats_by_type(self, threat_types: list):
        """Test /api/threats/{type} endpoints"""
        results = {}
        
        for threat_type in threat_types:
            success, data, status = self.test_endpoint(f"/api/threats/{threat_type}")
            
            if success and "threats" in data and isinstance(data["threats"], list):
                filtered_count = len(data["threats"])
                
                # Verify all threats are of the requested type
                if filtered_count > 0:
                    all_correct_type = all(threat.get("type") == threat_type for threat in data["threats"])
                    if all_correct_type:
                        self.log_test(f"Threats by Type ({threat_type})", True, f"- Status: {status}, Count: {filtered_count}")
                    else:
                        self.log_test(f"Threats by Type ({threat_type})", False, "- Contains threats of wrong type")
                else:
                    self.log_test(f"Threats by Type ({threat_type})", True, f"- Status: {status}, Count: 0 (no threats of this type)")
                
                results[threat_type] = filtered_count
            else:
                self.log_test(f"Threats by Type ({threat_type})", False, f"- Status: {status}, Data: {data}")
                results[threat_type] = 0
        
        return results

    def test_insights_endpoint(self):
        """Test /api/insights endpoint"""
        success, data, status = self.test_endpoint("/api/insights")
        
        if success and "insights" in data and isinstance(data["insights"], list):
            insights_count = len(data["insights"])
            self.log_test("Predictive Insights Endpoint", True, f"- Status: {status}, Count: {insights_count}")
            
            # Validate insight structure
            if insights_count > 0:
                insight = data["insights"][0]
                required_fields = ["id", "type", "title", "description", "risk_level", "probability", "timeframe", "affected_areas", "timestamp"]
                missing_fields = [field for field in required_fields if field not in insight]
                
                if not missing_fields:
                    self.log_test("Insight Data Structure", True, "- All required fields present")
                else:
                    self.log_test("Insight Data Structure", False, f"- Missing fields: {missing_fields}")
            
            return True, data["insights"]
        else:
            self.log_test("Predictive Insights Endpoint", False, f"- Status: {status}, Data: {data}")
            return False, []

    def test_stats_endpoint(self):
        """Test /api/stats endpoint"""
        success, data, status = self.test_endpoint("/api/stats")
        
        if success:
            required_fields = ["total_threats", "active_threats", "critical_threats", "resolved_threats", 
                             "threat_distribution", "severity_distribution", "last_updated"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                self.log_test("Dashboard Stats Endpoint", True, f"- Status: {status}")
                self.log_test("Stats Data Structure", True, "- All required fields present")
                
                # Log some key stats
                print(f"   📊 Total Threats: {data.get('total_threats', 0)}")
                print(f"   🔥 Active Threats: {data.get('active_threats', 0)}")
                print(f"   🚨 Critical Threats: {data.get('critical_threats', 0)}")
                print(f"   ✅ Resolved Threats: {data.get('resolved_threats', 0)}")
                
            else:
                self.log_test("Dashboard Stats Endpoint", True, f"- Status: {status}")
                self.log_test("Stats Data Structure", False, f"- Missing fields: {missing_fields}")
            
            return True, data
        else:
            self.log_test("Dashboard Stats Endpoint", False, f"- Status: {status}, Data: {data}")
            return False, {}

    def test_recent_alerts_endpoint(self):
        """Test /api/alerts/recent endpoint"""
        success, data, status = self.test_endpoint("/api/alerts/recent")
        
        if success and "alerts" in data and isinstance(data["alerts"], list):
            alerts_count = len(data["alerts"])
            self.log_test("Recent Alerts Endpoint", True, f"- Status: {status}, Count: {alerts_count}")
            
            # Verify alerts are sorted by timestamp (most recent first)
            if alerts_count > 1:
                timestamps = [alert.get("timestamp") for alert in data["alerts"] if "timestamp" in alert]
                if len(timestamps) > 1:
                    sorted_check = all(timestamps[i] >= timestamps[i+1] for i in range(len(timestamps)-1))
                    if sorted_check:
                        self.log_test("Recent Alerts Sorting", True, "- Alerts properly sorted by timestamp")
                    else:
                        self.log_test("Recent Alerts Sorting", False, "- Alerts not properly sorted")
            
            return True, data["alerts"]
        else:
            self.log_test("Recent Alerts Endpoint", False, f"- Status: {status}, Data: {data}")
            return False, []

    def test_error_handling(self):
        """Test error handling for invalid endpoints"""
        # Test non-existent endpoint
        success, data, status = self.test_endpoint("/api/nonexistent", expected_status=404)
        if status == 404:
            self.log_test("404 Error Handling", True, f"- Status: {status}")
        else:
            self.log_test("404 Error Handling", False, f"- Expected 404, got {status}")
        
        # Test invalid threat type
        success, data, status = self.test_endpoint("/api/threats/invalid_type")
        # This should return empty list, not error
        if success and "threats" in data:
            self.log_test("Invalid Threat Type Handling", True, f"- Status: {status}, Returns empty list")
        else:
            self.log_test("Invalid Threat Type Handling", False, f"- Status: {status}")

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting EnviroIntel KE API Tests")
        print(f"🌐 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Test root endpoint
        self.test_root_endpoint()
        
        # Test threats endpoints
        threats_success, threats_data = self.test_threats_endpoint()
        
        # Test threat filtering
        threat_types = ["deforestation", "pollution", "illegal_dumping", "climate_anomaly"]
        type_results = self.test_threats_by_type(threat_types)
        
        # Test insights
        insights_success, insights_data = self.test_insights_endpoint()
        
        # Test stats
        stats_success, stats_data = self.test_stats_endpoint()
        
        # Test recent alerts
        alerts_success, alerts_data = self.test_recent_alerts_endpoint()
        
        # Test error handling
        self.test_error_handling()
        
        # Summary
        print("=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed! API is working correctly.")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed.")
            return 1

def main():
    # Get the backend URL from frontend/.env
    backend_url = "https://f9bbc3dd-2e29-4315-bb07-d9bcc3854234.preview.emergentagent.com"
    
    print(f"EnviroIntel KE API Testing Suite")
    print(f"Testing against: {backend_url}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tester = EnviroIntelAPITester(backend_url)
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())