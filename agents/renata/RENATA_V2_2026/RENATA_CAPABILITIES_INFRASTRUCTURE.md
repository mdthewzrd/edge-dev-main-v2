# 🤖 RENATA V2 - COMPLETE CAPABILITIES & INFRASTRUCTURE SPECIFICATION
## What Renata Knows, What She Can Do, and How She Works

**Date**: January 24, 2026
**Purpose**: Complete system specification for RENATA V2 AI Agent Platform
**Status**: FINAL SPECIFICATION - Ready for development

---

## 🎯 RENATA VISION STATEMENT

**Renata V2 is an AI-powered trading strategy development platform that transforms ideas, code, and market examples into production-ready V31 scanners through intelligent multi-agent collaboration.**

**Core Promise**: Turn ANY input → V31 scanner → tested strategy in minutes, not hours.

---

## 🧠 RENATA'S KNOWLEDGE BASE

### What Renata Knows

#### 1. V31 Gold Standard (950+ Lines)
**Source**: `/projects/edge-dev-main/V31_GOLD_STANDARD_SPECIFICATION.md`

**Renata Knows**:
- ✅ **PILLAR 0: MARKET SCANNING ARCHITECTURE** (CRITICAL)
  - Full market scanning: NYSE + NASDAQ + ETF lists (~12,000 tickers)
  - Universal market coverage unless ticker/ticker-group specific scan
  - Multi-symbol grouped endpoint optimization
  - Batch processing for large-scale scans
  - Symbol filtering and categorization
- ✅ **PILLAR 1: 3-STAGE GROUPED ENDPOINT ARCHITECTURE**
  - Stage 1: Preliminary fetch (grouped symbols)
  - Stage 2: Secondary pass (per-ticker operations)
  - Stage 3: Grouping and aggregation
- ✅ **PILLAR 2: PER-TICKER OPERATIONS**
  - Independent symbol processing
  - Smart filters (preliminary, secondary, tertiary)
  - Two-pass features (historical buffers)
- ✅ **PILLAR 3: PARALLEL PROCESSING & OPTIMIZATION**
  - Parallel processing patterns
  - Parameter systems and naming conventions
  - Code structure rules
  - Transformation rules (non-V31 → V31)

**How She Uses It**:
- **Default**: Always generates scanners with full market coverage (~12k tickers)
- Generates V31-compliant code with market scanning pillar
- Validates existing code against V31 standard (including market coverage)
- Explains V31 concepts including universal scanning approach
- Suggests V31 improvements for market-wide strategies

---

#### 2. Lingua Trading Framework (772 Lines)
**Source**: `/Users/michaeldurante/Downloads/Private & Shared 8/Lingua original notes.md`

**Renata Knows**:
- ✅ Trend cycle (9 stages: consolidation, breakout, uptrend, extreme deviation, euphoric top, trend break, backside, etc.)
- ✅ Timeframe hierarchy (HTF, MTF, LTF)
- ✅ Market structure (higher highs, higher lows)
- ✅ Daily context (gaps, trend direction)
- ✅ Indicators (EMA clouds, deviation bands, trails, VWAP, PDC)
- ✅ 13 trading setups:
  - Systematized: OS D1, G2G S1, SC DMR, SC MDR Swing
  - Not systematized: Daily Para Run, EXT Uptrend Gap, Para FRD, MDR, LC FBO, LC T30, LC Extended Trendbreak, LC Breakdown, Backside Trend Pop, Backside Euphoric

**How She Uses It**:
- Suggests appropriate setups for market conditions
- Explains trend cycle position
- Recommends timeframe analysis
- Provides setup-specific parameters
- Guides execution strategies

---

#### 3. Libraries & Tools Knowledge Base
**Source**: Technical documentation, API references, code examples

**Renata Knows**:

**Data & Market APIs**:
- ✅ **Polygon API** (`polygon.io`)
  - Real-time and historical market data
  - OHLCV candles (open, high, low, close, volume)
  - Ticker snapshots, quotes, trades
  - Corporate actions (splits, dividends)
  - Market status, holidays, trading days
  - Grouped daily bars (bulk fetching)
  - Aggregates (multi-timeframe)
  - Reference data: tickers, types, exchanges
  - **How She Uses It**: Fetches market data for scanners, backtests, real-time analysis

**Technical Analysis Libraries**:
- ✅ **TA-Lib** (Technical Analysis Library)
  - 150+ technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR, etc.)
  - Pattern recognition functions
  - Price transformations
  - Overlap studies, momentum indicators, volume indicators, volatility indicators
  - **How She Uses It**: Generates code with TA-Lib indicators, chooses appropriate indicators for setups

**Python Data Science Stack**:
- ✅ **pandas** - Data manipulation, time series analysis, DataFrame operations
- ✅ **numpy** - Numerical computing, array operations, mathematical functions
- ✅ **scipy** - Statistical functions, signal processing, optimization
- ✅ **How She Uses It**: Manipulates market data, calculates custom indicators, statistical analysis

**Backtesting Frameworks**:
- ✅ **backtesting.py** (`kernc/backtesting.py`)
  - Strategy definition and execution
  - Backtesting engine with realistic simulation
  - Performance metrics (Sharpe, Sortino, drawdown, etc.)
  - Order management, slippage, commission modeling
  - **How She Uses It**: Generates backtest code, validates strategy logic, calculates performance

- ✅ **VectorBT** (alternative)
  - Vectorized backtesting
  - Fast execution on large datasets
  - **How She Uses It**: Quick backtests on large symbol universes

**Execution & Trading Tools**:
- ✅ **Execution algorithms** (to be documented)
  - Entry order types (market, limit, stop-limit, stop-market)
  - Position sizing algorithms (fixed, volatility-based, Kelly criterion)
  - Risk management (stop-loss, take-profit, trailing stops)
  - **How She Uses It**: Generates execution code, implements risk management

**Data Storage & Caching**:
- ✅ **SQLite / PostgreSQL** - Local data storage
- ✅ **Redis** - Caching layer for market data
- ✅ **Parquet / HDF5** - Efficient data file formats
- ✅ **How She Uses It**: Caches market data, stores backtest results, retrieves historical data

**Visualization & Charts**:
- ✅ **Plotly** (Python & JavaScript)
  - Interactive charting library with 40+ chart types
  - Candlestick charts (OHLCV data for price action)
  - Line charts (equity curves, indicator values, cumulative returns)
  - Scatter plots (trade analysis, parameter optimization)
  - Heatmaps (correlation matrices, performance by regime)
  - Bar charts (volume analysis, trade distribution)
  - **How She Uses It**: Generates chart configurations for market data visualization

- ✅ **Technical Indicator Plotting**
  - Overlay indicators: SMA, EMA, Bollinger Bands, VWAP, ATR trails
  - Subplot indicators: RSI, MACD, Stochastic, Volume, ADX
  - Multi-timeframe layouts: HTF trend + MTF setup + LTF entry
  - Signal markers: Buy/sell signals, entry/exit points, stop-loss levels
  - Annotations: Pattern labels, price levels, trade notes
  - **How She Uses It**: Creates visual representations of scanner signals and indicators

- ✅ **Real-Time Chart Updates**
  - WebSocket integration for live data streaming
  - Incremental updates (append new candles without full redraw)
  - Animation and transitions (smooth chart updates)
  - Performance optimization (decimation, downsampling for large datasets)
  - **How She Uses It**: Builds responsive charts that update with live market data

- ✅ **Chart Integration with Execution**
  - Entry signal markers: Show where scanner triggered
  - Exit markers: Display trade exits with profit/loss
  - Position shading: Highlight holding periods
  - P&L visualization: Equity curve, drawdown periods, cumulative returns
  - Trade list: Table of trades linked to chart points
  - Performance dashboard: Metrics cards, win rate gauges, stats summaries
  - **How She Uses It**: Provides complete visual feedback on execution results

- ✅ **Interactive Features**
  - Zoom/pan: Navigate through time series data
  - Hover tooltips: Show OHLCV, indicator values, signal details
  - Range selector: Quick date range selection
  - Toggle buttons: Show/hide indicators, switch chart types
  - Click events: View trade details, analyze specific signals
  - **How She Uses It**: Creates user-friendly exploratory analysis tools

- ✅ **Dashboard Integration** (EdgeChart Component)
  - React Plotly integration in Next.js
  - Component: `/src/components/EdgeChart.tsx`
  - Chart controls: Timeframe selector, date navigation, symbol switching
  - State management: Sync chart with scanner results, backtest data
  - Responsive layout: Adapts to different screen sizes
  - Theme support: Dark mode styling matching EdgeDev design
  - **How She Uses It**: Generates Plotly configurations that integrate with existing EdgeChart

