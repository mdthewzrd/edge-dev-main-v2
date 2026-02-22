"""
Debug script to check tool errors
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from tools.indicator_calculator import indicator_calculator
from tools.a_plus_analyzer import a_plus_analyzer
from tools.quick_backtester import quick_backtester
from tools.sensitivity_analyzer import sensitivity_analyzer
from tools.tool_types import ToolStatus

# Create sample data
dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
np.random.seed(42)
base_price = 100
returns = np.random.normal(0, 0.02, 100)
closes = base_price * (1 + returns).cumprod()

data = pd.DataFrame({
    'date': dates,
    'open': closes * (1 + np.random.uniform(-0.01, 0.01, 100)),
    'high': closes * (1 + np.random.uniform(0, 0.02, 100)),
    'low': closes * (1 - np.random.uniform(0, 0.02, 100)),
    'close': closes,
    'volume': np.random.randint(1000000, 10000000, 100)
})

print("=" * 70)
print("DEBUGGING TOOL ERRORS")
print("=" * 70)

# Test 1: indicator_calculator
print("\n1. Testing indicator_calculator...")
result = indicator_calculator({
    "ticker": "TEST",
    "data": data,
    "indicators": ["EMA_CLOUD_72_89", "DUAL_DEVIATION_20"],
    "parameters": {}
})
print(f"   Status: {result.status}")
if result.status == ToolStatus.ERROR:
    print(f"   ❌ Error: {result.error}")

# Test 2: a_plus_analyzer
print("\n2. Testing a_plus_analyzer...")
result = a_plus_analyzer({
    "scanner_data": data,
    "a_plus_examples": [
        {
            "date": "2024-01-10",
            "setup_type": "BACKSIDE_B",
            "gap_percent": 2.5,
            "volume_ratio": 1.5,
            "outcome": "profitable",
            "return_percent": 3.2
        }
    ],
    "validation_criteria": {
        "min_gap_percent": 2.0,
        "min_volume_ratio": 1.2,
        "max_holding_days": 3
    }
})
print(f"   Status: {result.status}")
if result.status == ToolStatus.ERROR:
    print(f"   ❌ Error: {result.error}")

# Test 3: quick_backtester
print("\n3. Testing quick_backtester...")
scanner_results = pd.DataFrame([
    {
        'date': '2024-01-01',
        'entry_price': 100,
        'exit_price': 103,
        'return_pct': 3.0
    }
])
result = quick_backtester({
    "scanner_results": scanner_results,
    "entry_price_col": "entry_price",
    "exit_price_col": "exit_price",
    "date_col": "date"
})
print(f"   Status: {result.status}")
if result.status == ToolStatus.ERROR:
    print(f"   ❌ Error: {result.error}")
else:
    print(f"   ✅ Result keys: {result.result.keys() if result.result else 'None'}")

# Test 4: sensitivity_analyzer
print("\n4. Testing sensitivity_analyzer...")
def simple_scanner(params, data):
    gap_threshold = params.get("gap_percent", 2.0)
    data_copy = data.copy()
    data_copy["gap"] = ((data_copy["open"] - data_copy["close"].shift(1)) / data_copy["close"].shift(1) * 100)
    signals = data_copy[data_copy["gap"] > gap_threshold]
    return len(signals)

result = sensitivity_analyzer({
    "scanner_function": simple_scanner,
    "base_parameters": {"gap_percent": 2.0},
    "parameter_variations": {"gap_percent": 0.3},
    "evaluation_data": data
})
print(f"   Status: {result.status}")
if result.status == ToolStatus.ERROR:
    print(f"   ❌ Error: {result.error}")

print("\n" + "=" * 70)
