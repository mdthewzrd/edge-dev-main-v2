"""
V31 Validator Tool

Purpose: Validate code against V31 Gold Standard
Version: 1.0.0
Estimated LOC: 80 lines
Target Execution: <1 second

This tool does ONE thing: Check if scanner code complies with V31 standards.
"""

import re
import ast
from typing import Dict, Any, Optional, List
import time

# Import shared types - handle both relative and absolute imports
try:
    from .tool_types import ToolStatus, ToolResult
except ImportError:
    from tool_types import ToolStatus, ToolResult


def v31_validator(input_data: Dict[str, Any]) -> ToolResult:
    """
    Validate scanner code against V31 Gold Standard

    Args:
        input_data: Dictionary with:
            - scanner_code (str): Python code to validate [REQUIRED]
            - strict_mode (bool): Fail fast or warnings only
            - check_pillars (list): Which pillars to check [1, 2, 3, 4]
            - return_fixes (bool): Include fix suggestions

    Returns:
        ToolResult with compliance score, violations, and fixes
    """

    start_time = time.time()
    tool_version = "1.0.0"

    try:
        # Validate input
        validation_result = validate_input(input_data)
        if not validation_result["valid"]:
            return ToolResult(
                status=ToolStatus.ERROR,
                result=None,
                error=validation_result["error"],
                warnings=None,
                execution_time=time.time() - start_time,
                tool_version=tool_version
            )

        # Extract inputs
        scanner_code = input_data.get("scanner_code", "")
        strict_mode = input_data.get("strict_mode", False)
        check_pillars = input_data.get("check_pillars", [1, 2, 3, 4])
        return_fixes = input_data.get("return_fixes", True)

        # Validate Python syntax first
        syntax_valid = validate_python_syntax(scanner_code)
        if not syntax_valid["valid"]:
            return ToolResult(
                status=ToolStatus.ERROR,
                result=None,
                error={
                    "code": "INVALID_INPUT",
                    "message": "Code must be valid Python syntax",
                    "details": syntax_valid["error"]
                },
                warnings=None,
                execution_time=time.time() - start_time,
                tool_version=tool_version
            )

        # Check each pillar
        pillar_results = {}
        all_violations = []

        # Pillar 0: Market Scanning
        if 0 in check_pillars:
            pillar_0_result = check_pillar_0_market_scanning(scanner_code)
            pillar_results["pillar_0_market_scanning"] = pillar_0_result
            all_violations.extend(pillar_0_result.get("violations", []))

        # Pillar 1: 3-Stage Architecture
        if 1 in check_pillars:
            pillar_1_result = check_pillar_1_3stage_architecture(scanner_code, return_fixes)
            pillar_results["pillar_1_3stage_architecture"] = pillar_1_result
            all_violations.extend(pillar_1_result.get("violations", []))

        # Pillar 2: Per-Ticker Operations
        if 2 in check_pillars:
            pillar_2_result = check_pillar_2_per_ticker_operations(scanner_code, return_fixes)
            pillar_results["pillar_2_per_ticker_operations"] = pillar_2_result
            all_violations.extend(pillar_2_result.get("violations", []))

        # Pillar 3: Parallel Processing
        if 3 in check_pillars:
            pillar_3_result = check_pillar_3_parallel_processing(scanner_code, return_fixes)
            pillar_results["pillar_3_parallel_processing"] = pillar_3_result
            all_violations.extend(pillar_3_result.get("violations", []))

        # Calculate overall compliance
        compliance_score = calculate_compliance_score(pillar_results)
        is_v31_compliant = compliance_score >= 0.8

        # Count violations by severity
        violation_counts = count_violations(all_violations)

        # Build result
        result = {
            "is_v31_compliant": is_v31_compliant,
            "compliance_score": compliance_score,
            "pillar_results": pillar_results,
            "violations": all_violations,
            "total_violations": violation_counts["total"],
            "critical_violations": violation_counts["critical"],
            "major_violations": violation_counts["major"],
            "minor_violations": violation_counts["minor"],
            "warnings": [] if is_v31_compliant else ["Scanner does not meet V31 standards"]
        }

        return ToolResult(
            status=ToolStatus.SUCCESS if is_v31_compliant or not strict_mode else ToolStatus.ERROR,
            result=result,
            error=None,
            warnings=result.get("warnings", []),
            execution_time=time.time() - start_time,
            tool_version=tool_version
        )

    except Exception as e:
        import traceback
        return ToolResult(
            status=ToolStatus.ERROR,
            result=None,
            error={
                "code": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            },
            warnings=None,
            execution_time=time.time() - start_time,
            tool_version=tool_version
        )


