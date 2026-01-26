# 🔧 RENATA V2 - TOOL EXTRACTION PLAN
## From 5 Agents (56 Capabilities) → 1 Orchestrator + 15-20 Tools

**Date**: January 25, 2026
**Principle**: Cole Medina's "Tools Before Agents" - Build well-tested, parameterized tools first, then coordinate with simple orchestrator
**Objective**: Refactor complex multi-agent system into maintainable, testable tool architecture

---

## 📊 CURRENT STATE ANALYSIS

### Agent → Capability Breakdown (From Capabilities Matrix)

**PLANNING AGENT** (12 capabilities)
1. Generate scanner from idea
2. Build from A+ example
3. A+ analysis & parameter extraction
4. Mold generation (Lingua patterns)
5. Explain V31 concepts
6. Trading principles guidance
7. Sequential workflow coordination
8. Parallel processing coordination
9. Context preservation
10. Multi-agent problem solving
11. RAG knowledge access
12. Chat on /plan page

**RESEARCHER AGENT** (10 capabilities)
1. Archon RAG search
2. Find similar strategies
3. Suggest parameters
4. Market regime analysis
5. Sequential workflow coordination
6. Parallel processing coordination
7. Context preservation
8. Multi-agent problem solving
9. RAG knowledge access
10. Chat on /plan page

**BUILDER AGENT** (16 capabilities)
1. Transform legacy code to V31
2. Validate V31 compliance
3. Edit scanner parameters
4. Modify scanner logic
5. Add/remove patterns
6. Refactor scanner code
7. Generate execution code
8. Build position sizing
9. Create stop-loss systems
10. Portfolio risk controls
11. Trade management logic
12. Edit execution rules
13. Sequential workflow coordination
14. Parallel processing coordination
15. Context preservation
16. RAG knowledge access

**EXECUTOR AGENT** (10 capabilities)
1. Run backtest
2. Run analyzer codes (A+ validation)
3. Quick 30-day validation
4. IS/OOS validation
5. Monte Carlo simulation
6. Scanner execution
7. Real-time progress tracking
8. Sequential workflow coordination
9. Context preservation
10. Dashboard integration

**ANALYST AGENT** (12 capabilities)
1. Optimize parameters
2. Parameter grid search
3. A/B testing
4. Analyze backtest results
5. Regime analysis
6. Performance metrics calculation
7. IS/OOS analysis
8. Monte Carlo analysis
9. Suggest parameters
10. Sequential workflow coordination
11. Context preservation
12. RAG knowledge access

**Total Unique Capabilities**: 56
**Duplicate/Cross-cutting**: ~20 (workflow coordination, context, RAG access appear in multiple agents)

---

## 🎯 TARGET ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                     RENATA ORCHESTRATOR                      │
│                  (Simple Coordinator Agent)                  │
│                                                              │
│  Responsibilities:                                           │
│  - Interpret user intent                                     │
│  - Select appropriate tools                                  │
│  - Chain tool calls in workflows                             │
│  - Handle errors and retries                                 │
│  - Present results to user                                   │
│                                                              │
│  Size: ~150-200 lines (lightweight!)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ├─→ Tool 1: Parameter Extractor
                            ├─→ Tool 2: Code Generator
                            ├─→ Tool 3: V31 Validator
                            ├─→ Tool 4: Scanner Executor
                            ├─→ Tool 5: Backtest Runner
                            ├─→ Tool 6: Performance Analyzer
                            ├─→ Tool 7: Parameter Optimizer
                            ├─→ Tool 8: Knowledge Retriever
                            ├─→ Tool 9: Pattern Detector
                            ├─→ Tool 10: Risk Manager
                            ├─→ Tool 11: Execution Builder
                            ├─→ Tool 12: Code Transformer
                            ├─→ Tool 13: A+ Validator
                            ├─→ Tool 14: Market Analyzer
                            └─→ Tool 15: Visualizer
