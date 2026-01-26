# Frontend - Next.js

React frontend built with Next.js 16 and shadcn/ui.

## Quick Start

```bash
# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with your configuration

# Run development server
npm run dev
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                # Next.js app directory
│   ├── components/         # React components
│   │   ├── ui/             # shadcn/ui components
│   │   ├── charts/         # Chart components
│   │   ├── forms/          # Form components
│   │   └── agents/         # AI agent components
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API services
│   ├── utils/              # Utility functions
│   └── types/              # TypeScript types
└── tests/                  # Frontend tests
```

## Key Pages

- `/` - Main dashboard
- `/scan` - Scanner creation and execution
- `/backtest` - Backtesting interface
- `/exec` - Strategy execution
- `/projects` - Project management

## Development

```bash
# Run dev server (port 5665)
npm run dev

# Run type checking
npm run type-check

# Run linting
npm run lint

# Build for production
npm run build
```

## Testing

```bash
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e
```
