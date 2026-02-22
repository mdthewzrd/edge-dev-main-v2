"""
Debug remaining test failures
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from tools.market_structure_analyzer import market_structure_analyzer
from tools.sensitivity_analyzer import sensitivity_analyzer
from tools.quick_backtester import quick_backtester
from tools.backtest_analyzer import backtest_analyzer
from tools.tool_types import ToolStatus

# Create test data
dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
np.random.seed(42)
base_price = 100
returns = np.random.normal(0, 0.02, 100)
closes = base_price * (1 + returns).cumprod()

df = pd.DataFrame({
    'date': dates,
    'open': closes * (1 + np.random.uniform(-0.01, 0.01, 100)),
    'high': closes * (1 + np.random.uniform(0, 0.02, 100)),
    'low': closes * (1 - np.random.uniform(0, 0.02, 100)),
    'close': closes,
    'volume': np.random.randint(1000000, 10000010, 100)
})

print("Testing market_structure_analyzer...")
result = market_structure_analyzer({
    "ticker": "AAPL",
    "df": df,
    "pivot_lookback": 10,
    "trend_lookback": 20
})
print(f"Status: {result.status}")
if result.error:
    print(f"Error: {result.error}")
else:
    print(f"Result keys: {result.result.keys() if result.result else 'None'}")

print("\n" + "="*70 + "\n")

print("Testing sensitivity_analyzer...")
def test_strategy(params, df):
    gap_threshold = params.get("gap_percent", 2.0)
    df_copy = df.copy()
    df_copy["gap"] = ((df_copy["open"] - df_copy["close"].shift(1)) / df_copy["close"].shift(1) * 100)
    signals = df_copy[df_copy["gap"] > gap_threshold]
    return len(signals)

result = sensitivity_analyzer({
    "scanner_function": test_strategy,
    "base_parameters": {"gap_percent": 2.0},
    "parameter_variations": {"gap_percent": 0.3},
    "evaluation_data": df
})
print(f"Status: {result.status}")
if result.error:
    print(f"Error: {result.error}")
else:
    print(f"Result keys: {result.result.keys() if result.result else 'None'}")

print("\n" + "="*70 + "\n")

print("Testing quick_backtester...")
scanner_results = pd.DataFrame([
    {
        'date': '2024-01-01',
        'ticker': 'TEST',
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
print(f"Status: {result.status}")
if result.error:
    print(f"Error: {result.error}")
else:
    print(f"Result keys: {result.result.keys() if result.result else 'None'}")
    print(f"Has 'performance' key: {'performance' in result.result if result.result else False}")

print("\n" + "="*70 + "\n")

print("Testing backtest_analyzer...")
result = backtest_analyzer({
    "backtest_results": scanner_results,
    "initial_capital": 10000,
    "benchmark_return": 0.02
})
print(f"Status: {result.status}")
if result.error:
    print(f"Error: {result.error}")
else:
    print(f"Result keys: {result.result.keys() if result.result else 'None'}")
