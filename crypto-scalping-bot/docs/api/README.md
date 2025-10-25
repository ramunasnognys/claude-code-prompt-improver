# API Documentation

Comprehensive reference documentation for all modules in the crypto scalping bot.

## Overview

This directory contains detailed API documentation for each module, including class definitions, method signatures, parameters, return types, and usage examples.

## Documentation Structure

Each module is documented in its own file with:
- **Module Overview**: Purpose and responsibilities
- **Class Reference**: All classes with detailed documentation
- **Function Reference**: Standalone functions (if any)
- **Usage Examples**: Practical code examples
- **Design Notes**: Internal implementation details

## Module Documentation

### Data Layer
- **[data-module.md](data-module.md)** - Data fetching and preprocessing
  - `OKXDataFetcher`: Historical OHLCV data retrieval
  - `DataPreprocessor`: Technical indicators and sequence creation

### Model Layer
- **[models-module.md](models-module.md)** - Machine learning models
  - `LSTMPricePredictor`: LSTM neural network for price prediction

### Strategy Layer
- **[strategies-module.md](strategies-module.md)** - Trading strategies
  - `LSTMScalpingStrategy`: Default LSTM-based scalping strategy
  - `AggressiveLSTMStrategy`: High-frequency variant
  - `ConservativeLSTMStrategy`: Risk-averse variant

### Backtesting Layer
- **[backtest-module.md](backtest-module.md)** - Backtesting and analysis
  - `BacktestRunner`: Execute and manage backtests
  - `PerformanceAnalyzer`: Calculate and visualize metrics

## Quick Start

1. Start with [data-module.md](data-module.md) to understand data flow
2. Review [models-module.md](models-module.md) for model architecture
3. Check [strategies-module.md](strategies-module.md) for trading logic
4. See [backtest-module.md](backtest-module.md) for evaluation

## Conventions

- All code examples are runnable (tested)
- Type hints follow Python 3.8+ standards
- Examples assume you're in the project root directory
- Config file path defaults to `config/config.yaml`

## Additional Resources

- Main README: `../README.md`
- Quick Start Guide: `../QUICKSTART.md`
- Architecture Decisions: `../adr/`
- Troubleshooting: `../TROUBLESHOOTING.md`
- Known Limitations: `../LIMITATIONS.md`