```

---

## 🛠️ TOOL SPECIFICATIONS

### Tool 1: Parameter Extractor
**Source**: Planning Agent (capabilities 3-4)
**Purpose**: Extract parameters from user ideas, A+ examples, or code

**Inputs**:
- `source_type`: "idea" | "a_plus_example" | "code" | "chart_image"
- `source_data`: Text description, example dict, or code string
- `setup_type`: One of 13 Lingua setups (optional, auto-detect if not provided)

**Outputs**:
```python
{
    "parameters": {
        "gap_over_atr": {"value": 0.8, "range": [0.7, 0.95], "description": "..."},
        "ema_cloud_bullish": {"value": True, "type": "boolean", "description": "..."},
        # ... all extracted parameters
    },
    "setup_type": "Backside_ET",
    "confidence_score": 0.92,
    "missing_parameters": ["stop_loss_atr_multiple"],  # if any
    "suggestions": ["Consider adding volume confirmation"]
}
```

**Estimated LOC**: 120 lines
**Dependencies**: Knowledge Retriever Tool, Pattern Detector Tool
**Testing Strategy**:
- Test with all 13 setup types
- Test with partial information (idea only, no example)
- Test parameter range extraction
- Test confidence scoring accuracy

---

### Tool 2: Code Generator
**Source**: Builder Agent (capabilities 1, 7-11)
**Purpose**: Generate V31-compliant scanner code from parameters

**Inputs**:
```python
{
    "parameters": {...},  # from Tool 1
    "setup_type": "Backside_ET",
    "v31_compliance": True,
    "include_execution": False,  # generate execution code too?
    "target_framework": "backtesting.py" | "vectorbt" | "custom"
}
```

**Outputs**:
```python
{
    "scanner_code": "# Complete V31 scanner code...",
    "execution_code": "# Execution logic (if requested)...",
    "parameters_used": [...],
    "v31_pillars_implemented": ["P0_Market_Scanning", "P1_3_Stage", "P2_Per_Ticker", "P3_Parallel"],
    "warnings": ["Market scanning will cover 12k symbols"],
    "estimated_execution_time": "30-45 seconds"
}
```

**Estimated LOC**: 180 lines
**Dependencies**: Parameter Extractor, V31 Validator, Knowledge Retriever
**Testing Strategy**:
- Generate code for all 13 setups
- Test V31 compliance (check all pillars present)
- Test compilation (syntax check)
- Test with edge cases (missing params, invalid combinations)

---

### Tool 3: V31 Validator
**Source**: Builder Agent (capability 2)
**Purpose**: Validate code against V31 Gold Standard

**Inputs**:
```python
{
    "code": "scanner code string",
    "strict_mode": True,  # fail or warn on violations
    "check_pillars": ["P0", "P1", "P2", "P3"]  # which pillars to check
}
```

**Outputs**:
```python
{
    "is_compliant": False,
    "compliance_score": 0.85,
    "pillar_status": {
        "P0_Market_Scanning": {"status": "PASS", "details": "Full NYSE+NASDAQ+ETF coverage"},
        "P1_3_Stage_Architecture": {"status": "FAIL", "details": "Missing Stage 2 secondary pass"},
        "P2_Per_Ticker_Operations": {"status": "WARN", "details": "No two-pass buffers"},
        "P3_Parallel_Processing": {"status": "PASS", "details": "Batch processing implemented"}
    },
    "violations": [
        {"line": 45, "issue": "Single API call per symbol (should batch)", "severity": "ERROR"},
        {"line": 120, "issue": "No smart filter in Stage 1", "severity": "WARNING"}
    ],
    "suggestions": ["Implement grouped endpoint for Stage 1", "Add historical buffer for two-pass features"]
}
```

**Estimated LOC**: 150 lines
**Dependencies**: None (standalone validator)
**Testing Strategy**:
- Test with known V31-compliant code (should pass)
- Test with known non-compliant code (should catch violations)
- Test each pillar independently
- Test strict vs warning mode

---

### Tool 4: Scanner Executor
**Source**: Executor Agent (capability 6)
**Purpose**: Execute scanner on backend API with progress tracking

**Inputs**:
```python
{
    "scanner_code": "code string",
    "date_range": {"start": "2024-01-01", "end": "2024-03-31"},
    "symbol_universe": "ALL" | ["SPY", "QQQ", ...],  # "ALL" = 12k V31 default
    "execution_mode": "full" | "quick" | "analyzer",
    "callback_url": "optional webhook for progress"
}
```

**Outputs**:
```python
{
    "execution_id": "exec_123456",
    "status": "running" | "completed" | "failed",
    "progress": 0.67,  # 67% complete
    "current_stage": "Stage 2: Per-ticker operations",
    "results": {
        "signals": [
            {"ticker": "SPY", "date": "2024-01-15", "type": "entry", "price": 478.50, ...},
            # ... all signals
        ],
        "total_symbols_scanned": 11847,
        "signals_found": 47,
        "execution_time_seconds": 38.2
    },
    "error": null  # if failed
}
```

**Estimated LOC**: 140 lines
**Dependencies**: Backend API (FastAPI), Knowledge Retriever (for symbol lists)
**Testing Strategy**:
- Test with small symbol list (fast execution)
- Test with full universe (12k symbols)
- Test error handling (invalid code, API failures)
- Test progress tracking accuracy

---

### Tool 5: Backtest Runner
**Source**: Executor Agent (capabilities 1, 3-5)
**Purpose**: Run backtests with various validation modes

**Inputs**:
```python
{
    "scanner_code": "code string",
    "execution_code": "optional execution logic",
    "date_range": {"start": "2024-01-01", "end": "2024-03-31"},
    "backtest_mode": "full" | "quick_30day" | "is_oos" | "monte_carlo",
    "is_oos_split": {"in_sample_end": "2024-02-15"} if is_oos else None,
    "monte_carlo_runs": 1000 if monte_carlo else None,
    "commission": 0.001,
    "slippage": 0.0001
}
```

**Outputs**:
```python
{
    "backtest_id": "bt_789012",
    "results": {
        "total_return": 0.24,
        "sharpe_ratio": 1.85,
        "max_drawdown": -0.12,
        "win_rate": 0.68,
        "profit_factor": 2.1,
        "total_trades": 47,
        "equity_curve": [/* array of values */],
        "trades": [
            {"entry_date": "2024-01-15", "exit_date": "2024-01-18", "return_pct": 3.2, ...},
            # ... all trades
        ]
    },
    "is_oos_results": {  # if IS/OOS mode
        "in_sample": {"sharpe": 1.92, "return": 0.26},
        "out_of_sample": {"sharpe": 1.65, "return": 0.19},
        "robustness_score": 0.78  # similarity between IS and OOS
    },
    "monte_carlo_results": {  # if Monte Carlo mode
        "mean_return": 0.23,
        "percentile_5": 0.11,
        "percentile_95": 0.38,
        "confidence_interval_95": [0.15, 0.31]
    }
}
```

**Estimated LOC**: 160 lines
**Dependencies**: Backend API, Performance Analyzer Tool
**Testing Strategy**:
- Test all backtest modes (full, quick, IS/OOS, Monte Carlo)
- Test with known strategies (verify expected results)
- Test edge cases (no signals, all losses, extreme volatility)

---

### Tool 6: Performance Analyzer
**Source**: Analyst Agent (capabilities 4, 6)
**Purpose**: Calculate and analyze performance metrics

**Inputs**:
```python
{
    "backtest_results": {...},  # from Tool 5
    "benchmark": "SPY" | null,  # compare to benchmark
    "metrics": ["sharpe", "sortino", "calmar", "win_rate", "profit_factor", "expectancy"]
}
```

**Outputs**:
```python
{
    "metrics": {
        "return_metrics": {
            "total_return": 0.24,
            "cagr": 0.32,
            "monthly_returns": [0.02, -0.01, 0.03, ...],
            "annual_returns": {2023: 0.18, 2024: 0.24}
        },
        "risk_metrics": {
            "max_drawdown": -0.12,
            "volatility": 0.15,
            "downside_deviation": 0.09,
            "var_95": -0.03  # Value at Risk
        },
        "risk_adjusted_returns": {
            "sharpe_ratio": 1.85,
            "sortino_ratio": 2.12,
            "calmar_ratio": 2.0,
            "information_ratio": 0.45  # if benchmark provided
        },
        "trading_metrics": {
            "win_rate": 0.68,
            "profit_factor": 2.1,
            "avg_win": 0.032,
            "avg_loss": -0.018,
            "expectancy": 0.014,
            "largest_win": 0.12,
            "largest_loss": -0.05
        }
    },
    "analysis": {
        "strengths": [
            "High Sharpe ratio (1.85) indicates good risk-adjusted returns",
            "Win rate (68%) with 2:1 profit factor shows positive expectancy"
        ],
        "weaknesses": [
            "Max drawdown (-12%) could be reduced with tighter stops",
            "Win rate declined in volatile periods (regime dependency)"
        ],
        "regime_analysis": {
            "bull_market": {"win_rate": 0.75, "return": 0.31},
            "bear_market": {"win_rate": 0.58, "return": 0.12},
            "sideways": {"win_rate": 0.52, "return": 0.04}
        }
    },
    "recommendations": [
        "Consider volatility-adjusted position sizing",
        "Add regime filter to avoid sideways markets"
    ]
}
```

**Estimated LOC**: 200 lines
**Dependencies**: None (pure analysis)
**Testing Strategy**:
- Test with known good strategy (verify metrics accuracy)
- Test with losing strategy (negative metrics, warnings)
- Test benchmark comparison
- Test regime detection logic

---

### Tool 7: Parameter Optimizer
**Source**: Analyst Agent (capabilities 1-2, 9)
**Purpose**: Optimize parameters using grid search or advanced methods

**Inputs**:
```python
{
    "scanner_code": "code with parameter placeholders",
    "parameters_to_optimize": {
        "gap_over_atr": {"range": [0.7, 0.95], "step": 0.05},
        "rsi_threshold": {"range": [65, 80], "step": 5}
    },
    "optimization_target": "sharpe" | "return" | "win_rate" | "profit_factor",
    "date_range": {"start": "2024-01-01", "end": "2024-03-31"},
    "optimization_method": "grid_search" | "random_search" | "bayesian",
    "max_iterations": 100
}
```

**Outputs**:
```python
{
    "best_parameters": {
        "gap_over_atr": 0.85,
        "rsi_threshold": 70
    },
    "optimization_results": [
        {
            "parameters": {"gap_over_atr": 0.85, "rsi_threshold": 70},
            "metrics": {"sharpe": 1.95, "return": 0.26, "win_rate": 0.74}
        },
        {
            "parameters": {"gap_over_atr": 0.80, "rsi_threshold": 70},
            "metrics": {"sharpe": 1.85, "return": 0.24, "win_rate": 0.68}
        },
        # ... sorted by optimization_target
    ],
    "parameter_sensitivity": {
        "gap_over_atr": {
            "0.70": {"sharpe": 1.45, "signals": 156},
            "0.75": {"sharpe": 1.65, "signals": 98},
            "0.80": {"sharpe": 1.85, "signals": 67},
            "0.85": {"sharpe": 1.95, "signals": 41},  # best
            "0.90": {"sharpe": 1.82, "signals": 32},
            "0.95": {"sharpe": 1.65, "signals": 18}
        }
    },
    "recommendation": "gap_over_atr=0.85 provides optimal Sharpe (1.95) with reasonable signal frequency (41 signals)"
}
```

**Estimated LOC**: 180 lines
**Dependencies**: Backtest Runner Tool (for evaluating each parameter set)
**Testing Strategy**:
- Test grid search convergence
- Test with known optimal parameters (should find them)
- Test parameter sensitivity analysis
- Test optimization for different targets (Sharpe vs return vs win rate)

---

### Tool 8: Knowledge Retriever
**Source**: Researcher Agent (capability 1), All agents (capability 11)
**Purpose**: Query Archon MCP for V31, Lingua, strategies, examples

**Inputs**:
```python
{
    "query": "backside euphoric top setup parameters",
    "domain": "v31" | "lingua" | "strategies" | "examples" | "all",
    "max_results": 5,
    "filters": {
        "setup_type": "Backside_ET",
        "timeframe": "15m",
        "market_regime": "bull"
    }
}
```

**Outputs**:
```python
{
    "results": [
        {
            "type": "strategy",
            "name": "Backside_ET_Scanner",
            "relevance_score": 0.94,
            "summary": "Backside euphoric top scanner with gap + trend break",
            "parameters": {"gap_over_atr": 0.8, "euphoric_rsi": 70, "trend_break_confirm": True},
            "performance": {"win_rate": 0.72, "sharpe": 1.92},
            "code_snippet": "def detect_backside_et(data):\n    # ...",
            "location": "/backend/backside_b_scanner.py"
        },
        {
            "type": "a_plus_example",
            "name": "SPY_Backside_ET_2024-01-15",
            "relevance_score": 0.87,
            "summary": "Perfect A+ example of backside ET setup",
            "ticker": "SPY",
            "date": "2024-01-15",
            "chart_image": "/examples/spy_backside_2024-01-15.png",
            "parameters_matched": {"gap_over_atr": 0.82, "euphoric_rsi": 72}
        },
        # ... up to max_results
    ],
    "total_found": 23,
    "query_understood": True,
    "suggested_queries": ["backside execution rules", "euphoric top detection"]
}
```

**Estimated LOC**: 100 lines
**Dependencies**: Archon MCP Server (port 8051)
**Testing Strategy**:
- Test query understanding accuracy
- Test domain filtering (V31 vs Lingua vs strategies)
- Test relevance ranking
- Test with ambiguous queries (should suggest alternatives)

---

### Tool 9: Pattern Detector
**Source**: Planning Agent (capability 4), Researcher Agent (capability 3)
**Purpose**: Detect Lingua patterns from market data or A+ examples

**Inputs**:
```python
{
    "input_type": "a_plus_example" | "market_data" | "code",
    "data": {
        "ticker": "SPY",
        "date": "2024-01-15",
        "ohlcv": {/* dataframe */},
        "indicators": {"ema72": 475.2, "ema89": 474.8, "rsi": 72, ...}
    } if a_plus_example or market_data,
    "code": "scanner code string" if code
}
```

**Outputs**:
```python
{
    "detected_patterns": [
        {
            "pattern_name": "Backside_ET",
            "confidence": 0.92,
            "indicators_present": {
                "gap_up": 0.012,  # 1.2% gap over ATR
                "euphoric_top": True,  # RSI 72
                "trend_break": "10:32 AM",
                "backside_context": True  # not at ATH
            },
            "parameters_extracted": {
                "gap_over_atr": 0.8,
                "euphoric_rsi_threshold": 70,
                "trend_break_confirmation": True
            },
            "missing_indicators": ["volume_confirmation"],
            "market_regime": "bull",
            "daily_context": "Backside",
            "timeframe": "15m"
        }
    ],
    "alternative_patterns": [
        {"pattern": "Daily_Para_Run", "confidence": 0.34, "reason": "Also fits parabolic criteria"}
    ],
    "setup_category": "Backside_Molds",
    "recommended_execution": "Short entry at euphoric top, cover at trend break or -2R stop"
}
```

**Estimated LOC**: 150 lines
**Dependencies**: Knowledge Retriever (for pattern definitions), Parameter Extractor
**Testing Strategy**:
- Test detection of all 13 Lingua setups
- Test with ambiguous examples (should show alternatives)
- Test confidence scoring
- Test parameter extraction accuracy

---

### Tool 10: Risk Manager
**Source**: Builder Agent (capabilities 8-10)
**Purpose**: Calculate position sizing, stops, portfolio risk

**Inputs**:
```python
{
    "account_size": 100000,
    "risk_per_trade": 0.02,  # 2%
    "entry_price": 478.50,
    "stop_loss": {"type": "atr_based", "atr_multiple": 2.0, "atr": 3.2},
    "position_sizing_method": "fixed_risk" | "volatility_based" | "kelly",
    "max_portfolio_risk": 0.03,  # 3% max total risk
    "existing_positions": [
        {"ticker": "QQQ", "risk": 0.015, "entry": 412.0, "stop": 398.0}
    ]
}
```

**Outputs**:
```python
{
    "position_size": {
        "shares": 180,
        "dollar_amount": 86130,  # 86% of account
        "risk_amount": 2000,  # 2% of account
        "risk_per_share": 2.56  # distance to stop
    },
    "stop_loss": {
        "price": 475.94,
        "type": "atr_based",
        "atr_multiple": 2.0,
        "distance_from_entry_pct": -0.0054  # -0.54%
    },
    "portfolio_check": {
        "total_risk_if_added": 0.035,  # 3.5% (exceeds max!)
        "warning": "Adding this position exceeds max portfolio risk (3%)",
        "suggested_reduction": "Reduce position size to 130 shares to stay within 3% limit"
    },
    "take_profits": [
        {"level": 1, "price": 483.64, "r_multiple": 1.0, "action": "take_partial_profit"},
        {"level": 2, "price": 491.28, "r_multiple": 2.0, "action": "take_half_profit"},
        {"level": 3, "price": 502.46, "r_multiple": 3.0, "action": "trail_stop"}
    ],
    "pyramiding_opportunities": [
        {"condition": "pullback to 15m mean", "add_size": 36, "new_stop": 476.50},
        {"condition": "break to +2R", "add_size": 36, "new_stop": 478.50}
    ]
}
```

**Estimated LOC**: 140 lines
**Dependencies**: None (pure calculation)
**Testing Strategy**:
- Test all position sizing methods
- Test portfolio risk warnings
- Test ATR-based stop calculations
- Test pyramiding recommendations

---

### Tool 11: Execution Builder
**Source**: Builder Agent (capabilities 7, 11-12)
**Purpose**: Generate execution code (entries, exits, position management)

**Inputs**:
```python
{
    "scanner_signals": [{/* from Tool 4 */}],
    "entry_rules": {
        "type": "market" | "limit",
        "limit_offset": 0.001,  # 0.1% below signal price
        "time_in_force": "DAY"
    },
    "exit_rules": {
        "stop_loss": {"type": "atr_based", "atr_multiple": 2.0},
        "take_profit": {"type": "r_multiple", "target": 3.0},
        "trailing_stop": {"trigger_after_r": 1.0, "trail_atr": 1.5}
    },
    "position_management": {
        "pyramiding": True,
        "scale_in_conditions": ["pullback_to_mean", "break_to_2R"],
        "partial_exits": [{"at_r": 1.0, "exit_pct": 0.25}, {"at_r": 2.0, "exit_pct": 0.50}]
    }
}
```

**Outputs**:
```python
{
    "execution_code": """
# Auto-generated execution code
def execute_signals(signals, account_size, risk_per_trade):
    positions = []
    for signal in signals:
        # Calculate position size
        stop_price = signal['entry'] - (signal['atr'] * 2.0)
        shares = calculate_position_size(account_size, risk_per_trade, signal['entry'], stop_price)

        # Entry order
        entry_order = {
            'type': 'LIMIT',
            'price': signal['entry'] * 0.999,  # 0.1% below
            'shares': shares,
            'time_in_force': 'DAY'
        }

        # Stop loss
        stop_order = {
            'type': 'STOP_MARKET',
            'stop_price': stop_price,
            'shares': shares
        }

        # Take profit
        take_profit_order = {
            'type': 'LIMIT',
            'price': signal['entry'] * 1.03,  # +3% (3R)
            'shares': int(shares * 0.25)  # Take 25% profit
        }

        positions.append({
            'entry': entry_order,
            'stop': stop_order,
            'take_profit': take_profit_order,
            'pyramiding_enabled': True,
            'trail_stop_trigger_r': 1.0
        })

    return positions
    """,
    "backtest_integration": "Compatible with backtesting.py framework",
    "paper_trading_ready": True,
    "warnings": ["Pyramiding not supported in all backtesting frameworks"]
}
```

**Estimated LOC**: 160 lines
**Dependencies**: Risk Manager Tool (for position sizing)
**Testing Strategy**:
- Test execution code compilation
- Test different entry/exit rule combinations
- Test pyramiding logic
- Test integration with backtesting frameworks

---

### Tool 12: Code Transformer
**Source**: Builder Agent (capability 1)
**Purpose**: Transform legacy/non-V31 code to V31 compliance

**Inputs**:
```python
{
    "source_code": "legacy scanner code",
    "source_type": "legacy_scanner" | "non_v31" | "idea_description",
    "target_pillars": ["P0", "P1", "P2", "P3"],  # which pillars to implement
    "preserve_logic": True  # keep original detection logic, just add V31 structure
}
```

**Outputs**:
```python
{
    "transformed_code": "# V31-compliant scanner...",
    "changes_made": [
        {"type": "added", "description": "P0: Full market scanning (12k symbols)"},
        {"type": "refactored", "description": "P1: Restructured into 3-stage grouped endpoint"},
        {"type": "added", "description": "P2: Implemented per-ticker operations with smart filters"},
        {"type": "optimized", "description": "P3: Batched API calls for parallel processing"}
    ],
    "preserved_logic": [
        "Original gap detection logic",
        "RSI threshold conditions",
        "Volume confirmation rules"
    ],
    "v31_compliance": {
        "before": 0.35,
        "after": 1.0,
        "pillars_added": ["P0", "P1", "P2", "P3"]
    },
    "warnings": [
        "Execution time will increase (scanning 12k symbols vs 500)",
        "Some parameters adjusted for V31 compatibility"
    ]
}
```

**Estimated LOC**: 200 lines
**Dependencies**: V31 Validator, Code Generator
**Testing Strategy**:
- Test transformation of known legacy scanners
- Test logic preservation (verify original logic still works)
- Test V31 compliance after transformation
- Test with various source types

---

### Tool 13: A+ Validator
**Source**: Executor Agent (capability 2)
**Purpose**: Validate scanner captures A+ example (analyzer code)

**Inputs**:
```python
{
    "scanner_code": "code to validate",
    "a_plus_examples": [
        {"ticker": "SPY", "date": "2024-01-15", "expected_signal": True},
        {"ticker": "QQQ", "date": "2024-01-16", "expected_signal": True}
    ],
    "visual_output": True  # generate chart overlay?
}
```

**Outputs**:
```python
{
    "validation_results": [
        {
            "example": {"ticker": "SPY", "date": "2024-01-15"},
            "signal_found": True,
            "signal_details": {
                "timestamp": "2024-01-15 10:32:00",
                "entry_price": 478.50,
                "stop_price": 472.30,
                "indicators": {
                    "gap_over_atr": 0.82,
                    "rsi": 72,
                    "volume_confirm": True
                }
            },
            "chart_overlay": {
                "url": "/charts/spy_2024-01-15_validation.png",
                "markers": [
                    {"type": "signal", "x": "2024-01-15 10:32", "y": 478.50, "label": "ENTRY"},
                    {"type": "stop", "x": "2024-01-15 10:32", "y": 472.30, "label": "STOP"}
                ]
            },
            "status": "✅ CAPTURED"
        },
        {
            "example": {"ticker": "QQQ", "date": "2024-01-16"},
            "signal_found": False,
            "reason": "Gap threshold too tight (0.82 vs required 0.78)",
            "suggestion": "Reduce gap_over_atr from 0.8 to 0.75",
            "status": "❌ MISSED"
        }
    ],
    "summary": {
        "total_examples": 2,
        "captured": 1,
        "missed": 1,
        "capture_rate": 0.5,
        "overall_status": "NEEDS_ADJUSTMENT"
    }
}
```

**Estimated LOC**: 130 lines
**Dependencies**: Scanner Executor Tool
**Testing Strategy**:
- Test with known A+ examples (should capture)
- Test with examples that should be missed (verify rejection)
- Test visual output generation
- Test suggestion accuracy (why missed?)

---

### Tool 14: Market Analyzer
**Source**: Researcher Agent (capabilities 3, 8)
**Purpose**: Analyze market regime, conditions, context

**Inputs**:
```python
{
    "ticker": "SPY",
    "date": "2024-01-15",
    "lookback_days": 60,
    "analysis_type": "regime" | "context" | "volatility" | "trend"
}
```

**Outputs**:
```python
{
    "market_regime": {
        "classification": "bull_market",
        "confidence": 0.87,
        "characteristics": {
            "trend": "uptrend",
            "volatility": "low",
            "volume": "above_average"
        },
        "duration": "45 days",  # how long in current regime
        "expected_setup_performance": {
            "Backside_ET": {"expected_win_rate": 0.72, "sample_size": 23},
            "Daily_Para": {"expected_win_rate": 0.68, "sample_size": 18}
        }
    },
    "daily_context": {
        "classification": "Front_Side",
        "ath_distance_pct": -2.3,  # 2.3% below ATH
        "mold_type": "Daily_Parabolic",
        "characteristics": {
            "parabolic_acceleration": True,
            "multiple_green_candles": 7,
            "volume_expansion": 1.8
        }
    },
    "volatility_analysis": {
        "current_atr": 3.2,
        "atr_percentile": 65,  # higher than 65% of last 60 days
        "volatility_regime": "normal",
        "suggested_stop_multiplier": 2.0
    },
    "trend_analysis": {
        "htf_trend": "bullish",  # Daily
        "mtf_trend": "bullish",  # 4hr
        "ltf_trend": "consolidating",  # 15m
        "trend_strength": 0.78,
        "recommended_action": "Look for long entries on LTF pullbacks"
    }
}
```

**Estimated LOC**: 120 lines
**Dependencies**: Knowledge Retriever (for historical context)
**Testing Strategy**:
- Test regime detection accuracy
- Test daily context classification (Front Side vs Backside vs IPO)
- Test volatility analysis
- Test trend identification across timeframes

---

### Tool 15: Visualizer
**Source**: Executor Agent (capability 10), Analyst Agent (capability 4)
**Purpose**: Generate charts, plots, visual representations

**Inputs**:
```python
{
    "visualization_type": "scanner_signals" | "equity_curve" | "parameter_sensitivity" | "trade_distribution",
    "data": {/* depends on type */},
    "chart_format": "plotly" | "matplotlib" | "tradingview",
    "output_format": "json" | "png" | "html",
    "styling": {
        "theme": "dark",
        "colors": {"primary": "#D4AF37", "secondary": "#111111"},
        "show_indicators": True
    }
}
```

**Outputs**:
```python
{
    "visualization": {
        "type": "plotly_figure",
        "data": [
            {
                "type": "candlestick",
                "x": ["2024-01-15 09:30", ...],
                "open": [477.0, ...],
                "high": [479.5, ...],
                "low": [476.2, ...],
                "close": [478.5, ...]
            },
            {
                "type": "scatter",
                "mode": "markers",
                "x": ["2024-01-15 10:32"],  # signal timestamp
                "y": [478.50],  # signal price
                "marker": {"size": 15, "color": "#D4AF37", "symbol": "triangle-up"},
                "name": "Entry Signal"
            }
        ],
        "layout": {
            "title": "SPY - Backside ET Signal (2024-01-15)",
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Price"},
            "template": "plotly_dark"
        }
    },
    "chart_url": "/charts/spy_backside_2024-01-15.html",
    "embed_code": '<iframe src="/charts/spy_backside_2024-01-15.html"></iframe>'
}
```

**Estimated LOC**: 140 lines
**Dependencies**: None (generates visualization config)
**Testing Strategy**:
- Test all visualization types
- Test different chart formats (Plotly, Matplotlib)
- Test styling/themes
- Test output generation (JSON, PNG, HTML)

---

## 🔄 RENATA ORCHESTRATOR

### Architecture
**Size**: 150-200 lines (lightweight coordinator)
**Responsibilities**:
1. Interpret user intent from chat messages
2. Determine which tools to call
3. Chain tool calls in workflows
4. Handle errors and retries
5. Present results to user in natural language

### Example Workflow: "Build a backside scanner from this A+ example"

```python
class RenataOrchestrator:
    def __init__(self):
        self.tools = {
            'parameter_extractor': ParameterExtractor(),
            'pattern_detector': PatternDetector(),
            'code_generator': CodeGenerator(),
            'v31_validator': V31Validator(),
            'scanner_executor': ScannerExecutor(),
            'a_plus_validator': APlusValidator(),
            # ... all 15 tools
        }

    def process_request(self, user_message, context):
        # Step 1: Understand intent
        intent = self.parse_intent(user_message)
        # intent = {"action": "build_scanner", "source": "a_plus_example", "setup": "backside"}

        # Step 2: Execute tool chain
        if intent['action'] == 'build_scanner':
            return self.workflow_build_from_a_plus(intent, context)

    def workflow_build_from_a_plus(self, intent, context):
        # Tool 1: Detect pattern from A+ example
        pattern_result = self.tools['pattern_detector'].execute(
            input_type='a_plus_example',
            data=context['a_plus_example']
        )

        # Tool 2: Extract parameters
        param_result = self.tools['parameter_extractor'].execute(
            source_type='a_plus_example',
            source_data=context['a_plus_example'],
            setup_type=pattern_result['detected_patterns'][0]['pattern_name']
        )

        # Tool 3: Generate scanner code
        code_result = self.tools['code_generator'].execute(
            parameters=param_result['parameters'],
            setup_type=param_result['setup_type'],
            v31_compliance=True
        )

        # Tool 4: Validate V31 compliance
        validation_result = self.tools['v31_validator'].execute(
            code=code_result['scanner_code'],
            strict_mode=True
        )

        if not validation_result['is_compliant']:
            return {
                'status': 'FAILED',
                'message': 'Generated code not V31 compliant',
                'violations': validation_result['violations']
            }

        # Tool 5: Validate against A+ example
        a_plus_validation = self.tools['a_plus_validator'].execute(
            scanner_code=code_result['scanner_code'],
            a_plus_examples=[context['a_plus_example']],
            visual_output=True
        )

        # Step 3: Present results
        return {
            'status': 'SUCCESS',
            'scanner_code': code_result['scanner_code'],
            'parameters': param_result['parameters'],
            'setup_type': pattern_result['detected_patterns'][0]['pattern_name'],
            'v31_compliance': validation_result['compliance_score'],
            'a_plus_validation': a_plus_validation['summary'],
            'chart_url': a_plus_validation['validation_results'][0]['chart_overlay']['url'],
            'message': f"""
✅ Built {pattern_result['detected_patterns'][0]['pattern_name']} scanner from A+ example!

**Parameters Extracted:**
{self.format_parameters(param_result['parameters'])}

**V31 Compliance:** {validation_result['compliance_score']:.1%}

**A+ Validation:** {a_plus_validation['summary']['overall_status']}
- Captured: {a_plus_validation['summary']['captured']}/{a_plus_validation['summary']['total_examples']} examples

[View Chart]({a_plus_validation['validation_results'][0]['chart_overlay']['url']})

Ready to run quick backtest?
"""
        }
