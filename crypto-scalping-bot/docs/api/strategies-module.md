# Strategies Module API Reference

The strategies module implements trading strategies that combine LSTM predictions with technical indicators to generate buy/sell signals.

**Module Path**: `src/strategies/`

**Files**:
- `lstm_strategy.py` - LSTM-based scalping strategies with variants

---

## Table of Contents

1. [LSTMScalpingStrategy](#lstmscalpingstrategy)
2. [AggressiveLSTMStrategy](#aggressivelstmstrategy)
3. [ConservativeLSTMStrategy](#conservativelstmstrategy)
4. [Usage Examples](#usage-examples)

---

## LSTMScalpingStrategy

**Class**: `LSTMScalpingStrategy`
**File**: `src/strategies/lstm_strategy.py`
**Purpose**: Default LSTM-based scalping strategy for perpetual futures

**Inherits**: `backtesting.Strategy`

### Overview

Combines LSTM price predictions with technical indicator confirmations to generate long/short signals. Uses normalized predictions directly without denormalization (see [ADR-0005](../adr/0005-normalized-predictions.md)).

**Signal Generation Flow**:
1. LSTM predicts next period's normalized price
2. Calculate predicted price change percentage in normalized space
3. Check if change exceeds threshold (filters noise)
4. Confirm with RSI (avoid overbought/oversold extremes)
5. Confirm with MACD (align with trend direction)
6. Execute with stop-loss and take-profit

---

### Strategy Parameters

**Optimizable class attributes** (can be modified or optimized):

```python
prediction_threshold = 0.0005  # Min predicted change (0.05%)
rsi_oversold = 30              # RSI lower bound
rsi_overbought = 70            # RSI upper bound
stop_loss_pct = 0.005          # Stop loss % (0.5%)
take_profit_pct = 0.01         # Take profit % (1.0%)
position_size = 0.95           # Equity fraction per trade (95%)
```

**Parameters Explained**:

- **prediction_threshold** (float): Minimum predicted price change to trigger signal
  - Default: `0.0005` (0.05% change)
  - Lower = more signals (aggressive)
  - Higher = fewer signals (selective)
  - Expressed as decimal: `0.001` = 0.1%

- **rsi_oversold** (int): RSI level below which market considered oversold
  - Default: `30`
  - Long signals require RSI < `rsi_overbought` (not overbought)
  - Short signals require RSI > `rsi_oversold` (not oversold)

- **rsi_overbought** (int): RSI level above which market considered overbought
  - Default: `70`

- **stop_loss_pct** (float): Stop loss distance from entry
  - Default: `0.005` (0.5%)
  - Tighter stops = less loss per trade, more frequent stopouts
  - Wider stops = larger losses possible, more room for volatility

- **take_profit_pct** (float): Take profit distance from entry
  - Default: `0.01` (1.0%)
  - Should be > `stop_loss_pct` for positive expectancy
  - Common ratio: 2:1 (TP = 2x SL)

- **position_size** (float): Fraction of equity to use per trade
  - Default: `0.95` (95%)
  - With `FractionalBacktest`: 0.95 = use 95% of available capital
  - Range: 0-1 (0.5 = 50%, 1.0 = 100%)

---

### Required DataFrame Columns

**Input**: DataFrame passed to Backtest must include:

**OHLCV** (standard backtesting.py format):
- `Open` (float): Opening price
- `High` (float): High price
- `Low` (float): Low price
- `Close` (float): Closing price
- `Volume` (float): Trading volume

**Technical Indicators**:
- `RSI` (float): Relative Strength Index [0-100]
- `MACD` (float): MACD line
- `MACD_Signal` (float): MACD signal line
- `BB_Upper` (float): Upper Bollinger Band
- `BB_Lower` (float): Lower Bollinger Band

**LSTM Predictions** (normalized [0-1]):
- `Predicted_Norm` (float): LSTM predicted normalized price
- `Actual_Norm` (float): Actual normalized price (for alignment)

**Note**: Column names are case-sensitive. See `backtest_runner.py:prepare_data_for_backtest()` for preparation logic.

---

### Methods

#### init

```python
def init(self) -> None
```

Initialize strategy: load predictions and calculate signal strength.

**Called automatically** by backtesting.py framework before first `next()` call.

**Calculations**:
1. Extracts predictions and actuals from DataFrame
2. Calculates predicted price change percentage:
   ```python
   prev_actual_norm = actuals_norm[i-1]
   current_pred_norm = predictions_norm[i]
   price_change_predicted = (current_pred_norm - prev_actual_norm) / prev_actual_norm
   ```
3. Prints diagnostic statistics about predictions

**Console Output Example**:
```
============================================================
Strategy Initialization - Prediction Analysis
============================================================
Prediction changes mean: 0.0012%
Prediction changes std: 0.3456%
Prediction changes range: -2.1234% to 1.9876%
Strategy threshold: ±0.0500%
Potential bullish signals: 1234 (12.34%)
Potential bearish signals: 1198 (11.98%)
============================================================
```

**Design Note**: Prediction alignment critical here. See `lstm_strategy.py:72-82` for detailed comments.

---

#### next

```python
def next(self) -> None
```

Execute strategy logic for each new candle.

**Called automatically** by backtesting.py for every bar in the dataset.

**Flow**:
1. Skip if insufficient data (`len(self.data) < 2`)
2. Get current prediction and indicators
3. If in position: check exit conditions (`_manage_position()`)
4. If flat: evaluate entry conditions (`_should_go_long()` / `_should_go_short()`)
5. Execute trades via `_open_long()` / `_open_short()`

**No manual implementation needed** - framework calls this automatically.

---

#### _should_go_long

```python
def _should_go_long(
    self,
    prediction: float,
    rsi: float,
    macd: float,
    macd_signal: float
) -> bool
```

Evaluate long entry conditions.

**Parameters**:
- `prediction` (float): Predicted price change percentage
- `rsi` (float): Current RSI value [0-100]
- `macd` (float): MACD line value
- `macd_signal` (float): MACD signal line value

**Returns**:
- `bool`: True if all conditions met, False otherwise

**Long Entry Logic** (all must be True):
1. `prediction > prediction_threshold` - LSTM predicts bullish move
2. `rsi < rsi_overbought` - Room to move up (not overbought)
3. `macd > macd_signal` - MACD confirms uptrend

**Example**:
```python
# Current state:
# prediction = 0.0008 (0.08% predicted increase)
# rsi = 65
# macd = 15.2, macd_signal = 14.8

should_enter = self._should_go_long(0.0008, 65, 15.2, 14.8)
# Returns: True (all conditions met)

# If RSI = 75 (overbought):
should_enter = self._should_go_long(0.0008, 75, 15.2, 14.8)
# Returns: False (RSI too high, risk of reversal)
```

---

#### _should_go_short

```python
def _should_go_short(
    self,
    prediction: float,
    rsi: float,
    macd: float,
    macd_signal: float
) -> bool
```

Evaluate short entry conditions.

**Parameters**: Same as `_should_go_long()`

**Returns**:
- `bool`: True if all conditions met, False otherwise

**Short Entry Logic** (all must be True):
1. `prediction < -prediction_threshold` - LSTM predicts bearish move
2. `rsi > rsi_oversold` - Room to move down (not oversold)
3. `macd < macd_signal` - MACD confirms downtrend

---

#### _open_long

```python
def _open_long(self) -> None
```

Open a long position with risk management.

**Execution**:
1. Calculate entry price from current close
2. Set stop-loss: `entry_price * (1 - stop_loss_pct)`
3. Set take-profit: `entry_price * (1 + take_profit_pct)`
4. Execute buy with fractional position sizing

**Example**:
```python
# Current close: $50,000
# stop_loss_pct: 0.005 (0.5%)
# take_profit_pct: 0.01 (1.0%)

# Calculates:
# SL: $50,000 * 0.995 = $49,750
# TP: $50,000 * 1.01 = $50,500

# Executes:
self.buy(size=0.95, sl=49750, tp=50500)
```

**Position Size**: With `FractionalBacktest`, `size=0.95` uses 95% of available equity.

---

#### _open_short

```python
def _open_short(self) -> None
```

Open a short position with risk management.

**Execution**:
1. Calculate entry price
2. Set stop-loss: `entry_price * (1 + stop_loss_pct)` *(higher for shorts)*
3. Set take-profit: `entry_price * (1 - take_profit_pct)` *(lower for shorts)*
4. Execute sell

**Example**:
```python
# Current close: $50,000
# stop_loss_pct: 0.005
# take_profit_pct: 0.01

# Calculates:
# SL: $50,000 * 1.005 = $50,250 (above entry for shorts)
# TP: $50,000 * 0.99 = $49,500 (below entry for shorts)

self.sell(size=0.95, sl=50250, tp=49500)
```

---

#### _manage_position

```python
def _manage_position(self) -> None
```

Manage existing position with exit logic.

**Called from** `next()` when `self.position` is not None.

**Exit Conditions**:

**For Long Positions**:
- Close if prediction turns bearish: `prediction < -prediction_threshold`
- Example: Holding long, but LSTM now predicts -0.1% move → exit

**For Short Positions**:
- Close if prediction turns bullish: `prediction > prediction_threshold`
- Example: Holding short, but LSTM now predicts +0.08% move → exit

**Design**: Allows early exit before SL/TP hit if LSTM signals reversal.

---

## AggressiveLSTMStrategy

**Class**: `AggressiveLSTMStrategy`
**Inherits**: `LSTMScalpingStrategy`
**Purpose**: High-frequency trading variant for active scalping

### Parameter Overrides

```python
prediction_threshold = 0.0002  # 0.02% (very sensitive)
stop_loss_pct = 0.003          # 0.3% (tight stop)
take_profit_pct = 0.006        # 0.6% (quick target)
position_size = 0.98           # 98% equity (aggressive)
```

### Characteristics

**Pros**:
- More trades (10-50% more than default)
- Quick exits minimize exposure
- Maximizes capital efficiency

**Cons**:
- Higher transaction costs (more trades)
- More sensitive to noise and false signals
- Tighter stops = more stopouts
- Higher drawdown potential

**Use When**:
- High confidence in model accuracy
- Liquid markets with tight spreads
- Can tolerate higher trade frequency
- Backtests show model has >60% direction accuracy

**Avoid When**:
- Volatile, choppy markets
- Wide spreads or high slippage
- Model direction accuracy <55%

---

## ConservativeLSTMStrategy

**Class**: `ConservativeLSTMStrategy`
**Inherits**: `LSTMScalpingStrategy`
**Purpose**: Risk-averse variant for stable trading

### Parameter Overrides

```python
prediction_threshold = 0.001   # 0.1% (less sensitive)
stop_loss_pct = 0.01           # 1.0% (wide stop)
take_profit_pct = 0.02         # 2.0% (patient target)
position_size = 0.5            # 50% equity (conservative)
```

### Characteristics

**Pros**:
- Fewer, higher-quality trades
- Wide stops accommodate volatility
- Lower drawdown
- Capital preservation focus

**Cons**:
- Misses quick opportunities
- Lower capital efficiency (50% idle)
- May underperform in trending markets
- Fewer trades = less statistical significance

**Use When**:
- Model accuracy uncertain or in testing
- Volatile markets with wide swings
- Priority is capital preservation
- Learning or validating strategy

**Avoid When**:
- Confident in model (underutilizes edge)
- Low-volatility markets (stops too wide)
- Need frequent trades for statistics

---

## Usage Examples

### Basic Backtest with Default Strategy

```python
from backtesting import Backtest
from src.strategies.lstm_strategy import LSTMScalpingStrategy
import pandas as pd

# Load prepared data (with LSTM predictions and indicators)
data = pd.read_csv('data/backtest_data.csv', index_col='datetime', parse_dates=True)

# Ensure required columns present
required_cols = ['Open', 'High', 'Low', 'Close', 'Volume',
                  'RSI', 'MACD', 'MACD_Signal',
                  'Predicted_Norm', 'Actual_Norm']
assert all(col in data.columns for col in required_cols)

# Run backtest
bt = Backtest(
    data,
    LSTMScalpingStrategy,
    cash=10000,
    commission=0.0004,  # 0.04% taker fee
    exclusive_orders=True
)

stats = bt.run()
print(stats)

# Plot results
bt.plot(filename='results/backtest.html', open_browser=True)
```

---

### Comparing Strategy Variants

```python
from backtesting import Backtest
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

results = {}

for name, strategy_class in strategies.items():
    bt = Backtest(data, strategy_class, cash=10000, commission=0.0004)
    stats = bt.run()

    results[name] = {
        'Return [%]': stats['Return [%]'],
        'Sharpe Ratio': stats['Sharpe Ratio'],
        'Max Drawdown [%]': stats['Max. Drawdown [%]'],
        '# Trades': stats['# Trades'],
        'Win Rate [%]': stats['Win Rate [%]']
    }

# Display comparison
import pandas as pd
comparison_df = pd.DataFrame(results).T
print(comparison_df)

# Output:
#              Return [%]  Sharpe Ratio  Max Drawdown [%]  # Trades  Win Rate [%]
# Default           12.45          1.23             -8.92       156         54.23
# Aggressive        18.67          0.98            -15.34       312         52.14
# Conservative       8.91          1.56             -5.12        78         58.97
```

---

### Parameter Optimization

```python
from backtesting import Backtest
from src.strategies.lstm_strategy import LSTMScalpingStrategy

bt = Backtest(data, LSTMScalpingStrategy, cash=10000, commission=0.0004)

# Optimize parameters
stats = bt.optimize(
    prediction_threshold=[0.0002, 0.0005, 0.001, 0.002],
    stop_loss_pct=[0.003, 0.005, 0.007, 0.01],
    take_profit_pct=[0.006, 0.01, 0.015, 0.02],
    position_size=[0.5, 0.7, 0.9, 0.95],
    maximize='Sharpe Ratio',
    constraint=lambda p: p.take_profit_pct > p.stop_loss_pct  # TP must exceed SL
)

print("\nOptimal Parameters:")
print(f"prediction_threshold: {stats._strategy.prediction_threshold}")
print(f"stop_loss_pct: {stats._strategy.stop_loss_pct}")
print(f"take_profit_pct: {stats._strategy.take_profit_pct}")
print(f"position_size: {stats._strategy.position_size}")

print(f"\nOptimized Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
```

---

### Custom Strategy Variant

```python
from src.strategies.lstm_strategy import LSTMScalpingStrategy

class CustomStrategy(LSTMScalpingStrategy):
    """Custom variant with dynamic position sizing based on prediction confidence."""

    prediction_threshold = 0.0005
    stop_loss_pct = 0.005
    take_profit_pct = 0.01

    def _open_long(self):
        """Adjust position size based on prediction strength."""
        prediction = self.price_change_predicted[-1]

        # Scale position size by prediction confidence
        # Stronger predictions = larger positions
        confidence = abs(prediction) / self.prediction_threshold
        size = min(0.5 + (confidence * 0.1), 0.95)  # Range: 0.5 to 0.95

        entry_price = self.data.Close[-1]
        sl_price = entry_price * (1 - self.stop_loss_pct)
        tp_price = entry_price * (1 + self.take_profit_pct)

        self.buy(size=size, sl=sl_price, tp=tp_price)

    # Similar for _open_short...

# Use custom strategy
bt = Backtest(data, CustomStrategy, cash=10000, commission=0.0004)
stats = bt.run()
```

---

## Design Notes

### Normalized Predictions

**Critical Design Decision** (see [ADR-0005](../adr/0005-normalized-predictions.md)):

Strategy uses predictions in normalized space without denormalization:
```python
# Percentage change in normalized space ≈ percentage change in real price
price_change_pct = (pred_norm[i] - actual_norm[i-1]) / actual_norm[i-1]
```

**Advantages**:
- Simpler code, no scaler dependency
- Fewer bugs (no inverse transform errors)
- Faster execution

**Caveat**:
- Less intuitive for humans ("0.0008 change" vs "$40 move")
- Approximation breaks down for large changes (>5%)

### Risk Management

**Stop-Loss and Take-Profit**:
- Set at position entry, managed by backtesting.py framework
- Automatically close position if price hits levels
- Overridable via `_manage_position()` for early exits

**Position Sizing**:
- Fixed fraction of equity (not dynamic)
- For dynamic sizing (e.g., Kelly criterion, volatility-based), override `_open_long()/_open_short()`

### Indicator Confirmations

**Why RSI and MACD?**
- Filters LSTM signals in extreme conditions
- Reduces false signals during consolidation
- Proven indicators with standard parameters

**Trade-off**:
- Filters some valid LSTM signals (conservative bias)
- May underperform pure LSTM in strong trends
- To test LSTM alone, remove confirmations in `_should_go_long()/_should_go_short()`

### Strategy Performance

**Realistic Expectations** (1m crypto scalping):
- **Win Rate**: 50-55% (slightly above breakeven)
- **Sharpe Ratio**: 0.5-1.5 (1+ is good)
- **Max Drawdown**: 10-20%
- **# Trades**: 50-200 per month

**Warning Signs**:
- Win rate >60%: Likely overfitting
- Sharpe >3: Data leakage or bugs
- # Trades = 0: Threshold too high or predictions misaligned

---

## Related Documentation

- Data preparation: [data-module.md](data-module.md)
- Model training: [models-module.md](models-module.md)
- Backtesting: [backtest-module.md](backtest-module.md)
- ADR on predictions: [ADR-0005](../adr/0005-normalized-predictions.md)
- ADR on indicators: [ADR-0003](../adr/0003-technical-indicators.md)
- Troubleshooting: [TROUBLESHOOTING.md](../TROUBLESHOOTING.md#backtesting-issues)

---

**Source Code**: `src/strategies/lstm_strategy.py`
**Framework**: backtesting.py Strategy class
**Last Updated**: 2025-01-25
