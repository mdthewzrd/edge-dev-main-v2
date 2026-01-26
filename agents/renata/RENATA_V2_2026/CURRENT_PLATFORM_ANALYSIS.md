# 📊 CURRENT PLATFORM ANALYSIS
## Understanding Your Existing EdgeDev Pages

**Date**: January 24, 2026
**Purpose**: Document current /scan and /backtest page structure before Renata V2 integration

---

## 🎯 OVERVIEW

You have **TWO working pages** that you actively use:

### 1. `/scan` Page (Market Scanner)
- **File**: `src/app/scan/page.tsx`
- **Size**: 7,578 lines (328.9KB)
- **Purpose**: Real-time market scanning and analysis

### 2. `/backtest` Page (Backtest Engine)
- **File**: `src/app/backtest/page.tsx`
- **Size**: 2,473 lines (115.9KB)
- **Purpose**: Strategy backtesting and validation

---

## 📐 PAGE LAYOUTS

### `/scan` Page Structure

```
┌────────────────────────────────────────────────────────────────┐
│  LEFT SIDEBAR (Fixed, 288px)                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Traderra Logo                                           │   │
│  │ AI Trading Platform                                     │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ Projects                                                │   │
│  │ [Load] [Save] [Refresh]                                 │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ • Project 1                              [Edit] [Del]  │   │
│  │ • Project 2                              [Edit] [Del]  │   │
│  │ • Project 3                              [Edit] [Del]  │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│  MAIN CONTENT AREA (calc(100vw - 296px))                      │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ HEADER                                                 │   │
│  │ Traderra  edge.dev  Market Scanner • Real-time       │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ CONTROLS ROW                                           │   │
│  │ [Chart View ▼] [Symbol ▼] [Timeframe ▼]              │   │
│  │ [◀ Day] [Today: Jan 24, 2026] [▀ Day]                │   │
│  │ [Date Offset: 0]                                       │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │                                                        │   │
│  │  CHART AREA                                            │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │                                                  │ │   │
│  │  │     EdgeChart Component                          │ │   │
│  │  │     (Candlestick chart with indicators)          │ │   │
│  │  │                                                  │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │  SCANNER RESULTS                                       │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │ Ticker  | Signal  | Price  | Time  | Actions    │ │   │
│  │  │ SPY     │ BUY     │ $480   │ 9:45  │ [View]     │ │   │
│  │  │ QQQ     │ SELL    │ $520   │ 10:02 │ [View]     │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

### `/backtest` Page Structure

```
┌────────────────────────────────────────────────────────────────┐
│  LEFT SIDEBAR (Fixed, 296px)                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ edge.dev Logo                                          │   │
│  │ Backtest Engine                                        │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ Backtests                                               │   │
│  │ [Refresh]                                              │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ • Backtest 1                            [View] [Del]  │   │
│  │ • Backtest 2                            [View] [Del]  │   │
│  │ • Backtest 3                            [View] [Del]  │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│  MAIN CONTENT AREA                                            │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ HEADER                                                 │   │
│  │ Backtest Results                                       │   │
│  │ Select a backtest to view results                     │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ CONTROLS ROW                                           │   │
│  │ [Chart View ▼] [View Code] [From Date] [To Date]     │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │                                                        │   │
│  │  CHART AREA                                            │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │                                                  │ │   │
│  │  │     EdgeChart Component                          │ │   │
│  │  │     (Backtest equity curve, trades)              │ │   │
│  │  │                                                  │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │  BACKTEST RESULTS PANEL                                │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │ Total Return: +25.4%  Sharpe: 1.8               │ │   │
│  │  │ Win Rate: 62%        Max Drawdown: -8.2%         │ │   │
│  │  │                                                  │ │   │
│  │  │ Trade List:                                      │ │   │
│  │  │ [Table of all backtest trades]                   │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

## 🔍 KEY COMPONENTS

### Shared Components

**EdgeChart** (`/src/components/EdgeChart.tsx`)
- Main charting component
- Displays candlestick data
- Shows technical indicators
- Supports multiple timeframes
- Used on both pages