```

### Workflow Templates
**Idea → Scanner**:
1. Parameter Extractor (from idea)
2. Code Generator
3. V31 Validator
4. Scanner Executor (quick test)

**A+ Example → Scanner**:
1. Pattern Detector
2. Parameter Extractor
3. Code Generator
4. V31 Validator
5. A+ Validator

**Optimization Loop**:
1. Backtest Runner (current params)
2. Performance Analyzer
3. Parameter Optimizer
4. Code Generator (with optimized params)
5. Backtest Runner (compare)

**Legacy Code → V31**:
1. V31 Validator (analyze current state)
2. Code Transformer
3. V31 Validator (verify transformation)
4. Scanner Executor (test)

---

## 📋 IMPLEMENTATION PLAN

### Phase 1: Tool Development (Weeks 1-2)
**Goal**: Build and test all 15 tools independently

**Week 1: Core Tools**
- Tool 3: V31 Validator (foundational, other tools depend on it)
- Tool 8: Knowledge Retriever (needed by most tools)
- Tool 1: Parameter Extractor
- Tool 9: Pattern Detector
- Tool 2: Code Generator

**Week 2: Execution & Analysis Tools**
- Tool 4: Scanner Executor
- Tool 5: Backtest Runner
- Tool 6: Performance Analyzer
- Tool 7: Parameter Optimizer
- Tool 13: A+ Validator

**Week 3: Specialized Tools**
- Tool 10: Risk Manager
- Tool 11: Execution Builder
- Tool 12: Code Transformer
- Tool 14: Market Analyzer
- Tool 15: Visualizer

### Phase 2: Orchestrator Development (Week 3)
**Goal**: Build simple orchestrator with workflow templates

**Tasks**:
1. Intent parser (user message → action)
2. Tool chaining logic
3. Error handling & retries
4. Result formatting (natural language)
5. Workflow templates (4 core workflows)

### Phase 3: Integration & Testing (Week 4)
**Goal**: End-to-end testing of all workflows

**Test Scenarios**:
1. Build scanner from idea (full workflow)
2. Build scanner from A+ example (full workflow)
3. Transform legacy code to V31 (full workflow)
4. Optimize existing scanner (full workflow)
5. Analyze backtest results (full workflow)

### Phase 4: Refinement (Week 5)
**Goal**: Polish, optimize, document

**Tasks**:
1. Performance optimization
2. Error message improvements
3. Tool parameter refinement
4. Documentation completion
5. User guide creation

---

## 🎯 SUCCESS METRICS

### Tool Quality Metrics
- **Test Coverage**: Each tool >90% unit test coverage
- **Independence**: Each tool runnable without orchestrator
- **Parameterization**: Each tool supports user's 13 setups
- **Error Handling**: Graceful failures with helpful messages
- **Performance**: Each tool <5 seconds response time

### Orchestrator Quality Metrics
- **Code Size**: 150-200 lines (lightweight!)
- **Workflow Success Rate**: >95% successful completions
- **Intent Understanding**: >90% accuracy in selecting correct tools
- **Error Recovery**: >80% successful retry on first failure

### System Quality Metrics
- **Total LOC**: ~2500 lines (15 tools × 150 avg + 200 orchestrator)
- **Reduction from Original**: ~60% reduction from 5 agents (~6500 lines)
- **Maintainability**: Each tool can be updated independently
- **Testability**: Each tool testable without other tools
- **Extensibility**: New tools can be added without modifying orchestrator

---

## 📊 COMPARISON: Before vs After

### Before: 5 Agents (Current Architecture)
```
PLANNING AGENT (800 LOC)
├─ Parameter extraction
├─ Pattern detection
├─ Workflow coordination
└─ [duplicate coordination code]

