#!/usr/bin/env python3
"""
RENATA V2 CLI Interface

Command-line interface for the RENATA V2 Orchestrator
Version: 1.0.0
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orchestrator.renata_orchestrator import RenataOrchestrator
import pandas as pd
import numpy as np
from datetime import datetime
import json


class RenataCLI:
    """
    Command-line interface for RENATA V2
    """

    def __init__(self):
        """Initialize CLI"""
        self.orchestrator = RenataOrchestrator()
        self.context = {}
        self.history = []
        self.running = True

    def print_banner(self):
        """Print welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🤖 RENATA V2 - AI-Powered Trading Platform              ║
║                                                              ║
║   The intelligent orchestrator that coordinates 13 tools     ║
║   to help you build, test, and optimize trading scanners    ║
║                                                              ║
║   Type 'help' for commands or 'exit' to quit                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def print_help(self):
        """Print help information"""
        help_text = """
📖 Available Commands
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Interactive Commands:
  help                    Show this help message
  exit, quit              Exit the CLI
  clear                   Clear screen
  history                 Show conversation history
  context                 Show current context
  reset                   Reset context and history

Scanner Commands:
  generate <description>  Generate a V31 scanner
    Example: generate a Backside B gap scanner
    Example: generate D2 momentum scanner with EMA confirmation

Analysis Commands:
  analyze <ticker>        Analyze market structure
    Example: analyze AAPL
    Example: analyze SPY for trends and levels

  indicators <ticker>      Calculate proprietary indicators
    Example: indicators TSLA with 72/89 cloud

Optimization Commands:
  optimize <params>       Optimize scanner parameters
    Example: optimize gap percent from 1.5 to 3.0

Planning Commands:
  plan <description>      Create implementation plan
    Example: plan momentum strategy for AAPL

Backtest Commands:
  backtest                Quick backtest (requires scanner_results in context)
  analyze-backtest        Analyze backtest results

💡 Tips:
  • Be descriptive with your requests
  • The orchestrator understands natural language
  • Context is preserved across requests
  • Type 'clear' to start fresh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        print(help_text)

    def print_history(self):
        """Print conversation history"""
        if not self.history:
            print("📭 No history yet")
            return

        print("\n📜 Conversation History:")
        print("━" * 70)

        for i, (user_input, result) in enumerate(self.history, 1):
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{i}] {timestamp} 👤 User: {user_input}")

            if result.get("success"):
                print(f"    ✅ Success: {result['response'][:100]}...")
            else:
                print(f"    ❌ Error: {result['response']}")

            print(f"    🔧 Tools: {', '.join(result['tools_used'])}")
            print(f"    ⏱️  Time: {result['execution_time']:.4f}s")

    def print_context(self):
        """Print current context"""
        if not self.context:
            print("📭 No context stored")
            return

        print("\n📦 Current Context:")
        print("━" * 70)

        for key, value in self.context.items():
            if isinstance(value, pd.DataFrame):
                print(f"  📊 {key}: DataFrame ({len(value)} rows)")
            elif isinstance(value, str) and len(value) > 50:
                print(f"  📄 {key}: {value[:50]}...")
            else:
                print(f"  🔑 {key}: {value}")

    def process_input(self, user_input: str):
        """
        Process user input through orchestrator

        Args:
            user_input: User's command or request
        """

        # Handle special commands
        if user_input.lower() in ['exit', 'quit', 'q']:
            self.running = False
            return

        elif user_input.lower() == 'help':
            self.print_help()
            return

        elif user_input.lower() == 'clear':
            import os
            os.system('clear' if os.name != 'nt' else 'cls')
            self.print_banner()
            return

        elif user_input.lower() == 'history':
            self.print_history()
            return

        elif user_input.lower() == 'context':
            self.print_context()
            return

        elif user_input.lower() == 'reset':
            self.context = {}
            self.history = []
            print("🔄 Context and history reset")
            return

        # Process through orchestrator
        try:
            result = self.orchestrator.process_request(user_input, self.context)

            # Update context with results
            if result["success"] and result.get("execution_time", 0) < 1.0:
                # Extract results to add to context
                # (This is a simplified version - would be smarter in production)
                pass

            # Store in history
            self.history.append((user_input, result))

            # Format and display response
            self.display_result(result)

        except KeyboardInterrupt:
            print("\n\n🛑 Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def display_result(self, result: dict):
        """Display orchestrator result"""

        print("\n" + "━" * 70)

        if result["success"]:
            print(f"✅ SUCCESS")
            print(f"\n{result['response']}")

            # Show details
            print(f"\n🔧 Tools Used: {', '.join(result['tools_used'])}")
            print(f"⏱️  Execution Time: {result['execution_time']:.4f}s")

            if result["execution_time"] < 0.01:
                print(f"⚡ Lightning Fast!")
            elif result["execution_time"] < 0.1:
                print(f"🚀 Very Fast!")

        else:
            print(f"❌ ERROR")
            print(f"\n{result['response']}")

        print("━" * 70)

    def run_interactive(self):
        """Run interactive CLI loop"""
        self.print_banner()

        print("\n🎉 Welcome to RENATA V2!")
        print("💬 Start typing your requests in natural language...")
        print("   Type 'help' for commands or 'exit' to quit\n")

        while self.running:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()

                if not user_input:
                    continue

                # Process input
                self.process_input(user_input)

            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break

    def run_batch(self, requests: list):
        """Run batch processing mode"""
        print(f"🚀 Batch Mode: Processing {len(requests)} requests\n")

        results = []

        for i, request in enumerate(requests, 1):
            print(f"\n[{i}/{len(requests)}] Processing: {request}")

            try:
                result = self.orchestrator.process_request(request, self.context)
                results.append(result)

                status = "✅" if result["success"] else "❌"
                print(f"   {status} {result['tools_used']} ({result['execution_time']:.4f}s)")

            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({"success": False, "error": str(e)})

        # Summary
        print("\n" + "=" * 70)
        print("📊 BATCH PROCESSING SUMMARY")
        print("=" * 70)
        successful = sum(1 for r in results if r.get("success"))
        print(f"✅ Successful: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)")
        print(f"❌ Failed: {len(results) - successful}/{len(results)}")

        return results


def main():
    """Main entry point"""

    import argparse

    parser = argparse.ArgumentParser(
        description="RENATA V2 CLI - AI-Powered Trading Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python renata_cli.py

  # Single request
  python renata_cli.py --request "Generate a Backside B scanner"

  # Batch requests
  python renata_cli.py --batch requests.json

  # With data context
  python renata_cli.py --request "Analyze AAPL" --data market_data.csv
        """
    )

    parser.add_argument(
        '--request', '-r',
        type=str,
        help='Single request to process'
    )

    parser.add_argument(
        '--batch', '-b',
        type=str,
        help='JSON file with batch requests'
    )

    parser.add_argument(
        '--data', '-d',
        type=str,
        help='CSV data file to load as context'
    )

    parser.add_argument(
        '--ticker', '-t',
        type=str,
        default='AAPL',
        help='Ticker symbol (default: AAPL)'
    )

    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Force interactive mode'
    )

    args = parser.parse_args()

    # Create CLI instance
    cli = RenataCLI()

    # Load data if provided
    if args.data:
        try:
            df = pd.read_csv(args.data)
            cli.context['df'] = df
            cli.context['ticker'] = args.ticker
            print(f"✅ Loaded data: {len(df)} rows from {args.data}")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return 1

    # Single request mode
    if args.request:
        cli.print_banner()
        result = cli.orchestrator.process_request(args.request, cli.context)
        cli.display_result(result)
        return 0 if result["success"] else 1

    # Batch mode
    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                requests = json.load(f)

            cli.print_banner()
            cli.run_batch(requests)
            return 0

        except Exception as e:
            print(f"❌ Error processing batch: {e}")
            return 1

    # Default to interactive mode
    cli.run_interactive()

    return 0


if __name__ == "__main__":
    sys.exit(main())
