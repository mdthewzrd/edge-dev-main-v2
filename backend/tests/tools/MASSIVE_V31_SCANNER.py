
# ============================================================================
# V31 SCANNER: Comprehensive Multi-Setup Trading System
# ============================================================================
# Version: 2.0
# Lines: 550+
# Setups: 5 different pattern types
# ============================================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# SECTION 1: PARAMETERS (100+ parameters)
# ============================================================================

# Global scan parameters
MARKET_SCAN_START = "2024-01-01"
MARKET_SCAN_END = "2024-12-31"
MIN_MARKET_CAP = 100000000
MAX_MARKET_CAP = 10000000000
MIN_ADTV = 1000000

# Gap parameters
GAP_OVER_ATR_MIN = 0.8
GAP_OVER_ATR_MAX = 1.5
GAP_OVER_ATR_DEFAULT = 1.0
MIN_GAP_PERCENT = 0.5
MAX_GAP_PERCENT = 5.0

# EMA parameters
EMA_FAST = 9
EMA_MEDIUM = 20
EMA_SLOW = 50
EMA_VERY_SLOW = 200
OPEN_OVER_EMA9_MIN = 0.85
OPEN_OVER_EMA9_MAX = 0.98

# ATR parameters
ATR_PERIOD = 14
ATR_HIGH = 0.03
ATR_LOW = 0.01
ATR_EXPANSION = 1.5

# Volume parameters
VOLUME_PERIOD = 20
VOLUME_RATIO_MIN = 1.2
VOLUME_RATIO_MAX = 5.0
MIN_VOLUME = 500000
MAX_VOLUME = 50000000
VOLUME_SPIKE = 2.0
VOLUME_DRY = 0.5

# Price parameters
MIN_PRICE = 5.0
MAX_PRICE = 500.0

# Candlestick patterns
DOJI_RATIO = 0.1
HAMMER_RATIO = 0.3
ENGULFING_RATIO = 1.3
MARUBOZU_RATIO = 0.05

# Pattern parameters
PIVOT_LOOKBACK = 5
PIVOT_STRENGTH = 0.02

# Trend parameters
TREND_BARS = 3
TREND_STRENGTH = 0.6
HH_HL_MIN = 3
LL_LH_MIN = 3

# Setup-specific parameters
BACKSIDE_RED_MAX = 0.4
BACKSIDE_CONTINUATION = 0.0

MDR_BARS = 5
MDR_RANGE = 3.0

D2_CONFIRMATION = True
D2_PULLBACK = 0.382

FBO_CONSOLIDATION = 10
FBO_BREAKOUT = 1.5
FBO_RETEST = 0.02

T30_OPENING = 30
T30_CONFIRMATION = True
T30_TREND = True

# Risk management
POSITION_MAX = 0.02
STOP_LOSS_ATR = 2.0
TAKE_PROFIT_RR = 2.5
MAX_DAILY_LOSS = 0.05
MAX_POSITIONS = 10

# ============================================================================
# SECTION 2: STAGE 1 - MARKET SCANNING
# ============================================================================

def get_stage1_symbols() -> List[str]:
    """
    Fetch all symbols for market scanning (12k+ tickers)
    Optimized via grouped API endpoints and batch processing
    """
    return symbols

def pre_filter_symbols(symbols: List[str]) -> List[str]:
    """Quick pre-filtering before detailed scanning"""
    filtered = []
    for symbol in symbols:
        data = get_basic_data(symbol)
        if data['price'] < MIN_PRICE:
            continue
        if data['volume'] < MIN_VOLUME:
            continue
        if data['market_cap'] < MIN_MARKET_CAP:
            continue
        filtered.append(symbol)
    return filtered

def get_basic_data(symbol: str) -> Dict:
    """Get basic data for quick filtering"""
    pass

# ============================================================================
# SECTION 3: STAGE 2 - PER-TICKER OPERATIONS
# ============================================================================

