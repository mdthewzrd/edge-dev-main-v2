#!/usr/bin/env python3
"""
RENATA V2 Orchestrator Server

Standalone FastAPI server for the RENATA V2 Orchestrator
This is a simplified server that only includes the orchestrator API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import argparse

# Import orchestrator
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orchestrator.renata_orchestrator import RenataOrchestrator
from tools.tool_types import ToolStatus

# Create FastAPI app
app = FastAPI(
    title="RENATA V2 Orchestrator API",
    description="AI-powered trading platform orchestrator coordinating 13 specialized tools",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = RenataOrchestrator()

# Import API routes
from api_routes import router as orchestrator_router
app.include_router(orchestrator_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "service": "RENATA V2 Orchestrator",
        "version": "2.0.0",
        "tools_count": len(orchestrator.tool_registry)
    })

@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse({
        "message": "RENATA V2 Orchestrator API",
        "version": "2.0.0",
        "endpoints": {
            "chat": "/api/renata/chat",
            "analyze": "/api/renata/analyze",
            "tools": "/api/renata/tools",
            "status": "/api/renata/status",
            "validate": "/api/renata/validate",
            "health": "/health"
        }
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RENATA V2 Orchestrator Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5666, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")

    args = parser.parse_args()

    print("=" * 70)
    print("🚀 RENATA V2 ORCHESTRATOR SERVER")
    print("=" * 70)
    print(f"📍 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"🔄 Reload: {args.reload}")
    print(f"🤖 Tools Registered: {len(orchestrator.tool_registry)}")
    print("")
    print("Available endpoints:")
    print("  POST /api/renata/chat        - Process natural language requests")
    print("  POST /api/renata/analyze     - Analyze market data")
    print("  GET  /api/renata/tools       - List available tools")
    print("  GET  /api/renata/status      - Get orchestrator status")
    print("  POST /api/renata/validate    - Validate scanner code")
    print("  GET  /health                 - Health check")
    print("=" * 70)
    print("")

    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)
