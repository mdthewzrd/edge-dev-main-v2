# Edge-Dev-Main

AI-powered trading scanner platform with RENATA V2 agent integration.

## Quick Start

### Prerequisites
- Node.js 25+
- Python 3.9+
- PostgreSQL 14+ (optional)

### Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/mdthewzrd/edge-dev-main.git
   cd edge-dev-main
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env  # Configure your environment
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cp .env.local.example .env.local  # Configure your environment
   ```

4. **Start development servers**
   ```bash
   # Terminal 1: Backend
   cd backend && python main.py

   # Terminal 2: Frontend
   cd frontend && npm run dev
   ```

5. **Access application**
   - Frontend: http://localhost:5665
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Documentation

- [Architecture](docs/architecture/SYSTEM_OVERVIEW.md)
- [Quick Start Guide](docs/guides/QUICK_START.md)
- [Developer Setup](docs/guides/DEVELOPER_SETUP.md)
- [API Reference](docs/api/ENDPOINT_REFERENCE.md)
- [Sprint Workflow](docs/guides/SPRINT_WORKFLOW.md)

## Project Structure

```
edge-dev-main/
├── frontend/          # Next.js frontend (port 5665)
├── backend/           # FastAPI backend (port 8000)
├── scanners/          # Scanner system and templates
├── agents/            # AI agent system (RENATA V2)
├── docs/              # Documentation
├── scripts/           # Utility scripts
└── tests/             # Integration tests
```

## Development

See [SPRINT_WORKFLOW.md](docs/guides/SPRINT_WORKFLOW.md) for sprint-based development process.

## License

MIT
