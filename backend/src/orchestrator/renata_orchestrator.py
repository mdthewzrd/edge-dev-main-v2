"""
RENATA V2 Orchestrator Agent

The brain that coordinates all 13 tools
Version: 1.0.0
Purpose: Understand user requests and route to appropriate tools
"""

from typing import Dict, Any, List, Optional, Tuple
import re
import time

# Import shared types
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

# Import all 13 tools
from tools.v31_scanner_generator import v31_scanner_generator
from tools.v31_validator import v31_validator
from tools.scanner_executor import scanner_executor
from tools.indicator_calculator import indicator_calculator
from tools.market_structure_analyzer import market_structure_analyzer
from tools.daily_context_detector import daily_context_detector
from tools.a_plus_analyzer import a_plus_analyzer
from tools.quick_backtester import quick_backtester
from tools.parameter_optimizer import parameter_optimizer
from tools.sensitivity_analyzer import sensitivity_analyzer
from tools.backtest_generator import backtest_generator
from tools.backtest_analyzer import backtest_analyzer
from tools.build_plan_generator import build_plan_generator
from tools.tool_types import ToolStatus, ToolResult


class RenataOrchestrator:
    """
    RENATA V2 Orchestrator Agent

    The intelligent coordinator that:
    1. Understands user intent from natural language
    2. Selects appropriate tools
    3. Gathers required parameters
    4. Executes workflows
    5. Formats results for users
    """

    def __init__(self):
        """Initialize the orchestrator"""
        self.tool_registry = self._build_tool_registry()
        self.conversation_history = []

    def _build_tool_registry(self) -> Dict[str, Dict]:
        """
        Build registry of all available tools

        Returns:
            Dictionary mapping tool names to their metadata
        """
        return {
            "v31_scanner_generator": {
                "name": "V31 Scanner Generator",
                "description": "Generate V31-compliant scanner code from description",
                "keywords": ["generate", "create", "scanner", "code", "v31"],
                "required_params": ["description"],
                "optional_params": ["parameters"],
                "function": v31_scanner_generator
            },
            "v31_validator": {
                "name": "V31 Validator",
                "description": "Validate scanner meets V31 Gold Standard",
                "keywords": ["validate", "check", "compliance", "v31", "standards"],
                "required_params": ["scanner_code"],
                "optional_params": ["strict_mode"],
                "function": v31_validator
            },
            "indicator_calculator": {
                "name": "Indicator Calculator",
                "description": "Calculate proprietary indicators (RahulLines Cloud, Deviation Bands)",
                "keywords": ["indicator", "rahullines", "cloud", "ema", "deviation", "calculate"],
                "required_params": ["ticker", "df"],
                "optional_params": ["indicators"],
                "function": indicator_calculator
            },
            "market_structure_analyzer": {
                "name": "Market Structure Analyzer",
                "description": "Detect pivots, trends, support/resistance levels",
                "keywords": ["pivot", "trend", "support", "resistance", "structure", "levels"],
                "required_params": ["ticker", "df"],
                "optional_params": ["pivot_lookback", "trend_lookback"],
                "function": market_structure_analyzer
            },
            "daily_context_detector": {
                "name": "Daily Context Detector",
                "description": "Detect daily market molds (D2, MDR, FBO, T30)",
                "keywords": ["daily", "context", "mold", "market type", "d2", "mdr", "fbo"],
                "required_params": ["df"],
                "optional_params": ["date"],
                "function": daily_context_detector
            },
            "a_plus_analyzer": {
                "name": "A+ Analyzer",
                "description": "Validate scanner against A+ historical examples",
                "keywords": ["a+", "example", "validate", "historical", "backtest"],
                "required_params": ["scanner_code", "a_plus_examples"],
                "optional_params": ["strict_mode"],
                "function": a_plus_analyzer
            },
            "quick_backtester": {
                "name": "Quick Backtester",
                "description": "Fast 30-day backtest validation",
                "keywords": ["backtest", "test", "validate", "performance", "quick", "30-day"],
                "required_params": ["scanner_results"],
                "optional_params": ["entry_price_col", "exit_price_col"],
                "function": quick_backtester
            },
            "parameter_optimizer": {
                "name": "Parameter Optimizer",
                "description": "Optimize scanner parameters using grid search",
                "keywords": ["optimize", "parameter", "tune", "grid search", "best"],
                "required_params": ["scanner_function", "parameter_ranges", "evaluation_data"],
                "optional_params": ["metric"],
                "function": parameter_optimizer
            },
            "sensitivity_analyzer": {
                "name": "Sensitivity Analyzer",
                "description": "Test parameter sensitivity and robustness",
                "keywords": ["sensitivity", "robustness", "variation", "stable"],
                "required_params": ["scanner_function", "base_parameters", "evaluation_data"],
                "optional_params": ["parameter_variations"],
                "function": sensitivity_analyzer
            },
            "backtest_generator": {
                "name": "Backtest Generator",
                "description": "Generate complete backtest script from scanner",
                "keywords": ["generate", "backtest", "script", "code"],
                "required_params": ["scanner_code"],
                "optional_params": ["backtest_config"],
                "function": backtest_generator
            },
            "backtest_analyzer": {
                "name": "Backtest Analyzer",
                "description": "Analyze backtest results and metrics",
                "keywords": ["analyze", "metrics", "performance", "sharpe", "drawdown"],
                "required_params": ["backtest_results"],
                "optional_params": ["initial_capital"],
                "function": backtest_analyzer
            },
            "build_plan_generator": {
                "name": "Build Plan Generator",
                "description": "Generate implementation plan for trading strategies",
                "keywords": ["plan", "strategy", "implementation", "roadmap", "steps"],
                "required_params": ["strategy_description", "setup_types"],
                "optional_params": ["complexity_level"],
                "function": build_plan_generator
            },
            "scanner_executor": {
                "name": "Scanner Executor",
                "description": "Execute scanner on live market data",
                "keywords": ["execute", "run", "scanner", "live", "market"],
                "required_params": ["scanner_code", "symbols"],
                "optional_params": ["date"],
                "function": scanner_executor
            }
        }

    def process_request(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process user request and coordinate tools

        Args:
            user_input: Natural language request from user
            context: Additional context (data, previous results, etc.)

        Returns:
            Dictionary with response and metadata
        """

        start_time = time.time()

        # Step 1: Understand intent
        intent = self._understand_intent(user_input)

        # Step 2: Select tools
        selected_tools = self._select_tools(intent, user_input)

        # Step 3: Execute workflow
        results = self._execute_workflow(selected_tools, user_input, context)

        # Step 4: Format response
        response = self._format_response(results, intent)

        execution_time = time.time() - start_time

        return {
            "response": response,
            "intent": intent,
            "tools_used": [tool["name"] for tool in selected_tools],
            "execution_time": execution_time,
            "success": all(r.status == ToolStatus.SUCCESS for r in results)
        }

    def _understand_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Understand user intent from natural language

        Returns:
            Dictionary with intent classification
        """

        user_input_lower = user_input.lower()

        # Classify intent type
        # Check for multi-intent requests first
        has_generate = any(word in user_input_lower for word in ["generate", "create", "build"])
        has_validate = any(word in user_input_lower for word in ["validate", "check", "compliance"])
        has_backtest = any(word in user_input_lower for word in ["backtest", "performance"])
        has_analyze = any(word in user_input_lower for word in ["analyze", "indicator", "structure", "trend", "market"])
        has_optimize = any(word in user_input_lower for word in ["optimize", "tune"])
        has_plan = any(word in user_input_lower for word in ["plan", "strategy", "implementation"])
        has_execute = any(word in user_input_lower for word in ["execute", "run"])

        # Priority: multi-tool workflows > specific intents
        if has_generate and has_validate:
            intent_type = "GENERATE_SCANNER"  # Will chain validator
        elif has_generate and has_backtest:
            intent_type = "GENERATE_SCANNER"  # Will chain backtest
        elif has_validate and not has_generate:
            intent_type = "VALIDATE"
        elif has_backtest and not has_generate:
            intent_type = "BACKTEST"
        elif has_optimize:
            intent_type = "OPTIMIZE"
        elif has_plan:
            intent_type = "PLAN"
        elif has_analyze:
            intent_type = "ANALYZE"
        elif has_execute:
            intent_type = "EXECUTE"
        elif has_generate:
            intent_type = "GENERATE_SCANNER"
        else:
            intent_type = "GENERAL"

        # Extract details
        details = self._extract_details(user_input, intent_type)

        return {
            "type": intent_type,
            "details": details,
            "original_input": user_input
        }

    def _extract_details(self, user_input: str, intent_type: str) -> Dict[str, Any]:
        """Extract relevant details from user input"""

        details = {}
        user_input_lower = user_input.lower()

        # Detect setup types
        setup_types = []
        if "backside" in user_input_lower or "gap" in user_input_lower:
            setup_types.append("BACKSIDE_B")
        if "d2" in user_input_lower:
            setup_types.append("D2")
        if "mdr" in user_input_lower or "multi" in user_input_lower:
            setup_types.append("MDR")
        if "fbo" in user_input_lower:
            setup_types.append("FBO")

        if setup_types:
            details["setup_types"] = setup_types

        # Detect complexity
        if any(word in user_input_lower for word in ["simple", "basic"]):
            details["complexity"] = "simple"
        elif any(word in user_input_lower for word in ["complex", "advanced", "comprehensive"]):
            details["complexity"] = "complex"
        else:
            details["complexity"] = "medium"

        # Detect tickers/symbols
        ticker_pattern = r'\b[A-Z]{1,5}\b'
        tickers = re.findall(ticker_pattern, user_input)
        if tickers:
            details["tickers"] = tickers

        return details

    def _select_tools(self, intent: Dict[str, Any], user_input: str) -> List[Dict]:
        """
        Select appropriate tools based on intent

        Returns:
            List of selected tool configurations
        """

        intent_type = intent["type"]
        details = intent["details"]
        selected = []

        # Tool selection logic
        if intent_type == "GENERATE_SCANNER":
            selected.append(self.tool_registry["v31_scanner_generator"])
            selected.append(self.tool_registry["v31_validator"])

        elif intent_type == "VALIDATE":
            if "scanner" in user_input.lower():
                selected.append(self.tool_registry["v31_validator"])
            if "a+" in user_input.lower():
                selected.append(self.tool_registry["a_plus_analyzer"])

        elif intent_type == "BACKTEST":
            selected.append(self.tool_registry["quick_backtester"])
            selected.append(self.tool_registry["backtest_analyzer"])

        elif intent_type == "ANALYZE":
            selected.append(self.tool_registry["indicator_calculator"])
            selected.append(self.tool_registry["market_structure_analyzer"])

        elif intent_type == "OPTIMIZE":
            selected.append(self.tool_registry["parameter_optimizer"])
            selected.append(self.tool_registry["sensitivity_analyzer"])

        elif intent_type == "PLAN":
            selected.append(self.tool_registry["build_plan_generator"])

        elif intent_type == "EXECUTE":
            selected.append(self.tool_registry["scanner_executor"])

        return selected

    def _execute_workflow(self, tools: List[Dict], user_input: str, context: Optional[Dict]) -> List[ToolResult]:
        """
        Execute selected tools as workflow

        Returns:
            List of tool results
        """

        results = []

        for tool in tools:
            try:
                # Prepare input for tool
                tool_input = self._prepare_tool_input(tool, user_input, context, results)

                # Execute tool
                result = tool["function"](tool_input)
                results.append(result)

                # Stop if critical error
                if result.status == ToolStatus.ERROR and "FATAL" in str(result.error).upper():
                    break

            except Exception as e:
                # Create error result
                results.append(ToolResult(
                    status=ToolStatus.ERROR,
                    result=None,
                    error={"code": "EXECUTION_ERROR", "message": str(e)},
                    warnings=None,
                    execution_time=0,
                    tool_version="1.0.0"
                ))

        return results

    def _prepare_tool_input(self, tool: Dict, user_input: str, context: Optional[Dict], previous_results: List) -> Dict[str, Any]:
        """
        Prepare input parameters for tool

        Returns:
            Dictionary with tool input parameters
        """

        tool_name = tool["name"]
        input_data = {}

        # Use context if available
        if context:
            if "df" in context and "df" in tool.get("required_params", []):
                input_data["df"] = context["df"]
            if "scanner_code" in context and "scanner_code" in tool.get("required_params", []):
                input_data["scanner_code"] = context["scanner_code"]

        # Extract from previous results
        for result in previous_results:
            if result.status == ToolStatus.SUCCESS and result.result:
                if "scanner_code" in result.result and "scanner_code" in tool.get("required_params", []):
                    input_data["scanner_code"] = result.result["scanner_code"]

        # Tool-specific preparation
        if tool_name == "V31 Scanner Generator":
            input_data["description"] = user_input
            input_data["parameters"] = context.get("parameters", {}) if context else {}

        elif tool_name == "V31 Validator":
            if "scanner_code" not in input_data:
                # Generate scanner first
                scanner_result = v31_scanner_generator({"description": user_input})
                if scanner_result.status == ToolStatus.SUCCESS:
                    input_data["scanner_code"] = scanner_result.result["scanner_code"]

        elif tool_name == "Indicator Calculator":
            if "df" not in input_data:
                # Use sample data if no context
                import pandas as pd
                import numpy as np
                dates = pd.date_range('2024-01-01', periods=100, freq='D')
                input_data["df"] = pd.DataFrame({
                    'date': dates,
                    'open': np.random.uniform(90, 110, 100),
                    'high': np.random.uniform(90, 110, 100),
                    'low': np.random.uniform(90, 110, 100),
                    'close': np.random.uniform(90, 110, 100),
                    'volume': np.random.randint(1000000, 10000000, 100)
                })
            if "ticker" not in input_data:
                input_data["ticker"] = context.get("ticker", "AAPL") if context else "AAPL"
            # Add default indicators if not specified
            if "indicators" not in input_data:
                input_data["indicators"] = ["72_89_cloud", "9_20_cloud"]

        elif tool_name == "Build Plan Generator":
            input_data["strategy_description"] = context.get("strategy_description", user_input) if context else user_input
            input_data["setup_types"] = context.get("setup_types", ["D2"]) if context else ["D2"]
            input_data["complexity_level"] = context.get("complexity_level", "medium") if context else "medium"

        # Add default values for optional params
        for param in tool.get("optional_params", []):
            if param not in input_data:
                input_data[param] = None  # Tool will use default

        return input_data

    def _format_response(self, results: List[ToolResult], intent: Dict) -> str:
        """
        Format tool results into user-friendly response

        Returns:
            Formatted response string
        """

        intent_type = intent["type"]

        # Check for errors
        errors = [r for r in results if r.status == ToolStatus.ERROR]
        if errors:
            error_msg = f"❌ Error: {errors[0].error.get('message', 'Unknown error')}"
            return error_msg

        # Format based on intent type
        if intent_type == "GENERATE_SCANNER":
            return self._format_scanner_generation(results)
        elif intent_type == "ANALYZE":
            return self._format_analysis(results)
        elif intent_type == "OPTIMIZE":
            return self._format_optimization(results)
        elif intent_type == "BACKTEST":
            return self._format_backtest(results)
        elif intent_type == "PLAN":
            return self._format_plan(results)
        else:
            return self._format_generic(results)

    def _format_scanner_generation(self, results: List[ToolResult]) -> str:
        """Format scanner generation results"""

        response = ["✅ **Scanner Generated Successfully!**\n"]

        for result in results:
            if result.status == ToolStatus.SUCCESS:
                if "scanner_code" in result.result:
                    response.append(f"📄 Scanner code: {len(result.result['scanner_code'])} characters")
                if "compliance_score" in result.result:
                    score = result.result["compliance_score"]
                    response.append(f"✅ Compliance Score: {score}/100")

        return "\n".join(response)

    def _format_analysis(self, results: List[ToolResult]) -> str:
        """Format analysis results"""

        response = ["✅ **Analysis Complete**\n"]

        for result in results:
            if result.status == ToolStatus.SUCCESS:
                if "trend" in result.result:
                    trend = result.result["trend"]["direction"]
                    response.append(f"📈 Trend: {trend}")
                if "pivots" in result.result:
                    high_pivots = len(result.result["pivots"].get("high_pivots", []))
                    low_pivots = len(result.result["pivots"].get("low_pivots", []))
                    response.append(f"🔺 High Pivots: {high_pivots}")
                    response.append(f"🔻 Low Pivots: {low_pivots}")

        return "\n".join(response)

    def _format_optimization(self, results: List[ToolResult]) -> str:
        """Format optimization results"""

        response = ["✅ **Optimization Complete**\n"]

        for result in results:
            if result.status == ToolStatus.SUCCESS:
                if "best_parameters" in result.result:
                    response.append(f"🎯 Best Parameters: {result.result['best_parameters']}")
                if "robustness_score" in result.result:
                    response.append(f"🛡️ Robustness: {result.result['robustness_score']}/100")

        return "\n".join(response)

    def _format_backtest(self, results: List[ToolResult]) -> str:
        """Format backtest results"""

        response = ["✅ **Backtest Complete**\n"]

        for result in results:
            if result.status == ToolStatus.SUCCESS:
                if "total_return" in result.result:
                    response.append(f"📊 Total Return: {result.result['total_return']:.2f}%")
                if "win_rate" in result.result:
                    response.append(f"📈 Win Rate: {result.result['win_rate']:.1f}%")
                if "sharpe_ratio" in result.result:
                    response.append(f"⚡ Sharpe Ratio: {result.result['sharpe_ratio']:.2f}")

        return "\n".join(response)

    def _format_plan(self, results: List[ToolResult]) -> str:
        """Format plan results"""

        response = ["✅ **Implementation Plan Generated**\n"]

        for result in results:
            if result.status == ToolStatus.SUCCESS:
                if "strategy_name" in result.result:
                    response.append(f"📋 Strategy: {result.result['strategy_name']}")
                if "implementation_steps" in result.result:
                    steps = result.result["implementation_steps"]
                    response.append(f"📝 Steps: {len(steps)} implementation steps")
                if "estimates" in result.result:
                    estimates = result.result["estimates"]
                    response.append(f"⏱️ Estimated: {estimates.get('total_days', 'N/A')} days")

        return "\n".join(response)

    def _format_generic(self, results: List[ToolResult]) -> str:
        """Format generic results"""

        response = ["✅ **Request Processed**\n"]
        response.append(f"🔧 Tools executed: {len(results)}")
        response.append(f"⏱️ Total time: {sum(r.execution_time for r in results):.4f}s")

        return "\n".join(response)


# Convenience function for direct usage
def process_user_request(user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Process user request through orchestrator

    Args:
        user_input: Natural language request
        context: Additional context (data, previous results, etc.)

    Returns:
        Dictionary with response and metadata
    """
    orchestrator = RenataOrchestrator()
    return orchestrator.process_request(user_input, context)


if __name__ == "__main__":
    # Test the orchestrator
    print("=" * 70)
    print("🤖 RENATA V2 ORCHESTRATOR AGENT")
    print("=" * 70)

    orchestrator = RenataOrchestrator()

    # Test request
    test_requests = [
        "Generate a Backside B gap scanner",
        "Analyze AAPL market structure",
        "Create implementation plan for momentum strategy"
    ]

    for request in test_requests:
        print(f"\n👤 User: {request}")
        result = orchestrator.process_request(request)
        print(f"\n🤖 Renata: {result['response']}")
        print(f"\n   Tools: {', '.join(result['tools_used'])}")
        print(f"   Time: {result['execution_time']:.4f}s")
        print(f"   Success: {result['success']}")
