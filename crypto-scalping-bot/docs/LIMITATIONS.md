# Known Limitations

This document outlines the current limitations of the crypto scalping bot across trading, technical, and architectural dimensions. Understanding these constraints is critical for setting realistic expectations and avoiding common pitfalls.

---

## Trading Limitations

### Backtesting Assumptions

**Perfect Execution**
- Orders execute instantly at the open of the next bar
- No order book slippage beyond fixed percentage (0.01%)
- Cannot model market impact for larger positions
- Assumes infinite liquidity at displayed prices

**Reality**: Live execution slower, slippage varies with order size and volatility.

**Lookahead Bias Risk**
- Indicators calculated on full dataset before backtesting
- No rebalancing or walk-forward validation in default setup
- Model trained on historical data including some test period dates

**Mitigation**: Use proper train/val/test splits, consider walk-forward optimization.

**No Funding Rates**
- Perpetual futures charge/pay funding every 8 hours
- Backtests ignore funding rate P&L
- Multi-day positions may have very different actual returns

**Impact**: Short-term scalping minimally affected (<24hr holds), but multi-day positions significantly impacted.

### Overfitting Risks

**In-Sample Performance**
- Model trained and tested on same market regime (e.g., 2024 bull market)
- Technical indicators with standard parameters may not generalize
- Risk of data snooping through iterative parameter tuning

**Warning**: Backtest Sharpe >2 often doesn't translate to live trading. Expect 30-50% degradation.

**Model Overfitting**
- LSTM can memorize training data patterns
- Dropout (0.2) and early stopping mitigate but don't eliminate risk
- Small datasets (<3 months) increase overfitting probability

**Best Practice**: Test on completely out-of-sample data (different time period, different asset).

### Market Regime Changes

**Model Brittleness**
- LSTM trained on specific volatility and trend conditions
- Black swan events (flash crashes, exchange outages) not in training data
- Correlation breakdowns during crises invalidate learned patterns

**Example**: Model trained on 2024 bull market may fail catastrophically in 2025 bear market.

**Adaptation**: Retrain monthly on recent data, implement circuit breakers for anomaly detection.

### Slippage Modeling

**Fixed Percentage Assumption**
- Current: 0.01% slippage on all trades
- Reality: Slippage varies by:
  - Order size (larger orders = more slippage)
  - Volatility (higher vol = wider spreads)
  - Time of day (thin liquidity during Asia hours)
  - Market regime (crisis = extreme slippage)

**Impact**: Actual slippage may be 2-5x higher during volatile periods.

---

## Technical Limitations

### LSTM Architecture Constraints

**Single-Step Prediction**
- Model predicts only next period (next 1-minute candle)
- Cannot predict multiple steps ahead
- No uncertainty quantification (confidence intervals)

**Implication**: Strategy reacts to short-term noise, not long-term trends.

**Sequence Length Limit**
- 60-period lookback window (1 hour for 1m timeframe)
- Longer sequences don't improve accuracy (vanishing gradient problem)
- Cannot capture patterns beyond 1-hour context

**Trade-off**: Longer lookback = more context but slower training and overfitting risk.

**Feature Set**
- Limited to 6 input features (close, volume, RSI, MACD, BB upper/lower)
- No order book data (depth, bid-ask spread)
- No sentiment data (social media, news)
- No inter-asset correlations (BTC vs ETH)

**Expansion**: Adding features requires retraining and may not improve accuracy.

### Data Requirements

**Minimum Dataset Size**
- Requires ~100,000 samples for stable training
- For 1m timeframe: ~70 days of continuous data
- For 5m timeframe: ~350 days of data

**Warning**: Training on <2 months often produces unstable models.

**Data Quality Dependencies**
- Missing candles cause sequence breaks
- Exchange API errors propagate through pipeline
- No outlier detection or cleaning (bad ticks included)

**Mitigation**: Manual inspection of fetched data recommended.

### Single-Asset Limitation

**No Portfolio Management**
- Bot trades only one symbol at a time (e.g., BTC/USDT)
- Cannot diversify across assets (BTC, ETH, SOL)
- Cannot hedge positions with correlated assets
- No correlation-based pair trading

**Workaround**: Run multiple bot instances for different assets (requires manual coordination).

### Memory Constraints

**RAM Requirements**
- Full OHLCV dataset loaded into memory (backtesting.py requirement)
- 1m data for 1 year ≈ 500MB RAM
- LSTM training: ~2GB GPU memory for typical configuration

**Limitation**: Cannot backtest on multi-year datasets without splitting or downsampling.

### Single Timeframe

