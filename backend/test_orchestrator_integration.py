#!/usr/bin/env python3
"""
Test RENATA V2 Orchestrator Integration

This script tests the complete integration of the RENATA V2 Orchestrator:
1. Backend API endpoints
2. Intent classification
3. Tool selection
4. Workflow execution
5. Response formatting
"""

import requests
import json

BASE_URL = "http://localhost:5666"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_health_check():
    """Test health check endpoint"""
    print_section("Test 1: Health Check")

    response = requests.get(f"{BASE_URL}/health")
    data = response.json()

    print(f"✅ Status: {data['status']}")
    print(f"🤖 Tools Registered: {data['tools_count']}")
    print(f"📦 Version: {data['version']}")

    assert response.status_code == 200
    assert data['status'] == 'healthy'
    assert data['tools_count'] == 13

    print("✅ Health check passed!")

def test_scanner_generation():
    """Test scanner generation through chat endpoint"""
    print_section("Test 2: Scanner Generation (Backside B)")

    payload = {
        "message": "Generate a Backside B gap scanner"
    }

    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json=payload
    )
    data = response.json()

    print(f"✅ Success: {data['success']}")
    print(f"🔧 Tools Used: {', '.join(data['tools_used'])}")
    print(f"⏱️  Execution Time: {data['execution_time']:.4f}s")
    print(f"🎯 Intent: {data['intent']['type']}")
    print(f"📄 Response: {data['response'][:100]}...")

    assert response.status_code == 200
    assert data['success'] == True
    assert 'V31 Scanner Generator' in data['tools_used']
    assert data['intent']['type'] == 'GENERATE_SCANNER'

    print("✅ Scanner generation passed!")

def test_implementation_planning():
    """Test implementation planning"""
    print_section("Test 3: Implementation Planning")

    payload = {
        "message": "Plan momentum strategy implementation with D2 and MDR setups",
        "context": {
            "strategy_description": "Momentum strategy trading D2 and MDR setups",
            "setup_types": ["D2", "MDR"]
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json=payload
    )
    data = response.json()

    print(f"✅ Success: {data['success']}")
    print(f"🔧 Tools Used: {', '.join(data['tools_used'])}")
    print(f"⏱️  Execution Time: {data['execution_time']:.4f}s")
    print(f"🎯 Intent: {data['intent']['type']}")
    print(f"📄 Response: {data['response'][:100]}...")

    assert response.status_code == 200
    assert data['success'] == True
    assert 'Build Plan Generator' in data['tools_used']

    print("✅ Implementation planning passed!")

def test_list_tools():
    """Test listing available tools"""
    print_section("Test 4: List Available Tools")

    response = requests.get(f"{BASE_URL}/api/renata/tools")
    data = response.json()

    print(f"✅ Success: {data['success']}")
    print(f"🤖 Tools Count: {data['count']}")

    print("\nAvailable Tools:")
    for tool in data['tools'][:5]:  # Show first 5
        print(f"  • {tool['name']}: {tool['description'][:50]}...")

    assert response.status_code == 200
    assert data['success'] == True
    assert data['count'] == 13

    print("✅ List tools passed!")

def test_get_status():
    """Test getting orchestrator status"""
    print_section("Test 5: Get Orchestrator Status")

    response = requests.get(f"{BASE_URL}/api/renata/status")
    data = response.json()

    print(f"✅ Status: {data['status']}")
    print(f"📦 Version: {data['version']}")
    print(f"🤖 Tools Count: {data['tools_count']}")

    print("\nCapabilities:")
    for capability, enabled in data['capabilities'].items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {capability}")

    assert response.status_code == 200
    assert data['status'] == 'operational'

    print("✅ Get status passed!")

def test_multi_tool_workflow():
    """Test multi-tool workflow"""
    print_section("Test 6: Multi-Tool Workflow")

    payload = {
        "message": "Generate D2 scanner, validate it, and create backtest code"
    }

    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json=payload
    )
    data = response.json()

    print(f"✅ Success: {data['success']}")
    print(f"🔧 Tools Used: {', '.join(data['tools_used'])}")
    print(f"⏱️  Execution Time: {data['execution_time']:.4f}s")
    print(f"🎯 Intent: {data['intent']['type']}")

    assert response.status_code == 200
    assert data['success'] == True
    assert len(data['tools_used']) >= 2  # Should use multiple tools

    print("✅ Multi-tool workflow passed!")

def main():
    """Run all integration tests"""
    print("\n")
    print("🚀" * 35)
    print("  RENATA V2 ORCHESTRATOR INTEGRATION TESTS")
    print("🚀" * 35)

    try:
        # Run all tests
        test_health_check()
        test_scanner_generation()
        test_implementation_planning()
        test_list_tools()
        test_get_status()
        test_multi_tool_workflow()

        # Summary
        print_section("✅ ALL TESTS PASSED!")
        print("\n🎉 Integration is working perfectly!")
        print("\n📊 Test Summary:")
        print("  • Health Check: ✅")
        print("  • Scanner Generation: ✅")
        print("  • Implementation Planning: ✅")
        print("  • List Tools: ✅")
        print("  • Get Status: ✅")
        print("  • Multi-Tool Workflow: ✅")
        print("\n🚀 RENATA V2 is ready for frontend integration!")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
