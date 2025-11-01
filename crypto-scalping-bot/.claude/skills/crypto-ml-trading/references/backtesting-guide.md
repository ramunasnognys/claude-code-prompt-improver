# Backtesting Framework Guide

## Simulation Pipeline

```
Raw OHLCV → Features → LSTM Predictions → Backtest Engine → Metrics
  (1min)     (Tech Indicators)  (Change %)   (Execution Sim)   (Sharpe, DD)
```

## Backtesting.py Integration

### Why Backtesting.py?

- **Realistic simulation:** Executes trades at actual prices
- **Built-in metrics:** Sharpe, max DD, return, win rate
- **Order types:** Market, limit, stop-loss, take-profit
- **Cost simulation:** Commissions + slippage

### Data Format

```python
# Required columns for Strategy:
df = pd.DataFrame({
    'Date': timestamps,
    'Open': prices,
    'High': prices,
    'Low': prices,
    'Close': prices,
    'Volume': volumes,
    # Technical indicators (used by strategy)
    'RSI': rsi_values,
    'MACD': macd_values,
    'MACD_Signal': signal_values,
    # LSTM predictions
    'Predicted_Norm': lstm_predictions,     # Normalized prices
    'Predicted_Change': lstm_price_changes, # % changes
    # Required for position sizing
    'Close': prices  # Duplicated for backtesting
})

# Set date as index (Backtest.py requirement)
df.set_index(pd.DatetimeIndex(df['Date']), inplace=True)
```

### Backtest Execution

```python
from backtesting import Backtest
from src.strategies.lstm_strategy import LSTMScalpingStrategy

# Initialize
bt = Backtest(
    data=df_with_predictions,
    strategy=LSTMScalpingStrategy,
    cash=10000,
    commission=0.0004,        # OKX taker: 0.04%
    margin=0.1,               # 10x leverage available
    exclusive_orders=True     # No simultaneous buy/sell
)

# Run
stats = bt.run()

# Print metrics
print(f"Return: {stats['Return [%]']:.2f}%")
print(f"Sharpe: {stats['Sharpe Ratio']:.2f}")
print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
print(f"Trades: {stats['# Trades']}")
```

## Performance Interpretation

### Return vs Risk

```
Sharpe Ratio = (Return - Risk-free Rate) / Volatility

Example:
- Strategy return: 12% annual
- Risk-free rate: 4% (Treasury bills)
- Volatility: 16%

Sharpe = (0.12 - 0.04) / 0.16 = 0.50
```

**Sharpe interpretation:**
- 0.0 to 0.5: Mediocre (barely beats risk-free)
- 0.5 to 1.0: Good (worth the risk)
- 1.0+: Excellent (institutional quality)

### Maximum Drawdown Severity

```
Portfolio value: 10,000 → 12,000 → 10,800 → 8,500 → 11,500

Max DD = (8,500 - 12,000) / 12,000 = -29.2%
→ Worst peak-to-trough loss
```