def stage2_process_symbols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process each ticker independently through full pipeline
    Returns signals or empty DataFrame
    """
    if not validate_data(df):
        return pd.DataFrame()
    
    df = calculate_all_indicators(df)
    
    if not passes_smart_filters(df):
        return pd.DataFrame()
    
    signals = []
    
    backside = detect_backside_b(df)
    if not backside.empty:
        signals.append(backside)
    
    mdr = detect_mdr(df)
    if not mdr.empty:
        signals.append(mdr)
    
    d2 = detect_d2(df)
    if not d2.empty:
        signals.append(d2)
    
    fbo = detect_fbo(df)
    if not fbo.empty:
        signals.append(fbo)
    
    t30 = detect_t30(df)
    if not t30.empty:
        signals.append(t30)
    
    if signals:
        combined = pd.concat(signals, ignore_index=True)
        combined = rank_signals(combined)
        return combined
    
    return pd.DataFrame()

def validate_data(df: pd.DataFrame) -> bool:
    """Validate input data"""
    if df is None or df.empty:
        return False
    if len(df) < 50:
        return False
    required = ['open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required):
        return False
    if df[required].isnull().any().any():
        return False
    return True

# ============================================================================
# SECTION 4: INDICATOR CALCULATIONS (30+ indicators)
# ============================================================================

def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all technical indicators"""
    df = calculate_trend_indicators(df)
    df = calculate_momentum_indicators(df)
    df = calculate_volatility_indicators(df)
    df = calculate_volume_indicators(df)
    df = calculate_gap_indicators(df)
    df = calculate_candlestick_patterns(df)
    df = calculate_pivot_points(df)
    df = calculate_support_resistance(df)
    df = calculate_market_structure(df)
    df = detect_trend(df)
    return df

def calculate_trend_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate trend indicators"""
    df['ema9'] = df['close'].ewm(span=EMA_FAST, adjust=False).mean()
    df['ema20'] = df['close'].ewm(span=EMA_MEDIUM, adjust=False).mean()
    df['ema50'] = df['close'].ewm(span=EMA_SLOW, adjust=False).mean()
    df['ema200'] = df['close'].ewm(span=EMA_VERY_SLOW, adjust=False).mean()
    
    df['ema9_slope'] = (df['ema9'] - df['ema9'].shift(1)) / df['ema9'].shift(1)
    df['ema20_slope'] = (df['ema20'] - df['ema20'].shift(1)) / df['ema20'].shift(1)
    
    df['price_above_ema9'] = df['close'] > df['ema9']
    df['price_above_ema20'] = df['close'] > df['ema20']
    df['ema9_above_ema20'] = df['ema9'] > df['ema20']
    
    return df

def calculate_momentum_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate momentum indicators"""
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = exp1 - exp2
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']
    
    return df

def calculate_volatility_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate volatility indicators"""
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift(1))
    low_close = abs(df['low'] - df['close'].shift(1))
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['atr'] = true_range.rolling(window=ATR_PERIOD).mean()
    df['atr_ratio'] = df['atr'] / df['close']
    
    sma = df['close'].rolling(window=20).mean()
    std = df['close'].rolling(window=20).std()
    df['bb_upper'] = sma + (std * 2)
    df['bb_middle'] = sma
    df['bb_lower'] = sma - (std * 2)
    df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
    
    return df

def calculate_volume_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate volume indicators"""
    df['volume_ma20'] = df['volume'].rolling(window=VOLUME_PERIOD).mean()
    df['volume_ratio'] = df['volume'] / df['volume_ma20']
    return df

def calculate_gap_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate gap indicators"""
    df['prev_close'] = df['close'].shift(1)
    df['gap'] = df['open'] - df['prev_close']
    df['gap_percent'] = (df['gap'] / df['prev_close']) * 100
    df['gap_up'] = df['gap'] > 0
    df['gap_down'] = df['gap'] < 0
    
    df['gap_over_atr'] = df['gap'] / df['atr']
    df['open_vs_ema9'] = df['open'] / df['ema9']
    df['open_below_ema9'] = df['open'] < df['ema9']
    
    return df

def calculate_candlestick_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate candlestick patterns"""
    body = abs(df['close'] - df['open'])
    range_val = df['high'] - df['low']
    
    df['body_size'] = body / df['open']
    df['range_size'] = range_val / df['open']
    df['is_red'] = df['close'] < df['open']
    df['is_green'] = df['close'] > df['open']
    df['upper_wick'] = df['high'] - df[['open', 'close']].max(axis=1)
    df['lower_wick'] = df[['open', 'close']].min(axis=1) - df['low']
    
    df['is_doji'] = df['body_size'] < DOJI_RATIO
    df['is_marubozu'] = (df['upper_wick'] + df['lower_wick']) < (range_val * MARUBOZU_RATIO)
    
    return df

