# 🛠️ RENATA V2 REFACTOR IMPLEMENTATION GUIDE
## Cole Medina "Tools Before Agents" Approach

**Date**: January 25, 2026
**Status**: ⏳ IN PROGRESS (Tool extraction phase)
**Timeline**: 5 weeks (Week 1-2: Tool extraction, Week 3: Orchestrator, Week 4: Integration, Week 5: Deploy)

---

## 🎯 REFACTOR GOALS

### Current Architecture Issues:
- ❌ **Over-engineered**: 5 agents with 56 capabilities
- ❌ **Complex**: Agents "thinking" instead of calling tools
- ❌ **Hard to test**: 56 code paths across 5 agents
- ❌ **Hard to debug**: Which agent capability failed?
- ❌ **Hard to scale**: Complex orchestration bottleneck

### Target Architecture Benefits:
- ✅ **Simple**: 1 orchestrator, 10-15 tools
- ✅ **Fast**: Direct tool calls (5-10x faster)
- ✅ **Testable**: Tools tested independently
- ✅ **Debuggable**: Clear failure modes (which tool failed?)
- ✅ **Scalable**: Tools scale horizontally

---

## 📋 PHASE 1: TOOL EXTRACTION (Week 1-2)

### Step 1: Map Agent Capabilities → Tools

**From Planner Agent (8 capabilities) → Tools**:
- Parameter extraction → `parameter_extraction_tool()`
- A+ example analysis → `a_analyzer_tool()`
- Mold generation → `mold_detector_tool()`
- Plan creation → `workflow_planner_tool()`

**From Researcher Agent (8 capabilities) → Tools**:
- Archon RAG search → `knowledge_search_tool()`
- Similar strategy search → `setup_matcher_tool()`
- Pattern matching → `pattern_detector_tool()`
- Market regime analysis → `regime_analyzer_tool()`
- Parameter suggestions → `parameter_suggester_tool()`

**From Builder Agent (20 capabilities) → Tools**:
- Scanner generation → `scanner_generator_tool()`
- Non-V31 to V31 transformation → `v31_transformer_tool()`
- Backtest code generation → `backtest_generator_tool()`
- Execution code generation → `execution_generator_tool()`
- Risk management code → `risk_manager_tool()`
- Position management code → `position_manager_tool()`
- V31 validation → `v31_validator_tool()`
- Code refactoring → `code_refactor_tool()`

**From Executor Agent (10 capabilities) → Tools**:
- FastAPI execution → `scanner_executor_tool()`
- Real-time progress → `progress_tracker_tool()`
- Result collection → `result_collector_tool()`
- A+ Example Analyzer → `a_analyzer_tool()`
- Idea Visualizer → `idea_visualizer_tool()`
- Parameter Sensitivity Analyzer → `sensitivity_analyzer_tool()`
- Quick Backtest Analyzer → `quick_backtest_tool()`
- Execution queue management → `queue_manager_tool()`

**From Analyst Agent (10 capabilities) → Tools**:
- Backtest analysis → `backtest_analyzer_tool()`
- IS/OOS validation → `robustness_validator_tool()`
- Monte Carlo simulation → `monte_carlo_tool()`
- Regime analysis → `regime_analyzer_tool()`
- Parameter optimization → `parameter_optimizer_tool()`

### Step 2: Consolidate into 15 Core Tools

After mapping and consolidating similar capabilities:

#### **Category 1: Scanner Tools (3 tools)**
1. **`scanner_generator_tool()`** (150 lines)
   - **Input**: Setup type, parameters, timeframe
   - **Output**: V31-compliant scanner code
   - **Capabilities from**: Builder (scanner generation from ideas, A+, molds)
   - **Test**: Generate scanner for known setup, validate V31 compliance

2. **`v31_validator_tool()`** (80 lines)
   - **Input**: Scanner code
   - **Output**: Validation result + issues
   - **Capabilities from**: Builder (V31 validation)
   - **Test**: Validate known V31 scanner (should pass), non-V31 (should fail with specific issues)

3. **`scanner_executor_tool()`** (120 lines)
   - **Input**: Scanner code, symbol(s), date range
   - **Output**: Execution results (signals, metrics)
   - **Capabilities from**: Executor (FastAPI execution, result collection)
   - **Test**: Execute on AAPL 2024-01-15, verify signal count