RESEARCHER AGENT (650 LOC)
├─ RAG search
├─ Market analysis
└─ [duplicate coordination code]

BUILDER AGENT (1500 LOC)
├─ Code generation
├─ V31 validation
├─ Execution building
├─ Risk management
└─ [duplicate coordination code]

EXECUTOR AGENT (900 LOC)
├─ Scanner execution
├─ Backtesting
└─ [duplicate coordination code]

ANALYST AGENT (1200 LOC)
├─ Performance analysis
├─ Optimization
└─ [duplicate coordination code]

Total: ~5050 LOC (unique functionality)
Total: ~6500 LOC (with duplicated coordination/wrappers)
```

### After: 1 Orchestrator + 15 Tools
```
ORCHESTRATOR (200 LOC)
├─ Intent parsing
├─ Tool selection
├─ Workflow chaining
└─ Result formatting

TOOLS (2500 LOC total)
├─ Tool 1: Parameter Extractor (120 LOC)
├─ Tool 2: Code Generator (180 LOC)
├─ Tool 3: V31 Validator (150 LOC)
├─ Tool 4: Scanner Executor (140 LOC)
├─ Tool 5: Backtest Runner (160 LOC)
├─ Tool 6: Performance Analyzer (200 LOC)
├─ Tool 7: Parameter Optimizer (180 LOC)
├─ Tool 8: Knowledge Retriever (100 LOC)
├─ Tool 9: Pattern Detector (150 LOC)
├─ Tool 10: Risk Manager (140 LOC)
├─ Tool 11: Execution Builder (160 LOC)
├─ Tool 12: Code Transformer (200 LOC)
├─ Tool 13: A+ Validator (130 LOC)
├─ Tool 14: Market Analyzer (120 LOC)
└─ Tool 15: Visualizer (140 LOC)