def validate_input(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate input parameters"""

    if "scanner_code" not in input_data:
        return {
            "valid": False,
            "error": {
                "code": "MISSING_PARAMETER",
                "message": "Required parameter 'scanner_code' is missing",
                "parameter": "scanner_code"
            }
        }

    scanner_code = input_data.get("scanner_code", "")

    if not isinstance(scanner_code, str):
        return {
            "valid": False,
            "error": {
                "code": "INVALID_TYPE",
                "message": "Scanner code must be a string",
                "parameter": "scanner_code",
                "expected_type": "str",
                "actual_type": type(scanner_code).__name__
            }
        }

    if not scanner_code.strip():
        return {
            "valid": False,
            "error": {
                "code": "MISSING_PARAMETER",
                "message": "Scanner code is empty",
                "parameter": "scanner_code"
            }
        }

    return {"valid": True}


def validate_python_syntax(code: str) -> Dict[str, Any]:
    """Validate that code is valid Python syntax"""

    try:
        ast.parse(code)
        return {"valid": True}
    except SyntaxError as e:
        return {
            "valid": False,
            "error": {
                "line": e.lineno,
                "offset": e.offset,
                "message": e.msg
            }
        }


def check_pillar_0_market_scanning(code: str) -> Dict[str, Any]:
    """
    Check Pillar 0: Market Scanning

    Requirements:
    - Full market coverage (12k+ tickers)
    - Grouped endpoint optimization
    - Batch processing
    """

    violations = []

    checks = {
        "full_market_coverage": "get_stage1_symbols" in code or "symbols" in code,
        "grouped_endpoint_optimization": "grouped" in code.lower() or "batch" in code.lower(),
        "batch_processing": "batch" in code.lower() or "process" in code.lower()
    }

    # Generate violations for failed checks
    if not checks["full_market_coverage"]:
        violations.append({
            "pillar": "Pillar 0: Market Scanning",
            "severity": "MAJOR",
            "issue": "Missing market scanning function",
            "fix_suggestion": "Add get_stage1_symbols() function to fetch all market symbols"
        })

    compliant = all(checks.values())
    score = sum(checks.values()) / len(checks)

    return {
        "compliant": compliant,
        "score": score,
        "violations": violations,
        "checks": checks
    }


def check_pillar_1_3stage_architecture(code: str, return_fixes: bool) -> Dict[str, Any]:
    """
    Check Pillar 1: 3-Stage Architecture

    Requirements:
    - Stage 1: get_stage1_symbols()
    - Stage 2: stage2_process_symbols()
    - Stage 3: aggregate_signals()
    """

    violations = []

    checks = {
        "has_stage1": bool(re.search(r"def\s+get_stage1_symbols", code)),
        "has_stage2": bool(re.search(r"def\s+stage2_process_symbols", code)),
        "has_stage3": bool(re.search(r"def\s+aggregate_signals", code))
    }

    # Generate violations with fixes
    if not checks["has_stage1"] and return_fixes:
        violations.append({
            "pillar": "Pillar 1: 3-Stage Architecture",
            "severity": "CRITICAL",
            "issue": "Missing get_stage1_symbols() function",
            "location": "Stage 1",
            "fix_suggestion": "Add: def get_stage1_symbols(): return symbols",
            "code_example": "def get_stage1_symbols():\n    # Return full market universe\n    return symbols"
        })

    if not checks["has_stage2"] and return_fixes:
        violations.append({
            "pillar": "Pillar 1: 3-Stage Architecture",
            "severity": "CRITICAL",
            "issue": "Missing stage2_process_symbols() function",
            "location": "Stage 2",
            "fix_suggestion": "Add: def stage2_process_symbols(df): return processed_df",
            "code_example": "def stage2_process_symbols(df: pd.DataFrame) -> pd.DataFrame:\n    # Process each ticker independently\n    return df[df['condition']]"
        })

    if not checks["has_stage3"] and return_fixes:
        violations.append({
            "pillar": "Pillar 1: 3-Stage Architecture",
            "severity": "MAJOR",
            "issue": "Missing aggregate_signals() function",
            "location": "Stage 3",
            "fix_suggestion": "Add: def aggregate_signals(signals): return combined",
            "code_example": "def aggregate_signals(all_signals):\n    return pd.concat(all_signals)"
        })

    compliant = all(checks.values())
    score = sum(checks.values()) / len(checks)

    return {
        "compliant": compliant,
        "score": score,
        "violations": violations,
        "checks": checks
    }


def check_pillar_2_per_ticker_operations(code: str, return_fixes: bool) -> Dict[str, Any]:
    """
    Check Pillar 2: Per-Ticker Operations

    Requirements:
    - Independent processing (no cross-ticker dependencies)
    - Smart filters for quick rejection
    - No lookahead bias
    """

    violations = []

    checks = {
        "independent_processing": "def stage2_process_symbols" in code,
        "smart_filters": any(keyword in code.lower() for keyword in ["smart_filter", "passes_smart_filters", "quick_rejection"]),
        "no_lookahead_bias": ".shift(" in code or ".shift(1)" in code
    }

    # Generate violations
    if not checks["independent_processing"] and return_fixes:
        violations.append({
            "pillar": "Pillar 2: Per-Ticker Operations",
            "severity": "CRITICAL",
            "issue": "Missing per-ticker processing function",
            "fix_suggestion": "Ensure stage2_process_symbols() processes each ticker independently"
        })

    if not checks["smart_filters"] and return_fixes:
        violations.append({
            "pillar": "Pillar 2: Per-Ticker Operations",
            "severity": "MAJOR",
            "issue": "Missing smart filters for quick rejection",
            "fix_suggestion": "Add passes_smart_filters() function to reject unqualified tickers early"
        })

    compliant = all(checks.values())
    score = sum(checks.values()) / len(checks)

    return {
        "compliant": compliant,
        "score": score,
        "violations": violations,
        "checks": checks
    }


def check_pillar_3_parallel_processing(code: str, return_fixes: bool) -> Dict[str, Any]:
    """
    Check Pillar 3: Parallel Processing

    Requirements:
    - Parameter system for easy adjustment
    - Clean code structure
    - Proper naming conventions
    """

    violations = []

    checks = {
        "parameter_system": bool(re.search(r"#\s*=?PARAMETERS|param\s+\w+\s*=", code, re.IGNORECASE)),
        "code_structure": len(re.findall(r"def\s+\w+", code)) >= 3,  # At least 3 functions
        "naming_conventions": not bool(re.search(r"def\s+[a-z]+[A-Z]", code))  # No camelCase (lowercase then uppercase)
    }

    # Generate violations
    if not checks["parameter_system"] and return_fixes:
        violations.append({
            "pillar": "Pillar 3: Parallel Processing",
            "severity": "MINOR",
            "issue": "Missing clear parameter section",
            "fix_suggestion": "Add a PARAMETERS section at the top with all configurable values"
        })

    if not checks["naming_conventions"] and return_fixes:
        violations.append({
            "pillar": "Pillar 3: Parallel Processing",
            "severity": "MAJOR",
            "issue": "Incorrect naming convention (use snake_case, not CamelCase)",
            "fix_suggestion": "Rename functions to use snake_case (e.g., get_stage1_symbols, not GetStage1Symbols)"
        })

    compliant = all(checks.values())
    score = sum(checks.values()) / len(checks)

    return {
        "compliant": compliant,
        "score": score,
        "violations": violations,
        "checks": checks
    }


def calculate_compliance_score(pillar_results: Dict[str, Any]) -> float:
    """Calculate overall compliance score from pillar results"""

    if not pillar_results:
        return 0.0

    total_score = 0.0
    total_pillars = len(pillar_results)

    for pillar_name, pillar_result in pillar_results.items():
        total_score += pillar_result.get("score", 0.0)

    return round(total_score / total_pillars, 2)


def count_violations(violations: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count violations by severity"""

    counts = {
        "critical": 0,
        "major": 0,
        "minor": 0,
        "total": len(violations)
    }

    for violation in violations:
        severity = violation.get("severity", "MINOR").upper()
        # Convert to lowercase for counting
        severity_lower = severity.lower()
        if severity_lower in counts:
            counts[severity_lower] += 1

    return counts


if __name__ == "__main__":
    # Test the tool
    test_code = """
def get_stage1_symbols():
    return symbols

def stage2_process_symbols(df):
    return df[df['gap_over_atr'] > 0.8]

def aggregate_signals(signals):
    return signals
"""

    test_input = {
        "scanner_code": test_code,
        "strict_mode": False,
        "return_fixes": True
    }

    result = v31_validator(test_input)

    if result.status == ToolStatus.SUCCESS or result.status == ToolStatus.PARTIAL:
        print(f"✅ Validation complete!")
        print(f"Compliance Score: {result.result['compliance_score']}")
        print(f"V31 Compliant: {result.result['is_v31_compliant']}")
        print(f"Violations: {result.result['total_violations']}")
        print(f"Execution time: {result.execution_time:.3f}s")
    else:
        print(f"❌ Error: {result.error}")
