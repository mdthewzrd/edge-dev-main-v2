"""
Debug script for integration tests
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from tools.indicator_calculator import indicator_calculator
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

print("Testing indicator_calculator...")
print(f"Data shape: {data.shape}")
print(f"Data columns: {data.columns.tolist()}")

indicator_input = {
    "data": data,
    "indicators": ["EMA_CLOUD_72_89"],
    "parameters": {}
}

print(f"\nInput: {indicator_input}")

try:
    result = indicator_calculator(indicator_input)
    print(f"\nStatus: {result.status}")
    print(f"Result: {result.result}")
    if result.error:
        print(f"Error: {result.error}")
except Exception as e:
    import traceback
    print(f"\n💥 Exception: {e}")
    print(f"\nTraceback:")
    traceback.print_exc()
