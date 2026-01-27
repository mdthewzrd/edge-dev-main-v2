"""
RENATA V2 Tools - Cole Medina "Tools Before Agents" Architecture

This package contains 13 focused tools that replace the over-engineered
5-agent system. Each tool does ONE thing well.

Tool Categories:
- Core Scanner Tools (3): v31_scanner_generator, v31_validator, scanner_executor ✅
- Market Analysis Tools (3): indicator_calculator, market_structure_analyzer, daily_context_detector ✅
- Validation Tools (2): a_plus_analyzer, quick_backtester
- Research Tools (2): knowledge_base_search, similar_strategy_finder
- Optimization & Risk Tools (2): parameter_optimizer, position_risk_calculator
- Planning Tools (1): build_plan_generator

Version: 1.0.0
Status: Task 2.2 - Implementing Market Analysis Tools
"""

__version__ = "1.0.0"

# Import shared types
from .tool_types import ToolStatus, ToolResult

# Import all tools (will be available as we implement them)
from .v31_scanner_generator import v31_scanner_generator
from .v31_validator import v31_validator
from .scanner_executor import scanner_executor
from .indicator_calculator import indicator_calculator
from .market_structure_analyzer import market_structure_analyzer
from .daily_context_detector import daily_context_detector
from .a_plus_analyzer import a_plus_analyzer
from .quick_backtester import quick_backtester

__all__ = [
    "ToolStatus",
    "ToolResult",
    # Core Scanner Tools
    "v31_scanner_generator",
    "v31_validator",
    "scanner_executor",
    # Market Analysis Tools
    "indicator_calculator",
    "market_structure_analyzer",
    "daily_context_detector",
    # Validation Tools
    "a_plus_analyzer",
    "quick_backtester",
]
