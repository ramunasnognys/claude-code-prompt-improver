# ADR-0002: Backtesting.py Framework Selection

## Status

Accepted

## Context

Need backtesting framework to simulate trading strategy on historical data. Requirements:
- Support perpetual futures (long/short positions)
- Accurate commission and slippage modeling
- Fractional position sizing for expensive assets (BTC)
- Interactive visualization of results
- Position management (stop-loss, take-profit)
- Performance metrics (Sharpe, drawdown, win rate)

Alternatives considered:
1. **Backtesting.py**: Python library, simple API, vectorized, built-in plotting
2. **Backtrader**: Feature-rich, complex API, slower, no fractional positions
3. **Zipline**: Quantopian's framework, heavy, designed for stocks not crypto
4. **Custom**: Full control but requires implementing metrics, plotting, position logic
5. **VectorBT**: Fast vectorized backtesting, complex for beginners, less documentation

## Decision

Use `backtesting.py` with `FractionalBacktest` extension for fractional position sizing.

Configuration:
- `exclusive_orders=True`: Close position before opening new one (prevents hedging)
- `trade_on_close=False`: Trade on next bar open (realistic execution)
- Commission: 0.04% (OKX taker fees)
- Strategy class: Inherit from `backtesting.Strategy` base

Rationale:
- Clean, Pythonic API easy to understand and extend
- Built-in support for long/short positions (essential for futures)
- Excellent HTML visualization with Bokeh (interactive zoom, pan)
- FractionalBacktest handles expensive assets like BTC
- Comprehensive metrics out-of-box (Sharpe, Sortino, drawdown, etc.)
- Active development and community support

## Consequences

### Positive

- Rapid strategy iteration: <100 lines for complex strategy
- Interactive plots make strategy debugging intuitive
- Vectorized execution: backtests run in seconds (vs minutes for event-driven)
- Built-in parameter optimization with grid search
- Stop-loss and take-profit handled automatically
- Clear separation of strategy logic from backtest infrastructure

### Negative

- Limited to single-asset backtests (no portfolio management)
- No built-in walk-forward optimization (need custom implementation)
- Slippage modeled as fixed percentage (not realistic order book simulation)
- Cannot model funding rates for perpetual futures (impacts multi-day holds)
- FractionalBacktest not in official release (dependency on fork/extension)
- Memory-intensive for very large datasets (loads full OHLCV into RAM)

### Neutral

- Requires OHLCV DataFrame with specific column names (Open, High, Low, Close, Volume)
- Indicator calculation happens outside backtest (in preprocessing step)
- Results saved as Pandas Series (easy to export to CSV)
- HTML plots require browser (not ideal for automated pipelines)

## References

- Backtesting.py documentation: https://kernc.github.io/backtesting.py/
- Implementation: `src/backtest/backtest_runner.py`
- Strategy: `src/strategies/lstm_strategy.py`
- Related ADR: [ADR-0004](0004-okx-exchange.md) on exchange-specific considerations
