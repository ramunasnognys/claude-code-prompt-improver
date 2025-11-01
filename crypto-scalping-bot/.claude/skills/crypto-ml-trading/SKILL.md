---
name: crypto-ml-trading
description: Use when working with ML-based crypto trading bots, LSTM price predictions, backtesting frameworks, technical indicator integration, or scalping strategy development. Guides architecture patterns, hyperparameter tuning, risk management standards, and validation best practices for perpetual futures trading systems.
---

# Crypto ML Trading Standards

This skill documents architecture patterns, code conventions, and best practices for LSTM-based crypto trading bots with backtesting validation.

## Core Architecture Pattern

```
Data Fetch → Preprocess → Train LSTM → Backtest → Analyze
(CCXT)     (Features)   (Neural Net) (Simulation) (Metrics)
```

**Modules:**
- `src/data/` - Exchange integration and OHLCV data
- `src/models/` - LSTM architecture and training logic
- `src/strategies/` - Signal generation and execution rules
- `src/backtesting/` - Simulation engine and performance analysis

## LSTM Architecture Standards

### Layer Configuration

Use sequential stacked LSTM with dropout regularization:

```yaml
model:
  lstm_units: [128, 64, 32]     # 3-layer architecture (complex patterns)
  dropout_rate: 0.3              # 30% neuron dropout (regularization)
  epochs: 50                      # Early stopping may halt earlier
  batch_size: 64                  # Balance speed vs stability
  learning_rate: 0.0005           # Tuned for crypto volatility
```

**Rationale:**
- **3 layers** capture temporal hierarchies: fast (layer 1), intermediate (layer 2), slow (layer 3)
- **128→64→32 units** progressively compress features into price signal
- **Dropout 0.3** prevents overfitting without over-regularizing
- **Batch 64** = fast GPU training + stable gradient estimates

### Input Specification

**Lookback window:** 120 periods (2 hours at 1m timeframe)

```python
# 120 = Last 120 candles → Predict candle 121
lookback_periods: 120

# Feature set (14 indicators):
features: [
  close, volume,           # Price + liquidity
  rsi_14, macd, macd_diff, # Momentum (3)
  bb_upper, bb_lower, bb_width,  # Volatility (3)
  atr_pct, adx_14,         # Volatility + trend strength (2)
  ema_10, price_change,    # Trend + momentum (2)
  volume_ratio, hl_range   # Volume + intrabar volatility (2)
]
```

**Interpretation:**
- Shorter lookback (60) = fast but may miss patterns
- Longer lookback (240) = better context but slower training
- 120 balances both for 1m scalping

### Training Standards

1. **Data split:** Train 70% | Validation 20% | Test 10%
2. **Test period:** Must be chronologically after train/val (no peeking)
3. **Callbacks:**
   - `EarlyStopping(monitor='val_loss', patience=10)` - Prevent overfitting
   - `ReduceLROnPlateau(factor=0.5, patience=5)` - Adaptive learning rate
   - `ModelCheckpoint(save_best_only=True)` - Keep best weights

4. **Bias correction (Phase 3.1):**
   ```python
   bias = mean(predictions - actuals)  # Systematic bias
   scale = std(actuals) / std(predictions)  # Variance mismatch
   corrected = (predictions - bias) * scale
   ```
   Apply to correct prediction distribution post-training.

## Technical Indicator Integration

### Mandatory Indicators

| Indicator | Purpose | Config | Notes |
|-----------|---------|--------|-------|
| RSI(14) | Momentum | `oversold=25, overbought=75` | Avoid extreme levels |
| MACD(12,26,9) | Trend direction | `fast=12, slow=26, signal=9` | Standard params |
| Bollinger Bands(20,2) | Volatility bands | `period=20, std=2` | Volatility regime |

### Optional Indicators (Tested)

- **ADX(14):** Trend strength filter (disabled in Phase 2.3 - reduced performance)
- **ATR:** Volatility sizing (normalized as feature)
- **EMA(10):** Short-term trend confirmation

**Key insight:** Volume filter alone outperforms complex multi-indicator confirmations. Avoid over-engineering signal logic.

## Signal Generation Protocol

### 3-Level Confirmation

1. **Level 1: LSTM prediction**
   ```python
   predicted_change = model.predict(last_120_candles)
   if abs(predicted_change) > threshold:  # 0.2% minimum
       signal_strength = predicted_change
   ```

2. **Level 2: Indicator confirmation**
   ```python
   if signal_strength > 0:  # LONG predicted
       if rsi < 75 and macd > macd_signal:  # Confirmation
           long_signal = True
   ```

3. **Level 3: Volume filter**
   ```python
   if volume_current > volume_sma20 * 1.2:  # 20% above average
       execute_trade(signal)
   ```

### Why Multi-Level?
- LSTM alone = high sensitivity, false signals
- + Indicators = directional confirmation
- + Volume = liquidity check (avoids illiquid candles)

## Risk Management Standards

### Position Sizing

```yaml
trading:
  max_position_size: 0.3       # 30% of equity per trade
  max_open_positions: 3        # Concurrent position limit
  leverage: 5                  # Moderate leverage (avoid >10x)
```

**Interpretation:**
- 30% = Conservative for crypto volatility
- 3 concurrent = Portfolio diversification without over-leverage
- 5x leverage = 5% equity moves → 25% position moves (manageable)

### Stop Loss & Take Profit

```yaml
trading:
  stop_loss_pct: 0.01          # 1% loss threshold
  take_profit_pct: 0.025       # 2.5% profit target
  # Ratio: 2.5:1 (TP:SL) → Positive expectancy
```

