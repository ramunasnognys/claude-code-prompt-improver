# ADR-0005: Normalized Predictions Approach

## Status

Accepted

## Context

LSTM model predicts next-period price. Need to decide how to use predictions in trading strategy:

**Option A: Denormalize predictions back to real prices**
- Inverse transform scaler to get actual price predictions
- Calculate % change from current real price to predicted real price
- More intuitive for debugging (see actual price targets)

**Option B: Keep predictions in normalized space**
- Use normalized predictions directly (values in [0,1])
- Calculate % change in normalized space
- Never convert back to real prices

Key insight: Percentage changes are scale-invariant
- (pred_norm - actual_norm) / actual_norm ≈ (pred_real - actual_real) / actual_real
- For small changes (<5%), error is negligible

Considerations:
- LSTM trained on normalized data ([0,1] range via MinMaxScaler)
- Denormalization adds complexity and potential bugs
- Strategy only needs direction and magnitude of change, not absolute prices
- Backtesting framework uses real prices from OHLCV data (predictions are additional indicator)

## Decision

Use **normalized predictions directly** in strategy logic without denormalization.

Strategy implementation:
```python
# Calculate predicted price change in normalized space
prev_actual_norm = actuals_norm[i-1]
current_pred_norm = predictions_norm[i]
price_change_pct = (current_pred_norm - prev_actual_norm) / prev_actual_norm

# Generate signal if change exceeds threshold
if price_change_pct > threshold:
    go_long()
```

Rationale:
- Simpler code, fewer transformations, less bug surface area
- Predictions stay in same space as training (normalized)
- Percentage changes equivalent between normalized and real space
- No dependency on scaler pickle file in strategy (cleaner separation)
- Faster execution (no inverse transform overhead)

## Consequences

### Positive

- Cleaner code: No scaler loading, inverse transforms, or shape mismatches
- Fewer failure modes: Scaler file corruption, version mismatches eliminated
- Faster backtests: Skip denormalization step (negligible but cleaner)
- Easier debugging: All values in [0,1], easier to spot anomalies
- Better separation: Strategy independent of preprocessing implementation

### Negative

- Less intuitive for humans: Can't directly see "LSTM predicts BTC at $65,432"
- Harder to sanity-check: Is 0.6523 normalized price reasonable? (vs $65k obviously is)
- Debugging output cryptic: "Predicted change: 0.0012" less clear than "$50 move"
- Documentation burden: Must explain why we use normalized space
- Approximation error: For large % changes (>5%), normalized vs real diverge slightly

### Neutral

- Alignment critical: predictions[i] must match actuals[i] timestamps (handled in backtest_runner.py)
- Threshold tuning: prediction_threshold in normalized % (0.0005 = 0.05% change)
- No impact on model training: Model always trained on normalized targets
- Real prices still used for position sizing, stop-loss, take-profit (from OHLCV data)

## References

- Implementation: `src/strategies/lstm_strategy.py` (LSTMScalpingStrategy.init)
- Backtest runner: `src/backtest/backtest_runner.py` (prediction alignment logic)
- Preprocessing: `src/data/preprocess.py` (MinMaxScaler usage)
- Related ADR: [ADR-0001](0001-lstm-model-choice.md) on model architecture
- Discussion in code comments: `lstm_strategy.py:72-82`
