#!/usr/bin/env python3
"""
Show what scanner code looks like
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.v31_scanner_generator import v31_scanner_generator

# Generate a D2 scanner
result = v31_scanner_generator({
    "description": "D2 momentum scanner"
})

if result.status.value == "SUCCESS":
    code = result.result["scanner_code"]

    # Show first 80 lines
    lines = code.split('\n')
    print("=" * 70)
    print("  YOUR D2 SCANNER CODE (First 80 lines)")
    print("=" * 70)
    print('\n'.join(lines[:80]))
    print("\n" + "=" * 70)
    print(f"  TOTAL: {len(code)} characters, {len(lines)} lines")
    print("=" * 70)
