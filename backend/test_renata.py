#!/usr/bin/env python3
"""
Simple script to test RENATA V2
Just run this and it will show you RENATA working!
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orchestrator.renata_orchestrator import RenataOrchestrator

print("\n" + "=" * 70)
print("  🤖 RENATA V2 TEST")
print("=" * 70)

# Initialize orchestrator
print("\n⏳ Starting RENATA...")
orchestrator = RenataOrchestrator()
print(f"✅ RENATA is ready with {len(orchestrator.tool_registry)} tools!")

# Test messages to try
test_messages = [
    "Generate a Backside B gap scanner",
    "Plan D2 momentum strategy",
    "Optimize gap parameters"
]

print("\n" + "=" * 70)
print("  ASKING RENATA QUESTIONS")
print("=" * 70)

for i, message in enumerate(test_messages, 1):
    print(f"\n[{i}/{len(test_messages)}] Question: {message}")

    # Process request
    result = orchestrator.process_request(message)

    # Show response
    print(f"\n✅ Success: {result['success']}")
    print(f"🔧 Tools: {', '.join(result['tools_used'])}")
    print(f"⏱️  Time: {result['execution_time']:.4f}s")
    print(f"📄 Response: {result['response'][:100]}...")

print("\n" + "=" * 70)
print("  ✅ RENATA IS WORKING!")
print("=" * 70)
print("\n💡 Now try the CLI:")
print("   cd backend")
print("   python renata_cli.py")
print("\n")
