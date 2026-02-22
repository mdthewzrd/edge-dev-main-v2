#!/usr/bin/env python3
"""
RENATA V2 CLI Demo

Demonstrates the CLI in action
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from renata_cli import RenataCLI
import json


def demo_interactive_mode():
    """Demonstrate interactive mode"""
    print("=" * 70)
    print("🎬 RENATA V2 CLI - INTERACTIVE MODE DEMO")
    print("=" * 70)
    print("\nSimulating interactive session...\n")

    cli = RenataCLI()

    # Simulate conversation
    demo_conversation = [
        "help",
        "Generate a Backside B gap scanner",
        "Create implementation plan for momentum strategy",
        "exit"
    ]

    for user_input in demo_conversation:
        print(f"\n👤 You: {user_input}")
        cli.process_input(user_input)

        if not cli.running:
            break


def demo_single_request_mode():
    """Demonstrate single request mode"""
    print("\n" + "=" * 70)
    print("🎬 RENATA V2 CLI - SINGLE REQUEST MODE DEMO")
    print("=" * 70 + "\n")

    cli = RenataCLI()

    # Test requests
    test_requests = [
        "Generate a D2 trend scanner",
        "Plan momentum strategy for AAPL",
        "Optimize gap parameters"
    ]

    for request in test_requests:
        print(f"\n👤 Request: {request}")
        result = cli.orchestrator.process_request(request)
        cli.display_result(result)
        print()


def demo_batch_mode():
    """Demonstrate batch processing mode"""
    print("\n" + "=" * 70)
    print("🎬 RENATA V2 CLI - BATCH MODE DEMO")
    print("=" * 70 + "\n")

    # Create batch requests file
    batch_requests = [
        "Generate Backside B scanner",
        "Generate D2 scanner",
        "Generate MDR scanner",
        "Validate scanner",
        "Plan momentum strategy"
    ]

    # Save to file
    batch_file = "/tmp/renata_batch_demo.json"
    with open(batch_file, 'w') as f:
        json.dump(batch_requests, f, indent=2)

    print(f"✅ Created batch file: {batch_file}")
    print(f"   Requests: {len(batch_requests)}")

    # Run batch mode
    cli = RenataCLI()
    cli.run_batch(batch_requests)

    print(f"\n✅ Batch processing complete!")


def main():
    """Run demo"""
    print("\n")
    print("🎬 RENATA V2 CLI - DEMONSTRATION")
    print("=" * 70)

    # Run demos
    demo_interactive_mode()
    demo_single_request_mode()
    demo_batch_mode()

    print("\n" + "=" * 70)
    print("✅ DEMONSTRATION COMPLETE!")
    print("=" * 70)

    print("\n🚀 To use the CLI:")
    print("   Interactive:  python backend/renata_cli.py")
    print("   Single req:  python backend/renata_cli.py -r 'your request'")
    print("   Batch mode:  python backend/renata_cli.py -b requests.json")
    print("\n")


if __name__ == "__main__":
    main()