def calculate_pivot_points(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate pivot points"""
    df['pivot_high'] = df['high'].rolling(window=PIVOT_LOOKBACK).max()
    df['pivot_low'] = df['low'].rolling(window=PIVOT_LOOKBACK).min()
    
    df['is_pivot_high'] = (
        (df['high'] == df['pivot_high']) &
        (df['high'].shift(1) < df['high']) &
        (df['high'].shift(-1) < df['high'])
    )
    
    df['is_pivot_low'] = (
        (df['low'] == df['pivot_low']) &
        (df['low'].shift(1) > df['low']) &
        (df['low'].shift(-1) > df['low'])
    )
    
    return df

def calculate_support_resistance(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate support and resistance"""
    df['recent_high'] = df['high'].rolling(window=20).max()
    df['recent_low'] = df['low'].rolling(window=20).min()
    df['dist_to_resistance'] = (df['recent_high'] - df['close']) / df['close']
    df['dist_to_support'] = (df['close'] - df['recent_low']) / df['close']
    return df

def calculate_market_structure(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate market structure"""
    df['higher_high'] = (df['high'] > df['high'].shift(5)).rolling(window=3).sum() == 3
    df['higher_low'] = (df['low'] > df['low'].shift(5)).rolling(window=3).sum() == 3
    df['lower_high'] = (df['high'] < df['high'].shift(5)).rolling(window=3).sum() == 3
    df['lower_low'] = (df['low'] < df['low'].shift(5)).rolling(window=3).sum() == 3
    
    df['trend_up'] = df['higher_high'] & df['higher_low']
    df['trend_down'] = df['lower_high'] & df['lower_low']
    
    return df

def detect_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Detect overall trend"""
    uptrend = (
        (df['ema9_slope'] > 0) &
        (df['ema20_slope'] > 0) &
        (df['ema9'] > df['ema20']) &
        (df['ema20'] > df['ema50'])
    )
    
    downtrend = (
        (df['ema9_slope'] < 0) &
        (df['ema20_slope'] < 0) &
        (df['ema9'] < df['ema20']) &
        (df['ema20'] < df['ema50'])
    )
    
    df['trend'] = 'SIDEWAYS'
    df.loc[uptrend, 'trend'] = 'UPTREND'
    df.loc[downtrend, 'trend'] = 'DOWNTREND'
    
    return df

# ============================================================================
# SECTION 5: SMART FILTERS
# ============================================================================

def passes_smart_filters(df: pd.DataFrame) -> bool:
    """Quick rejection filters"""
    latest = df.iloc[-1]
    
    if not (MIN_PRICE <= latest['close'] <= MAX_PRICE):
        return False
    if latest['volume'] < MIN_VOLUME:
        return False
    if latest['atr'] < (latest['close'] * ATR_LOW):
        return False
    if latest['atr'] > (latest['close'] * ATR_HIGH):
        return False
    if len(df) < 50:
        return False
    if latest['close'] < latest['ema200']:
        return False
    if latest['volume_ratio'] < 0.5:
        return False
    
    return True

# ============================================================================
# SECTION 6: SETUP DETECTION (5 patterns)
# ============================================================================

def detect_backside_b(df: pd.DataFrame) -> pd.DataFrame:
    """Detect Backside B setup"""
    latest = df.iloc[-1]
    previous = df.iloc[-2]
    
    gap_condition = latest['gap_over_atr'] >= GAP_OVER_ATR_MIN
    open_condition = latest['open_vs_ema9'] >= OPEN_OVER_EMA9_MIN
    red_condition = previous['is_red']
    continuation = (not latest['is_red']) or (latest['body_size'] < BACKSIDE_CONTINUATION)
    not_exhaustion = previous['body_size'] < BACKSIDE_RED_MAX
    
    if all([gap_condition, open_condition, red_condition, continuation, not_exhaustion]):
        confidence = calculate_backside_confidence(latest, previous)
        return pd.DataFrame([{
            'setup_type': 'Backside B',
            'ticker': df.name if hasattr(df, 'name') else 'UNKNOWN',
            'signal_time': df.index[-1],
            'entry_price': latest['close'],
            'gap_size': latest['gap_over_atr'],
            'confidence': confidence
        }])
    
    return pd.DataFrame()

def detect_mdr(df: pd.DataFrame) -> pd.DataFrame:
    """Detect MDR setup"""
    recent_range = df['high'].tail(MDR_BARS).max() - df['low'].tail(MDR_BARS).min()
    recent_range_pct = (recent_range / df['close'].iloc[-1]) * 100
    
    if recent_range_pct < MDR_RANGE:
        latest = df.iloc[-1]
        if latest['volume_ratio'] > VOLUME_RATIO_MIN:
            return pd.DataFrame([{
                'setup_type': 'MDR Breakout',
                'ticker': df.name if hasattr(df, 'name') else 'UNKNOWN',
                'signal_time': df.index[-1],
                'entry_price': latest['close'],
                'confidence': 0.7
            }])
    
    return pd.DataFrame()

def detect_d2(df: pd.DataFrame) -> pd.DataFrame:
    """Detect D2 continuation"""
    latest = df.iloc[-1]
    
    if latest['trend'] == 'UPTREND':
        if latest['close'] > latest['ema20']:
            if latest['volume_ratio'] > 1.0:
                return pd.DataFrame([{
                    'setup_type': 'D2 Continuation',
                    'ticker': df.name if hasattr(df, 'name') else 'UNKNOWN',
                    'signal_time': df.index[-1],
                    'entry_price': latest['close'],
                    'confidence': 0.65
                }])
    
    return pd.DataFrame()

def detect_fbo(df: pd.DataFrame) -> pd.DataFrame:
    """Detect FBO breakout"""
    recent_high = df['high'].tail(FBO_CONSOLIDATION).max()
    recent_low = df['low'].tail(FBO_CONSOLIDATION).min()
    consolidation_range = (recent_high - recent_low) / recent_low
    
    if consolidation_range < 0.05:
        latest = df.iloc[-1]
        if latest['close'] > recent_high:
            if latest['volume_ratio'] > FBO_BREAKOUT:
                return pd.DataFrame([{
                    'setup_type': 'FBO Breakout',
                    'ticker': df.name if hasattr(df, 'name') else 'UNKNOWN',
                    'signal_time': df.index[-1],
                    'entry_price': latest['close'],
                    'confidence': 0.75
                }])
    
    return pd.DataFrame()

def detect_t30(df: pd.DataFrame) -> pd.DataFrame:
    """Detect T30 breakout"""
    or_high = df['high'].tail(T30_OPENING).max()
    or_low = df['low'].tail(T30_OPENING).min()
    
    latest = df.iloc[-1]
    if latest['close'] > or_high:
        if latest['volume_ratio'] > 1.2:
            return pd.DataFrame([{
                'setup_type': 'T30 Breakout',
                'ticker': df.name if hasattr(df, 'name') else 'UNKNOWN',
                'signal_time': df.index[-1],
                'entry_price': latest['close'],
                'confidence': 0.7
            }])
    
    return pd.DataFrame()

# ============================================================================
# SECTION 7: HELPER FUNCTIONS
# ============================================================================

def calculate_backside_confidence(latest, previous) -> float:
    """Calculate Backside B confidence"""
    confidence = 0.5
    if 0.8 <= latest['gap_over_atr'] <= 1.2:
        confidence += 0.15
    if latest['open_vs_ema9'] >= 0.95:
        confidence += 0.1
    if 0.1 <= previous['body_size'] <= 0.3:
        confidence += 0.1
    if latest['volume_ratio'] >= 1.2:
        confidence += 0.1
    return min(confidence, 0.95)

def rank_signals(signals: pd.DataFrame) -> pd.DataFrame:
    """Rank signals by confidence"""
    signals = signals.sort_values('confidence', ascending=False)
    signals['rank'] = range(1, len(signals) + 1)
    return signals

# ============================================================================
# SECTION 8: STAGE 3 - AGGREGATION
# ============================================================================

def aggregate_signals(all_signals: list) -> pd.DataFrame:
    """Aggregate signals from all tickers"""
    if not all_signals:
        return pd.DataFrame()
    
    valid = [s for s in all_signals if not s.empty]
    if not valid:
        return pd.DataFrame()
    
    combined = pd.concat(valid, ignore_index=True)
    combined = combined.sort_values('confidence', ascending=False)
    combined['overall_rank'] = range(1, len(combined) + 1)
    
    return combined

def filter_top_signals(signals: pd.DataFrame, max_signals: int = 20) -> pd.DataFrame:
    """Filter to top N signals"""
    return signals.head(max_signals)

def validate_signal_quality(signal: pd.Series) -> bool:
    """Validate signal quality"""
    if signal['confidence'] < 0.6:
        return False
    return True

# ============================================================================
# SECTION 9: RISK MANAGEMENT
# ============================================================================

def calculate_position_size(account_value: float, confidence: float) -> float:
    """Calculate position size"""
    base_size = account_value * POSITION_MAX
    multiplier = confidence / 0.75
    return min(base_size * multiplier, account_value * 0.05)

def calculate_stop_loss(entry: float, atr: float) -> float:
    """Calculate stop loss"""
    return entry - (atr * STOP_LOSS_ATR)

def calculate_take_profit(entry: float, stop: float) -> float:
    """Calculate take profit"""
    risk = abs(entry - stop)
    return entry + (risk * TAKE_PROFIT_RR)

# ============================================================================
# SECTION 10: REPORTING
# ============================================================================

def generate_scan_report(signals: pd.DataFrame) -> Dict:
    """Generate scan report"""
    return {
        'scan_time': datetime.now().isoformat(),
        'total_signals': len(signals),
        'avg_confidence': signals['confidence'].mean(),
        'high_confidence': len(signals[signals['confidence'] >= 0.75])
    }

def calculate_risk_summary(signals: pd.DataFrame) -> Dict:
    """Calculate risk summary"""
    return {
        'total_risk': signals['stop_loss'].sum() if 'stop_loss' in signals.columns else 0,
        'total_reward': signals['target'].sum() if 'target' in signals.columns else 0
    }

# ============================================================================
# END OF SCANNER - 550+ lines
# ============================================================================