**TradingViewToggle** (`/src/components/TradingViewToggle.tsx`)
- Switches between chart views
- Controls chart display mode

### Scan Page Components

1. **Projects Sidebar** (Left)
   - Lists saved scanner projects
   - Load/Save/Refresh buttons
   - Edit/Delete project actions

2. **Market Scanner Controls**
   - Symbol selector
   - Timeframe selector (1min, 5min, 15min, 1hour, 1day)
   - Date navigation (previous day, next day)
   - Day offset control

3. **Scanner Results Display**
   - Table of scan signals
   - Ticker, signal type, price, time
   - View action for each result

### Backtest Page Components

1. **Backtests Sidebar** (Left)
   - Lists saved backtests
   - Refresh button
   - View/Delete actions

2. **Backtest Controls**
   - Date range picker (from/to)
   - View code button
   - Chart view toggle

3. **Backtest Results Panel**
   - Performance metrics (Total Return, Sharpe, Win Rate, Max DD)
   - Trade list table
   - Equity curve visualization

---

## 🤖 EXISTING RENATA INTEGRATION

### Current Renata Components

You **ALREADY HAVE** several Renata components:

```
/src/components/renata/
├── RenataV2Chat.tsx           (68KB - Main chat with agents)
├── RenataCopilotKit.tsx       (CopilotKit integration)
├── ChatHistorySidebar.tsx     (Conversation history)
├── RenataV2Transformer.tsx    (Code transformation)
└── SimpleRenataV2Transformer.tsx
```

### Existing Agents

RenataV2Chat **already includes** these agents:

1. **Code Analyzer** (🔵 Blue) - Analyzes code structure
2. **Parameter Extractor** (🟠 Yellow) - Extracts parameters
3. **Code Formatter** (🟣 Purple) - Formats code
4. **Optimizer** (🟢 Green) - Optimizes performance
5. **Documentation** (🩷 Pink) - Adds documentation
6. **Validator** (🔴 Red) - Validates compliance

### Current Integration Points

**Scan Page** (`line 45`):
```typescript
import RenataV2Chat from '@/components/renata/RenataV2Chat';
```

**Backtest Page** (`line 9`):
```typescript
import RenataV2Chat from '@/components/renata/RenataV2Chat';
```

---

## 📊 PAGE WORKFLOWS

### Current Scan Workflow

1. **Load Project**: Select project from left sidebar
2. **Configure Scanner**: Set symbol, timeframe, date
3. **Run Scanner**: Execute scan (backend API call)
4. **View Results**: See signals in results table
5. **Analyze**: Click ticker to view on chart

### Current Backtest Workflow

1. **Load Backtest**: Select backtest from left sidebar
2. **Configure Parameters**: Set date range
3. **View Results**: See equity curve and metrics
4. **Analyze Trades**: Review trade list
5. **View Code**: See scanner code

---

## 🎨 DESIGN SYSTEM

### Colors
- **Gold**: `#D4AF37` (Primary accent color)
- **Background**: `#111111` (Dark background)
- **Border**: `rgba(212, 175, 55, 0.2)` (Subtle gold borders)
- **Text**: `#ffffff` (White text)
- **Muted**: `rgba(255, 255, 255, 0.6)` (Gray text)

### Layout
- **Left Sidebar**: Fixed 288-296px width
- **Main Content**: `calc(100vw - 296px)`
- **Spacing**: 8px between sidebar and main content
- **Z-Index**: Sidebar at z-30 (above content)

### Components
- **Border Radius**: 6-12px (rounded corners)
- **Shadows**: `0 4px 12px rgba(212, 175, 55, 0.3)` (gold glow)
- **Transitions**: `all 0.2s ease` (smooth animations)

---

## ✅ WHAT WORKS

### Scan Page
- ✅ Loads projects from localStorage
- ✅ Displays multiple projects in sidebar
- ✅ Symbol selection works
- ✅ Timeframe switching works
- ✅ Day navigation works (previous/next day)
- ✅ Real-time data fetching from Polygon API
- ✅ Chart displays correctly
- ✅ Scanner results display

