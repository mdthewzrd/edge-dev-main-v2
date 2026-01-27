"""
Shared types for all RENATA V2 tools

This module defines common data structures used across all tools.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional, List


class ToolStatus(Enum):
    """Standard tool execution status"""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"


@dataclass
class ToolResult:
    """Standard tool result structure"""
    status: ToolStatus
    result: Optional[Dict[str, Any]]
    error: Optional[Dict[str, str]]
    warnings: Optional[List[str]]
    execution_time: float
    tool_version: str
