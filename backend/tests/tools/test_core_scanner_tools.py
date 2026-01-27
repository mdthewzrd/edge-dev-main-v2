"""
Unit Tests for Core Scanner Tools

Tests:
- v31_scanner_generator
- v31_validator
- scanner_executor
"""

import pytest
import sys
from pathlib import Path

# Add backend src to path
backend_src = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(backend_src))
sys.path.insert(0, str(backend_src / "tools"))

# Import from shared types
from tool_types import ToolStatus, ToolResult
from v31_scanner_generator import v31_scanner_generator
from v31_validator import v31_validator
from scanner_executor import scanner_executor


class TestV31ScannerGenerator:
    """Test suite for v31_scanner_generator tool"""

    def test_basic_scanner_generation(self):
        """Test 1: Basic scanner generation from description"""
        input_data = {
            "description": "Backside scanner for gap ups with ATR filter",
        }

        result = v31_scanner_generator(input_data)

        assert result.status == ToolStatus.SUCCESS
        assert result.result is not None
        assert "scanner_code" in result.result
        assert len(result.result["scanner_code"]) > 0
        assert "def get_stage1_symbols" in result.result["scanner_code"]
        assert "def stage2_process_symbols" in result.result["scanner_code"]
        assert result.execution_time < 2.0  # Target: <2 seconds

    def test_scanner_generation_with_parameters(self):
        """Test 2: Scanner generation with custom parameters"""
        input_data = {
            "description": "Gap up scanner",
            "parameters": {
                "gap_over_atr": {"min": 0.8, "max": 1.2, "default": 0.85},
                "open_over_ema9": {"min": 0.85, "max": 0.98, "default": 0.92}
            }
        }

        result = v31_scanner_generator(input_data)

        assert result.status == ToolStatus.SUCCESS
        assert result.result is not None
        assert "parameters_used" in result.result
        assert "gap_over_atr" in result.result["parameters_used"]
        assert result.result["parameters_used"]["gap_over_atr"]["default"] == 0.85

    def test_scanner_generation_from_a_plus_example(self):
        """Test 3: Scanner generation from A+ example"""
        input_data = {
            "description": "Backside setup",
            "a_plus_example": {
                "text_description": "Gap up into resistance, red candle close",
                "parameters": {"gap_over_atr": 0.85}
            }
        }

        result = v31_scanner_generator(input_data)

        assert result.status == ToolStatus.SUCCESS
        assert result.result is not None
        assert result.result["parameters_used"]["gap_over_atr"]["default"] == 0.85

    def test_missing_description_error(self):
        """Test 4: Error when description is empty"""
        input_data = {
            "description": ""
        }

        result = v31_scanner_generator(input_data)

        assert result.status == ToolStatus.ERROR
        assert result.error is not None
        assert result.error["code"] == "MISSING_PARAMETER"

    def test_code_structure_validation(self):
        """Test 5: Generated code has correct V31 structure"""
        input_data = {
            "description": "Backside scanner",
            "include_validation": False  # Skip validation for this test
        }

        result = v31_scanner_generator(input_data)

        assert result.status == ToolStatus.SUCCESS
        structure = result.result["code_structure"]
        assert structure["has_stage1"] == True
        assert structure["has_stage2"] == True
        assert structure["has_stage3"] == True
        assert structure["per_ticker_operations"] == True
        assert structure["smart_filters"] == True


class TestV31Validator:
    """Test suite for v31_validator tool"""

    def test_v31_compliant_scanner(self):
        """Test 1: Validate V31 compliant scanner"""
        compliant_code = """
def get_stage1_symbols():
    return symbols

def stage2_process_symbols(df):
    # Calculate indicators
    df['atr'] = calculate_atr(df, 14)
    # Smart filters
    if not passes_smart_filters(df):
        return pd.DataFrame()
    # Detect setup
    return df[df['gap_over_atr'] > 0.8]

def aggregate_signals(signals):
    return pd.concat(signals)
"""

        result = v31_validator({
            "scanner_code": compliant_code,
            "strict_mode": False,
            "return_fixes": True
        })

        assert result.status in [ToolStatus.SUCCESS, ToolStatus.PARTIAL]
        assert result.result is not None
        # Should have good compliance score
        assert result.result["compliance_score"] >= 0.5
        assert result.execution_time < 1.0  # Target: <1 second

    def test_missing_stage2_violation(self):
        """Test 2: Detect missing stage2 function"""
        non_compliant_code = """
def get_stage1_symbols():
    return symbols

# Missing stage2_process_symbols!

def aggregate_signals(signals):
    return signals
"""

        result = v31_validator({
            "scanner_code": non_compliant_code,
            "return_fixes": True
        })

        assert result.status in [ToolStatus.SUCCESS, ToolStatus.PARTIAL]
        assert result.result is not None
        # Should have violations
        assert result.result["total_violations"] > 0
        # Should include CRITICAL violation for missing stage2
        assert result.result["critical_violations"] > 0

    def test_invalid_python_syntax(self):
        """Test 3: Error on invalid Python syntax"""
        invalid_code = "this is not valid python code {{{"

        result = v31_validator({
            "scanner_code": invalid_code
        })

        assert result.status == ToolStatus.ERROR
        assert result.error is not None
        assert result.error["code"] == "INVALID_INPUT"

    def test_naming_convention_violation(self):
        """Test 4: Detect incorrect naming convention (CamelCase)"""
        bad_naming_code = """
def getStage1Symbols():  # Wrong: should be snake_case
    return symbols

def stage2_process_symbols(df):
    return df

def aggregate_signals(signals):
    return signals
"""

        result = v31_validator({
            "scanner_code": bad_naming_code,
            "return_fixes": True
        })

        assert result.status in [ToolStatus.SUCCESS, ToolStatus.PARTIAL]
        # Should detect naming violation
        violations = result.result["violations"]
        naming_violations = [v for v in violations if "naming" in v["issue"].lower()]
        assert len(naming_violations) > 0

    def test_empty_scanner_code_error(self):
        """Test 5: Error when scanner code is empty"""
        result = v31_validator({
            "scanner_code": ""
        })

        assert result.status == ToolStatus.ERROR
        assert result.error is not None
        assert result.error["code"] == "MISSING_PARAMETER"


