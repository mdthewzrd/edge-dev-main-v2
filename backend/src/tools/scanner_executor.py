"""
Scanner Executor Tool

Purpose: Execute scanner and collect results with progress tracking
Version: 1.0.0
Estimated LOC: 120 lines
Target Execution: 300s timeout (actual scanner execution)

This tool does ONE thing: Submit scanner to backend and track execution progress.
"""

import uuid
import time
import json
from typing import Dict, Any, Optional, List
import requests

# Import shared types - handle both relative and absolute imports
try:
    from .tool_types import ToolStatus, ToolResult
except ImportError:
    from tool_types import ToolStatus, ToolResult


def scanner_executor(input_data: Dict[str, Any]) -> ToolResult:
    """
    Execute scanner code on backend and track progress

    Args:
        input_data: Dictionary with:
            - scanner_code (str): Python code to execute [REQUIRED]
            - scan_date (str): ISO format YYYY-MM-DD [REQUIRED]
            - parameters (dict): Scanner parameters [REQUIRED]
            - backend_url (str): http://localhost:8000 [REQUIRED]
            - websocket_url (str): ws://localhost:8000/ws [REQUIRED]
            - timeout (int): Seconds to wait (default: 300)
            - poll_interval (int): Progress check frequency in seconds (default: 1)
            - save_results (bool): Save results to disk (default: True)
            - output_format (str): json, csv (default: json)

    Returns:
        ToolResult with execution_id, progress tracking, and results
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
        scan_date = input_data.get("scan_date", "")
        parameters = input_data.get("parameters", {})
        backend_url = input_data.get("backend_url", "http://localhost:8000")
        websocket_url = input_data.get("websocket_url", "ws://localhost:8000/ws")
        timeout = input_data.get("timeout", 300)
        poll_interval = input_data.get("poll_interval", 1)
        save_results = input_data.get("save_results", True)
        output_format = input_data.get("output_format", "json")

        # Generate execution ID
        execution_id = str(uuid.uuid4())

        # Submit scanner to backend
        submit_result = submit_scanner_to_backend(
            backend_url=backend_url,
            scanner_code=scanner_code,
            scan_date=scan_date,
            parameters=parameters,
            execution_id=execution_id
        )

        if not submit_result["success"]:
            return ToolResult(
                status=ToolStatus.ERROR,
                result=None,
                error={
                    "code": "BACKEND_CONNECTION_FAILED",
                    "message": "Failed to submit scanner to backend",
                    "details": submit_result.get("error", "Unknown error")
                },
                warnings=None,
                execution_time=time.time() - start_time,
                tool_version=tool_version
            )

        # Track execution progress
        progress_result = track_execution_progress(
            backend_url=backend_url,
            execution_id=execution_id,
            timeout=timeout,
            poll_interval=poll_interval
        )

        # Build result
        result = {
            "execution_id": execution_id,
            "status": progress_result["status"],
            "progress": progress_result.get("progress", {}),
        }

        # Add results if complete
        if progress_result["status"] == "COMPLETE":
            result["results"] = progress_result.get("results", {})

            # Save results if requested
            if save_results:
                save_execution_results(execution_id, result, output_format)

        # Add error if failed
        if progress_result["status"] == "FAILED":
            result["error"] = progress_result.get("error", {})

        return ToolResult(
            status=ToolStatus.SUCCESS if progress_result["status"] == "COMPLETE" else ToolStatus.PARTIAL,
            result=result,
            error=None,
            warnings=[],
            execution_time=time.time() - start_time,
            tool_version=tool_version
        )

    except requests.exceptions.ConnectionError:
        return ToolResult(
            status=ToolStatus.ERROR,
            result=None,
            error={
                "code": "BACKEND_CONNECTION_FAILED",
                "message": "Cannot connect to backend - is it running?",
                "backend_url": input_data.get("backend_url", "unknown"),
                "suggestion": "Start backend with: python backend/main.py"
            },
            warnings=None,
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

    required_fields = ["scanner_code", "scan_date", "parameters", "backend_url", "websocket_url"]

    for field in required_fields:
        if field not in input_data:
            return {
                "valid": False,
                "error": {
                    "code": "MISSING_PARAMETER",
                    "message": f"Required parameter '{field}' is missing",
                    "parameter": field
                }
            }

    # Validate scan_date format
    scan_date = input_data.get("scan_date", "")
    if not is_valid_date(scan_date):
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "scan_date must be in ISO format YYYY-MM-DD",
                "parameter": "scan_date",
                "provided": scan_date,
                "example": "2024-01-26"
            }
        }

    return {"valid": True}


def is_valid_date(date_str: str) -> bool:
    """Validate date is in YYYY-MM-DD format"""

    try:
        parts = date_str.split("-")
        return len(parts) == 3 and len(parts[0]) == 4 and len(parts[1]) == 2 and len(parts[2]) == 2
    except:
        return False


def submit_scanner_to_backend(
    backend_url: str,
    scanner_code: str,
    scan_date: str,
    parameters: Dict[str, Any],
    execution_id: str
) -> Dict[str, Any]:
    """
    Submit scanner code to backend for execution

    Returns:
        Dict with success status and execution details
    """

    try:
        # Prepare submission payload
        payload = {
            "scanner_code": scanner_code,
            "scan_date": scan_date,
            "parameters": parameters,
            "execution_id": execution_id
        }

        # Submit to backend API
        response = requests.post(
            f"{backend_url}/api/scan/submit",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            return {
                "success": True,
                "execution_id": execution_id,
                "status": "QUEUED"
            }
        else:
            return {
                "success": False,
                "error": f"Backend returned status {response.status_code}: {response.text}"
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Backend request timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def track_execution_progress(
    backend_url: str,
    execution_id: str,
    timeout: int,
    poll_interval: int
) -> Dict[str, Any]:
    """
    Track execution progress by polling backend

    Returns:
        Dict with final status, progress details, and results
    """

    start_time = time.time()
    last_progress = {}

    while True:
        # Check timeout
        elapsed = time.time() - start_time
        if elapsed > timeout:
            return {
                "status": "FAILED",
                "error": {
                    "code": "TIMEOUT",
                    "message": f"Scanner execution exceeded {timeout}s timeout",
                    "elapsed_seconds": elapsed
                },
                "progress": last_progress
            }

        # Poll for progress
        try:
            response = requests.get(
                f"{backend_url}/api/scan/progress/{execution_id}",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()

                # Update progress
                last_progress = data.get("progress", {})
                status = data.get("status", "QUEUED")

                # Check if complete
                if status == "COMPLETE":
                    return {
                        "status": "COMPLETE",
                        "progress": last_progress,
                        "results": data.get("results", {})
                    }

                # Check if failed
                if status == "FAILED":
                    return {
                        "status": "FAILED",
                        "error": data.get("error", {}),
                        "progress": last_progress
                    }

                # Still running - wait before next poll
                time.sleep(poll_interval)

            else:
                # Backend error
                return {
                    "status": "FAILED",
                    "error": {
                        "code": "BACKEND_ERROR",
                        "message": f"Backend returned status {response.status_code}"
                    },
                    "progress": last_progress
                }

        except requests.exceptions.Timeout:
            # Poll timeout - continue to next iteration
            time.sleep(poll_interval)
            continue

        except Exception as e:
            return {
                "status": "FAILED",
                "error": {
                    "code": "POLLING_ERROR",
                    "message": str(e)
                },
                "progress": last_progress
            }


def save_execution_results(execution_id: str, result: Dict[str, Any], output_format: str) -> bool:
    """
    Save execution results to disk

    Returns:
        True if saved successfully, False otherwise
    """

    try:
        import os
        from datetime import datetime

        # Create results directory if needed
        results_dir = "backend/data/results"
        os.makedirs(results_dir, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{results_dir}/scan_{execution_id[:8]}_{timestamp}.{output_format}"

        # Save based on format
        if output_format == "json":
            with open(filename, "w") as f:
                json.dump(result, f, indent=2)
        else:
            # CSV format - save signals
            if "results" in result and "signals" in result["results"]:
                import pandas as pd
                df = pd.DataFrame(result["results"]["signals"])
                df.to_csv(filename, index=False)

        return True

    except Exception as e:
        print(f"Warning: Failed to save results: {e}")
        return False


if __name__ == "__main__":
    # Test the tool (requires backend to be running)
    test_input = {
        "scanner_code": """
def get_stage1_symbols():
    return symbols

def stage2_process_symbols(df):
    return df[df['close'] > df['open']]

def aggregate_signals(signals):
    return pd.concat(signals)
""",
        "scan_date": "2024-01-26",
        "parameters": {},
        "backend_url": "http://localhost:8000",
        "websocket_url": "ws://localhost:8000/ws",
        "timeout": 300,
        "poll_interval": 1
    }

    print("⚠️  Note: This test requires backend to be running on http://localhost:8000")
    print("    Start backend with: python backend/main.py")
    print("\nRunning test...")

    result = scanner_executor(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Scanner executed successfully!")
        print(f"Execution ID: {result.result['execution_id']}")
        print(f"Status: {result.result['status']}")
        print(f"Execution time: {result.execution_time:.3f}s")
        if "results" in result.result:
            print(f"Signals found: {result.result['results'].get('total_signals', 0)}")
    elif result.status == ToolStatus.PARTIAL:
        print("⚠️  Scanner execution incomplete")
        print(f"Status: {result.result['status']}")
        print(f"Execution time: {result.execution_time:.3f}s")
    else:
        print(f"❌ Error: {result.error}")