**Severity guide:**
- <10%: Conservative strategy
- 10-20%: Moderate risk
- 20-30%: Aggressive
- >30%: Unacceptable (can't handle)

### Win Rate Significance

```
Win Rate = Winning Trades / Total Trades

Example:
- 50 trades total
- 25 wins, 25 losses
- Win Rate = 50%

BUT with 2.5:1 reward/risk ratio:
Profit = 25 × 2.5 - 25 × 1.0 = 62.5 units
→ Profitable even at 50% win rate!
```

**Key insight:** Win rate < 50% can still be profitable with right risk/reward

## Out-of-Sample Testing (Critical!)

### Walk-Forward Analysis

```
Scenario: 1 year of data

Month 1-9 (Train)   Month 10 (Val)   Month 11-12 (Test)
├─ Train model      ├─ Tune params   ├─ Evaluate
└─ Optimize params  └─ Watch for O/F └─ No modifications!

Repeat:
Month 2-10 (Train)   Month 11 (Val)   Month 12 + Jan (Test)
```

**Purpose:** Simulate real trading where future is unknown

### Avoiding Overfitting

```
❌ Overfitting scenario:
- Tune strategy parameters on backtest period
- Get 50% Sharpe
- Deploy → Get -0.5% Sharpe (disaster!)

✅ Correct approach:
- Split data (train/val/test) FIRST
- Never look at test data
- Tune only on train/val
- Report test results as final

Result: Test Sharpe ≈ Live Sharpe
```

## Fee Realistic Simulation

### Commission Calculation

```
OKX Perpetual Futures Fees:
- Taker: 0.04% (market orders)
- Maker: 0.02% (limit orders)

Round-trip cost (market order):
Entry: 1.0 BTC @ $40,000 = $40,000
  → Commission: 0.04% × $40,000 = $16

Exit: 1.0 BTC @ $40,100 = $40,100
  → Commission: 0.04% × $40,100 = $16

Total cost: $32 (0.08% of position)
```

### Slippage Model

```
Expected price: $40,000
Actual execution (market order): $40,004

Slippage = $4 / $40,000 = 0.01%

Backtesting formula:
- Buy:  price × (1 + slippage + commission)
- Sell: price × (1 - slippage - commission)
```

**Conservative estimate for crypto:**
- Large liquid pairs (BTC/USDT): 0.01%
- Medium pairs (ETH/USDT): 0.02%
- Small/illiquid: 0.05-0.1%

## Metric Interpretation Reference

### Profit Factor

```
Profit Factor = Gross Profit / Gross Loss

Example:
- 20 winning trades: +$1,200 total
- 30 losing trades: -$600 total

Profit Factor = 1,200 / 600 = 2.0
```

**Target:** >1.5 (earn 1.5x losses made)

### Recovery Factor

```
Recovery Factor = Net Profit / Max Drawdown

Example:
- Net profit: $5,000
- Max drawdown: $2,000

Recovery = 5,000 / 2,000 = 2.5
```

**Interpretation:**
- <1: Profit less than max loss (risky)
- 1-2: Barely recovers from drawdown
- 2+: Healthy recovery speed

### Calmar Ratio

```
Calmar = Annual Return / Max Drawdown

Example:
- Annual return: 15%
- Max drawdown: 30%

Calmar = 0.15 / 0.30 = 0.5
```

**Benchmark:**
- <0.2: Poor risk-adjusted return
- 0.5+: Acceptable
- 1.0+: Excellent

## Common Backtest Gotchas

### Gap Openings

Overnight/weekend gaps not simulated in 1m data:
```
Friday 16:59: $40,000
Monday 09:30: $39,500 (gap down)

Backtest: Continuous ✓
Reality: Gap risk ✗

Mitigation: Use daily stops, account for gaps
```

### Survivorship Bias

Testing only on pairs that exist today:
```
2020: 100 altcoins
2025: 50 still tradeable (50 delisted)

Backtest success rate: Artificially inflated
→ Included only survivors
```

### Low Volume Periods

Tight spreads during high volume:
```
Day: High volume period
- Bid: $40,000
- Ask: $40,002
- Slippage: 0.01%

Night: Low volume
- Bid: $40,000
- Ask: $40,100 (100x spread!)
- Slippage: 0.2%

Backtest assumes constant slippage ✗
```

## Validation Checklist

Before deploying strategy:

- [ ] Data not contaminated by future prices
- [ ] Test period chronologically after train
- [ ] Test period >= 2 weeks minimum
- [ ] Sharpe ratio > 0 (better than random)
- [ ] Profit factor > 1.5
- [ ] Max drawdown < 20-30%
- [ ] Win rate > 40% OR positive expectancy
- [ ] Trade count: 20-500 (not 0 or 10,000)
- [ ] Walk-forward analysis shows consistency
- [ ] Multiple assets tested (not single pair)

## Metrics to Track During Tuning

Create tuning log:

```
Parameter          | Sharpe | Max DD | Win Rate | Trades | Notes
prediction_0.001   | 0.45   | -18%   | 52%      | 245    | Too many
prediction_0.002   | 0.52   | -16%   | 48%      | 168    | ✓ Best
prediction_0.003   | 0.38   | -20%   | 45%      | 95     | Too few
```

**Decision rule:** Highest Sharpe on test set, but verify profit factor >1.5
