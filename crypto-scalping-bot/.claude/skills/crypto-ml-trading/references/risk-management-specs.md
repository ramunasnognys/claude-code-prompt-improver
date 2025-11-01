# Risk Management Specifications

## Position Sizing Formula

### Kelly Criterion (Optimal Sizing)

Kelly % = (Sharpe × σ) / (Profit Factor - 1)

Where:
- Sharpe = Sharpe ratio of strategy
- σ = Volatility (standard deviation of returns)
- Profit Factor = Gross profit / Gross loss

```python
def kelly_criterion(sharpe, volatility, profit_factor):
    if profit_factor <= 1:
        return 0  # Negative expectancy
    return (sharpe * volatility) / (profit_factor - 1)

# Example
kelly = kelly_criterion(0.5, 0.2, 1.8)
# kelly = (0.5 × 0.2) / (1.8 - 1) = 0.125 = 12.5%

# Safe usage (avoid bankruptcy): Kelly / 4 = 3.1%
# Aggressive usage: Kelly / 2 = 6.25%
```

### Fractional Kelly (Recommended)

```
Full Kelly: Too aggressive, risks ruin
Half Kelly: Balanced growth and safety
Quarter Kelly: Conservative, slow growth

Current config (30% per trade):
→ Aggressive Kelly equivalent
→ Use when high confidence in backtest
→ Reduce to 10-20% when model is new
```

### Position Size Calculation

```python
equity = 10000
max_position_size = 0.3
risk_per_trade = equity * max_position_size
# risk_per_trade = $3,000 per trade

# For 5x leverage:
notional_value = risk_per_trade * 5
# notional_value = $15,000

# BTC @ $40,000:
btc_to_buy = notional_value / 40000
# btc_to_buy = 0.375 BTC
```

## Stop Loss Implementation

### Percentage-Based (Current)

```
Entry price: $40,000
Stop loss %: 1%
Stop price: $40,000 × (1 - 0.01) = $39,600

Maximum loss per trade: $400 (1% of position)
With 30% position size: $3,000 × 1% = $30 actual loss
```

### ATR-Based (Alternative)

```
ATR(14) = $120

Stop distance: 2 × ATR = $240
Entry: $40,000
Stop: $40,000 - $240 = $39,760

Adapts to volatility:
- Calm markets: Tight stops (saves $ in small moves)
- Volatile markets: Wide stops (avoids whipsaws)
```

### Time-Based (Advanced)

```
Entry time: 09:00
Max hold: 30 minutes
Forced exit: 09:30 (regardless of profit/loss)

Prevents: Overnight gap risk, execution drift
```

## Take Profit Levels

### Single Level (Simple)

```
Entry: $40,000
Take profit: 2.5% = $41,000

All profit crystallized at TP
```

### Multi-Level Pyramid (Advanced)

```
Entry: $40,000

Position 1/3: Close at 1% (+$133)
Position 1/3: Close at 2.5% (+$333)
Position 1/3: Close at 5% (+$667)

Average profit: 2.83%
Locks in gains gradually
Keeps some exposure if trending continues
```

### Trailing Stop (Dynamic)

```
Entry: $40,000
Peak reached: $40,500

Trailing stop distance: 1%
Stop level: $40,500 × (1 - 0.01) = $40,095

As price rises → Stop rises with it
Captures uptrend, exits on reversal
```

## Risk/Reward Ratio

### Expectancy Formula

```
E = (Win% × AvgWin) - (Loss% × AvgLoss)

Example:
Win%: 50%, AvgWin: $100
Loss%: 50%, AvgLoss: $50

E = (0.5 × 100) - (0.5 × 50) = $25
Expected value per trade: +$25
```

### Ratio Targets

| RR Ratio | Required Win% | Interpretation |
|----------|---------------|-----------------|
| 1:1 | >50% | Coin flip expected |
| 1.5:1 | >40% | Good probability |
| 2.0:1 | >33% | Reasonable |
| 2.5:1 | >28.6% | High threshold |
| 3:1 | >25% | Only need 1/4 wins |

**Current config: 2.5:1 ratio**
```
TP: 2.5% profit
SL: 1% loss

Need: 1 / (1 + 2.5) = 28.6% win rate minimum
With 45% actual win rate: Expected profit each trade
```

## Leverage Impact

### Risk Amplification