**No Multi-Timeframe Analysis**
- Strategy uses only 1m candles
- Cannot combine 1m signals with 15m trend confirmation
- Missing higher-timeframe context (daily S/R levels)

**Enhancement**: Requires architectural changes to preprocessing and strategy layers.

---

## Architectural Limitations

### No Live Trading Support

**Simulation Only**
- Codebase designed for backtesting, not production trading
- No real-time data streaming
- No order execution interface
- No position reconciliation or error handling
- No logging or monitoring infrastructure

**Production Readiness**: Would require complete rewrite of execution layer.

### No Portfolio Management

**Single Position**
- One position at a time (long OR short)
- No position scaling (add to winners)
- No portfolio-level risk management
- No allocation across multiple strategies

**Limitation**: Cannot implement advanced money management techniques.

### No Dynamic Position Sizing

**Fixed Percentage**
- Position size hardcoded as % of equity (default 95%)
- No volatility-based sizing (Kelly criterion, ATR-based)
- No drawdown-based adjustments
- No correlation-aware sizing

**Impact**: Fixed risk regardless of market conditions.

### Single Strategy Per Backtest

**No Ensemble Methods**
- Cannot combine multiple LSTM models
- Cannot blend LSTM with classical strategies
- No voting or averaging across predictions

**Workaround**: Must run separate backtests and manually compare.

### No Walk-Forward Optimization

**Static Optimization**
- Parameter optimization uses full dataset (overfitting risk)
- No rolling window retraining
- No out-of-sample validation during optimization

**Best Practice**: Implement manually by splitting data and rerunning pipeline.

### Configuration Inflexibility

**Single Config File**
- All parameters in one config.yaml
- Cannot A/B test configurations easily
- No environment-specific configs (dev/prod)

**Workaround**: Copy and modify config files, specify path at runtime.

---

## Known Bugs/Issues

### FractionalBacktest Dependency

**Issue**: `FractionalBacktest` not in official backtesting.py release
- Requires fork or manual implementation
- May break with library updates
- Not well-documented

**Workaround**: Falls back to standard `Backtest` (no fractional positions) if unavailable.

**Impact**: Cannot properly size positions for expensive assets like BTC.

### Prediction-Data Alignment

**Issue**: Predictions must align exactly with backtest data by timestamp
- Off-by-one errors cause strategy to use wrong predictions
- Easy to introduce bugs when modifying preprocessing

**Safeguard**: `backtest_runner.py` includes alignment validation (lines 241-262).

**Symptom**: Strategy generates no signals or nonsensical signals.

### Rate Limiting Edge Cases

**Issue**: OKX API rate limits (20 req/s) occasionally triggered
- Script includes 100ms delay, but burst requests still possible
- Failed requests silently truncate data

**Mitigation**: Increase sleep time to 150-200ms for large fetches (edit fetch_data.py:117).

**Detection**: Check logs for "Error fetching data" messages.

### Indicator Warmup Period

**Issue**: First 60 candles lost to indicator warmup
- RSI needs 14 periods, MACD needs 26, sequences need 60
- Reduces usable backtest data

**Impact**: 60 minutes of data unusable for 1m timeframe.

**Not fixable**: Inherent to technical indicators and sequence modeling.

### TensorFlow Version Sensitivity

**Issue**: TensorFlow 2.x versions have breaking changes
- Model saved in TF 2.15 may not load in TF 2.16
- Keras 3.x compatibility issues

**Mitigation**: Pin TensorFlow version in requirements.txt, use virtual environment.

**Symptom**: "Unable to load model" or "Unknown layer type" errors.

---

## Recommendations

### For Research Use
- Always test on out-of-sample data (different time period)
- Use walk-forward validation for realistic performance estimates
- Compare against simple baselines (buy-and-hold, random forest)
- Document all parameter tuning to avoid data snooping

### For Production Consideration
- Paper trade for minimum 3 months before live capital
- Implement real-time monitoring and circuit breakers
- Model funding rates explicitly for multi-day positions
- Add order book data to improve slippage modeling
- Retrain model monthly on recent data
- Never risk more than 1-2% per trade

### For Further Development
- Implement walk-forward optimization framework
- Add multi-asset support with correlation modeling
- Integrate order book data (Bybit/Binance WebSocket)
- Add sentiment features (LunarCrush, social media)
- Implement ensemble methods (multiple models voting)
- Build production execution layer with Hummingbot or CCXT

---

## Related Documentation

- Architecture decisions: [docs/adr/](adr/)
- Troubleshooting: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- API reference: [docs/api/](api/)
- Quick start: [QUICKSTART.md](../QUICKSTART.md)

---

**Last Updated**: 2025-01-25
**Version**: 1.0
