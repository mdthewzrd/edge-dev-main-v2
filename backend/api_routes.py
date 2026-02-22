"""
RENATA V2 API Routes for Orchestrator Integration

Provides API endpoints for the frontend to communicate with RENATA orchestrator
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import pandas as pd
from pydantic import BaseModel
import io
import json

# Import orchestrator
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orchestrator.renata_orchestrator import RenataOrchestrator
from tools.tool_types import ToolStatus


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str
    tools_used: list[str]
    execution_time: float
    success: bool
    intent: Optional[Dict[str, Any]] = None


class MarketDataRequest(BaseModel):
    ticker: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    rows: Optional[int] = 100


# Initialize orchestrator
orchestrator = RenataOrchestrator()

# Create router
router = APIRouter(
    prefix="/api/renata",
    tags=["renata"]
)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process chat message through RENATA orchestrator

    This is the main endpoint that the frontend uses to communicate with RENATA.
    """
    try:
        # Validate message is not empty
        if not request.message or request.message.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )

        # Process request through orchestrator
        result = orchestrator.process_request(
            request.message,
            request.context or {}
        )

        return ChatResponse(
            response=result["response"],
            tools_used=result["tools_used"],
            execution_time=result["execution_time"],
            success=result["success"],
            intent=result.get("intent")
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@router.post("/analyze")
async def analyze_market(request: MarketDataRequest):
    """
    Analyze market data for ticker

    Loads market data and runs analysis through orchestrator
    """
    try:
        # For now, generate sample data
        # In production, this would fetch from Polygon API
        import numpy as np
        from datetime import datetime, timedelta

        # Generate sample data
        if request.rows:
            rows = request.rows
        else:
            rows = 100

        # Generate dates first, ensure we have enough
        start = request.start_date or "2024-01-01"
        end = request.end_date or (datetime.now() + timedelta(days=rows)).strftime("%Y-%m-%d")

        dates = pd.date_range(start=start, end=end, freq='D')

        # If not enough dates, extend the range
        if len(dates) < rows:
            dates = pd.date_range(start=start, periods=rows, freq='D')

        dates = dates[:rows]  # Trim to exact rows needed

        np.random.seed(42)
        base_price = 100
        returns = np.random.normal(0, 0.02, rows)
        closes = base_price * (1 + returns).cumprod()

        df = pd.DataFrame({
            'date': dates,
            'open': closes * (1 + np.random.uniform(-0.01, 0.01, rows)),
            'high': closes * (1 + np.random.uniform(0, 0.02, rows)),
            'low': closes * (1 - np.random.uniform(0, 0.02, rows)),
            'close': closes,
            'volume': np.random.randint(1000000, 10000000, rows)
        })

        # Add to context
        context = {
            "df": df,
            "ticker": request.ticker
        }

        # Process analysis request
        result = orchestrator.process_request(
            f"Analyze {request.ticker} market structure with indicators",
            context=context
        )

        return JSONResponse({
            "success": result["success"],
            "response": result["response"],
            "tools_used": result["tools_used"],
            "execution_time": result["execution_time"],
            "data_summary": {
                "rows": len(df),
                "date_range": f"{df['date'].min()} to {df['date'].max()}",
                "ticker": request.ticker
            }
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing market: {str(e)}"
        )


@router.get("/tools")
async def list_tools():
    """
    List all available tools and their capabilities
    """
    try:
        tools = orchestrator.tool_registry

        tool_list = []
        for tool_id, tool_info in tools.items():
            tool_list.append({
                "id": tool_id,
                "name": tool_info["name"],
                "description": tool_info["description"],
                "keywords": tool_info["keywords"]
            })

        return JSONResponse({
            "success": True,
            "tools": tool_list,
            "count": len(tool_list)
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing tools: {str(e)}"
        )


@router.get("/status")
async def get_status():
    """
    Get orchestrator status and capabilities
    """
    try:
        return JSONResponse({
            "success": True,
            "status": "operational",
            "version": "1.0.0",
            "tools_count": len(orchestrator.tool_registry),
            "capabilities": {
                "scanner_generation": True,
                "validation": True,
                "market_analysis": True,
                "parameter_optimization": True,
                "backtesting": True,
                "planning": True,
                "execution": True
            }
        })

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting status: {str(e)}"
        )


@router.post("/validate")
async def validate_scanner(scanner_data: Dict[str, Any]):
    """
    Validate scanner code against V31 standards

    Expects scanner_code in request body
    """
    try:
        scanner_code = scanner_data.get("scanner_code", "")

        if not scanner_code:
            raise HTTPException(
                status_code=400,
                detail="scanner_code is required"
            )

        # Validate through orchestrator
        result = orchestrator.process_request(
            f"Validate this scanner code",
            context={"scanner_code": scanner_code}
        )

        return JSONResponse({
            "success": result["success"],
            "response": result["response"],
            "tools_used": result["tools_used"],
            "execution_time": result["execution_time"],
            "compliance_score": result.get("intent", {}).get("details", {})
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error validating scanner: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return JSONResponse({
        "status": "healthy",
        "service": "RENATA V2 Orchestrator",
        "version": "1.0.0"
    })
