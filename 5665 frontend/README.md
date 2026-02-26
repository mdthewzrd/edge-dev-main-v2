# Edge.dev 5665 Frontend

This is the frontend for the Edge.dev Market Scanner running on port 5665.

## Overview

- **Port**: 5665
- **Main Route**: `/scan`
- **Features**:
  - Real-time market scanning with LC D2 Extended patterns
  - Interactive candlestick charts with Plotly.js
  - TradingView-style chart components
  - Scan results display with gap analysis
  - Trade signal tracking and P&L

## Setup

```bash
cd "5665 frontend"
npm install
npm run dev
```

Access at: http://localhost:5665/scan

## Project Structure

```
src/
├── app/
│   └── scan/
│       └── page.tsx        # Main scan page with charts and results
├── components/
│   ├── EdgeChart.tsx        # TradingView-style chart component
│   ├── TradingViewToggle.tsx
│   ├── ManageProjectsModal.tsx
│   ├── EdgeChartPlaceholder.tsx
│   ├── validation/         # Validation dashboard components
│   └── debug/             # Debug studio components
├── config/
│   ├── globalChartConfig.ts # Global chart configuration
│   └── globalChartConfig-OLD.ts
├── utils/
│   ├── polygonData.ts       # Polygon.io data fetching
│   ├── tradingDays.ts      # Trading day calculations
│   ├── chartDayNavigation.ts
│   └── codeFormatterAPI.ts
└── services/
    ├── fastApiScanService.ts
    ├── marketDataCache.ts
    └── projectApiService.ts
```

## Key Technologies

- **Next.js 16.0** - React framework
- **Plotly.js** - Interactive charts
- **Tailwind CSS 4** - Styling
- **TypeScript** - Type safety
- **Lucide React** - Icons
- **Zustand** - State management

## Scan Features

### LC Frontside D2 Extended Scanner

This scanner identifies high-probability gap continuation setups with the following criteria:

- High Change ATR ≥ 1.5
- 9EMA Distance ATR ≥ 2
- 20EMA Distance ATR ≥ 3
- Volume ≥ 10M shares
- Dollar Volume ≥ $500M
- Bullish EMA Stack (9≥20≥50)
- Price ≥ $5
- Higher High/Low vs Previous Day
- Bullish Close (Close ≥ Open)

### Chart Features

- Timeframe selection: 1D, 1W, 1M
- Day navigation for LC pattern analysis
- Hover legend with OHLCV values
- Market session shapes
- TradingView-style aesthetics

## Environment Variables

Required `.env.local`:

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_key
CLERK_SECRET_KEY=your_key
```

## API Endpoints

The frontend connects to:
- `/api/scan` - Execute market scans
- `/api/projects` - Manage scan projects
- Polygon.io - Market data

## License

Proprietary - Edge.dev