class TestScannerExecutor:
    """Test suite for scanner_executor tool"""

    def test_missing_required_parameters(self):
        """Test 1: Error when required parameters are missing"""
        # Missing scan_date
        result = scanner_executor({
            "scanner_code": "def test(): pass",
            "parameters": {},
            "backend_url": "http://localhost:8000",
            "websocket_url": "ws://localhost:8000/ws"
        })

        assert result.status == ToolStatus.ERROR
        assert result.error is not None
        assert result.error["code"] == "MISSING_PARAMETER"

    def test_invalid_date_format(self):
        """Test 2: Error on invalid date format"""
        result = scanner_executor({
            "scanner_code": "def test(): pass",
            "scan_date": "01-26-2024",  # Wrong format (should be YYYY-MM-DD)
            "parameters": {},
            "backend_url": "http://localhost:8000",
            "websocket_url": "ws://localhost:8000/ws"
        })

        assert result.status == ToolStatus.ERROR
        assert result.error is not None
        assert result.error["code"] == "INVALID_INPUT"

    def test_backend_connection_failure(self):
        """Test 3: Graceful error when backend is not running"""
        # Use wrong port to simulate backend not running
        result = scanner_executor({
            "scanner_code": "def test(): pass",
            "scan_date": "2024-01-26",
            "parameters": {},
            "backend_url": "http://localhost:9999",  # Wrong port
            "websocket_url": "ws://localhost:9999/ws",
            "timeout": 5  # Short timeout for test
        })

        # Should fail gracefully with backend connection error
        assert result.status == ToolStatus.ERROR
        assert result.error is not None
        assert result.error["code"] == "BACKEND_CONNECTION_FAILED"


class TestToolIntegration:
    """Integration tests for tool combinations"""

    def test_generator_to_validator_workflow(self):
        """Test 1: Generate scanner then validate it"""
        # Step 1: Generate scanner
        gen_result = v31_scanner_generator({
            "description": "Backside scanner for gap ups",
            "include_validation": False
        })

        assert gen_result.status == ToolStatus.SUCCESS
        scanner_code = gen_result.result["scanner_code"]

        # Step 2: Validate generated scanner
        val_result = v31_validator({
            "scanner_code": scanner_code,
            "return_fixes": True
        })

        assert val_result.status in [ToolStatus.SUCCESS, ToolStatus.PARTIAL]
        # Generated code should be V31 compliant
        assert val_result.result["compliance_score"] >= 0.7

    def test_generator_with_validation_enabled(self):
        """Test 2: Generate scanner with automatic validation"""
        result = v31_scanner_generator({
            "description": "Backside scanner",
            "include_validation": True
        })

        assert result.status == ToolStatus.SUCCESS
        assert result.result is not None
        assert "v31_validated" in result.result
        assert "validation_report" in result.result


# Run tests if executed directly
if __name__ == "__main__":
    print("🧪 Running Core Scanner Tools Tests...\n")

    # Test v31_scanner_generator
    print("📦 Testing v31_scanner_generator...")
    test_gen = TestV31ScannerGenerator()
    test_gen.test_basic_scanner_generation()
    print("  ✅ Test 1: Basic generation")
    test_gen.test_scanner_generation_with_parameters()
    print("  ✅ Test 2: With parameters")
    test_gen.test_scanner_generation_from_a_plus_example()
    print("  ✅ Test 3: From A+ example")
    test_gen.test_missing_description_error()
    print("  ✅ Test 4: Missing description error")
    test_gen.test_code_structure_validation()
    print("  ✅ Test 5: Code structure validation")

    # Test v31_validator
    print("\n📦 Testing v31_validator...")
    test_val = TestV31Validator()
    test_val.test_v31_compliant_scanner()
    print("  ✅ Test 1: V31 compliant scanner")
    test_val.test_missing_stage2_violation()
    print("  ✅ Test 2: Missing stage2 violation")
    test_val.test_invalid_python_syntax()
    print("  ✅ Test 3: Invalid Python syntax")
    test_val.test_naming_convention_violation()
    print("  ✅ Test 4: Naming convention violation")
    test_val.test_empty_scanner_code_error()
    print("  ✅ Test 5: Empty scanner code error")

    # Test scanner_executor
    print("\n📦 Testing scanner_executor...")
    test_exec = TestScannerExecutor()
    test_exec.test_missing_required_parameters()
    print("  ✅ Test 1: Missing required parameters")
    test_exec.test_invalid_date_format()
    print("  ✅ Test 2: Invalid date format")
    test_exec.test_backend_connection_failure()
    print("  ✅ Test 3: Backend connection failure")

    # Test integration
    print("\n📦 Testing tool integration...")
    test_int = TestToolIntegration()
    test_int.test_generator_to_validator_workflow()
    print("  ✅ Test 1: Generator → Validator workflow")
    test_int.test_generator_with_validation_enabled()
    print("  ✅ Test 2: Generator with validation")

    print("\n✅ All tests passed!")
