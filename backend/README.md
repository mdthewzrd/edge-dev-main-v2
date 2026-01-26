# Backend - FastAPI

Python FastAPI backend for edge-dev-main trading platform.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run development server
python main.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── src/                    # Source code (when organized)
│   ├── api/               # API route handlers
│   ├── core/              # Core business logic
│   ├── services/          # External service integrations
│   ├── models/            # Pydantic models
│   ├── utils/             # Utility functions
│   └── config/            # Configuration
├── data/                  # Static data
└── tests/                 # Backend tests
```

## Key Services

- **Scanner API**: V31 standard scanner generation and execution
- **Backtest API**: Historical backtesting engine
- **Chart API**: Real-time chart data delivery
- **Project API**: Project and scan management
- **Agent API**: AI agent integration

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/unit/test_scanner.py

# Run with coverage
pytest --cov=src tests/
```

## Environment Variables

See `.env.example` for full list.