Total: ~2700 LOC
Reduction: 60% less code
```

---

## ✅ CHECKLIST: Tool Extraction Complete

**Core Principles Verified**:
- ✅ Each tool does ONE thing well
- ✅ Each tool is testable independently
- ✅ Each tool is parameterized (supports 13 setups)
- ✅ Orchestrator is simple coordinator (200 LOC)
- ✅ No duplicate code across tools
- ✅ Clear dependencies between tools
- ✅ All 56 capabilities mapped to tools

**Mapping Verification**:
- ✅ All 5 agent capabilities covered
- ✅ No capabilities lost in extraction
- ✅ Duplicate capabilities consolidated
- ✅ Cross-cutting concerns (RAG, context) handled properly

**Testing Strategy**:
- ✅ Each tool has testing approach defined
- ✅ Tool dependencies clear
- ✅ Integration test scenarios defined

**Implementation Plan**:
- ✅ 5-week development schedule
- ✅ Week-by-week breakdown
- ✅ Success metrics defined
- ✅ Comparison shows 60% code reduction

---

## 🚀 NEXT STEPS

1. **Review this plan** with team/stakeholders
2. **Prioritize tools** for Week 1 development
3. **Setup testing framework** for tool validation
4. **Begin implementation** with Tool 3 (V31 Validator)
5. **Daily progress tracking** against this plan

**Expected Outcome**: By end of Week 5, RENATA V2 will be a lean, maintainable, testable system with 15 powerful tools coordinated by a simple orchestrator - following Cole Medina's proven "tools before agents" principle.

---

**Document Status**: ✅ COMPLETE - Ready for implementation
**Total Tools Specified**: 15
**Total LOC Estimated**: ~2700 (60% reduction from ~6500)
**Implementation Timeline**: 5 weeks