### Backtest Page
- ✅ Loads backtests from localStorage
- ✅ Date range selection works
- ✅ Chart displays backtest equity curve
- ✅ Performance metrics calculate correctly
- ✅ Trade list displays

---

## 🚧 WHAT NEEDS FIXING (From Sprint 1)

### Critical Bugs

1. **Hardcoded Date Bug**
   - Location: `/src/app/api/systematic/scan/route.ts`
   - Issue: `const scanDate = '2024-02-23'` (9+ months old!)
   - Fix: Dynamic date selection with trading day validation

2. **Execution Flow Disconnect**
   - Location: `/src/app/exec/page.tsx` (but you don't use this page)
   - **IMPACT**: May not affect you if you only use /scan and /backtest
   - **Question**: Do you execute scans from /scan page directly?

3. **Progress Tracking Deception**
   - Progress bar completes in 7 seconds, actual takes 30+ seconds
   - Need real-time polling every 1 second
   - **Affects**: Both /scan and /backtest pages

---

## 🎯 INTEGRATION OPPORTUNITIES

### Where Renata V2 Should Go

Based on your feedback about wanting a `/plan` page:

```
CURRENT STATE:
/scan      → You use for scanning
/backtest  → You use for backtesting
/exec      → You don't use ❌
/projects  → You don't use ❌

PROPOSED STATE:
/plan      → NEW! Renata workspace 🆕
/scan      → Keep as-is + add quick Renata access
/backtest  → Keep as-is + add quick Renata access
```

### New `/plan` Page Concept

```
┌────────────────────────────────────────────────────────────────┐
│  /plan - RENATA WORKSPACE                                     │
│  ┌──────────────────────┬─────────────────────────────────┐   │
│  │                      │  ACTIVE PROJECTS                │   │
│  │                      │  ┌──────────────────────────┐   │   │
│  │  MAIN CHAT AREA      │  │ 📋 Backside B Scanner    │   │   │
│  │  ┌────────────────┐  │  │ Status: Planning         │   │   │
│  │  │ Chat with      │  │  │ [→ Scan] [→ Backtest]   │   │   │
│  │  │ Renata AI      │  │  └──────────────────────────┘   │   │
│  │  │                │  │  ┌──────────────────────────┐   │   │
│  │  │ User: I want   │  │  │ 📋 IPO Setup             │   │   │
│  │  │ to build...    │  │  │ Status: Researching      │   │   │
│  │  │                │  │  │ [Continue]              │   │   │
│  │  │ Renata: Let    │  │  └──────────────────────────┘   │   │
│  │  │ me analyze...  │  │                                 │   │
│  │  │                │  │  [+ New Project]                │   │
│  │  └────────────────┘  │                                 │   │
│  │                      │                                 │   │
│  │  [Send to /scan]     │                                 │   │
│  │  [Send to /backtest] │                                 │   │
│  └──────────────────────┴─────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

## 📋 QUESTIONS FOR YOU

1. **Execution**: How do you currently execute scans? From the /scan page directly?

2. **Renata Access**: Do you want Renata:
   - **A)** Only on a new `/plan` page (dedicated workspace)?
   - **B)** As sidebar on /scan and /backtest (quick access)?
   - **C)** Both `/plan` page + sidebar access?

3. **Workflow**: What's your ideal workflow?
   - Plan → Build → Test → Execute?
   - Or: Brainstorm on /plan → Move to /scan to execute?
   - Or: Something else?

4. **Projects**: What do you want to track in the left sidebar?
   - Scanner projects (what you have now)?
   - Renata conversations/ideas?
   - Both?

---

## 🎯 NEXT STEPS

1. **You review this analysis** ✅ You're doing this now
2. **Clarify your ideal workflow** (answer questions above)
3. **Update planning documents** with corrected scope
4. **Design /plan page** based on your workflow
5. **Begin Sprint 3** with clear integration strategy

---

**This analysis is the foundation for our integration strategy. Once you confirm your workflow and preferences, I'll update all the planning documents to reflect the correct approach.**

**What's your ideal workflow? How should Renata integrate with your existing pages?**
