# ADR-0001: LSTM Model for Price Prediction

## Status

Accepted

## Context

Need ML model for crypto price prediction on 1-minute timeframes for scalping strategy. Requirements:
- Handle sequential time-series data with temporal dependencies
- Predict next-period price from historical OHLCV + indicators
- Train on limited data (3-6 months typical)
- Fast inference (<100ms) for near-real-time signals
- Interpretable enough to debug strategy issues

Alternatives considered:
1. **LSTM**: Proven for time-series, handles sequences naturally, moderate complexity
2. **Transformers**: State-of-art but requires massive data, slow training, complex
3. **Random Forest**: Fast, interpretable, but no temporal awareness without feature engineering
4. **ARIMA/GARCH**: Classical stats, limited to linear patterns, can't leverage indicators
5. **Reinforcement Learning**: Promising but requires extensive tuning, unstable training

## Decision

Use stacked LSTM (Long Short-Term Memory) architecture with:
- 2-layer configuration: [64, 32] units
- Dropout regularization (0.2) to prevent overfitting
- 60-period lookback window (1 hour for 1m timeframe)
- Input features: close, volume, RSI, MACD, Bollinger Bands
- Output: Single predicted price (normalized)

Rationale:
- LSTMs explicitly designed for sequences, capture temporal patterns naturally
- Proven track record in financial time-series prediction
- Moderate data requirements (~100K samples = 2-3 months of 1m data)
- Fast inference on CPU (20-50ms per prediction)
- Well-understood architecture, easy to debug
- TensorFlow/Keras ecosystem mature and stable

## Consequences

### Positive

- Natural fit for sequential data, no manual lag feature engineering required
- Memory cells capture both short and long-term dependencies
- Dropout + early stopping control overfitting effectively
- Fast enough for near-real-time backtesting and potential live trading
- Extensive online resources for troubleshooting and optimization

### Negative

- Still prone to overfitting on small datasets (mitigated by validation split, dropout)
- Black box compared to classical models, hard to interpret specific predictions
- Requires GPU for fast training (CPU training slow for large datasets)
- May struggle with sudden regime changes (black swans, flash crashes)
- Vanishing gradient issues on very long sequences (mitigated by 60-period cap)

### Neutral

- Requires normalization/scaling (handled in DataPreprocessor)
- Needs careful hyperparameter tuning (epochs, learning rate, architecture)
- Training time: 5-15 minutes on GPU for typical dataset
- Model size: 200-500KB (small, easy to version control)

## References

- TensorFlow LSTM documentation: https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM
- Implementation: `src/models/lstm_model.py`
- Configuration: `config/config.yaml` model section
- Related ADR: [ADR-0003](0003-technical-indicators.md) on feature selection