```
Position size: $10,000 (no leverage)
- 1% loss = $100
- 2.5% gain = $250

With 5x leverage: $50,000 notional
- 1% loss = $500 (5x worse)
- 2.5% gain = $1,250 (5x better)
```

### Leverage Safety Rules

```
Leverage = Account Size / Notional Position

Safe leverage:
- 2x: Very conservative
- 5x: Moderate (current)
- 10x: Aggressive
- 20x+: Dangerous (one bad trade = ruin)

For crypto volatility: Use 5x max
For known conditions (trending): 10x acceptable
```

## Drawdown Management

### Maximum Daily Loss

```yaml
max_daily_loss: 0.05  # 5% equity loss → stop trading

Example:
Opening equity: $10,000
After trades: $9,500
Loss: 5% → STOP TRADING

Next day: Reset, can trade again
```

**Rationale:**
- Prevents revenge trading (emotional decisions)
- Protects capital when signal is weak
- Resets mind for next opportunity

### Consecutive Loss Limit

```
Consecutive losses: 3, 4, 5...

Action: After 3 consecutive losses
- Stop trading for rest of day
- Review recent trades
- Check if signal quality degraded
- Only resume after analysis

Reason: Signal may have broken in current market
```

### Recovery Time

```
Max drawdown: -20% ($2,000 loss)
Assume: 1% profit per day

Days to recover: 20% / 1% ≈ 20 days

Planning: If aiming to recoup in 5 days
Required daily profit: 20% / 5 = 4%
→ More aggressive parameters needed
→ Higher risk of worse drawdowns
```

## Volatility Adjustment

### Volatility Regimes

```
Low volatility (ATR < 50):
- Tight stops: 0.5% (quick exit)
- Wide TPs: 3% (let winner run)
- More frequent trades

High volatility (ATR > 200):
- Wide stops: 1.5-2% (survive noise)
- Tight TPs: 1.5% (book quick gains)
- Fewer trades
```

### VIX-Style Scaling

```python
def position_size_by_volatility(base_size, volatility_pct):
    # Reduce size as volatility increases
    volatility_adjustment = 1 / (1 + volatility_pct)
    return base_size * volatility_adjustment

# Example
# Base: 30% position
# Current volatility: 5%
# Adjusted: 30% × (1 / 1.05) = 28.6%

# High volatility: 20%
# Adjusted: 30% × (1 / 1.20) = 25%
```

## Correlation Risk

### Single Asset Strategy

```
Trading only BTC/USDT:
- All exposure to BTC
- No diversification
- If BTC crashes, entire portfolio crashes

Solution: Trade multiple uncorrelated pairs
```

### Correlation Matrix

```
        BTC   ETH   SOL
BTC    1.0   0.75  0.65
ETH    0.75  1.0   0.70
SOL    0.65  0.70  1.0

High correlation (>0.8) → Similar moves → No diversification
Medium (0.5-0.8) → Some independence
Low (<0.5) → Different dynamics
```

**Portfolio approach:**
- BTC (large cap)
- ETH (smart contracts)
- SOL (alternative L1)

Spread: 3 positions × 30% position size = 90% utilization

## Stress Testing

### What-If Scenarios

```
Current parameters:
- SL: 1%, TP: 2.5%, Win%: 45%

Stress test: Win rate drops to 30%
- Expected loss per trade: (0.3 × 2.5) - (0.7 × 1%) = 0.53%
- After 20 trades: -10% portfolio loss
- Acceptable? Yes (within max daily loss)

Stress test: Win rate drops to 20%
- Expected loss: (0.2 × 2.5) - (0.8 × 1%) = -0.3% per trade
- After 10 trades: -3% cumulative loss
- Acceptable? Marginal

Conclusion: Strategy breaks if real win rate < 30%
→ Real-time monitoring essential
```

## Live Trading Adjustments

### Parameter De-Risking

```
Backtest conditions: Ideal market, perfect fills
Reality: Slippage, partial fills, gaps

Live adjustments:
- Reduce position size: 30% → 20%
- Widen stop loss: 1% → 1.5%
- Tighten take profit: 2.5% → 1.5%

Effect: Lower returns, but account survives worse slippage
```

### Monitoring Checklist

- [ ] Win rate tracking (target: >40%)
- [ ] Sharpe ratio real-time (target: >0)
- [ ] Max drawdown watch (stop if >15%)
- [ ] Trade quality check (commission impact)
- [ ] Model drift: Refit weekly/monthly