- ✅ **Chart Styling & Theming**
  - Color schemes: Gold (#D4AF37) accent, dark backgrounds (#111111)
  - Fonts: Monospace for data, sans-serif for labels
  - Grid lines: Subtle borders, muted colors
  - Figure layout: Margins, spacing, legend positioning
  - Responsive sizing: Auto-resize to container
  - **How She Uses It**: Creates charts matching EdgeDev visual design system

- ✅ **Advanced Charting Patterns**
  - Multi-panel layouts: Price + subplots for indicators
  - Shared x-axis: Synchronized time across panels
  - Range buttons: 1D, 5D, 1M, 3M, 6M, YTD, MAX
  - Crosshair/hover: Show cursor position across all panels
  - Shape drawing: Support lines, trend lines, fibonacci retracements
  - **How She Uses It**: Builds professional-grade trading charts

**API Integration**:
- ✅ **REST APIs** - Standard API patterns, error handling, rate limiting
- ✅ **WebSockets** - Real-time data streaming
- ✅ **Async Python** (`asyncio`, `aiohttp`) - Concurrent API calls
- ✅ **How She Uses It**: Fetches data efficiently, handles API errors, implements rate limits

**How She Uses All Tools**:
- Selects appropriate library for each task (Polygon for data, TA-Lib for indicators, backtesting.py for validation)
- Generates code that uses these libraries correctly
- Troubleshoots library-related issues
- Optimizes code for performance (vectorization, caching, parallel processing)
- Ensures code follows best practices for each library

---

#### 4. Trading Concepts & Strategies Knowledge Base
**Source**: Trading literature, strategy research, experience documentation

**Renata Knows**:

**Profitable Trading Principles**:
- ✅ **Edge identification**: Statistical advantages in market behavior
- ✅ **Risk management**: Position sizing, stop-loss, portfolio risk
- ✅ **Expectancy**: Positive expected value calculations
- ✅ **Win rate vs risk-reward**: Balance of frequency and magnitude
- ✅ **Market regime awareness**: Adapting to bull/bear/volatile markets
- ✅ **Psychology**: Emotional discipline, patience, avoiding overtrading
- ✅ **Process over outcome**: Focus on execution, not just results
- ✅ **How She Uses It**: Guides users toward robust strategies, warns against risky approaches

**Quantitative Trading Concepts**:
- ✅ **Statistical analysis**: Mean reversion, momentum, cointegration
- ✅ **Backtesting methodology**: In-sample (IS) vs out-of-sample (OOS), walk-forward analysis
- ✅ **Overfitting avoidance**: Simple parameters, robust rules, sufficient sample size
- ✅ **Performance metrics**: Sharpe ratio, Sortino, Calmar, maximum drawdown, win rate, profit factor
- ✅ **Monte Carlo simulation**: Random permutation testing, confidence intervals
- ✅ **Portfolio optimization**: Correlation, diversification, position allocation
- ✅ **How She Uses It**: Validates strategies, explains quant concepts, suggests robustness checks

**Systematic Trading Framework**:
- ✅ **Rule-based systems**: Clear entry/exit rules, no discretion
- ✅ **Setup definitions**: Precise criteria for trade opportunities
- ✅ **Timeframe selection**: Higher timeframes for context, lower for entry
- ✅ **Multi-timeframe analysis**: HTF trend, MTF setup, LTF entry
- ✅ **Market structure**: Higher highs/lows, support/resistance, key levels
- ✅ **Indicators**: EMA clouds, deviation bands, VWAP, ATR, volume profile
- ✅ **How She Uses It**: Builds systematic scanners, enforces clear rules, explains framework

**Execution Strategies**:
- ✅ **Entry types**: Market orders (immediate), limit orders (better price), stop orders (breakout)
- ✅ **Position sizing**: Fixed dollar, volatility-based (ATR), percentage of account, Kelly criterion
- ✅ **Risk management**: Stop-loss placement (ATR-based, structural), position limits, daily loss limits
- ✅ **Exit strategies**: Profit targets (risk-reward based), trailing stops, time-based exits
- ✅ **Trade management**: Scaling in/out, partial profits, breakeven stops
- ✅ **Slippage & commission**: Realistic cost modeling in backtests
- ✅ **How She Uses It**: Generates execution code, implements risk management, suggests position sizing

**Market Microstructure**:
- ✅ **Order book dynamics**: Bid-ask spread, liquidity, market depth
- ✅ **Volume analysis**: Volume profiles, accumulation/distribution, volume patterns
- ✅ **Gaps**: Gap ups/downs, gap fill probability, gap continuation
- ✅ **Volatility**: ATR, VIX, implied vs realized volatility, volatility regimes
- ✅ **Market sessions**: Pre-market, regular hours, after-hours dynamics
- ✅ **How She Uses It**: Explains market behavior, suggests appropriate strategies for conditions

**Strategy Types**:
- ✅ **Trend following**: Moving average crossovers, breakout strategies, momentum
- ✅ **Mean reversion**: RSI extremes, Bollinger Bands, support/resistance bounces
- ✅ **Gap trading**: Gap continuation, gap fade, gap and go
- ✅ **Pattern trading**: Technical patterns (flags, triangles, head & shoulders)
- ✅ **Breakout strategies**: Range breakouts, volatility breakouts, momentum breakouts
- ✅ **How She Uses It**: Categorizes user ideas, suggests appropriate strategy types

**Performance Evaluation**:
- ✅ **Return metrics**: Total return, CAGR, monthly/annual returns
- ✅ **Risk metrics**: Max drawdown, volatility, downside deviation
- ✅ **Risk-adjusted returns**: Sharpe, Sortino, Calmar, Information ratio
- ✅ **Trading metrics**: Win rate, profit factor, average win/loss, expectancy
- ✅ **Robustness**: IS/OOS comparison, parameter sensitivity, market stability
- ✅ **How She Uses It**: Analyzes backtest results, compares strategies, identifies weaknesses

**How She Uses All Trading Knowledge**:
- Explains trading concepts in accessible language
- Guides users toward robust, systematic approaches
- Warns against common mistakes (overfitting, poor risk management, emotional trading)
- Suggests improvements based on quantitative principles
- Validates that strategies follow sound trading logic

---

#### 5. Vision & State Understanding
**Source**: System design, state management patterns, UI/UX principles

**Renata Understands**:

**System State Awareness**:
- ✅ **Current page context**: Knows if user is on /plan, /scan, or /backtest
- ✅ **Active project**: Tracks which project user is working on
- ✅ **Chat history**: Maintains conversation context within project
- ✅ **Execution status**: Knows if scans/backtests are running, completed, or failed
- ✅ **Data availability**: Knows what market data is loaded/cached
- ✅ **How She Uses It**: Provides context-aware assistance, suggests appropriate actions

**Visual Pattern Recognition** (via Vision Agent - Future):
- ✅ **Chart analysis**: Can analyze chart screenshots for setups
- ✅ **Pattern identification**: Detects trend, structure, key levels
- ✅ **Parameter extraction**: Reads indicator values from charts
- ✅ **Comparison**: Compares user charts to A+ examples
- ✅ **How She Uses It**: Processes A+ example images, validates setup understanding

**User Intent Understanding**:
- ✅ **Natural language processing**: Understands user goals from conversation
- ✅ **Task inference**: Infers next steps from context (e.g., after building scanner, suggest execution)
- ✅ **Preference learning**: Remembers user's preferred approaches (timeframes, risk tolerance)
- ✅ **Question asking**: Asks clarifying questions when intent is unclear
- ✅ **How She Uses It**: Anticipates user needs, provides proactive suggestions

**Workflow State Tracking**:
- ✅ **Current workflow stage**: Knows if in planning, building, testing, or execution phase
- ✅ **Completion status**: Tracks which workflow steps are done
- ✅ **Loop detection**: Recognizes optimization loops, suggests convergence
- ✅ **Handoff coordination**: Smooth transitions between agents
- ✅ **How She Uses It**: Guides users through workflows, reminds of next steps

**Error & Edge Case Understanding**:
- ✅ **Failure detection**: Recognizes when executions fail, data is missing, code has bugs
- ✅ **Recovery strategies**: Suggests fixes for common errors
- ✅ **Fallback options**: Provides alternative approaches when primary fails
- ✅ **Error communication**: Explains errors clearly in user language
- ✅ **How She Uses It**: Troubleshoots issues, provides clear error messages

**How She Uses Vision & State Understanding**:
- Provides contextually relevant assistance
- Anticipates user needs based on current state
- Smoothly coordinates complex workflows
- Explains system status clearly
- Adapts responses to user's expertise level

---

#### 6. Existing Systematized Strategies (4 Scanners)
**Source**: `/projects/edge-dev-main/backend/` (to be located)

**Renata Knows**:
- ✅ OS D1: Overnight gap setup (parameters, logic, performance)
- ✅ G2G S1: Gap continuation setup
- ✅ SC DMR: Multi-pattern scanner (LC D2 format)
- ✅ SC MDR Swing: Swing trading variant
- ✅ Code patterns and structures
- ✅ Parameter ranges and optimizations
- ✅ Historical performance data

**How She Uses It**:
- Finds similar setups for inspiration
- Suggests parameter ranges based on history
- Compares new strategies to existing ones
- Identifies what works and what doesn't

---

#### 6. Analyzer Codes - Pre-Validation System
**Source**: Testing framework, dashboard integration, validation patterns

**What Are Analyzer Codes?**:
Analyzer codes are lightweight validation scripts that **confirm the vision is properly expressed with code** BEFORE running full backtests or executions. They provide quick visual feedback to ensure scanners capture the intended patterns.

**Renata Knows**:

**Analyzer Code Types**:

1. **A+ Example Analyzer** (Validate Pattern Capture)
   - **Purpose**: Confirm scanner captures the exact A+ example setup
   - **Process**:
     - Take user's A+ example (ticker + date)
     - Run scanner on that specific ticker/date
     - Show visual confirmation on dashboard/chart
     - Display: "✅ This A+ example triggered!" or "❌ Missed - need adjustment"
   - **Visual Output**: Chart showing the setup with scanner signal overlay
   - **How She Uses It**: Validates scan accuracy before full backtest

2. **Idea Visualizer** (Show on Example)
   - **Purpose**: For execution/strategy ideas, show them working on historical example
   - **Process**:
     - User describes idea (e.g., "buy gap ups with euphoric tops")
     - Renata suggests parameters
     - Runs analyzer on historical example
     - Shows visual: "Here's your idea on TSLA 2024-01-15"
   - **Visual Output**: Chart with proposed entry/exit points marked
   - **How She Uses It**: Confirms idea translates correctly to code

3. **Parameter Sensitivity Analyzer**
   - **Purpose**: Test how parameter changes affect signal capture
   - **Process**:
     - Vary key parameters (e.g., gap_over_atr: 0.7, 0.8, 0.9)
     - Show signal count changes: "12 signals → 47 signals → 156 signals"
     - Recommend: "Sweet spot: 0.8-0.9 captures best opportunities"
   - **Visual Output**: Parameter vs signal count table/chart
   - **How She Uses It**: Helps user optimize parameters

4. **Quick Backtest Analyzer**
   - **Purpose**: Fast validation on recent data (e.g., last 30 days)
   - **Process**:
     - Run scanner on last 30 days, all symbols
     - Show quick stats: "47 signals, 68% win rate, +8.4% return"
     - User decides: "Looks good, run full backtest" or "Needs adjustment"
   - **Visual Output**: Summary stats table, recent signals chart
   - **How She Uses It**: Rapid feedback loop before committing to full backtest

**Human-in-the-Loop Workflow**:
```
User: "Build a backside scanner from this A+ example"

Renata [Planning Agent]:
  "Analyzing A+ example...
   Parameters extracted: gap_over_atr=0.8, ..."

Renata [Builder Agent]:
  "Scanner generated! Before backtesting, let's validate:"

Renata [Executor Agent - Analyzer Mode]:
  "🔍 Running A+ Example Analyzer...

   Testing on: SPY 2024-01-15 (your A+ example)

   Result: ✅ CAPTURED!

   Chart: [Shows SPY chart with signal overlay]
   - Gap up: +1.2% (threshold: 0.8%)
   - Euphoric top: RSI 72
   - Backside trigger: 10:32 AM

   This scanner captured your A+ example perfectly!

   Ready for quick 30-day backtest? [Yes] [Adjust parameters]"
```

**Dashboard Integration**:
- ✅ **Primary UI**: All analyzers show results on /scan dashboard (EdgeChart)
- ✅ **Visual feedback**: Charts with signal overlays, entry/exit markers
- ✅ **Interactive**: User can explore results, drill down into specific signals
- ✅ **No over-engineering**: Keep it simple - dashboards not chat screenshots
- ✅ **Chat integration**: Renata summarizes results and provides link to dashboard

**How She Uses Analyzer Codes**:
1. **After building scanner**: Automatically suggest running A+ analyzer
2. **Before full backtest**: Require quick validation pass
3. **During optimization**: Show parameter sensitivity analysis
4. **Error detection**: If analyzer fails, diagnose and fix code
5. **User confidence**: Builds trust that scanner works as intended

**Benefits**:
- ✅ **Fast feedback**: Seconds vs minutes for full backtest
- ✅ **Visual confirmation**: See setup captured on actual chart
- ✅ **Iterative refinement**: Quick test-adjust loop
- ✅ **Error prevention**: Catch issues before expensive full backtests
- ✅ **User confidence**: Validates understanding before committing

---

#### 7. A+ Example Catalog

**Renata Will Know**:
- ✅ Chart breakdowns with parameters
- ✅ Market regime context for each example
- ✅ Results from running scans on examples
- ✅ Parameter sets that worked
- ✅ What made each example "A+"

**How She Uses It**:
- Extracts parameter molds from examples
- Identifies patterns in successful setups
- Suggests similar examples for user's ideas
- Builds scanners from A+ example molds

---

#### 9. Market Structure & Price Levels (Lingua Framework)
**Source**: `/Users/michaeldurante/Downloads/Private & Shared 8/Lingua original notes 25ad8836ce438123afedd0b69b25be3f.md`

**Renata Knows**:

**Market Structure Fundamentals**:
- ✅ **Higher Highs, Higher Lows** (Uptrend definition)
- ✅ **Lower Lows, Lower Highs** (Downtrend definition)
- ✅ **Pivot Points / Structure Points** (Key swing highs/lows)
- ✅ **Trend Drawing Rules** (minimum 3 touches preferred)
- ✅ **Structure Breaks** (Trend reversal confirmation)
- ✅ **Role Reversal** (Broken support becomes resistance, vice versa)

**Trend Identification**:
- ✅ **Main MTF Trend** (The trend supporting the entire leg)
- ✅ **Sub-Trends** (Trends within trends - "walking the trend")
- ✅ **Trend Angle** (Steeper trend = faster timeframe focus)
- ✅ **Trend Strength** (Higher timeframe = more weight)
- ✅ **Trend Break Height** (Higher in range = better fade)

**Key Level Detection**:
- ✅ **Support/Resistance Levels** (Historical price zones)
- ✅ **Pivot Highs/Lows** (Swing points for trend drawing)
- ✅ **Level Strength** (Number of tests + volume at level)
- ✅ **Level Confluence** (Multiple S/R at same price = stronger)
- ✅ **Previous Day High/Low/Close** (Daily context levels)

**Structure Break Patterns**:
- ✅ **Breakout/Trend Break** (Catalyst from consolidation)
- ✅ **Failed Breaks** (False breakout traps)
- ✅ **Re-Tests** (Return to broken level to confirm)
- ✅ **Consolidation Breaks** (Range expansion)

**Stair Stepping of Trends** (Advanced Concept):
- ✅ **Break Trend → Next Timeframe Mean** (e.g., break 1hr trend → revert to 2hr or 4hr mean)
- ✅ **Reset Logic** (Price goes too far too fast → reset to next timeframe up)
- ✅ **Hierarchy** (1m → 2m → 5m → 15m → 1hr → 2hr → 4hr → Daily)

**How She Uses It**:
- Generates code that detects structure breaks BEFORE triggering signals
- Validates setups are AT key pivot levels (not random price)
- Identifies trend break height (higher in range = better fade)
- Prevents false signals in "no man's land" (no structure nearby)
- Implements stair-stepping logic for target projections

**Code Generation Patterns**:
```python
# Pivot Point Detection
def detect_pivots(data, window=5):
    # Find swing highs (higher than neighbors)
    # Find swing lows (lower than neighbors)
    # Return list of pivot points with timestamps

# Trend Drawing
def draw_trend(pivots, min_touches=3):
    # Connect pivots to form trend line
    # Require minimum 3 touches for validation
    # Return trend slope, angle, strength

# Structure Break Detection
def detect_structure_break(price, trend_line):
    # Price closes through trend line
    # Volume confirmation (optional but preferred)
    # Return True if broken, False otherwise

# Level Strength
def level_strength(price_level, historical_data):
    # Count tests (how many times touched)
    # Volume at each test
    # Time since last test
    # Return strength score (0-100)
```

---

#### 10. User's Proprietary Indicators (Lingua System)
**Source**: `/Users/michaeldurante/Downloads/Private & Shared 8/Lingua original notes 25ad8836ce438123afedd0b69b25be3f.md`

**Renata Knows**:

**Indicator System Overview**:
- ✅ **Means** (EMAs - Multiple timeframes)
- ✅ **Extremes** (Deviation Bands - ATR-based)
- ✅ **Trail** (9/20 Cloud - Trend following)
- ✅ **Confirmation** (VWAP, Volume, PDC)
- ✅ **Execution Bands** (9/20 Deviation - Entry/Exit zones)

**1. MEANS - EMA Cloud System**

**Indicator Configuration**:
```
15m Chart:
  - 15m 50 EMA
  - 15m 72/89 Cloud (PRIMARY for MTF)
  - 15m 111 EMA
  - 15m 222 EMA
  - 30m 72/89 Cloud

Hourly Chart:
  - 1hr 72/89 Cloud
  - 2hr 72/89 Cloud
  - 4hr 72/89 Cloud
```

**Cloud Definition**:
- **Green Cloud**: EMA72 > EMA89 (Bullish bias)
- **Red Cloud**: EMA72 < EMA89 (Bearish bias)
- **Primary Mean**: 15m 72/89 cloud (follows MTF trends best)
- **Purpose**: Identify trend direction, pullback zones, route start/end

**2. EXTREMES - Deviation Bands**

**Type 1: Main Deviation Band** (Setup & Route Start)
- **Based on**: 72/89 EMA Cloud
- **Calculation**: EMA72 ± (ATR72 × multiplier)
- **Parameters**:
  - Upper Band Multiplier: 10.0
  - Lower Band Multiplier: 10.0
  - Secondary Upper: 8.0
  - Secondary Lower: 8.0
- **Purpose**: Setup identification, route start, extreme deviation zones
- **Usage**: "When in extreme deviation, stop looking for longs"

**Type 2: Execution Deviation Band** (Entry/Exit)
- **Based on**: 9/20 EMA Cloud (not 72/89!)
- **Calculation**: EMA9 ± (ATR9 × multiplier)
- **Parameters**:
  - Upper Band Multiplier: 1.5 (entry zones)
  - Lower Band Multiplier: 1.5 (cover zones)
- **Purpose**: LTF execution, entry timing, cover spots
- **Usage**: "Hit pops into dev bands, cover into bands"

**Key Insight**:
- **Red Upper Band** (main dev) is exceptional at picking trend tops
- Bands expand with volatility (ATR-based)
- Price interacts "like clockwork" with bands

**3. TRAIL - 9/20 Cloud**

**Indicator Configuration**:
- **9 EMA** (Fast)
- **20 EMA** (Slow)
- **Cloud Fill**: Green when fast > slow, Red when fast < slow

**Trail Confirmation**:
- **Trend Ends** when close outside top of cloud (both days shown)
- **Used for**: Trend validation when in actual trade
- **Purpose**: "Rough guide when trend isn't clear"
- **Timeframes**: All timeframes (primary: 15m, 1hr)

**4. CONFIRMATION INDICATORS**

**VWAP**:
- **Purpose**: Confirmation after entry, look for adds
- **Usage**: Standard VWAP calculation
- **Signal**: Price above VWAP = bullish, below = bearish

**Volume**:
- **Purpose**: See liquidity, confirm moves
- **Usage**: Standard volume bars
- **Signal**: High volume on break = valid, low volume = suspect

**Previous Day Close (PDC)**:
- **Purpose**: Daily context level
- **Usage**: Yesterday's closing price
- **Signal**: Gap up/down from PDC = context

**Historical Gap Stats** (Small Cap Day One Setup):
- **Purpose**: Gap statistics for IPOs/small caps
- **Usage**: Historical gap performance data
- **Signal**: Win rate based on historical stats

**Indicator Layout** (User Preference):
```
Primary (Always Visible):
- 2 Deviation Bands (Main + Execution)
- 2 EMA Clouds (72/89 + 9/20)
- VWAP
- PDC

Secondary (On Standby):
- Trail (9/20 cloud)
- Volume
- Historical gap stats
```

**Pine Script Code** (User's Exact Implementation):

**Cloud Indicator**:
```pine
//@version=4
study("RahulLines Cloud", overlay=true)

sl = input(72, "Smaller length")
hl = input(89, "Higher length")
res = input(title="JLines - Time Frame 1", type=input.resolution, defval="1")
res1 = input(title="JLines - Time Frame 2", type=input.resolution, defval="3")
enable515 = input(false,"5/15 EMA")
res2 = input(title="5 /15 EMA", type=input.resolution, defval="5")

tickprice1 = security(syminfo.tickerid, res, close)
tickprice2 = security(syminfo.tickerid, res, close)

ema1_72 = security(syminfo.tickerid, res, ema(close, sl))
ema1_89 = security(syminfo.tickerid, res, ema(close, hl))
ema2_72 = security(syminfo.tickerid, res1, ema(close, sl))
ema2_89 = security(syminfo.tickerid, res1, ema(close, hl))
ema3_5 = security(syminfo.tickerid, res2, ema(close, 5))
ema3_15 = security(syminfo.tickerid, res2, ema(close, 15))

fill(ema1_72, ema1_89, color=ema1_72>ema1_89?color.green:color.red, transp=30)
fill(ema2_72, ema2_89, color=ema2_72>ema2_89?color.green:color.red, transp=90)
```

**Deviation Band Indicator**:
```pine
//@version=5
indicator("Dual Deviation Cloud", overlay=true)

deviationAbove1 = input.float(10.0, "First Positive Deviation Multiplier")
deviationAbove2 = input.float(8.0, "Second Positive Deviation Multiplier")
deviationBelow1 = input.float(10.0, "First Negative Deviation Multiplier")
deviationBelow2 = input.float(8.0, "Second Negative Deviation Multiplier")
length72EMA = input.int(72, "Length for the 72 EMA")
length89EMA = input.int(89, "Length for the 89 EMA")

colorAbove = color.new(color.red, 60)
colorBelow = color.new(color.green, 60)

ema72 = ta.ema(close, length72EMA)
ema89 = ta.ema(close, length89EMA)
atr72 = ta.sma(ta.tr(true), length72EMA)
atr89 = ta.sma(ta.tr(true), length89EMA)

deviationAboveLine1 = ema72 + (deviationAbove1 * atr72)
deviationAboveLine2 = ema72 + (deviationAbove2 * atr72)
deviationBelowLine1 = ema89 - (deviationBelow1 * atr89)
deviationBelowLine2 = ema89 - (deviationBelow2 * atr89)

fill(plot1=plot(deviationAboveLine1, display=display.none),
      plot2=plot(deviationAboveLine2, display=display.none),
      color=colorAbove)
fill(plot1=plot(deviationBelowLine1, display=display.none),
      plot2=plot(deviationBelowLine2, display=display.none),
      color=colorBelow)
```

**How She Generates Code**:
- ✅ Uses YOUR exact indicator parameters (72/89, 9/20, 10.0/8.0 multipliers)
- ✅ Implements multi-timeframe clouds (15m, 1hr, 2hr, 4hr)
- ✅ Generates ATR-based deviation bands (not generic Bollinger Bands)
- ✅ Respects your indicator layout preferences (primary vs secondary)
- ✅ Implements "clockwork" price interactions you've validated

---

#### 11. Pyramiding & Execution Approach
**Source**: `/Users/michaeldurante/Downloads/Private & Shared 8/Lingua original notes 25ad8836ce438123afedd0b69b25be3f.md`

**Renata Knows**:

**Pyramiding Strategy** (Position Building):
- ✅ **Initial Position** (Route Start): Get majority of position size
- ✅ **Scale-In Rules**: Add to position at favorable spots
- ✅ **Position Sizing per Level**: Risk allocated across entries
- ✅ **Stop Adjustment**: Lower stops as position grows (reduce risk)
- ✅ **Risk-to-Reward Optimization**: Build position, improve R:R

**Execution Philosophy**:
- ✅ **Position Trading Style** (Not day trading)
- ✅ **Route Start → Route End**: Main position size at start, cover majority at end
- ✅ **In-Between Trading**: "Recycle" - use market structure between
- ✅ **LTF Execution Hub**: 2-minute chart for entries/exits
- ✅ **Simple Rule**: "Hitting pops and covering dips"

**Entry Rules**:
- ✅ **Short Entry Timing**: Enter shorts in HIGH part of trend
- ✅ **Cover Timing**: Cover into LOW part of trend
- ✅ **Completion**: Final cover on trend break
- ✅ **High EV Spots**: Deviation bands, extreme deviations, trend breaks

**Pyramiding Execution** (Step-by-Step):
```
1. Route Start (MTF):
   - Enter initial position (50-70% of full size)
   - Set initial stop loss
   - Target: Route end (HTF mean or target)

2. Scale-Ins (LTF - 2m chart):
   - Add to position at favorable spots
   - Entry triggers: Pops into dev bands, pullbacks to means, trend breaks
   - Each scale-in: 10-20% additional position
   - Adjust stop lower (reduce risk, lock in profit)

3. Position Management:
   - Trail stops as position grows
   - Take partial profits at intermediate targets
   - Build position, improve R:R

4. Route End (MTF):
   - Cover majority of position (70-80%)
   - Keep small position for potential continuation
```

**Stop Management**:
- ✅ **Initial Stop**: Based on structure (swing high/low)
- ✅ **Trail Stop**: Adjust down as position builds (lower risk)
- ✅ **Breakeven**: Move to breakeven after +1R profit
- ✅ **Time Stops**: End of day for intraday positions

**Risk Management**:
- ✅ **Per Pyramid Level**: Risk 0.5-1% per entry
- ✅ **Total Position Risk**: Max 2-3% of account
- ✅ **Correlation**: Avoid pyramid on highly correlated names
- ✅ **Position Limits**: Max 3-4 pyramids active simultaneously

**Execution Timeframes**:
- ✅ **HTF** (Daily, 4hr): Find setup, determine bias, key levels
- ✅ **MTF** (1hr, 15m): Route start, route end, trend breaks, resets
- ✅ **LTF** (5m, 2m): Execution hub, entries, adds, covers
- ✅ **Rule**: "Different questions answered on different timeframes"

**Pyramiding Code Generation Patterns**:
```python
# Route Start Detection
def detect_route_start(htf_data, mtf_data):
    # MTF trend break confirmation
    # Price at key level
    # Volume spike
    return signal, entry_zone, initial_stop

# Scale-In Triggers
def detect_scale_in_opportunity(ltf_data, current_position):
    # Pop into execution dev band
    # Pullback to 15m mean
    # Trend break confirmation
    return add_signal, add_size, new_stop

# Position Builder
def pyramid_position(signals, account_size, risk_per_trade):
    position = []

    for signal in signals:
        if signal.type == 'ROUTE_START':
            # Initial entry (50-70%)
            size = calculate_initial_size(account_size, risk_per_trade, signal.stop)
            position.append({'entry': signal.price, 'size': size, 'stop': signal.stop})

        elif signal.type == 'ADD':
            # Scale-in (10-20%)
            add_size = calculate_add_size(account_size, risk_per_trade, signal.stop, len(position))
            new_stop = adjust_stop_lower(position, signal.stop)
            position.append({'entry': signal.price, 'size': add_size, 'stop': new_stop})

    return position

# Stop Management
def adjust_stops_pyramid(position_entries, current_stop):
    # Move stop to breakeven once +1R
    if unrealized_profit(position_entries) >= initial_risk:
        return breakeven_stop

    # Trail stop as position grows
    elif unrealized_profit(position_entries) >= 2 * initial_risk:
        return trail_stop(current_stop)

    return current_stop
```

**How She Uses It**:
- ✅ Generates pyramiding code matching YOUR style
- ✅ Implements "route start → scale-ins → route end" flow
- ✅ Uses 2-minute LTF for execution (your preference)
- ✅ Implements "hitting pops and covering dips" logic
- ✅ Adjusts stops as position builds (YOUR approach)
- ✅ Respects your risk management rules (2-3% max, 0.5-1% per level)

---

#### 12. Daily Context & Market Molds (Lingua Categories)
**Source**: `/Users/michaeldurante/Downloads/Private & Shared 8/Lingua original notes 25ad8836ce438123afedd0b69b25be3f.md`

**Renata Knows**:

**Daily Context Categories**:

**1. Front Side**:
- ✅ **Definition**: At all-time highs (ATH)
- ✅ **Lookback**: Years (not just recent highs)
- ✅ **Characteristics**: No overhead resistance, clear air
- ✅ **Examples**: NVDA daily run to ATH

**2. Backside**:
- ✅ **Definition**: Not at ATH (trading below previous swing high)
- ✅ **Characteristics**: Overhead resistance from previous highs
- ✅ **Lookback**: Previous swing highs define resistance
- ✅ **Examples**: Moves under major highs, trading below resistance

**3. IPO**:
- ✅ **Definition**: Initial public offering
- ✅ **Characteristics**: No history, small cap typically
- ✅ **Special Setup**: Small Cap Day One Setup
- ✅ **Tools**: Historical gap stats for win rate

**Daily Molds** (Front Side Types):

**Daily Parabolic**:
- ✅ **Pattern**: Parabolic uptrend from daily move
- ✅ **Visual**: Steep acceleration, multiple green candles
- ✅ **Setup**: Euphoric tops, trend breaks on pullbacks

**Para MDR** (Parabolic Multi-Day Run):
- ✅ **Pattern**: Parabolic move NOT from uptrend
- ✅ **Visual**: Few candles spark big run "from nowhere"
- ✅ **Duration**: 2+ days

**FBO** (Fade Breakout):
- ✅ **Pattern**: Price sets high → fades (days/weeks/months) → retests high
- ✅ **Visual**: Failed breakout, then successful retest
- ✅ **Duration**: Gap between high and retest (can be weeks/months)

**D2** (Day 1 Up, Day 2 Fade):
- ✅ **Pattern**: Day 1 = big green, Day 2 = fade
- ✅ **Triggers**: Daily parabolic + big gap, or big green day + gap
- ✅ **Setup**: Day 2 euphoric top, trend break

**MDR** (Multi-Day Run):
- ✅ **Pattern**: D2 but 2+ days up
- ✅ **Visual**: Multiple big green days, then fade
- ✅ **Setup**: Similar to D2 but longer duration

**Uptrend ET** (Uptrend Euphoric Top):
- ✅ **Pattern**: Uptrend move → euphoric top (no parabolic speed)
- ✅ **Difference**: Lacks parabolic acceleration of daily parabolic
- ✅ **Setup**: Trend break or backside continuation

**Backside Molds** (Backside Types):

**Backside ET** (Euphoric Top on Backside):
- ✅ **Pattern**: After big move up + trend break, or stuck in downtrend
- ✅ **Types**: D2, MDR, or gap up
- ✅ **Setup**: Short euphoric tops, trade backside

**T30** (Trend + 30 Days):
- ✅ **Pattern**: Coming off massive euphoric top/fade
- ✅ **Timing**: 30-60 days after euphoric top
- ✅ **Logic**: "Trading into all the longs now underwater"
- ✅ **Types**: D2, MDR, or gap up

**How She Uses Daily Context**:
- ✅ **Differentiates** hundreds of similar setups (all uptrending vs specific mold)
- ✅ **Determines** execution approach (front side vs backside vs IPO)
- ✅ **Guides** risk management (front side = clearer air, backside = overhead resistance)
- ✅ **Categorizes** scanner results by daily context
- ✅ **Applies** mold-specific execution rules (D2 vs MDR vs FBO)

**Code Generation Patterns**:
```python
# Daily Context Detection
def detect_daily_context(daily_data, lookback_years=2):
    ath = daily_data['high'].max()  # All-time high

    if daily_data['high'].iloc[-1] >= ath * 0.999:
        return 'FRONT_SIDE'

    prev_high = daily_data['high'].rolling(window=252*lookback_years).max().iloc[-1]

    if daily_data['high'].iloc[-1] < prev_high:
        return 'BACKSIDE'

    # Check if IPO (no history beyond certain point)
    if len(daily_data) < 252:  # Less than 1 year
        return 'IPO'

# Daily Mold Detection
def detect_daily_mold(daily_data, context):
    if context == 'FRONT_SIDE':
        # Check for parabolic acceleration
        if detect_parabolic(daily_data):
            return 'DAILY_PARABOLIC'

        # Check for MDR pattern
        if detect_mdr(daily_data):
            return 'PARA_MDR'

        # Check for FBO pattern
        if detect_fbo(daily_data):
            return 'FBO'

    elif context == 'BACKSIDE':
        # Check for T30 timing
        if detect_t30_timing(daily_data):
            return 'T30'

        # Check for backside euphoric top
        if detect_backside_euphoric(daily_data):
            return 'BACKSIDE_ET'

def detect_parabolic(daily_data, window=5):
    # Steep acceleration
    # Multiple large green candles
    # Volume expansion
    recent_returns = daily_data['close'].pct_change(window)
    return recent_returns.sum() > threshold

def detect_fbo(daily_data, lookback_days=60):
    # Find recent high within lookback
    recent_high = daily_data['high'].rolling(window=lookback_days).max()

    # Check if current price is near recent high
    # Check if there was a fade after the high
    return (daily_data['high'].iloc[-1] >= recent_high * 0.98 and
            detect_fade_between_high_and_now(daily_data, recent_high))

def detect_t30_timing(daily_data, euphoric_top_date):
    # Check if 30-60 days after euphoric top
    days_since_top = (daily_data.index[-1] - euphoric_top_date).days

    return 30 <= days_since_top <= 60
```

---

#### 13. Trend Cycle Trading (Lingua Framework)
**Source**: `/Users/michaeldurante/Downloads/Private & Shared 8/Lingua original notes 25ad8836ce438123afedd0b69b25be3f.md`

**Renata Knows**:

**The Trend Cycle** (9 Stages):
1. **Consolidation** → Range-bound, waiting for breakout
2. **Breakout/Trend Break** → Catalyst from consolidation
3. **Uptrend** → Confirmed uptrend (higher highs, higher lows)
4. **Extreme Deviation** → Price at trend channel extremes
5. **Euphoric Top** → Move outside trend (speed up, volume spike)
6. **Trend Break** → Uptrend breaks, gravity takes over
7. **Backside** → Reverting to HTF mean
8. **Backside Reverted** → Hit HTF mean
9. **Consolidation/Backside Breakout** → Next cycle begins

**Trading Rules by Stage**:

**Consolidation**:
- ✅ **Bias**: Becoming aware (both thesis = catalyst)
- ✅ **Trades**: Main breakout only
- ✅ **High EV**: Dips to means/extremes, main breakout, break-and-retest
- ✅ **Early Trends**: Pre-breakout trend breaks (sizing spots)

**Uptrend**:
- ✅ **Bias**: Long only (confirmed uptrend)
- ✅ **Trades**: Dips to means or extremes
- ✅ **Rule**: Continue until extreme deviation
- ✅ **Stop Point**: Extreme deviation reached

**Extreme Deviation**:
- ✅ **Bias**: STOP looking for longs (trend can flip any time)
- ✅ **Trades**: Euphoric top shorts, trend break shorts
- ✅ **Guides**: 1hr/4hr/daily deviation bands, daily EMA extension
- ✅ **Rule**: Better to be early with this stage than late

**Euphoric Top**:
- ✅ **Timing**: 7am-12pm (gap-centric setup)
- ✅ **Types**: Euphoric Gap, Euphoric EXT, Partial Euphoric
- ✅ **After Hours**: Can have AH extension, retest near highs in pre/open
- ✅ **Probability**: High EV mean reversion spot

**Trend Break**:
- ✅ **Importance**: "Point of no return for trend"
- ✅ **Rule**: Use hourly chart to draw trends
- ✅ **Validation**: Higher in range = better fade
- ✅ **Requirement**: 3 touches on trend (ideal, 2 is okay)

**Backside**:
- ✅ **Bias**: Short until main reversion point
- ✅ **Trades**: Short means or extremes (like uptrend but opposite)
- ✅ **Awareness**: HTF targets (deviation bands downside)
- ✅ **Rule**: Don't aggressively short at mean (nobody knows where it goes)

**Backside Reverted**:
- ✅ **Bias**: Short-biased (still on backside)
- ✅ **Aggression**: Don't aggressively short means anymore
- ✅ **Trades**: Euphoric setups, quality trend breaks

**Timeframe Hierarchy**:
- ✅ **HTF** (Daily, 4hr): Setup, bias, key levels
- ✅ **MTF** (1hr, 15m): Route start, route end, trend breaks, resets
- ✅ **LTF** (5m, 2m): Execution spots, entries, position management
- ✅ **Execution Hub**: 2-minute chart (fills and confirms entries)

**"In Play"** (Liquidity Requirement):
- ✅ **Definition**: Liquid stocks, heightened volume, heightened range
- ✅ **Importance**: Liquidity = trust in charts
- ✅ **Rule**: "When in doubt, make sure it has fucking volume"

**How She Uses Trend Cycle**:
- ✅ **Identifies Current Stage**: Determine where stock is in cycle
- ✅ **Applies Stage-Specific Rules**: Different rules for each stage
- ✅ **Prevents Bad Trades**: No longs in extreme deviation, no shorts in uptrend
- ✅ **Targets Next Stage**: Anticipates what comes next
- ✅ **Multi-Timeframe**: Validate stage across HTF/MTF/LTF

**Trend Stage Code Generation**:
```python
def detect_trend_stage(data, indicators):
    # Detect consolidation
    if is_consolidating(data):
        if detect_breakout(data, indicators):
            return 'UPTREND'

    # Check for uptrend
    if is_uptrend(data, indicators):
        # Check for extreme deviation
        if is_extreme_deviation(data, indicators):
            return 'EXTREME_DEVIATION'

        # Check for euphoric top
        if detect_euphoric_top(data, indicators):
            return 'EUPHORIC_TOP'

        return 'UPTREND'

    # Check for trend break
    if detect_trend_break(data, indicators):
        return 'TREND_BREAK'

    # Check for backside
    if is_backside(data, indicators):
        # Check for mean reversion
        if is_at_mean(data, indicators):
            return 'BACKSIDE_REVERTED'

        return 'BACKSIDE'

    return 'CONSOLIDATION'

def is_extreme_deviation(data, indicators):
    # Price at upper deviation band (1hr, 4hr, daily)
    return (data['close'] >= indicators['dev_upper_1hr'] and
            data['close'] >= indicators['dev_upper_4hr'] and
            data['close'] >= indicators['dev_upper_daily'])

def detect_euphoric_top(data, indicators):
    # Gap up + volume spike + extension
    # Outside of trend channel
    return (detect_gap_up(data) and
            volume_spike(data) and
            price_extended_from_trend(data, indicators))

def detect_trend_break(data, indicators):
    # Price closes below main trend line
    # Prefer higher breaks (better fades)
    # Minimum 3 touches preferred
    return trend_line_broken(data, indicators['main_trend'])
```

---

#### 14. V31 Code Examples & Patterns
**Source**: Codebase analysis, template library

**Renata Will Know**:
- ✅ Common V31 code patterns
- ✅ Parameter extraction examples
- ✅ Code transformation examples
- ✅ Anti-patterns to avoid
- ✅ Best practices

**How She Uses It**:
- Generates code following established patterns
- Refactors code to V31 standard
- Ensures consistency across codebase

---

### Knowledge Storage & Retrieval

**Storage**: Archon MCP Server (port 8051)
- **Vector embeddings**: All knowledge converted to embeddings
- **RAG Search**: Semantic search across all knowledge
- **Metadata tagging**: All knowledge tagged with type, domain, keywords
- **Version tracking**: Knowledge updates tracked over time

**Retrieval**:
- **Query**: User asks question or describes idea
- **Search**: Archon RAG finds relevant knowledge
- **Ranking**: Results ranked by relevance score
- **Context**: Top N results provided to AI as context

---

## 🤖 RENATA'S FIVE AI AGENTS

### Agent 1: PLANNER Agent (Sprint 4)
**Purpose**: Analyze A+ examples, extract parameters, create build plans

**Capabilities**:
1. **A+ Example Analysis**
   - Accept: Chart images, descriptions, parameter sets
   - Process: Visual analysis, pattern recognition, parameter extraction
   - Output: Structured breakdown with parameters

2. **Parameter Extraction**
   - Accept: Natural language descriptions, chat messages
   - Process: NLP processing, entity extraction, parameter mapping
   - Output: Structured parameter sets with ranges

3. **Mold Generation**
   - Accept: Parameter sets, setup type
   - Process: Parameterization, template matching, mold creation
   - Output: Reusable scanner molds

4. **Plan Creation**
   - Accept: User requirements, mold, research findings
   - Process: Phased planning, task breakdown, dependency mapping
   - Output: Build plan with human approval workflow

**User Workflow**:
```
User: "Here's an A+ example of a backside setup from today"

Renata [Planning Agent]:
  "I've analyzed your A+ example. Here's what I found:

  📊 Setup: Backside B Euphoric Top
  📈 Market Context: Gap up into resistance, euphoric top
  🔑 Key Parameters:
     - gap_over_atr: 0.8 (range: 0.7-1.2)
     - open_over_ema9: 0.92 (range: 0.85-0.98)
     - vol_mult: 1.2 (range: 1.0-1.5)

  📋 Build Plan:
     Phase 1: Generate V31 code (15 min)
     Phase 2: Validate V31 compliance (5 min)
     Phase 3: Test on historical data (10 min)
     Phase 4: Execute on current market (ongoing)

  Ready to proceed? [Approve] [Modify] [Reject]"
```

---

### Agent 2: RESEARCHER Agent (Sprint 5)
**Purpose**: Deep analysis, find similar strategies, market regime analysis

**Capabilities**:
1. **Archon RAG Deep Search**
   - Accept: Research query
   - Process: Query Archon knowledge base, retrieve V31/Lingua/strategies
   - Output: Comprehensive research findings with sources

2. **Similar Strategy Search**
   - Accept: Strategy description or code
   - Process: Semantic search across existing strategies
   - Output: Similar strategies with performance data

3. **Pattern Matching**
   - Accept: Setup description, parameters
   - Process: Cross-reference with Lingua setups
   - Output: Matching setups with historical performance

4. **Market Regime Analysis**
   - Accept: Date range, market conditions
   - Process: Analyze volatility, trend, volume patterns
   - Output: Regime classification with recommendations

5. **Parameter Suggestions**
   - Accept: Setup type, market conditions
   - Process: Historical analysis, success rate optimization
   - Output: Optimized parameter ranges

**User Workflow**:
```
User: "I want to build a backside scanner for gap ups"

Renata [Researcher Agent]:
  "I've searched our knowledge base and found:

  🔍 Similar Setups:
     1. Backside B Scanner (2024)
        - Success rate: 68%
        - Optimal parameters: gap_over_atr=0.85
        - Best timeframe: 15min
        - Total return: +24%

     2. Gap Continuation Setup (2023)
        - Success rate: 62%
        - Note: Better in volatile markets

  📊 Market Regime (Current):
     - Volatility: High (VIX > 20)
     - Trend: Bullish but extended
     - Recommendation: Tighten stops, reduce position size

  💡 Parameter Suggestions:
     - gap_over_atr: 0.8-0.9 (conservative)
     - Volume multiplier: 1.2-1.5 (current market)
     - Timeframe: 15min (most reliable)
     - Stop loss: 2 ATR (protect in volatile conditions)

  Ready to build with these parameters?"
```

---

### Agent 3: BUILDER Agent (Sprint 6)
**Purpose**: Generate ALL code types - scanners, backtests, execution, risk management

**Capabilities**:

**A. Scanner Code Generation**

1. **V31 Code from Ideas**
   - Accept: Natural language description
   - Process: Understand requirements → Select template → Generate code → Validate V31
   - Output: Complete V31 scanner code

2. **Non-V31 to V31 Transformation**
   - Accept: Legacy scanner code
   - Process: Parse code → Extract logic → Restructure to V31 → Validate
   - Output: Transformed V31 code

3. **A+ Mold to Scanner**
   - Accept: Parameter mold (from Planner)
   - Process: Fill in parameters → Generate code → Add V31 structure
   - Output: Executable V31 scanner

4. **Template Library Expansion**
   - Maintain library of V31 templates
   - Add new patterns as discovered
   - Organize by setup type

5. **V31 Validation**
   - Accept: Generated code
   - Process: Check V31 compliance → Report issues → Suggest fixes
   - Output: Validation report with fixes

**B. Backtest Code Generation**

6. **Backtesting.py Strategy Code**
   - Accept: Scanner code + execution rules
   - Process: Convert scanner → backtesting.py strategy → Add entry/exit logic
   - Output: Complete backtesting.py strategy

7. **VectorBT Vectorized Backtest**
   - Accept: Strategy logic
   - Process: Vectorize operations → Optimize for performance
   - Output: Fast vectorized backtest code

8. **Walk-Forward Analysis Code**
   - Process: Split data → Rolling optimization → Forward testing
   - Output: Walk-forward backtest framework

9. **Monte Carlo Simulation Code**
   - Accept: Backtest results
   - Process: Add randomness → Run 1000+ simulations → Calculate distributions
   - Output: Monte Carlo analysis code

10. **Parameter Optimization Code**
    - Accept: Strategy code + parameter ranges
    - Process: Grid search / genetic algorithm / Bayesian optimization
    - Output: Optimization script

**C. Execution Code Generation**

11. **Entry Order Generation**
    - Accept: Entry rules, order type preference
    - Process: Generate market/limit/stop order code → Add timing logic
    - Output: Entry execution module

12. **Exit Strategy Code**
    - Accept: Exit rules (profit target, stop loss, time-based)
    - Process: Generate exit logic → Add trailing stops if needed
    - Output: Exit execution module

13. **Position Sizing Algorithms**
    - Accept: Account size, risk tolerance, method
    - Process: Implement sizing (fixed, volatility-based, Kelly, percentage)
    - Output: Position sizing calculator

14. **Order Management System**
    - Accept: Entry/exit rules + position sizing
    - Process: Coordinate orders → Handle partial fills → Manage open positions
    - Output: Complete OMS code

**D. Risk Management Code Generation**

15. **Stop-Loss Systems**
    - Accept: Risk tolerance, method (ATR-based, structural, percentage)
    - Process: Generate stop-loss logic → Add trailing stop capability
    - Output: Risk management module

16. **Portfolio Risk Controls**
    - Accept: Max position size, max portfolio risk, correlation limits
    - Process: Implement portfolio-level constraints
    - Output: Portfolio risk manager

17. **Drawdown Protection**
    - Accept: Max drawdown threshold
    - Process: Monitor equity curve → Implement trading halt if exceeded
    - Output: Drawdown protection system

18. **Daily Loss Limits**
    - Accept: Daily loss threshold
    - Process: Track daily P&L → Stop trading if limit hit
    - Output: Daily risk limit enforcer

**E. Position Management Code Generation**

19. **Trade Management Logic**
    - Accept: Scale in/out rules, partial profit rules
    - Process: Implement position adjustments → Add breakeven stops
    - Output: Position management module

20. **Multi-Strategy Position Allocation**
    - Accept: Multiple strategies, capital allocation rules
    - Process: Distribute capital → Manage position interactions
    - Output: Portfolio position allocator

**User Workflow - Scanner**:
```
User: "Generate a backside scanner with these parameters"

Renata [Builder Agent]:
  "Generating V31 scanner...

  ✅ Code Structure:
     - Stage 1: Grouped endpoint (gap_over_atr > 0.8)
     - Stage 2: Per-ticker operations (5 patterns)
     - Stage 3: Aggregation (smart filters)

  ✅ Code Generated:
     ```python
     # V31 Gold Standard Scanner
     # Generated by: Renata Builder Agent

     def get_stage1_symbols():
         # Preliminary fetch logic
         ...
     ```

  ✅ V31 Validation:
     - ✅ 3-stage architecture: PASS
     - ✅ Per-ticker operations: PASS
     - ✅ Smart filters: PASS
     - ✅ Code structure: PASS

  Scanner ready! What's next?
  [→ Execute on /scan]  [→ Backtest first]"
```

**User Workflow - Execution Strategy**:
```
User: "I want to execute these signals with risk management"

Renata [Builder Agent]:
  "Building execution system...

  ✅ Position Sizing:
     Method: Volatility-based (ATR)
     Risk per trade: 1% of account
     Position size = (Account * Risk%) / (Entry_Price + Stop_Distance)

  ✅ Entry Orders:
     Type: Limit order (better fill)
     Timing: 9:45 AM EST (after open volatility)
     Validation: Confirm gap still intact

  ✅ Stop Loss:
     Method: ATR-based (2 * ATR below entry)
     Trailing: Yes (trails at 1.5 * ATR after +1R profit)

  ✅ Exit Strategy:
     Profit target: 2.5R (risk-reward ratio)
     Time exit: 3:30 PM (avoid close volatility)
     Partial profit: 50% at 1.5R, move rest to breakeven

  ✅ Code Generated:
     ```python
     # Execution Strategy - Backside B Setup
     # Generated by: Renata Builder Agent

     class BacksideBExecution:
         def calculate_position_size(self, account_size, atr):
             ...

         def generate_entry_order(self, signal):
             ...

         def calculate_stop_loss(self, entry_price, atr):
             ...
     ```

  Execution code ready! Ready to backtest with execution?
  [→ Backtest with execution]  [→ Adjust parameters]"
```

**User Workflow - Risk Management**:
```
User: "Add portfolio risk controls"

Renata [Builder Agent]:
  "Adding risk management...

  ✅ Portfolio-Level Controls:
     - Max open positions: 5
     - Max portfolio risk: 10% (2% per position * 5)
     - Correlation filter: Skip if >2 positions in same sector

  ✅ Daily Loss Limit:
     - Threshold: -$2,000 (2% of $100k account)
     - Action: Stop all new entries if hit
     - Notification: Alert user

  ✅ Drawdown Protection:
     - Max drawdown: 15% from peak
     - Action: Reduce position sizes by 50%
     - Recovery: Gradually restore as equity improves

  ✅ Risk Manager generated!

  Integrated with execution system.
  Ready for portfolio backtest?"
```

---

### Agent 4: EXECUTOR Agent (Sprint 7)
**Purpose**: Execute scanners, collect results, track progress

**Capabilities**:
1. **FastAPI Backend Execution**
   - Accept: Scanner code, scan date, parameters
   - Process: Submit to backend, queue execution, track progress
   - Output: Execution ID, real-time status updates

2. **Real-Time Progress Tracking**
   - WebSocket connection to backend
   - Progress updates every 1 second
   - Stage tracking (fetching, filtering, detecting, aggregating)
   - Error detection and reporting

3. **Result Collection**
   - Collect execution results from backend
   - Parse results (signals, metadata, performance metrics)
   - Format results for display

4. **Execution Queue Management**
   - Multiple executions queued
   - Priority handling
   - Concurrent execution limits

**User Workflow**:
```
User: "Execute this backtest scanner"

Renata [Executor Agent]:
  "🚀 Starting execution...

  📊 Execution Details:
     - Scanner: Backside B Scanner
     - Date: 2024-01-24
     - Tickers: 5000 symbols
     - Estimated time: 3 minutes

  ⏳ Progress:
     [████████░░] 80% - Stage 2: Per-ticker operations

  ⏱️ Elapsed: 2m 15s

  🔴 Found 12 signals so far...

  ✅ Execution complete!

  📈 Results:
     - Total signals: 47
     - Winners: 32 (68%)
     - Losers: 15 (32%)
     - Total return: +8.4%

  View full results?"
```

---

### Agent 5: ANALYST Agent (Sprint 8)
**Purpose**: Optimize strategies, analyze backtests, suggest improvements

**Capabilities**:
1. **Backtest Result Analysis**
   - Accept: Backtest results data
   - Process: Calculate metrics, identify patterns, analyze drawdowns
   - Output: Comprehensive analysis report

2. **IS/OOS Validation**
   - Accept: Backtest results, date ranges
   - Process: Split data into in-sample and out-of-sample
   - Output: Overfitting analysis, robustness metrics

3. **Monte Carlo Simulation**
   - Accept: Strategy results
   - Process: Run 1000+ simulations with random noise
   - Output: Distribution of returns, confidence intervals

4. **Regime Analysis**
   - Accept: Backtest results by date
   - Process: Group by market regime (bull, bear, volatile)
   - Output: Performance by regime, regime-specific recommendations

5. **Parameter Optimization**
   - Accept: Strategy code, backtest results
   - Process: Grid search, genetic algorithms, or Bayesian optimization
   - Output: Optimized parameter sets

**User Workflow**:
```
User: "Analyze my backtest results"

Renata [Analyst Agent]:
  "📊 BACKTEST ANALYSIS REPORT

  📈 Overall Performance:
     - Total Return: +24.8%
     - Sharpe Ratio: 1.85
     - Sortino Ratio: 2.12
     - Max Drawdown: -12.3%

  ✅ IS/OOS Validation:
     - In-Sample (Jan-Sep): +28.5%
     - Out-of-Sample (Oct-Dec): +18.2%
     - Overfitting Risk: LOW
     - Robustness Score: 8.2/10

  🎲 Monte Carlo Simulation (1000 runs):
     - Mean Return: +24.1%
     - 95% CI: [+18.2%, +30.0%]
     - Probability of Loss: 12%

  📊 Regime Analysis:
     - Bull Markets: +32.4% (best performance)
     - Bear Markets: -8.2% (drawdown acceptable)
     - Volatile Markets: +15.6%

  💡 Optimization Suggestions:
     1. Increase gap_over_atr to 0.9 (improves win rate)
     2. Add max position size limit (reduces drawdown)
     3. Skip low-volume days (reduces slippage)

  Would you like me to apply these optimizations?"
```

---

## 🤝 AGENT COLLABORATION SYSTEM

### How Agents Work Together

**Orchestration Model**: Renata uses a central orchestrator that coordinates agents based on workflow stage. Agents don't work in isolation - they collaborate, share context, and hand off seamlessly.

**Collaboration Patterns**:

**Pattern 1: Sequential Workflow (Idea → Scanner)**
```
User: "Build a backside scanner"

1. PLANNING Agent → Analyzes request, extracts parameters
   ↓ Handoff: Parameter mold
2. RESEARCHER Agent → Searches Archon for similar setups, suggests optimal parameters
   ↓ Handoff: Refined parameters + research findings
3. BUILDER Agent → Generates V31 code with optimized parameters
   ↓ Handoff: Scanner code
4. EXECUTOR Agent (Analyzer Mode) → Runs A+ example analyzer
   ↓ Handoff: Validation results
5. USER → Reviews validation, approves backtest
   ↓ Handoff: User approval
6. EXECUTOR Agent → Runs full backtest
   ↓ Handoff: Backtest results
7. ANALYST Agent → Analyzes results, suggests improvements
   ↓ Loop back to Builder if user wants changes
```

**Pattern 2: Parallel Research + Building**
```
User: "Build this and optimize it"

PLANNING Agent → Creates plan
   ↓
   ├─→ RESEARCHER Agent (parallel) → Archon RAG search
   │     ↓
   │  Returns: Optimal parameters, similar strategies
   │
   └─→ BUILDER Agent (parallel) → Generates initial code
         ↓
      Returns: Draft scanner code

ORCHESTRATOR → Merges research + code
   ↓
BUILDER Agent → Refines code with research insights
   ↓
Complete: Optimized scanner
```

**Pattern 3: Agent Handoff with Context Preservation**
```
RESEARCHER Agent: "Found similar setup with 68% win rate"
  ↓ Context Handoff
BUILDER Agent: "Using parameters from Researcher (gap_over_atr=0.85)..."
  ↓ Context Handoff
EXECUTOR Agent: "Executing scanner with Researcher-suggested parameters..."
  ↓ Context Handoff
ANALYST Agent: "Results show 72% win rate, better than Researcher's similar setup (68%)"
```

**Pattern 4: Multi-Agent Problem Solving**
```
User: "Backtest failed, what's wrong?"

ORCHESTRATOR: Coordinates diagnostic workflow

ANALYST Agent: "Results show 0 signals - scanner too restrictive"
  ↓ Suggests parameter relaxation
RESEARCHER Agent: "Confirms - historical similar setups use wider ranges"
  ↓ Provides optimal ranges
BUILDER Agent: "Adjusts parameters based on Researcher recommendations"
  ↓ Generates updated code
EXECUTOR Agent: "Re-runs backtest with relaxed parameters"
  ↓
USER: "Results look great!"
```

**Context Sharing Mechanisms**:

1. **Shared Project State**
   - All agents see: Current project, chat history, scanner code, parameters
   - Maintained by: Orchestrator in project context
   - Updates: Real-time sync when agents make changes

2. **Agent Communication Messages**
   - Structured handoffs: "AGENT → AGENT: [context summary]"
   - Key info transferred: Parameters, decisions, recommendations
   - Avoids: Information loss between agent handoffs

3. **Archon Knowledge Access**
   - All agents can: Query Archon for relevant knowledge
   - RAG optimization: Each agent gets domain-specific context
   - Shared knowledge base: Avoids duplicate research

4. **User Feedback Loop**
   - Agents can: Ask user clarifying questions
   - User responses: Incorporated into all future agent actions
   - Continuous refinement: Agents learn user preferences

**Collaboration Examples**:

**Example 1: Building from A+ Example**
```
PLANNING: "A+ analysis complete - gap_up_atr=1.2, top_reversal=true"
  ↓ Handoff
RESEARCHER: "Searching Archon for similar gap setups..."
          "Found: Gap continuation (68% win rate) uses gap_up_atr=0.8-1.0"
          "Recommend: Widen range to capture more opportunities"
  ↓ Handoff
BUILDER: "Generating scanner with Researcher's suggested range (0.8-1.2)..."
       "Code generated with A+ parameters + Researcher optimizations"
  ↓ Handoff
EXECUTOR: "Running A+ analyzer to validate capture..."
         "✅ A+ example captured!"
  ↓ Handoff
ANALYST: "Quick 30-day backtest shows: 47 signals, 68% win rate"
        "Matches Researcher's prediction (68%)"
  ↓
USER: "Perfect, run full backtest"
```

**Example 2: Optimization Loop**
```
USER: "Win rate too low (45%), optimize this"

ANALYST: "Analyzing results..."
       "Issue: Too many false signals in choppy markets"
       "Recommendation: Add trend filter"
  ↓ Handoff
RESEARCHER: "Searching Archon for trend filter methods..."
          "Best practice: EMA cloud filter, HTF trend confirmation"
          "Similar setups: Use EMA9 > EMA21 for uptrend bias"
  ↓ Handoff
BUILDER: "Adding trend filter to scanner..."
       "Added: Check EMA9 > EMA21 (HTF uptrend required)"
       "Added: Skip if ADX < 20 (no trend = no trade)"
  ↓ Handoff
EXECUTOR: "Re-running backtest with trend filter..."
         "Results: 32 signals (down from 67), 72% win rate (up from 45%)"
  ↓ Handoff
ANALYST: "Analysis: Sharpe improved from 0.8 to 1.6"
        "Trade-off: Fewer signals but higher quality"
        "Recommendation: APPROVE for production"
```

**Agent Collaboration Benefits**:
- ✅ **No silos**: Agents share knowledge and context
- ✅ **Better decisions**: Multiple perspectives (research + building + analysis)
- ✅ **Faster iteration**: Parallel processing where possible
- ✅ **Continuous improvement**: Each agent builds on previous work
- ✅ **User-friendly**: Seamless experience, no manual handoffs

---

## 🧠 RAG CONTEXT OPTIMIZATION SYSTEM

### How Archon RAG Powers All Agents

**Core Principle**: Archon isn't just a knowledge base - it's an **active intelligence layer** that optimizes every agent's context in real-time.

**RAG Optimization Flow**:
```
AGENT REQUEST
    ↓
"Find knowledge about backside B setups"
    ↓
ARCHON RAG ENGINE
    ├─→ Query understanding
    ├─→ Vector similarity search
    ├─→ Domain-specific filtering
    ├─→ Relevance ranking
    ├─→ Context window optimization
    └─→ RETURN: Top 5 most relevant knowledge chunks
    ↓
AGENT USES OPTIMIZED CONTEXT
    ↓
BETTER DECISIONS + FASTER RESPONSES
```

**Domain-Specific RAG Queries**:

**PLANNING Agent RAG Queries**:
- "A+ examples with gap setups" → Returns: Chart examples, parameter sets
- "Parameter extraction patterns for [setup]" → Returns: Similar parameter molds
- "Best practices for analyzing charts" → Returns: Analysis frameworks
- **Context**: Chart analysis, pattern recognition, parameter extraction

**RESEARCHER Agent RAG Queries**:
- "Similar strategies to [description]" → Returns: Matching strategies with performance
- "Optimal parameters for [setup] in [market regime]" → Returns: Historical parameter performance
- "Lingua trading setups: [setup type]" → Returns: Setup definitions, examples
- "Market regime analysis: [date range]" → Returns: Volatility, trend data
- **Context**: Historical strategies, performance data, market conditions

**BUILDER Agent RAG Queries**:
- "V31 code templates: [setup type]" → Returns: Relevant code templates
- "Transformation rules: [non-V31 pattern]" → Returns: V31 transformation examples
- "Best practices: [code component]" → Returns: Code patterns, anti-patterns
- "Library usage: [function name]" → Returns: TA-Lib, Polygon API examples
- **Context**: Code patterns, V31 compliance, library usage

**EXECUTOR Agent RAG Queries**:
- "Execution patterns: [strategy type]" → Returns: Order entry logic
- "Risk management: [setup]" → Returns: Stop-loss, position sizing strategies
- "Backtest framework: [requirement]" → Returns: backtesting.py examples
- "Error handling: [error type]" → Returns: Troubleshooting guides
- **Context**: Execution logic, risk management, debugging

**ANALYST Agent RAG Queries**:
- "Performance metrics calculation" → Returns: Sharpe, drawdown formulas
- "Regime analysis methods" → Returns: Bull/bear/volatile classification
- "Optimization techniques" → Returns: Grid search, genetic algorithms
- "Robustness validation" → Returns: IS/OOS, Monte Carlo methods
- **Context**: Statistical analysis, performance evaluation, optimization

**RAG Optimization Techniques**:

1. **Semantic Search** (not just keyword matching)
   - Understands meaning: "gap up setup" ≈ "gap continuation" ≈ "gap and go"
   - Conceptual similarity: Finds related ideas even with different words

2. **Domain Filtering**
   - Planning agent only gets: A+ examples, parameter molds
   - Researcher agent only gets: Strategies, performance data, Lingua setups
   - Builder agent only gets: Code templates, V31 patterns, libraries
   - Prevents: Information overload

3. **Relevance Ranking**
   - Top results: Most semantically similar + domain-appropriate
   - Diversity: Include different perspectives (e.g., bullish + bearish examples)
   - Recency: Weight recent knowledge higher

4. **Context Window Management**
   - Limit: Top 5-10 knowledge chunks per query (fits in AI context)
   - Prioritization: Most relevant chunks first
   - Truncation: Cut less relevant sections if too long

5. **Query Expansion**
   - User query: "backside scanner"
   - Expanded: "backside scanner" + "gap down setup" + "trend reversal"
   - Broader search: Finds more relevant knowledge

6. **Caching & Performance**
   - Cache frequent queries: Similar strategies, common setups
   - Pre-load: V31 Gold Standard, Lingua Framework (always relevant)
   - Speed: <2 second response time for most queries

**Archon Knowledge Base Structure**:

```
ARCHON KNOWLEDGE GRAPH
├─→ V31 Gold Standard (950+ lines)
│   ├─→ 3-stage architecture
│   ├─→ Market scanning pillar (12k tickers)
│   ├─→ Per-ticker operations
│   └─→ Code patterns & templates
│
├─→ Lingua Trading Framework (772 lines)
│   ├─→ Trend cycle (9 stages)
│   ├─→ Timeframe hierarchy
│   ├─→ 13 trading setups
│   └─→ Indicator definitions
│
├─→ Systematized Strategies (4 scanners)
│   ├─→ OS D1 (gap setup)
│   ├─→ G2G S1 (gap continuation)
│   ├─→ SC DMR (multi-pattern)
│   └─→ SC MDR Swing
│
├─→ A+ Example Catalog
│   ├─→ Chart examples with parameters
│   ├─→ Market regime context
│   └─→ Performance data
│
├─→ Libraries & Tools
│   ├─→ Polygon API (market data)
│   ├─→ TA-Lib (indicators)
│   ├─→ backtesting.py (backtesting)
│   └─→ Python stack (pandas, numpy, scipy)
│
└─→ Trading Concepts
    ├─→ Profitable trading principles
    ├─→ Quantitative trading methods
    ├─→ Systematic trading framework
    ├─→ Execution strategies
    └─→ Risk management
```

**How RAG Optimizes Agent Performance**:

**Without RAG Optimization**:
```
AGENT: "Generate backside scanner"
  → Generic code generation
  → No historical context
  → Suboptimal parameters
  → Lower win rate
```

**With RAG Optimization**:
```
AGENT: "Generate backside scanner"
  → Archon RAG: Finds similar backside strategies
  → Archon RAG: Retrieves optimal parameters (68% win rate)
  → Archon RAG: Shows V31 template for gap setups
  → Agent uses: Optimized code + proven parameters
  → Result: Higher win rate, faster development
```

**RAG Success Metrics**:
- ✅ **Query speed**: <2 seconds for 95% of queries
- ✅ **Relevance**: Top 5 results contain answer for 90% of queries
- ✅ **Agent performance**: RAG-assisted agents perform 30% better (measured by user satisfaction)
- ✅ **Knowledge utilization**: 85% of Archon knowledge accessed by agents (not sitting unused)

**Continuous RAG Improvement**:
- **Query logging**: Track what agents ask, what results they use
- **Feedback loop**: Agents rate RAG result quality
- **Knowledge updates**: New strategies, examples, patterns ingested regularly
- **Search optimization**: Improve relevance ranking based on usage patterns

**Bottom Line**: Archon RAG is not a passive database - it's an **active intelligence layer** that ensures every agent has the right knowledge at the right time to make optimal decisions.

---

## 🔄 USER WORKFLOWS

### Workflow 1: Idea → Scanner (Primary)

**Steps**:
1. User has trading idea (natural language)
2. Go to `/plan` page
3. Chat with Renata: "I want a scanner for [idea description]"
4. **Planning Agent**: Analyzes, breaks down into parameters
5. **Researcher Agent**: Finds similar setups, suggests parameters
6. **Builder Agent**: Generates V31 code
7. Renata presents: Scanner ready!
8. User clicks: [→ Send to /scan]
9. Scanner loads on /scan page
10. User executes on /scan page
11. **Executor Agent**: Runs scan, collects results
12. **Analyst Agent**: Analyzes results, suggests optimizations
13. User reviews results, refinements if needed

**Time**: 10-15 minutes (vs 2-3 hours manual)

---

### Workflow 2: A+ Example → Scanner (Advanced)

**Steps**:
1. User has A+ chart example (image or breakdown)
2. Go to `/plan` page
3. Upload/chart A+ example
4. **Planning Agent**: Analyzes chart, extracts parameters
5. **Researcher Agent**: Finds similar examples in database
6. **Builder Agent**: Generates scanner from mold
7. **Executor Agent**: Backtests to validate
8. **Analyst Agent**: Compares to A+ example performance
9. Renata presents: Scanner validated!
10. User approves: [→ Send to /scan]

**Time**: 15-20 minutes (vs 4-6 hours manual)

---

### Workflow 3: Legacy Code → V31 (Transformation)

**Steps**:
1. User has old scanner code (non-V31)
2. Can go to `/plan`, `/scan`, or `/backtest`
3. Click [🧠 Renata] button (sidebar)
4. Chat: "Transform this to V31:" [paste code]
5. **Builder Agent**: Transforms code to V31
6. Renata presents: V21 code ready!
7. User reviews transformed code
8. User approves execution

**Time**: 5-10 minutes (vs 1-2 hours manual)

---

### Workflow 4: Optimization Loop (Iterative)

**Steps**:
1. User has running strategy (on /scan or /backtest)
2. Click [🧠 Renata] button
3. Chat: "Optimize my parameters"
4. **Analyst Agent**: Analyzes current performance
5. **Researcher Agent**: Suggests parameter improvements
6. User: "Apply these changes"
7. **Builder Agent**: Generates updated scanner
8. **Executor Agent**: Backtests new version
9. **Analyst Agent**: Compares old vs new
10. Rinse and repeat until satisfied

**Time**: 20-30 minutes per iteration

---

## ✏️ EDITING & ADJUSTMENT SYSTEM

### Robust Modification Capabilities

**Philosophy**: Building is step 1. Refining is steps 2-100. Renata provides **powerful, flexible editing capabilities** for both scans and backtests.

**Editing Scopes**:

**A. Scanner Code Editing**

1. **Parameter Adjustment**
   - **What**: Change parameter values, ranges, defaults
   - **How**: Chat: "Increase gap_over_atr from 0.8 to 0.9"
   - **Agent**: BUILDER updates parameters, preserves all other code
   - **Validation**: Quick analyzer run to confirm changes work
   - **Example**:
     ```
     User: "Tighten the gap threshold, too many false signals"

     Renata [Builder Agent]:
       "Adjusting gap_over_atr:
        - Old: 0.8 (67 signals, 45% win rate)
        - New: 0.95 (32 signals, 72% win rate)

       Code updated. Running quick analyzer...

       ✅ Results: Higher quality signals, win rate improved to 72%

       Ready to backtest?"
     ```

2. **Logic Modification**
   - **What**: Change detection rules, add/remove filters, modify conditions
   - **How**: Chat: "Add EMA cloud filter for uptrend only"
   - **Agent**: BUILDER understands intent, modifies code structure
   - **Validation**: Analyze on A+ example to confirm still captures
   - **Example**:
     ```
     User: "Only trade in uptrending markets"

     Renata [Builder Agent]:
       "Adding trend filter:
        - New condition: EMA9 > EMA21 (HTF uptrend required)
        - Modified: Stage 1 pre-filter (faster rejection)
        - Preserved: All existing logic

       Code structure:
       ```
       def get_stage1_symbols():
           # Existing gap filter
           if gap_over_atr < 0.8: return False

           # NEW: Trend filter
           if not check_ema_cloud_bullish(): return False

           return True
       ```

       Quick analyzer: ✅ Still captures A+ examples (they were in uptrend)

       Ready?"
     ```

3. **Pattern Addition/Removal**
   - **What**: Add new detection patterns, remove unused ones
   - **How**: Chat: "Add trailing stop pattern" or "Remove pattern 3"
   - **Agent**: BUILDER modifies Stage 2 per-ticker operations
   - **Validation**: Quick backtest to compare old vs new
   - **Example**:
     ```
     User: "Remove the weak pattern 3, it's dragging down win rate"

     Renata [Analyst Agent]:
       "Analyzing pattern performance:
        - Pattern 1: 78% win rate (keep)
        - Pattern 2: 65% win rate (keep)
        - Pattern 3: 42% win rate (weak - you're right)"

     Renata [Builder Agent]:
       "Removing pattern 3...
        - Deleted: pattern_3_backside_weak()
        - Updated: Smart filters (removed pattern 3 references)
        - Preserved: Patterns 1 and 2

       Quick backtest comparison:
        - Old (3 patterns): 67 signals, 58% win rate
        - New (2 patterns): 41 signals, 72% win rate

       Better! Ready to commit?"
     ```

4. **Code Refactoring**
   - **What**: Improve code structure, performance, readability
   - **How**: Chat: "Optimize this code for speed" or "Make it more readable"
   - **Agent**: BUILDER refactors while preserving logic
   - **Validation**: V31 compliance check + quick analyzer
   - **Example**:
     ```
     User: "This scan is slow, optimize it"

     Renata [Builder Agent]:
       "Analyzing performance bottlenecks:
        - Issue: Repeated Polygon API calls in Stage 2
        - Fix: Batch fetch in Stage 1, cache for Stage 2

       Refactored code:
       ```
       # OLD: Slow (5000 API calls)
       for ticker in tickers:
           data = fetch_polygon_data(ticker)  # Individual call

       # NEW: Fast (1 batch call)
       all_data = fetch_polygon_batch(tickers)  # Single call
       for ticker in tickers:
           data = all_data[ticker]  # From cache
       ```

       Speed improvement: ~10x faster (5min → 30sec)

       V31 validation: ✅ Still compliant"
     ```

**B. Backtest Editing**

1. **Date Range Adjustment**
   - **What**: Change backtest period, add IS/OOS split
   - **How**: Chat: "Backtest from Jan to Jun 2024" or "Add IS/OOS validation"
   - **Agent**: EXECUTOR reruns backtest with new parameters
   - **Validation**: Compare results across different periods
   - **Example**:
     ```
     User: "How did this perform in 2023?"

     Renata [Executor Agent]:
       "Running backtest for 2023...
        - Date range: 2023-01-01 to 2023-12-31
        - Signals: 156 (vs 47 in 2024)
        - Win rate: 71% (vs 68% in 2024)

       2023 was better! More volatile = more opportunities."
     ```

2. **Execution Rules Editing**
   - **What**: Modify entry/exit logic, position sizing, stop-loss
   - **How**: Chat: "Add trailing stop" or "Change to limit orders"
   - **Agent**: BUILDER updates execution code, EXECUTOR reruns backtest
   - **Validation**: Compare backtest results with/without changes
   - **Example**:
     ```
     User: "Add trailing stop, I'm giving back too much profit"

     Renata [Builder Agent]:
       "Adding trailing stop:
        - Trigger: After +1R profit
        - Trail distance: 1.5 * ATR
        - Floor: Breakeven (never go below entry)"

     Renata [Executor Agent]:
       "Re-running backtest with trailing stop...
        - Old: Fixed stop at -2R
        - New: Trailing stop after +1R

       Results:
        - Win rate: 68% → 71% (stopped out less)
        - Average win: +2.8R → +3.2R (held winners longer)
        - Total return: +24% → +31%

       Trailing stop helps! Ready to deploy?"
     ```

3. **Risk Parameter Adjustment**
   - **What**: Change position sizing, stop-loss, max drawdown
   - **How**: Chat: "Reduce risk to 1% per trade"
   - **Agent**: BUILDER updates risk management code
   - **Validation**: Monte Carlo simulation to ensure robustness
   - **Example**:
     ```
     User: "Too much volatility, reduce risk"

     Renata [Builder Agent]:
       "Adjusting risk parameters:
        - Old: 2% per trade, 3R stop loss
        - New: 1% per trade, 2R stop loss

       Position size calculation:
       ```
       # OLD: 2% risk, 3R stop
       shares = (account * 0.02) / (entry - stop)

       # NEW: 1% risk, 2R stop
       shares = (account * 0.01) / (entry - stop)
       ```

     Renata [Analyst Agent]:
       "Risk analysis (Monte Carlo, 1000 runs):
        - Max drawdown: -18% → -9% (cut in half)
        - Average return: +24% → +18% (lower but smoother)
        - Sharpe ratio: 1.6 → 1.9 (better risk-adjusted)

       Lower risk = more consistent performance."
     ```

**C. Iterative Refinement Workflows**

**Workflow 1: Parameter Optimization Loop**
```
User: "Optimize these parameters"

Renata [Analyst Agent]:
  "Running parameter grid search..."

  "Results (sorted by Sharpe ratio):
   ┌─────────────┬──────┬─────────┬────────┐
   │ gap_over_atr│ Win% │ Sharpe │ Return │
   ├─────────────┼──────┼─────────┼────────┤
   │ 0.85        │ 74%  │ 1.95   │ +26%   │ ← BEST
   │ 0.80        │ 68%  │ 1.85   │ +24%   │ ← CURRENT
   │ 0.90        │ 71%  │ 1.82   │ +23%   │
   │ 0.75        │ 62%  │ 1.65   │ +21%   │
   └─────────────┴──────┴─────────┴────────┘

  Recommendation: gap_over_atr=0.85 (slightly tighter)

  Apply this optimization?"

User: "Yes"

Renata [Builder Agent]:
  "Updating scanner code...
   gap_over_atr = 0.85  # Optimized for Sharpe ratio

  Running quick validation..."

Renata [Executor Agent]:
  "Quick 30-day backtest with new params:
   - Signals: 41 (vs 47 with old params)
   - Win rate: 74% (vs 68%)
   - Sharpe: 1.95 (vs 1.85)

  ✅ Improvement confirmed! Ready to commit?"
```

**Workflow 2: A/B Testing**
```
User: "I want to test two versions side-by-side"

Renata [Builder Agent]:
  "Creating Version A and Version B...

   Version A (Current):
   - gap_over_atr = 0.8
   - No trend filter

   Version B (Proposed):
   - gap_over_atr = 0.9
   - EMA cloud trend filter"

Renata [Executor Agent]:
  "Running A/B test on same data period (2024-01-01 to 2024-03-31)...

   ┌──────────┬─────────┬─────────┬──────────┬─────────┐
   │          │ Signals │ Win Rate│ Sharpe   │ Return  │
   ├──────────┼─────────┼─────────┼──────────┼─────────┤
   │ Version A│   67    │  58%    │  1.45    │ +18%    │
   │ Version B│   32    │  74%    │  1.92    │ +22%    │
   └──────────┴─────────┴─────────┴──────────┴─────────┘

   Version B wins: Higher quality signals, better risk-adjusted return.

   Switch to Version B?"

User: "Yes, use Version B"

Renata [Builder Agent]:
  "Version B is now the active scanner.

   Version A saved to history (can revert if needed)."
```

**D. Undo/Redo & Version Control**

1. **Automatic Versioning**
   - Every edit creates automatic version snapshot
   - Versions stored in project history
   - User can revert to any previous version

2. **Change Tracking**
   - Diff view: "Here's what changed" (old vs new code)
   - Performance comparison: "Here's how results changed"
   - User approval: "Apply this change?" or "Revert"

3. **Revert Capability**
   - Chat: "Revert to version from yesterday"
   - Agent: Restores previous code + parameters
   - Validation: Confirm revert works correctly

**Editing Success Metrics**:
- ✅ **Speed**: Most edits applied and validated in <30 seconds
- ✅ **Accuracy**: 95%+ of edits work correctly (no bugs introduced)
- ✅ **Validation**: Every edit validated with quick analyzer/backtest
- ✅ **User confidence**: Easy to experiment (can always revert)

**Bottom Line**: Renata's editing system makes refinement **fast, safe, and iterative**. Users can experiment freely, knowing they can always revert and see the impact of every change.

---

## 🔗 PAGE INTERLINKING SYSTEM

### Efficient Navigation Between /plan, /scan, and /backtest

**Philosophy**: Users shouldn't have to think about "which page does what". Pages are **interconnected workspaces** that flow seamlessly into each other.

**Page Definitions**:

**/plan (Dedicated Renata Workspace)**
- **Purpose**: Deep planning, building, and strategy development
- **Features**: Full-width chat, project management, A+ example analysis
- **When to use**: Starting new strategies, major refinements, A+ example work

**/scan (Market Scanner Execution)**
- **Purpose**: Real-time scanning, signal discovery, chart analysis
- **Features**: EdgeChart, scanner results, symbol/timeframe controls
- **When to use**: Executing scanners, viewing current market signals

**/backtest (Backtest Engine)**
- **Purpose**: Historical validation, performance analysis, optimization
- **Features**: Backtest chart, equity curve, trade list, metrics
- **When to use**: Validating strategies, analyzing performance, optimization

**Interlinking Flows**:

**Flow 1: Plan → Scan (Primary Workflow)**
```
User on /plan page:
  1. Chat with Renata: "Build a backside scanner"
  2. Builder Agent generates scanner
  3. Executor Agent runs A+ analyzer ✅
  4. Quick backtest looks good
  5. User clicks: [→ Send to /scan]

Navigation:
  - Redirect: /plan → /scan
  - Scanner auto-loaded: Code populated in /scan workspace
  - Projects synced: Active project shows on /scan sidebar
  - Chat preserved: Can click [🧠 Renata] to continue conversation

User on /scan page:
  - Scanner ready to execute
  - Click [Execute Scanner]
  - View results on EdgeChart
  - Need refinement? Click [🧠 Renata] → Sidebar opens for quick help
```

**Flow 2: Scan → Plan (Refinement Workflow)**
```
User on /scan page:
  1. Executing scanner, viewing results
  2. Notice: "Too many false signals"
  3. Click: [🧠 Renata] button (top-right)
  4. Sidebar opens (480px wide, slides from right)

Renata Sidebar:
  User: "Help me optimize this scanner"
  Renata: "I see the issue - gap threshold too loose.
           Suggest: gap_over_atr from 0.7 to 0.9.
           Shall I update the scanner?"

  User: "Yes"

  Renata [Builder]: "Scanner updated. Want to test on /plan or here?"

  User: "Go to /plan"

  Click: [→ Edit on /plan]

Navigation:
  - Redirect: /scan → /plan
  - Context preserved: Scanner code, chat history, parameters
  - Full workspace: Can do deeper analysis and refinement

User on /plan page:
  - Full chat interface (not cramped sidebar)
  - Run comprehensive backtest
  - A/B test different versions
  - When satisfied: [→ Send to /scan] to execute
```

**Flow 3: Plan → Backtest (Validation Workflow)**
```
User on /plan page:
  1. Built scanner, ran quick analyzer
  2. Want: Comprehensive validation
  3. Click: [→ Send to /backtest]

Navigation:
  - Redirect: /plan → /backtest
  - Scanner auto-loaded: Backtest configured with scanner code
  - Date range picker: Select validation period
  - Click: [Run Backtest]

User on /backtest page:
  - View equity curve, performance metrics
  - Analyze trade list
  - Click [🧠 Renata] for analysis suggestions
```

**Flow 4: Backtest → Scan (Production Workflow)**
```
User on /backtest page:
  1. Validated strategy (Sharpe 1.85, +24% return)
  2. Satisfied with results
  3. Click: [→ Deploy to /scan]

Navigation:
  - Redirect: /backtest → /scan
  - Scanner loaded: Production-ready version
  - Status: "Validated ✅" badge on scanner
  - Ready: Execute on current market data

User on /scan page:
  - Execute scanner on today's market
  - View live signals
  - Monitor performance in real-time
```

**Flow 5: Any Page → Sidebar (Quick Help)**
```
User on /scan or /backtest:
  - Need quick help
  - Click: [🧠 Renata] button (top-right, always visible)
  - Sidebar: Slides in from right (480px wide)

Sidebar Features:
  - Full chat functionality
  - Current project context loaded
  - Quick questions, quick answers
  - Don't need to navigate to /plan
  - Close sidebar when done

Example:
  User (on /scan): "How do I interpret this signal?"
  Renata (sidebar): "This signal shows:
   - Gap up: +1.3% (strong)
   - Euphoric top: RSI 71
   - Volume: 2.1x average (confirmed)

   Quality score: 8.5/10
   Suggested action: Enter at limit, stop at -2R"
```

**Navigation UI Elements**:

**On /plan Page**:
```
┌─────────────────────────────────────────────────────────┐
│ [📋 Back to /scan] [📊 Back to /backtest] │ [Settings] │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  MAIN CHAT AREA                                         │
│  ...                                                     │
│                                                           │
│  [→ Send to /scan] [→ Send to /backtest]               │
└─────────────────────────────────────────────────────────┘
```

**On /scan Page**:
```
┌─────────────────────────────────────────────────────────┐
│ [📋 Projects] │ [🧠 Renata] │ [📊 Backtests] │ [Settings]│
├─────────────────────────────────────────────────────────┤
│  LEFT: Projects │ MAIN: Chart & Results                 │
│                  │ [Execute Scanner]                     │
└─────────────────────────────────────────────────────────┘
```

**On /backtest Page**:
```
┌─────────────────────────────────────────────────────────┐
│ [📋 Projects] │ [🧠 Renata] │ [📊 Backtests] │ [Settings]│
├─────────────────────────────────────────────────────────┤
│  LEFT: Backtests │ MAIN: Chart & Results                │
│                   │ [Run Backtest]                       │
└─────────────────────────────────────────────────────────┘
```

**Context Preservation Rules**:

1. **Project State Sync**
   - Active project: Synced across all pages
   - Chat history: Same conversation, different view
   - Scanner code: Latest version always available

2. **Handoff Data**
   - /plan → /scan: Scanner code + parameters + validation status
   - /plan → /backtest: Scanner code + date range suggestions
   - /scan → /plan: Current scanner + execution results
   - /backtest → /scan: Validated scanner + deployment ready

3. **URL State Management**
   - `/plan?project=backside-b-scanner`
   - `/scan?project=backside-b-scanner&symbol=SPY`
   - `/backtest?project=backside-b-scanner&date=2024-01-15`

4. **Back Button Behavior**
   - Browser back: Returns to previous page with state
   - Breadcrumb navigation: "Plan → Scan → Backtest"
   - Quick jump: Dropdown to switch pages directly

**User Experience Benefits**:
- ✅ **No lost context**: Projects, chats, code sync across pages
- ✅ **Fast navigation**: One click to switch between workspaces
- ✅ **Flexible workflow**: Start on any page, go to any page
- ✅ **Right tool for job**: /plan for building, /scan for executing, /backtest for validating
- ✅ **Sidebar always available**: Quick help without leaving current page

**Bottom Line**: Pages are **interconnected workspaces**, not isolated silos. Users flow seamlessly between planning, execution, and validation without losing context or repeating work.

---

## 🏗️ TECHNICAL INFRASTRUCTURE

### Frontend Components

#### 1. CopilotKit v1.50 Integration
**File**: `/src/app/api/copilotkit/route.ts`
**Purpose**: AI chat runtime
**Provider**: OpenRouter (anthropic/claude-sonnet-4-5-20250514)
**API Key**: `OPENROUTER_API_KEY` from `.env`

**Features**:
- Multi-agent coordination
- AG-UI protocol (tool calls)
- Streaming responses
- Context management
- Chat history

#### 2. Renata UI Components
**Location**: `/src/components/renata/`

**Components**:
- **RenataV2Chat** (68KB): Main chat interface (to be replaced with Traderra clone)
- **RenataSidebar**: Fixed sidebar container
- **ChatHistorySidebar**: Conversation history dropdown
- **ProjectSelector**: Project and conversation management

#### 3. Pages
**Location**: `/src/app/`

**Pages**:
- `/plan/page.tsx` (NEW): Dedicated Renata workspace
- `/scan/page.tsx` (EXISTING): + sidebar button
- `/backtest/page.tsx` (EXISTING): + sidebar button

---

### Backend Services

#### 1. FastAPI Backend
**File**: `/projects/edge-dev-main/backend/main.py`
**Port**: 8000
**Purpose**: Scanner execution, backtesting, data management

**API Endpoints**:
- `POST /api/scan/execute` - Execute scanner
- `GET /api/scan/status/{executionId}` - Get execution status
- `GET /api/scan/results/{executionId}` - Get execution results
- `POST /api/backtest/run` - Run backtest
- `GET /api/backtest/results/{backtestId}` - Get backtest results

#### 2. Archon MCP Server
**Port**: 8051
**Purpose**: Knowledge graph, RAG search, project management

**Features**:
- Knowledge ingestion (V31, Lingua, strategies, examples)
- RAG semantic search
- Project and task tracking
- Code example search
- Metadata management

#### 3. Data Sources
**Polygon API**:
- Real-time and historical market data
- OHLCV candles
- Volume data
- Corporate actions
- Splits, dividends

**Cached Data**:
- Market data cache (`marketDataCache`)
- Trading day calculations
- Historical performance data

---

### Agent Actions (AG-UI Protocol)

Renata can execute actions through CopilotKit:

**Navigation Actions**:
- `navigateToPage` - Redirect to /scan, /backtest, /plan
- `switchDisplayMode` - Change chart view mode
- `setDateRange` - Set custom date range

**State Actions**:
- `loadProject` - Load project into workspace
- `saveProject` - Save project to localStorage
- `executeScanner` - Trigger scanner execution
- `runBacktest` - Trigger backtest

**Tool Actions** (via AG-UI):
- `fetchMarketData` - Fetch Polygon data
- `validateV31` - Check V31 compliance
- `optimizeParameters` - Optimize strategy parameters
- `analyzeResults` - Analyze backtest results

---

## 📊 DATA FLOW ARCHITECTURE

```
USER INPUT
    ↓
/plan page OR sidebar on /scan or /backtest
    ↓
CopilotKit Chat Interface
    ↓
OpenRouter API (Claude Sonnet 4.5)
    ↓
RENATA ORCHESTRATOR
    ├─→ Planning Agent (A+ analysis, planning)
    ├─→ Researcher Agent (Archon RAG search)
    ├─→ Builder Agent (code generation)
    ├─→ Executor Agent (backend execution)
    └─→ Analyst Agent (optimization)
    ↓
ARCHON MCP (port 8051)
    ├─→ RAG Search (V31, Lingua, strategies)
    ├─→ Code Examples
    ├─→ Project Management
    └─→ Knowledge Graph
    ↓
FASTAPI Backend (port 8000)
    ├─→ Scanner Execution
    ├─ Backtesting Engine
    ├─ Polygon Data Fetching
    └─ Result Storage
    ↓
RESULTS DISPLAY
    └─→ User Reviews → Refine if needed
```

---

## 🎯 RENATA'S CAPABILITIES MATRIX

| Task | Planning | Research | Building | Executing | Analyzing | Status |
|------|---------|---------|---------|-----------|----------|--------|
| **Scanner Building** |
| Generate scanner from idea | ✅ | ✅ | ✅ | ❌ | ❌ | **Sprint 4-6** |
| Transform legacy code to V31 | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Build from A+ example | ✅ | ✅ | ✅ | ❌ | ✅ | **Sprint 4-6** |
| Validate V31 compliance | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Edit scanner parameters | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Modify scanner logic | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Add/remove patterns | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Refactor scanner code | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| **Backtesting & Validation** |
| Run backtest | ❌ | ❌ | ❌ | ✅ | ❌ | **Sprint 7** |
| Run analyzer codes (A+ validation) | ❌ | ❌ | ❌ | ✅ | ❌ | **Sprint 7** |
| Quick 30-day validation | ❌ | ❌ | ❌ | ✅ | ❌ | **Sprint 7** |
| IS/OOS validation | ❌ | ❌ | ❌ | ✅ | ✅ | **Sprint 7-8** |
| Monte Carlo simulation | ❌ | ❌ | ❌ | ✅ | ✅ | **Sprint 8** |
| **Execution & Risk Management** |
| Generate execution code | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Build position sizing | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Create stop-loss systems | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Portfolio risk controls | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Trade management logic | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| Edit execution rules | ❌ | ❌ | ✅ | ❌ | ❌ | **Sprint 6** |
| **Optimization & Analysis** |
| Optimize parameters | ❌ | ✅ | ❌ | ❌ | ✅ | **Sprint 8** |
| Parameter grid search | ❌ | ❌ | ❌ | ✅ | ✅ | **Sprint 8** |
| A/B testing | ❌ | ❌ | ❌ | ✅ | ✅ | **Sprint 8** |
| Analyze backtest results | ❌ | ❌ | ❌ | ❌ | ✅ | **Sprint 8** |
| Regime analysis | ❌ | ✅ | ❌ | ❌ | ✅ | **Sprint 5,8** |
| Performance metrics | ❌ | ❌ | ❌ | ❌ | ✅ | **Sprint 8** |
| **Research & Knowledge** |
| Find similar strategies | ❌ | ✅ | ❌ | ❌ | ❌ | **Sprint 5** |
| Suggest parameters | ❌ | ✅ | ❌ | ❌ | ✅ | **Sprint 5,8** |
| Market regime analysis | ❌ | ✅ | ❌ | ❌ | ❌ | **Sprint 5** |
| Explain V31 concepts | ✅ | ❌ | ❌ | ❌ | ❌ | **All** |
| Trading principles | ✅ | ✅ | ❌ | ❌ | ❌ | **All** |
| **Agent Collaboration** |
| Sequential workflows | ✅ | ✅ | ✅ | ✅ | ✅ | **All** |
| Parallel processing | ✅ | ✅ | ✅ | ✅ | ✅ | **All** |
| Context preservation | ✅ | ✅ | ✅ | ✅ | ✅ | **All** |
| Multi-agent problem solving | ✅ | ✅ | ✅ | ✅ | ✅ | **All** |
| RAG knowledge access | ✅ | ✅ | ✅ | ✅ | ✅ | **All** |
| **User Interface** |
| Chat on /plan page | ✅ | ✅ | ✅ | ❌ | ❌ | **Sprint 3** |
| Sidebar on /scan | ✅ | ✅ | ✅ | ❌ | ❌ | **Sprint 3** |
| Sidebar on /backtest | ✅ | ✅ | ✅ | ❌ | ❌ | **Sprint 3** |
| Page interlinking | ✅ | ✅ | ✅ | ✅ | ✅ | **Sprint 3** |
| Dashboard integration | ❌ | ❌ | ❌ | ✅ | ❌ | **Sprint 7** |

**Legend**:
- ✅ = Agent responsible for this capability
- ❌ = Agent not involved
- **Sprint X-X** = When capability will be implemented

---

## 🔐 KNOWLEDGE LIMITATIONS

### What Renata DOES NOT Know:

1. **Real-time market data** (until user executes)
2. **Proprietary data** (unless ingested into Archon)
3. **News events** (earnings, Fed announcements)
4. **Social sentiment** (Twitter, Reddit, etc.)
5. **Options flow data** (unless ingested)
6. **Your account balances** (not connected to brokerage)
7. **Real-time execution** (backend handles this)

### What Renata CANNOT Do:

1. **Execute trades** (platform is scanning/analysis only, not execution)
2. **Access brokerage account** (not integrated)
3. **Place orders** (not connected to brokers)
4. **Guarantee profits** (past performance ≠ future results)
5. **Replace human judgment** (AI assists, doesn't replace)

---

## 📈 PERFORMANCE EXPECTATIONS

### Response Times
- **Simple queries**: <2 seconds (RAG search)
- **Complex analysis**: 5-15 seconds (multi-agent)
- **Code generation**: 10-30 seconds
- **Backtest execution**: Varies by data size (seconds to minutes)

### Accuracy Targets
- **V31 Validation**: >95% compliance
- **Parameter Extraction**: >90% accuracy
- **Code Generation**: Compilable code (may need refinement)
- **Backtesting**: Matches expected results within 5%

### Reliability
- **Uptime Target**: 99%+ (Archon + backend)
- **Error Handling**: Graceful failures with clear messages
- **Fallback**: If Archon unavailable, use template-based generation

---

## 🎓 USER TRAINING & ONBOARDING

### First-Time User Flow

**Onboarding**:
1. Welcome message with quick tour
2. Sample A+ example loaded
3. Suggested starter projects
4. Tutorial videos (if available)

**Learning Curve**:
- **Beginner**: Use A+ example workflow (guided)
- **Intermediate**: Use idea → scanner workflow
- **Advanced**: Use full agent orchestration

### Help & Documentation

**In-Chat Guidance**:
- Context-aware suggestions
- Progressive disclosure (simple→advanced)
- Example requests
- Error explanations

**Documentation**:
- Quick start guide
- Workflow tutorials
- Agent capability reference
- V31 specification reference
- API documentation

---

## 🚀 FUTURE ENHANCEMENTS (Post-Launch)

### Phase 2 Features (Sprints 11+)
- Real-time market data integration
- News and event analysis
- Sentiment analysis integration
- Options flow analysis
- Multi-strategy portfolio optimization

### Phase 3 Features
- Strategy comparison tools
- Performance attribution
- Risk management dashboards
- Automated reporting
- Strategy version control

---

## ✅ CAPABILITIES CONFIRMATION

**Before we proceed, please confirm:**

1. ✅ **Knowledge Sources**:
   - V31 Gold Standard (with Market Scanning Pillar - 12k tickers)
   - Lingua Trading Framework
   - 4 Systematized Strategies
   - A+ Example Catalog
   - Libraries & Tools (Polygon, TA-Lib, backtesting.py, Python stack)
   - Trading Concepts (profitable trading, quant, systematic, execution, risk management)
   - Vision & State Understanding
   - Sufficient?

2. ✅ **Analyzer Codes** (Pre-Validation System):
   - A+ Example Analyzer (validate pattern capture)
   - Idea Visualizer (show on historical example)
   - Parameter Sensitivity Analyzer
   - Quick Backtest Analyzer
   - Dashboard integration (EdgeChart visual feedback)
   - Human-in-the-loop confirmation before full backtest
   - Correct approach?

3. ✅ **Five Agents** (with expanded capabilities):
   - **PLANNING**: A+ analysis, parameter extraction, mold generation
   - **RESEARCHER**: Archon RAG search, similar strategies, market regime
   - **BUILDER**: Scanners, backtests, execution, risk management, position management
   - **EXECUTOR**: Scanner execution, backtesting, real-time progress, analyzer codes
   - **ANALYST**: Performance analysis, optimization, IS/OOS, Monte Carlo
   - Correct set with expanded scope?

4. ✅ **Agent Collaboration**:
   - Sequential workflows (Planning → Research → Building → Execution → Analysis)
   - Parallel processing (Research + Building)
   - Context preservation (no information loss)
   - Multi-agent problem solving
   - Seamless handoffs
   - Working together correctly?

5. ✅ **RAG Context Optimization**:
   - Domain-specific queries for each agent
   - Semantic search (not just keyword matching)
   - Relevance ranking & domain filtering
   - Context window management
   - <2 second response time
   - Active intelligence layer (not passive database)
   - Optimizing all agent usage?

6. ✅ **Editing & Adjustment System**:
   - Parameter adjustment (quick changes)
   - Logic modification (add filters, change rules)
   - Pattern addition/removal
   - Code refactoring (optimization)
   - Backtest editing (date ranges, execution rules, risk params)
   - Iterative refinement workflows
   - A/B testing, undo/redo, version control
   - Robust enough for your workflow?

7. ✅ **Page Interlinking**:
   - /plan ↔ /scan ↔ /backtest efficient navigation
   - Context preservation across pages
   - Sidebar quick access on /scan and /backtest
   - Handoff data (code, parameters, results)
   - URL state management
   - Flexible workflow (start anywhere, go anywhere)
   - Right user experience?

8. ✅ **User Workflows**:
   - Idea → Scanner (with analyzer validation)
   - A+ Example → Scanner (with visual confirmation)
   - Legacy Code → V31 (transformation)
   - Optimization Loop (iterative refinement)
   - 4 workflows documented above - match your expectations?

9. ✅ **Infrastructure**:
   - Frontend: CopilotKit v1.50 + Traderra UI clone + Next.js
   - AI: OpenRouter (Claude Sonnet 4.5) + 5 agents
   - Backend: FastAPI (port 8000)
   - Knowledge: Archon MCP (port 8051) with RAG
   - Data: Polygon API + TA-Lib + backtesting.py
   - Correct stack?

10. ✅ **Performance**:
    - Simple queries: <2 seconds
    - Complex analysis: 5-15 seconds
    - Code generation: 10-30 seconds
    - Backtest: Varies by data size
    - V31 Validation: >95% compliance
    - Acceptable?

11. ✅ **Limitations**:
    - No real-time market data (until user executes)
    - No proprietary data (unless ingested)
    - No news/events (earnings, Fed)
    - No social sentiment
    - No options flow (unless ingested)
    - No brokerage integration (not an execution platform)
    - Can't guarantee profits
    - Doesn't replace human judgment
    - Acceptable?

**Once confirmed, I'll:**
1. ✅ Update all planning documents with these specifications
2. ✅ Revise sprint tasks to include new capabilities
3. ✅ Update MASTER_TASK_LIST.md with expanded scope
4. ✅ Create detailed implementation tasks for analyzer codes, agent collaboration, editing system
5. ✅ Setup project tracking system
6. ✅ Begin Sprint 0 execution

---

**This is your complete RENATA V2 system specification - V2.0**

**Major Updates from User Feedback:**
- ✅ Added: Market Scanning Pillar (12k tickers NYSE/NASDAQ/ETFs)
- ✅ Added: Libraries & Tools Knowledge Base (Polygon, TA-Lib, backtesting.py, Python)
- ✅ Added: Trading Concepts Knowledge (profitable, quant, systematic, execution, risk)
- ✅ Added: Vision & State Understanding (system awareness, visual recognition)
- ✅ Added: Analyzer Codes System (A+ validation, idea visualizer, parameter sensitivity)
- ✅ Expanded: Builder Agent (now includes backtesting, execution, risk management, position management)
- ✅ Added: Agent Collaboration System (sequential, parallel, multi-agent workflows)
- ✅ Added: RAG Context Optimization (domain-specific queries, semantic search, <2s response)
- ✅ Added: Editing & Adjustment System (parameter, logic, pattern editing, iterative refinement)
- ✅ Added: Page Interlinking System (/plan ↔ /scan ↔ /backtest with context preservation)

**Review carefully and confirm - this defines what we're building!**
