# Backtest Module API Reference

The backtest module executes strategy simulations on historical data and generates performance reports.

**Module Path**: `src/backtest/`

**Files**:
- `backtest_runner.py` - Backtest execution and management
- `performance_analyzer.py` - Performance metrics and visualization

---

## Table of Contents

1. [BacktestRunner](#backtestrunner)
2. [Usage Examples](#usage-examples)
3. [Performance Metrics](#performance-metrics)

---

## BacktestRunner

**Class**: `BacktestRunner`
**File**: `src/backtest/backtest_runner.py`
**Purpose**: Execute and manage backtests with LSTM strategies

### Constructor

```python
BacktestRunner(config_path: str = 'config/config.yaml') -> None
```

**Parameters**:
- `config_path` (str): Path to YAML configuration file

**Attributes**:
- `config` (dict): Loaded configuration
- `results` (pd.Series): Last backtest results (None until `run_backtest()` called)
- `bt` (Backtest): Backtest instance (None until `run_backtest()` called)

**Example**:
```python
from src.backtest.backtest_runner import BacktestRunner

runner = BacktestRunner('config/config.yaml')
print(f"Initial capital: ${runner.config['trading']['initial_capital']}")
```

---

### Methods

#### prepare_data_for_backtest

```python
prepare_data_for_backtest(
    df: pd.DataFrame,
    predictions_norm: np.ndarray,
    actuals_norm: np.ndarray
) -> pd.DataFrame
```

Prepare data in the format required by backtesting.py framework.

**Parameters**:
- `df` (pd.DataFrame): OHLCV data with technical indicators. Required columns:
  - `datetime`: Timestamp
  - `open`, `high`, `low`, `close`, `volume`: OHLCV data
  - `rsi_14`, `macd`, `macd_signal`: Technical indicators
  - `bb_upper`, `bb_lower`: Bollinger Bands
- `predictions_norm` (np.ndarray): LSTM predictions (normalized [0,1])
- `actuals_norm` (np.ndarray): Actual values (normalized [0,1])

**Returns**:
- `pd.DataFrame`: Formatted for backtesting.py with columns:
  - Index: `datetime` (pandas DatetimeIndex)
  - OHLCV: `Open`, `High`, `Low`, `Close`, `Volume` (capitalized)
  - Indicators: `RSI`, `MACD`, `MACD_Signal`, `BB_Upper`, `BB_Lower`
  - Predictions: `Predicted_Norm`, `Actual_Norm`

**Side Effects**:
- Drops rows with NaN values
- Converts column names to backtesting.py conventions (capitalized OHLCV)

**Example**:
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/processed_data.csv')
predictions = np.load('models/predictions.npy')
actuals = np.load('models/actuals.npy')

# Prepare
runner = BacktestRunner()
bt_data = runner.prepare_data_for_backtest(df, predictions, actuals)

print(bt_data.head())
print(f"Backtest data shape: {bt_data.shape}")
print(f"Date range: {bt_data.index.min()} to {bt_data.index.max()}")
```

---

#### run_backtest

```python
run_backtest(
    data: pd.DataFrame,
    strategy_class: Type[Strategy] = LSTMScalpingStrategy,
    cash: float = 10000,
    commission: float = 0.0004
) -> pd.Series
```

Execute a backtest with the specified strategy.

**Parameters**:
- `data` (pd.DataFrame): Prepared backtest data (from `prepare_data_for_backtest()`)
- `strategy_class` (Type[Strategy]): Strategy class to use. Options:
  - `LSTMScalpingStrategy` (default)
  - `AggressiveLSTMStrategy`
  - `ConservativeLSTMStrategy`
  - Custom strategy inheriting from `backtesting.Strategy`
- `cash` (float): Initial capital in USDT. Default: 10000
- `commission` (float): Trading commission per trade (decimal). Default: 0.0004 (0.04%)

**Returns**:
- `pd.Series`: Backtest statistics including:
  - `Start`: Initial equity
  - `End`: Final equity
  - `Return [%]`: Total return percentage
  - `Max. Drawdown [%]`: Worst peak-to-trough decline
  - `Sharpe Ratio`: Risk-adjusted return metric
  - `# Trades`: Number of trades executed
  - `Win Rate [%]`: Percentage of profitable trades
  - `Best Trade [%]`: Best single trade return
  - `Worst Trade [%]`: Worst single trade return
  - `Avg. Trade [%]`: Average trade return
  - `Max. Drawdown Duration`: Longest drawdown period
  - `Calmar Ratio`: Return / max drawdown

**Side Effects**:
- Sets `self.bt` to Backtest instance
- Sets `self.results` to statistics Series
- Prints progress and summary to console

**Backtest Configuration**:
- Uses `FractionalBacktest` if available (for fractional position sizing)
- Falls back to standard `Backtest` otherwise
- `exclusive_orders=True`: Close position before opening new one
- `trade_on_close=False`: Trade on next bar open (realistic)

**Example**:
```python
from src.strategies.lstm_strategy import LSTMScalpingStrategy

runner = BacktestRunner()
results = runner.run_backtest(
    data=bt_data,
    strategy_class=LSTMScalpingStrategy,
    cash=10000,
    commission=0.0004
)

print(f"Final Return: {results['Return [%]']:.2f}%")
print(f"Sharpe Ratio: {results['Sharpe Ratio']:.2f}")
print(f"Total Trades: {results['# Trades']}")
```

**Console Output**:
```
Running backtest with LSTMScalpingStrategy...
Initial capital: $10,000.00
Commission: 0.04%
Data period: 2024-01-01 00:00:00 to 2024-03-31 23:59:00
Total bars: 129600

[Backtest runs...]

Strategy Initialization - Prediction Analysis
Prediction changes mean: 0.0012%
...
```

---

#### print_results

```python
print_results() -> None
```

Print formatted backtest results to console.

**Raises**:
- Early return if `self.results` is None (no backtest run yet)

**Output Format**:
```
============================================================
BACKTEST RESULTS
============================================================

Performance:
  Start Value:              $10,000.00
  End Value:                $11,245.67
  Return:                   12.46%
  Max Drawdown:             -8.92%
  Sharpe Ratio:             1.23

Trades:
  Total Trades:             156
  Win Rate:                 54.23%
  Best Trade:               3.45%
  Worst Trade:              -1.87%
  Avg Trade:                0.08%

Risk Metrics:
  Max Drawdown Duration:    5 days 03:45:00
  Calmar Ratio:             1.40

============================================================
```

**Example**:
```python
runner.run_backtest(bt_data)
runner.print_results()
```

---

#### plot_results

```python
plot_results(save_path: str = 'results/backtest_plot.html') -> None
```

Generate interactive HTML plot of backtest results.

**Parameters**:
- `save_path` (str): Output path for HTML file. Default: `'results/backtest_plot.html'`

**Side Effects**:
- Creates parent directory if it doesn't exist
- Saves interactive Bokeh plot to HTML file
- Does NOT open browser automatically (set `open_browser=True` in `bt.plot()` call to change)

**Plot Features**:
- **Equity Curve**: Portfolio value over time
- **Drawdown**: Underwater chart showing peak-to-trough declines
- **Trade Markers**: Entry/exit points on price chart
- **Indicators**: RSI, MACD, Bollinger Bands overlaid
- **Interactive**: Zoom, pan, hover for details

**Example**:
```python
runner.run_backtest(bt_data)
runner.plot_results('results/my_backtest.html')

# Open in browser
import webbrowser
webbrowser.open('results/my_backtest.html')
```

---

#### optimize_strategy

```python
optimize_strategy(
    data: pd.DataFrame,
    cash: float = 10000,
    commission: float = 0.0004
) -> pd.Series
```

Optimize strategy parameters using grid search.

**Parameters**:
- `data` (pd.DataFrame): Prepared backtest data
- `cash` (float): Initial capital
- `commission` (float): Trading commission

**Returns**:
- `pd.Series`: Best backtest results with optimal parameters

**Optimization Grid** (hardcoded in method):
- `prediction_threshold`: [0.001, 0.002, 0.003, 0.004]
- `stop_loss_pct`: [0.003, 0.005, 0.007, 0.01]
- `take_profit_pct`: [0.006, 0.01, 0.015, 0.02]
- `position_size`: [0.5, 0.7, 0.9, 0.95]

**Optimization Objective**: Maximize Sharpe Ratio

**Constraint**: `take_profit_pct > stop_loss_pct` (TP must exceed SL)

**Side Effects**:
- Prints progress during optimization (can take several minutes)
- Prints optimal parameters when complete

**Warning**:
- Grid search with 4^4 = 256 combinations
- Runtime: 5-15 minutes depending on data size
- Risk of overfitting to test period

**Example**:
```python
print("Optimizing strategy parameters...")
optimal_results = runner.optimize_strategy(bt_data, cash=10000)

print(f"\nOptimal Sharpe Ratio: {optimal_results['Sharpe Ratio']:.2f}")
print(f"Optimal Parameters:")
print(f"  prediction_threshold: {optimal_results._strategy.prediction_threshold}")
print(f"  stop_loss_pct: {optimal_results._strategy.stop_loss_pct}")
print(f"  take_profit_pct: {optimal_results._strategy.take_profit_pct}")
print(f"  position_size: {optimal_results._strategy.position_size}")
```

---

## Usage Examples

### Complete Backtesting Pipeline

```python
from src.backtest.backtest_runner import BacktestRunner
from src.strategies.lstm_strategy import LSTMScalpingStrategy
import pandas as pd

# 1. Load data and predictions
print("Loading data...")
df = pd.read_csv('data/processed_data.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

predictions_df = pd.read_csv('data/predictions.csv')
predictions_norm = predictions_df['predicted'].values
actuals_norm = predictions_df['actual'].values

# 2. Prepare backtest data
print("Preparing backtest data...")
runner = BacktestRunner()

# Align predictions with main dataframe by datetime
pred_dates = pd.to_datetime(predictions_df['datetime'])
pred_dict = dict(zip(pred_dates, predictions_norm))
actual_dict = dict(zip(pred_dates, actuals_norm))

df['predicted_normalized'] = df['datetime'].map(pred_dict)
df['actual_normalized'] = df['datetime'].map(actual_dict)

# Filter to rows with predictions
df_with_preds = df[df['predicted_normalized'].notna()].copy()

bt_data = runner.prepare_data_for_backtest(
    df_with_preds,
    df_with_preds['predicted_normalized'].values,
    df_with_preds['actual_normalized'].values
)

print(f"Backtest data ready: {len(bt_data)} bars")

# 3. Run backtest
print("\nRunning backtest...")
results = runner.run_backtest(
    bt_data,
    strategy_class=LSTMScalpingStrategy,
    cash=runner.config['trading']['initial_capital'],
    commission=runner.config['backtesting']['commission']
)

# 4. Display and save results
runner.print_results()

results_df = pd.DataFrame([results])
results_df.to_csv('results/backtest_results.csv')
print("\nResults saved to results/backtest_results.csv")

# 5. Generate plot
runner.plot_results()
print("Interactive plot saved to results/backtest_plot.html")
```

---

### Comparing Multiple Strategies

```python
from src.strategies.lstm_strategy import (
    LSTMScalpingStrategy,
    AggressiveLSTMStrategy,
    ConservativeLSTMStrategy
)

strategies = {
    'Default': LSTMScalpingStrategy,
    'Aggressive': AggressiveLSTMStrategy,
    'Conservative': ConservativeLSTMStrategy
}

comparison_results = []

for name, strategy_class in strategies.items():
    print(f"\nTesting {name} strategy...")

    runner = BacktestRunner()
    results = runner.run_backtest(
        bt_data,
        strategy_class=strategy_class,
        cash=10000,
        commission=0.0004
    )

    comparison_results.append({
        'Strategy': name,
        'Return [%]': results['Return [%]'],
        'Sharpe Ratio': results['Sharpe Ratio'],
        'Max Drawdown [%]': results['Max. Drawdown [%]'],
        'Win Rate [%]': results['Win Rate [%]'],
        '# Trades': results['# Trades']
    })

# Display comparison
import pandas as pd
comparison_df = pd.DataFrame(comparison_results)
print("\n" + "=" * 60)
print("STRATEGY COMPARISON")
print("=" * 60)
print(comparison_df.to_string(index=False))

comparison_df.to_csv('results/strategy_comparison.csv', index=False)
```

**Output**:
```
============================================================
STRATEGY COMPARISON
============================================================
    Strategy  Return [%]  Sharpe Ratio  Max Drawdown [%]  Win Rate [%]  # Trades
     Default       12.45          1.23             -8.92         54.23       156
  Aggressive       18.67          0.98            -15.34         52.14       312
Conservative        8.91          1.56             -5.12         58.97        78
```

---

### Running as Script

The module includes a `main()` function for standalone execution:

```bash
cd crypto-scalping-bot
python src/backtest/backtest_runner.py
```

**What it does**:
1. Loads processed data from `data/processed_data.csv`
2. Loads predictions from `data/predictions.csv`
3. Aligns predictions with data by timestamp
4. Prepares backtest data
5. Runs default LSTM strategy
6. Runs aggressive and conservative variants
7. Saves results and comparison to `results/`
8. Generates interactive plot

**Output**:
```
============================================================
CRYPTO SCALPING BOT - BACKTEST
============================================================

1. Loading data and model...
2. Preparing predictions...
3. Preparing data for backtesting...
Backtest data ready: 64321 bars

4. Running backtest with default LSTM strategy...
[Results...]

============================================================
COMPARING STRATEGY VARIANTS
============================================================
[Comparison table...]

============================================================
BACKTEST COMPLETE
============================================================
```

---

## Performance Metrics

### Key Metrics Explained

**Return [%]**:
- Total portfolio return over backtest period
- Formula: `(Final Equity - Initial Equity) / Initial Equity * 100`
- Example: Start $10k, end $11.5k → 15% return

**Sharpe Ratio**:
- Risk-adjusted return metric
- Formula: `(Mean Return - Risk-Free Rate) / StdDev(Returns)`
- Interpretation:
  - `< 0`: Losing money
  - `0-1`: Suboptimal risk/reward
  - `1-2`: Good
  - `2-3`: Very good
  - `> 3`: Excellent (or suspicious - check for bugs)

**Max Drawdown [%]**:
- Largest peak-to-trough decline
- Measures worst-case loss from peak
- Example: Peak at $12k, trough at $10.5k → 12.5% drawdown
- Lower is better

**Win Rate [%]**:
- Percentage of profitable trades
- Formula: `Winning Trades / Total Trades * 100`
- Common misconception: Higher isn't always better
- Can have 40% win rate but profitable (large wins, small losses)

**Calmar Ratio**:
- Return / Max Drawdown
- Higher is better (more return per unit of drawdown risk)
- Example: 20% return, 10% drawdown → 2.0 Calmar

### Interpreting Results

**Good Backtest** (1m crypto scalping):
```
Return [%]: 10-30%
Sharpe Ratio: 1.0-2.0
Max Drawdown: 5-15%
Win Rate: 50-55%
# Trades: 50-200
```

**Warning Signs**:
```
Return [%]: > 100%        # Likely overfitting or data leakage
Sharpe Ratio: > 3         # Too good to be true
Max Drawdown: < 2%        # Unrealistic, check for bugs
Win Rate: > 60%           # Overfitting on this period
# Trades: 0               # Strategy not working
```

**Poor Backtest**:
```
Return [%]: < 0%          # Losing money
Sharpe Ratio: < 0         # Worse than random
Win Rate: < 48%           # Below random (50%)
# Trades: < 20            # Insufficient statistical significance
```

---

## Design Notes

### FractionalBacktest

Uses `FractionalBacktest` extension when available:
- Allows fractional position sizing (e.g., 0.5 BTC)
- Essential for expensive assets like BTC
- Falls back to standard `Backtest` if unavailable

**Import handling** (src/backtest/backtest_runner.py:10-13):
```python
try:
    from backtesting.lib import FractionalBacktest
except ImportError:
    FractionalBacktest = None  # Fallback
```

### Prediction Alignment

**Critical**: Predictions must align with backtest data by timestamp.

**Alignment Process** (backtest_runner.py:241-262):
1. Load predictions with datetime column
2. Create datetime → prediction dictionary
3. Map predictions to main dataframe by datetime
4. Filter to rows where predictions exist
5. Pass aligned data to backtest

**Common Bug**: Off-by-one errors cause strategy to use wrong predictions → no trades or nonsensical results.

### Commission and Slippage

**Commission**:
- Modeled as percentage per trade
- Default: 0.0004 (0.04% = OKX taker fee)
- Applied to both entry and exit (0.08% roundtrip)

**Slippage**:
- Fixed percentage in config (default 0.0001 = 0.01%)
- Not explicitly applied in current implementation
- Real slippage varies by order size and volatility

**Recommendation**: Use conservative commission (0.05-0.10%) for realistic modeling.

### Overfitting Prevention

**Best Practices**:
1. **Walk-forward validation**: Train on period 1, test on period 2, repeat
2. **Out-of-sample testing**: Test on completely different time period
3. **Different asset**: Test on ETH if trained on BTC
4. **Parameter stability**: Small parameter changes shouldn't drastically change results

**Current Limitation**: No built-in walk-forward optimization (manual implementation required).

---

## Related Documentation

- Strategies: [strategies-module.md](strategies-module.md)
- Data preparation: [data-module.md](data-module.md)
- Architecture: [ADR-0002](../adr/0002-backtesting-framework.md)
- Troubleshooting: [TROUBLESHOOTING.md](../TROUBLESHOOTING.md#backtesting-issues)
- Known limitations: [LIMITATIONS.md](../LIMITATIONS.md#trading-limitations)

---

**Source Code**: `src/backtest/backtest_runner.py`, `src/backtest/performance_analyzer.py`
**Framework**: backtesting.py
**Last Updated**: 2025-01-25