#### **Category 2: Market Analysis Tools (3 tools)**
4. **`indicator_calculator_tool()`** (100 lines)
   - **Input**: Market data, indicator type (user's indicators)
   - **Output**: Indicator values
   - **Capabilities from**: Builder (generates indicator code)
   - **Test**: Calculate 72/89 cloud, verify against known values

5. **`market_structure_tool()`** (120 lines)
   - **Input**: Price data
   - **Output**: Pivots, trends, levels, strength
   - **Capabilities from**: Researcher (pattern matching, structure analysis)
   - **Test**: Detect pivots on SPY, verify trend lines

6. **`daily_context_tool()`** (80 lines)
   - **Input**: Daily data
   - **Output**: Context (front/back/IPO), mold (D2/MDR/FBO/etc)
   - **Capabilities from**: Planner (mold generation, daily context)
   - **Test**: Detect D2 pattern on known example

#### **Category 3: Validation Tools (3 tools)**
7. **`a_analyzer_tool()`** (100 lines)
   - **Input**: Scanner code, A+ example (ticker + date)
   - **Output**: Visual validation (chart overlay)
   - **Capabilities from**: Planner (A+ analysis), Executor (A+ analyzer)
   - **Test**: Validate backside scanner on SPY 2024-01-15

8. **`quick_backtest_tool()`** (90 lines)
   - **Input**: Scanner code, date range (default: 30 days)
   - **Output**: Quick stats (signals, win rate, return)
   - **Capabilities from**: Executor (quick backtest analyzer)
   - **Test**: Run on last 30 days, verify <10 seconds execution

9. **`robustness_validator_tool()`** (100 lines)
   - **Input**: Backtest results
   - **Output**: IS/OOS comparison, Monte Carlo simulation
   - **Capabilities from**: Analyst (IS/OOS, Monte Carlo)
   - **Test**: Validate robust strategy vs overfitted

#### **Category 4: Optimization Tools (2 tools)**
10. **`parameter_optimizer_tool()`** (80 lines)
    - **Input**: Scanner code, parameter ranges
    - **Output**: Best parameters (grid search)
    - **Capabilities from**: Analyst (parameter optimization)
    - **Test**: Optimize gap_over_atr: 0.6-1.0, find best

11. **`sensitivity_analyzer_tool()`** (60 lines)
    - **Input**: Scanner code, base parameters
    - **Output**: Sensitivity table (param changes → signal count)
    - **Capabilities from**: Executor (parameter sensitivity analyzer)
    - **Test**: Vary gap_atr 0.7/0.8/0.9, show signal changes

#### **Category 5: Backtest Tools (2 tools)**
12. **`backtest_generator_tool()`** (100 lines)
    - **Input**: Scanner code, backtest config
    - **Output**: Backtest engine code
    - **Capabilities from**: Builder (backtest generation)
    - **Test**: Generate backtest for known setup

13. **`backtest_analyzer_tool()`** (80 lines)
    - **Input**: Backtest results
    - **Output**: Analysis (Sharpe, drawdown, win rate, etc.)
    - **Capabilities from**: Analyst (backtest analysis)
    - **Test**: Analyze backtest, verify metrics

#### **Category 6: Knowledge Tools (2 tools)**
14. **`knowledge_search_tool()`** (70 lines)
    - **Input**: Query (Archon RAG)
    - **Output**: Relevant knowledge (setups, patterns, parameters)
    - **Capabilities from**: Researcher (Archon RAG search)
    - **Test**: Search "backside B", return relevant setups

15. **`setup_matcher_tool()`** (80 lines)
    - **Input**: User description
    - **Output**: Matching setups (from Lingua 13)
    - **Capabilities from**: Researcher (similar strategy search)
    - **Test**: Describe gap setup, match to OS D1

### Step 3: Tool Implementation Templates

#### Template: Scanner Generator Tool
```python
# File: tools/scanner_generator_tool.py

def scanner_generator_tool(
    setup_type: str,
    parameters: dict,
    timeframe: str = "15m",
    market_coverage: str = "all"
) -> dict:
    """
    Generate V31-compliant scanner code.

    Args:
        setup_type: One of 13 setups (OS D1, G2G S1, SC DMR, etc.)
        parameters: Setup-specific parameters (gap_over_atr, vol_mult, etc.)
        timeframe: Analysis timeframe (15m, 1hr, daily)
        market_coverage: "all" (12k tickers) or specific list

    Returns:
        dict: {
            "scanner_code": str,  # V31-compliant Python code
            "parameters": dict,    # Parameters used
            "v31_compliant": bool, # V31 validation result
            "warnings": list       # Any warnings
        }

    Raises:
        ValueError: If setup_type not recognized
        ValidationError: If parameters invalid for setup
    """

    # Step 1: Validate setup type
    valid_setups = [
        "OS D1", "G2G S1", "SC DMR", "SC MDR Swing",
        "Daily Para Run", "EXT Uptrend Gap", "Para FRD",
        "MDR", "LC FBO", "LC T30", "LC Extended Trendbreak",
        "LC Breakdown", "Backside Trend Pop", "Backside Euphoric"
    ]

    if setup_type not in valid_setups:
        raise ValueError(f"Unknown setup: {setup_type}")

    # Step 2: Get setup template
    template = SETUP_TEMPLATES[setup_type]

    # Step 3: Generate V31 scanner code
    scanner_code = generate_v31_scanner(
        setup_type=setup_type,
        parameters=parameters,
        timeframe=timeframe,
        market_coverage=market_coverage
    )

    # Step 4: Validate V31 compliance
    validation = v31_validator_tool(scanner_code)

    return {
        "scanner_code": scanner_code,
        "parameters": parameters,
        "v31_compliant": validation["compliant"],
        "warnings": validation.get("warnings", [])
    }


def generate_v31_scanner(setup_type, parameters, timeframe, market_coverage):
    """Generate V31-compliant scanner code (internal function)."""

    if market_coverage == "all":
        # Pillar 0: Market scanning architecture
        ticker_list = "NYSE_NASDAQ_ETF_ALL"  # ~12k tickers
    else:
        ticker_list = parameters.get("ticker_list", [])

    # Generate 3-stage V31 architecture
    code = f"""
import pandas as pd
import numpy as np
from polygon import RESTClient

# {setup_type} Scanner
# Generated: {datetime.now().isoformat()}

# Stage 1: Preliminary Fetch (Grouped)
def get_stage1_symbols(date):
    '''Fetch all symbols for preliminary filtering'''
    ticker_list = {ticker_list}
    # Fetch grouped daily bars from Polygon
    # Return: all symbols with OHLCV data

# Stage 2: Per-Ticker Operations
def stage2_per_ticker(symbol, date, params):
    '''Apply setup-specific logic per ticker'''
    gap_over_atr = params.get('gap_over_atr', {parameters.get('gap_over_atr', 0.8)})
    vol_mult = params.get('vol_mult', {parameters.get('vol_mult', 1.2)})

    # Calculate gap % from previous close
    # Check if gap_over_atr threshold met
    # Check volume spike
    # Return: signal or no signal

# Stage 3: Aggregation
def stage3_aggregation(signals):
    '''Aggregate all signals'''
    return pd.DataFrame(signals)

# Main execution
def run_scanner(date):
    stage1_symbols = get_stage1_symbols(date)
    signals = []
    for symbol in stage1_symbols:
        signal = stage2_per_ticker(symbol, date, {parameters})
        if signal:
            signals.append(signal)
    return stage3_aggregation(signals)
"""

    return code


# Setup templates (simplified)
SETUP_TEMPLATES = {
    "OS D1": {
        "required_params": ["gap_over_atr", "vol_mult"],
        "indicators": ["gap_percent", "volume_spike"],
        "timeframes": ["15m", "daily"]
    },
    "G2G S1": {
        "required_params": ["gap_continuation_threshold"],
        "indicators": ["gap_percent", "morning_trend"],
        "timeframes": ["15m"]
    },
    # ... other 11 setups
}
```

#### Template: Orchestrator Agent
```python
# File: agents/orchestrator_agent.py

class RenataOrchestrator:
    """
    Simple coordinator - doesn't do work, just calls tools.

    NO complex decision making.
    NO "thinking" or generating code.
    Just: Classify → Select → Run → Return
    """

    def __init__(self):
        # Available tools
        self.tools = {
            "generate_scanner": scanner_generator_tool,
            "validate_v31": v31_validator_tool,
            "execute_scanner": scanner_executor_tool,
            "a_analyze": a_analyzer_tool,
            "quick_backtest": quick_backtest_tool,
            "optimize_params": parameter_optimizer_tool,
            "analyze_backtest": backtest_analyzer_tool,
            "search_knowledge": knowledge_search_tool,
            "match_setup": setup_matcher_tool,
            # ... other tools
        }

    def handle_user_request(self, user_message: str, context: dict = None) -> dict:
        """
        Main entry point for all user requests.

        Args:
            user_message: Natural language request
            context: Current page (/plan, /scan, /backtest), active project, etc.

        Returns:
            dict: Result from tool execution
        """

        # Step 1: Classify intent
        intent = self.classify_intent(user_message, context)

        # Step 2: Select tool
        tool = self.select_tool(intent)

        # Step 3: Extract parameters
        parameters = self.extract_parameters(user_message, intent)

        # Step 4: Ask user if critical params missing
        missing_params = tool.get_required_parameters()
        if any(p not in parameters for p in missing_params):
            # Ask user for missing parameters
            return {"need_input": missing_params}

        # Step 5: Run tool
        result = tool(**parameters)

        # Step 6: Format result for user
        formatted = self.format_result(result, intent)

        return formatted

    def classify_intent(self, message: str, context: dict) -> str:
        """Classify what user wants to do."""

        # Simple keyword matching (NOT complex NLP)
        message_lower = message.lower()

        if "build" in message_lower and "scanner" in message_lower:
            return "generate_scanner"

        elif "validate" in message_lower or "check" in message_lower:
            return "validate_v31"

        elif "run" in message_lower or "execute" in message_lower:
            return "execute_scanner"

        elif "a+ example" in message_lower or "validate on" in message_lower:
            return "a_analyze"

        elif "quick backtest" in message_lower or "test" in message_lower:
            return "quick_backtest"

        elif "optimize" in message_lower or "best parameters" in message_lower:
            return "optimize_params"

        elif "analyze" in message_lower and "backtest" in message_lower:
            return "analyze_backtest"

        elif "search" in message_lower or "find" in message_lower:
            return "search_knowledge"

        elif "setup" in message_lower or "similar" in message_lower:
            return "match_setup"

        else:
            return "unknown"  # Ask user to clarify

    def select_tool(self, intent: str):
        """Select appropriate tool for intent."""
        return self.tools.get(intent)

    def extract_parameters(self, message: str, intent: str) -> dict:
        """Extract parameters from user message."""

        # Simple extraction (NOT complex NLP)
        params = {}

        if intent == "generate_scanner":
            # Extract setup type
            if "backside" in message.lower():
                params["setup_type"] = "Backside Trend Pop"
            elif "gap" in message.lower():
                params["setup_type"] = "OS D1"
            # ... other setups

            # Extract parameters
            # Use parameter_extraction_tool() here

        return params

    def format_result(self, result: dict, intent: str) -> dict:
        """Format tool result for user."""

        if intent == "generate_scanner":
            return {
                "message": f"✅ Scanner generated! V31 compliant: {result['v31_compliant']}",
                "scanner_code": result["scanner_code"],
                "next_action": "Run on test data?",
                "link": f"/scan?scanner={result['scanner_id']}"
            }

        elif intent == "quick_backtest":
            return {
                "message": f"📊 Backtest complete: {result['signal_count']} signals, {result['win_rate']}% win rate",
                "metrics": result["metrics"],
                "link": f"/backtest?backtest={result['backtest_id']}"
            }

        return result
```

### Step 4: Testing Strategy

#### Unit Tests (Per Tool)
```python
# tests/test_scanner_generator_tool.py

def test_generate_os_d1_scanner():
    """Test generating OS D1 scanner."""
    result = scanner_generator_tool(
        setup_type="OS D1",
        parameters={"gap_over_atr": 0.8, "vol_mult": 1.2}
    )

    assert result["v31_compliant"] == True
    assert "def get_stage1_symbols" in result["scanner_code"]
    assert "def stage2_per_ticker" in result["scanner_code"]
    assert "def stage3_aggregation" in result["scanner_code"]


def test_v31_validator_passes_valid_scanner():
    """Test validator passes known V31 scanner."""
    valid_v31_scanner = """
def get_stage1_symbols(date):
    return ["AAPL", "TSLA"]

def stage2_per_ticker(symbol, date, params):
    return {"signal": True}

def stage3_aggregation(signals):
    return pd.DataFrame(signals)
"""

    result = v31_validator_tool(valid_v31_scanner)
    assert result["compliant"] == True
    assert len(result["issues"]) == 0


def test_v31_validator_fails_non_v31_scanner():
    """Test validator fails non-V31 scanner."""
    non_v31_scanner = """
# Not V31 compliant - no 3-stage architecture
def scan_all_symbols(symbols):
    for symbol in symbols:
        if condition:
            return signal
"""

    result = v31_validator_tool(non_v31_scanner)
    assert result["compliant"] == False
    assert "missing 3-stage architecture" in str(result["issues"]).lower()
```

#### Integration Tests
```python
# tests/test_integration.py

def test_build_validate_execute_workflow():
    """Test complete workflow: build → validate → execute."""

    # Step 1: Generate scanner
    scanner = scanner_generator_tool(
        setup_type="OS D1",
        parameters={"gap_over_atr": 0.8, "vol_mult": 1.2}
    )
    assert scanner["v31_compliant"] == True

    # Step 2: Validate
    validation = v31_validator_tool(scanner["scanner_code"])
    assert validation["compliant"] == True

    # Step 3: Execute
    results = scanner_executor_tool(
        scanner_code=scanner["scanner_code"],
        symbols=["AAPL"],
        date="2024-01-15"
    )
    assert results["signal_count"] >= 0


def test_parameter_optimization_workflow():
    """Test optimize → sensitivity workflow."""

    # Optimize parameters
    best_params = parameter_optimizer_tool(
        scanner_code=scanner_code,
        parameter_ranges={"gap_over_atr": [0.6, 0.7, 0.8, 0.9, 1.0]}
    )
    assert "best_parameters" in best_params

    # Sensitivity analysis
    sensitivity = sensitivity_analyzer_tool(
        scanner_code=scanner_code,
        base_parameters=best_params["best_parameters"]
    )
    assert "sensitivity_table" in sensitivity
```

---

## 📋 PHASE 2: ORCHESTRATOR BUILD (Week 3)

### Orchestrator Design Principles:
1. **Simple routing**: Classify intent → Select tool → Run → Return
2. **No complex logic**: Tools do the work, orchestrator just coordinates
3. **Parameter gathering**: Ask user if missing critical parameters
4. **Result formatting**: Present tool results clearly to user

### Orchestrator Tasks:
- [ ] Build intent classifier (keyword matching, not NLP)
- [ ] Implement tool selection logic
- [ ] Create parameter extraction/gathering
- [ ] Implement result formatting
- [ ] Add error handling (tool failure → suggest fix)
- [ ] Test orchestrator with all 15 tools

---

## 📋 PHASE 3: INTEGRATION TESTING (Week 4)

### Integration Tasks:
- [ ] Connect orchestrator to all tools
- [ ] Test user workflows (build → validate → execute → analyze)
- [ ] Test all 13 setups through orchestrator
- [ ] Test error recovery (tool fails → orchestrator suggests fix)
- [ ] Performance testing (ensure <5 second response time)
- [ ] UI integration (test with /plan, /scan, /backtest pages)

---

## 📋 PHASE 4: DEPLOY & SCALE (Week 5)

### Deployment Tasks:
- [ ] Deploy tools to production (FastAPI endpoints)
- [ ] Deploy orchestrator (CopilotKit integration)
- [ ] Monitor reliability (track tool success rates)
- [ ] Scale tool instances (if needed)
- [ ] User acceptance testing (validate workflows)
- [ ] Documentation update (update all sprint docs)

---

## ✅ SUCCESS CRITERIA

### Tool Quality:
- [ ] All 15 tools unit tested (95%+ coverage)
- [ ] All tools tested independently
- [ ] All tools have clear interfaces (inputs/outputs documented)
- [ ] All tools execute in <2 seconds (except backtest tools)

### Orchestrator Quality:
- [ ] Orchestrator routes all requests correctly
- [ ] Orchestrator handles all 13 setups
- [ ] Orchestrator asks for missing parameters
- [ ] Orchestrator formats results clearly

### Integration Quality:
- [ ] All workflows tested (build → validate → execute)
- [ ] Error recovery works (tool fails → suggest fix)
- [ ] UI integration works (/plan, /scan, /backtest)
- [ ] Performance meets targets (<5 second response)

### User Acceptance:
- [ ] User validates tool quality
- [ ] User validates orchestrator workflows
- [ ] User validates UI integration
- [ ] System ready for production use

---

## 📊 METRICS TO TRACK

### Before Refactor (Current):
- Tool reliability: Unknown (no tools, everything in agents)
- Response time: 30-60 seconds (agent orchestration)
- Debugging difficulty: High (56 code paths across 5 agents)
- Scaling difficulty: High (complex agent coordination)

### After Refactor (Target):
- Tool reliability: 99%+ (tested independently)
- Response time: 5-10 seconds (direct tool calls)
- Debugging difficulty: Low (clear which tool failed)
- Scaling difficulty: Low (just add more tool instances)

---

## 🎯 NEXT STEPS

1. ✅ **COMPLETE**: Tool extraction plan (agent working on it)
2. ⏳ **IN PROGRESS**: Implement 15 core tools
3. ⏸️ **PENDING**: Build orchestrator agent
4. ⏸️ **PENDING**: Integration testing
5. ⏸️ **PENDING**: Deploy and scale

**This refactor achieves your vision better than the complex 5-agent system.**
**Tools = reliable, scalable, testable. Orchestrator = simple coordination.**
**Result: $1M/month path is clearer with simple, proven architecture.**