**Calculation example (BTC @ $40,000):**
- Entry: $40,000
- Stop: $39,600 (1% loss)
- Take-profit: $41,000 (2.5% gain)
- Risk/reward: 1 unit risk → 2.5 units reward
- Win rate needed: >28.6% for profitability

### Daily Circuit Breakers

```yaml
trading:
  max_daily_loss: 0.05         # Stop trading if equity drops 5%
```

**Purpose:** Prevent revenge trading and cascading losses. Reset next day.

## Backtesting Standards

### Data Leakage Prevention

```yaml
backtesting:
  train_date: 2024-01-01
  test_date: 2024-03-16         # MUST be after train period
  backtest_date: 2024-03-16
  end_date: 2024-03-31
```

**Critical:** Backtest period must NOT overlap training. Model has never seen this data.

### Realistic Simulation

```yaml
backtesting:
  commission: 0.0004            # OKX taker fee (0.04%)
  slippage: 0.0001              # 0.01% price slippage
```

**Formula:** `execution_price = predicted_price * (1 ± slippage) ± commission`

### Fee Breakdown

| Exchange | Taker | Maker | Notes |
|----------|-------|-------|-------|
| OKX | 0.04% | 0.02% | Perpetual futures |
| Binance | 0.04% | 0.02% | Market vs limit |
| Bybit | 0.06% | 0.01% | Volume discounts |

**Rule:** Use taker fees for market orders (conservative).

## Performance Metrics

### Primary Metrics

| Metric | Formula | Target | Interpretation |
|--------|---------|--------|-----------------|
| **Return %** | (final - initial) / initial | >5-10% | Total profit |
| **Sharpe Ratio** | (return - rf) / std | >0.5 | Risk-adjusted return |
| **Max Drawdown** | lowest_point / peak | <20% | Worst peak-to-trough |
| **Win Rate** | trades_won / total_trades | >45% | % profitable trades |

### Secondary Metrics

- **Profit Factor:** Gross profit / Gross loss (target >1.5)
- **Recovery Factor:** Net profit / Max drawdown (target >2.0)
- **Calmar Ratio:** Annual return / Max drawdown (target >0.5)

### Failure Indicators

⚠️ **Red flags:**
- Sharpe < -0.5: Losing money consistently
- Max DD > 30%: Risk tolerance exceeded
- Win rate < 40%: Worse than random
- 0 trades: Threshold too strict (lower `prediction_threshold`)
- 1000+ trades: Overfitting or noise trading (raise threshold)

## Configuration Best Practices

### Hyperparameter Tuning Workflow

1. **Baseline:** Train with default config, measure out-of-sample backtest Sharpe
2. **Single parameter:** Change one parameter, retrain, backtest
3. **Document:** Log parameter, Sharpe, max DD, win rate
4. **Iterate:** Select best parameter, repeat with next one

Example sweep:
```
Test prediction_threshold in [0.001, 0.002, 0.003, 0.005]
→ Measure each: Sharpe, DD, win rate, trade count
→ Pick best Sharpe on test set
→ Lock in, test next parameter
```

### Common Tuning Scenarios

**Problem: No trades in backtest**
- Lower `prediction_threshold` (0.002 → 0.001)
- Raise `rsi_oversold/overbought` bounds (25/75 → 20/80)
- Reduce `volume_threshold` (0.2 → 0.1)

**Problem: Too many trades (>500/day)**
- Raise `prediction_threshold` (0.002 → 0.005)
- Add RSI bounds tighter
- Require volume confirmation

**Problem: High drawdown (>30%)**
- Lower `max_position_size` (0.3 → 0.2)
- Tighten `stop_loss_pct` (0.01 → 0.005)
- Reduce `leverage` (5 → 3)

## Code Pattern Standards

### Model Training Template

```python
from src.models.lstm_model import LSTMPricePredictor

# Initialize
predictor = LSTMPricePredictor('config/config.yaml')
predictor.build_model((120, 14))  # (lookback, features)

# Train
history = predictor.train(X_train, y_train, X_val, y_val)

# Correct bias (Phase 3.1)
predictor.bias_corrector.fit(val_preds, y_val)
test_preds = predictor.bias_corrector.correct(test_preds)

# Save
predictor.save_model('models/lstm_model.keras')
```

### Strategy Instantiation Template

```python
from backtesting import Backtest
from src.strategies.lstm_strategy import LSTMScalpingStrategy

bt = Backtest(
    data=ohlcv_with_predictions,
    strategy=LSTMScalpingStrategy,
    cash=10000,
    commission=0.0004,
    exclusive_orders=True
)

stats = bt.run()
print(stats._metrics)  # Sharpe, DD, return, etc.
```

## Common Pitfalls

### 1. Data Leakage
❌ Using future prices in feature calculation
✅ Use only past data within lookback window

### 2. Overfitting
❌ Backtest period overlaps training
✅ Test on chronologically later out-of-sample data

### 3. Threshold Blindness
❌ Tuning only on backtest period
✅ Use cross-validation or walk-forward analysis

### 4. Fee Negligence
❌ Ignoring commissions in backtest
✅ Include exchange fees (0.04% per round-trip = 0.08%)

### 5. Survivor Bias
❌ Testing only on symbols that exist today
✅ Account for delisted/suspended pairs

## References

For detailed guidance, see:
- [ML Trading Patterns](references/ml-trading-patterns.md) - Architecture deep dives
- [Backtesting Guide](references/backtesting-guide.md) - Simulation best practices
- [Risk Management Specs](references/risk-management-specs.md) - Position sizing formulas
