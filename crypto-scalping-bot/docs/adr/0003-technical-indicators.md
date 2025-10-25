# ADR-0003: Technical Indicator Selection

## Status

Accepted

## Context

LSTM model needs feature inputs beyond raw OHLCV to capture market dynamics. Requirements:
- Complement LSTM predictions (not replace)
- Widely used in crypto trading (reduce overfitting to random patterns)
- Fast to calculate (must handle 1-minute bars)
- Provide diverse signal types: momentum, trend, volatility
- Available in TA-Lib or pandas-ta libraries

Candidates evaluated:
- **Momentum**: RSI, Stochastic, CCI, Williams %R
- **Trend**: MACD, EMA, SMA, ADX
- **Volatility**: Bollinger Bands, ATR, Keltner Channels
- **Volume**: OBV, Volume SMA, MFI
- **Custom**: Price change %, high-low range

## Decision

Use 3 core indicator families providing 6 features:
1. **RSI (14-period)**: Momentum, overbought/oversold detection
2. **MACD (12,26,9)**: Trend direction and strength
3. **Bollinger Bands (20,2)**: Volatility and price extremes

Plus raw features:
- **Close price**: Normalized, primary prediction target
- **Volume**: Normalized, liquidity indicator

Indicator signals used for:
- LSTM input features (6 total: close, volume, RSI, MACD, BB upper, BB lower)
- Strategy confirmation (prevent trades when indicators conflict with LSTM)

Rationale:
- RSI: Proven momentum indicator, prevents chasing pumps/dumps
- MACD: Captures trend changes, crossovers signal reversals
- Bollinger Bands: Mean reversion + breakout signals, adapts to volatility
- Diversity: Covers momentum, trend, volatility (uncorrelated signal types)
- Standard parameters: Reduces overfitting risk vs custom-tuned values

## Consequences

### Positive

- RSI filters LSTM signals during extreme conditions (RSI >70 = no long, <30 = no short)
- MACD confirms trend direction (MACD > signal = uptrend)
- Bollinger Bands capture volatility regime changes
- Well-documented indicators reduce "magic parameter" syndrome
- Fast calculation (<1ms per bar for all 3 indicators)
- Available in pandas-ta library (no TA-Lib compilation needed)

### Negative

- Indicators lag price by nature (RSI 14 periods behind)
- May filter out valid LSTM signals (conservative bias)
- Standard parameters not optimal for all market conditions (crypto vs stocks)
- Bollinger Bands can give false breakout signals in trending markets
- MACD whipsaws in sideways markets (frequent crossovers)
- RSI can stay overbought/oversold for extended periods in strong trends

### Neutral

- All indicators calculated in preprocessing step (cached, not recalculated per backtest)
- Normalization required for LSTM (RSI [0,100] → [0,1], prices min-max scaled)
- 60-period lookback means first 60 bars lost to indicator warmup
- Added features increase LSTM parameters (~20% more) but improve accuracy
- Can add more indicators later without breaking existing code

## References

- Implementation: `src/data/preprocess.py` (DataPreprocessor.add_technical_indicators)
- Configuration: `config/config.yaml` indicators section
- pandas-ta library: https://github.com/twopirllc/pandas-ta
- Strategy usage: `src/strategies/lstm_strategy.py` (confirmation logic)
- Related ADR: [ADR-0001](0001-lstm-model-choice.md) on model architecture
