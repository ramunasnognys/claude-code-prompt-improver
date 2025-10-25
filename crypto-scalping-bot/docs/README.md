# Crypto Scalping Bot Documentation

Comprehensive documentation for the crypto scalping bot project.

---

## Getting Started

**New to the project?** Start here:

1. **[Quick Start Guide](../QUICKSTART.md)** - Get up and running in minutes
2. **[Main README](../README.md)** - Project overview and features
3. **[Configuration Guide](../config/config.yaml)** - Detailed parameter explanations

---

## API Reference

Detailed documentation for all modules, classes, and functions:

### Core Modules

| Module | Description | Key Classes |
|--------|-------------|-------------|
| **[Data Module](api/data-module.md)** | Data fetching and preprocessing | `OKXDataFetcher`, `DataPreprocessor` |
| **[Models Module](api/models-module.md)** | LSTM neural network | `LSTMPricePredictor` |
| **[Strategies Module](api/strategies-module.md)** | Trading strategies | `LSTMScalpingStrategy`, `AggressiveLSTMStrategy`, `ConservativeLSTMStrategy` |
| **[Backtest Module](api/backtest-module.md)** | Backtesting framework | `BacktestRunner` |

### Learning Path

Follow this sequence to understand the system:

1. **Data Flow**: Start with [Data Module](api/data-module.md) to understand how data is fetched and prepared
2. **Model Training**: Read [Models Module](api/models-module.md) to learn LSTM architecture and training
3. **Strategy Logic**: Study [Strategies Module](api/strategies-module.md) for trading signal generation
4. **Backtesting**: Review [Backtest Module](api/backtest-module.md) to evaluate performance

---

## Architecture Decision Records (ADRs)

Understand why key design decisions were made:

| ADR | Title | Topic |
|-----|-------|-------|
| [ADR-0001](adr/0001-lstm-model-choice.md) | LSTM Model Choice | Why LSTM over transformers/random forests |
| [ADR-0002](adr/0002-backtesting-framework.md) | Backtesting Framework | Why backtesting.py library |
| [ADR-0003](adr/0003-technical-indicators.md) | Technical Indicators | RSI, MACD, Bollinger Bands selection |
| [ADR-0004](adr/0004-okx-exchange.md) | OKX Exchange | Exchange and perpetual futures choice |
| [ADR-0005](adr/0005-normalized-predictions.md) | Normalized Predictions | Why we use normalized space directly |

**Read ADRs to understand**:
- Technical trade-offs and alternatives considered
- Consequences (positive, negative, neutral)
- Context and constraints that drove decisions

---

## Reference Guides

### Known Limitations

**[LIMITATIONS.md](LIMITATIONS.md)** - Critical constraints to understand:

- **Trading Limitations**: Backtesting assumptions, overfitting risks, market regime changes
- **Technical Limitations**: LSTM constraints, data requirements, single-asset limitation
- **Architectural Limitations**: No live trading, no portfolio management, single timeframe
- **Known Bugs**: FractionalBacktest dependency, alignment issues, rate limiting

**Read this before**:
- Interpreting backtest results
- Planning live trading deployment
- Setting performance expectations

---

### Troubleshooting Guide

**[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solutions to common issues:

- **Installation/Setup**: Dependency conflicts, environment setup, config errors
- **Data Fetching**: API rate limits, SSL errors, missing data
- **Model Training**: OOM errors, convergence issues, overfitting
- **Backtesting**: No trades, poor performance, interpretation questions

**Use this when**:
- Errors occur during setup or execution
- Results don't match expectations
- Performance is unexpectedly poor

---

## How to Use This Documentation

### For First-Time Users

1. Read [Quick Start](../QUICKSTART.md) and run the complete pipeline
2. Review [Known Limitations](LIMITATIONS.md) to set realistic expectations
3. Study [Data Module API](api/data-module.md) to understand data flow
4. Follow with [Models](api/models-module.md) → [Strategies](api/strategies-module.md) → [Backtest](api/backtest-module.md)

### For Developers

1. Read all ADRs to understand design rationale
2. Study API documentation for module you're working on
3. Reference [Troubleshooting Guide](TROUBLESHOOTING.md) when issues arise
4. Check [Known Limitations](LIMITATIONS.md) before proposing features

### For Researchers

1. Understand constraints in [Known Limitations](LIMITATIONS.md)
2. Review [ADR-0001](adr/0001-lstm-model-choice.md) and [ADR-0003](adr/0003-technical-indicators.md) for model/feature choices
3. Study [Models Module](api/models-module.md) for architecture details
4. Read [Strategies Module](api/strategies-module.md) for trading logic
5. Consider limitations when interpreting backtest results

---

## Project Structure

```
crypto-scalping-bot/
├── src/
│   ├── data/              # fetch_data.py, preprocess.py
│   ├── models/            # lstm_model.py
│   ├── strategies/        # lstm_strategy.py
│   └── backtest/          # backtest_runner.py, performance_analyzer.py
├── config/
│   └── config.yaml        # All configurable parameters
├── docs/                  # You are here!
│   ├── api/               # Module API documentation
│   ├── adr/               # Architecture Decision Records
│   ├── LIMITATIONS.md     # Known limitations
│   └── TROUBLESHOOTING.md # Solutions to common issues
├── data/                  # Generated data files (CSV)
├── models/                # Trained models and checkpoints
├── results/               # Backtest results and plots
├── README.md              # Project overview
├── QUICKSTART.md          # Quick start guide
└── run_pipeline.py        # Complete pipeline script
```

---

## Documentation Conventions

### Code Examples

- All examples are runnable (tested)
- Assume working directory is project root (`crypto-scalping-bot/`)
- Type hints follow Python 3.8+ standards
- Config paths default to `config/config.yaml`

### Cross-References

- Internal links use relative paths: `[text](../path/file.md)`
- Code references include line numbers: `lstm_model.py:127`
- External links use full URLs

### Terminology

- **OHLCV**: Open, High, Low, Close, Volume
- **Normalized**: Scaled to [0,1] range using MinMaxScaler
- **Sequence**: Sliding window of historical data (e.g., 60 timesteps)
- **Lookback**: Number of historical periods in a sequence
- **Perpetual Futures (Perps)**: Contracts without expiration date
- **Scalping**: High-frequency trading strategy targeting small price movements

---

## Additional Resources

### External Documentation

- **CCXT Library**: https://docs.ccxt.com/
- **TensorFlow/Keras**: https://www.tensorflow.org/api_docs/python/tf/keras
- **Backtesting.py**: https://kernc.github.io/backtesting.py/
- **pandas-ta**: https://github.com/twopirllc/pandas-ta
- **OKX API**: https://www.okx.com/docs-v5/en/

### Related Topics

- **LSTM Networks**: Understanding recurrent architectures for time-series
- **Technical Analysis**: RSI, MACD, Bollinger Bands fundamentals
- **Risk Management**: Stop-loss, take-profit, position sizing
- **Backtesting**: Avoiding lookahead bias, slippage modeling, overfitting

---

## Contributing to Documentation

When adding or updating documentation:

1. **ADRs**: Use the template in `docs/adr/adr-template.md`
2. **API Docs**: Include overview, parameters, returns, examples, design notes
3. **Cross-Reference**: Link related docs (ADRs, API, troubleshooting)
4. **Code Examples**: Test all examples before committing
5. **Update Index**: Add new docs to this README

---

## Feedback

Found an issue or have suggestions?
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first
- Review [Known Limitations](LIMITATIONS.md) for documented constraints
- Consult relevant [ADR](adr/) for design context

---

**Last Updated**: 2025-01-25
**Documentation Version**: 1.0
