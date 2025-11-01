# Skill Testing Guide

## How to Verify crypto-ml-trading Skill Works

Use these prompt examples to test that the skill triggers and applies its standards.

---

## Test 1: Prompt Trigger Verification

**Prompt:**
```
I'm tuning the LSTM model architecture. Should I increase lstm_units from [64, 32] to [128, 64, 32]?
What's the tradeoff vs training time?
```

**Expected:** Skill should trigger on "LSTM" + "architecture"
**Skill response should include:**
- Reference to 3-layer design rationale
- Trade-off explanation (capacity vs overfitting vs speed)
- Link to ml-trading-patterns.md for details

---

## Test 2: Risk Management Standards

**Prompt:**
```
My strategy uses stop_loss_pct: 0.005 and take_profit_pct: 0.01.
Is this a good risk/reward ratio for crypto scalping?
```

**Expected:** Skill should trigger on "risk/reward" + "stop_loss"
**Skill response should:**
- Calculate RR ratio: 0.01 / 0.005 = 2:1
- Reference target 2.5:1 from standards
- Suggest required win rate: 33% minimum
- Point to risk-management-specs.md

---

## Test 3: Backtesting Validation

**Prompt:**
```
I'm getting amazing backtest results: 80% return, 2.5 Sharpe ratio on my 6-month backtest.
But the model has never been tested on data after training. How do I know it will work live?
```

**Expected:** Skill should trigger on "backtest" + "live trading"
**Skill response should:**
- Identify data leakage risk (test period overlaps training)
- Reference backtesting-guide.md walk-forward section
- Recommend: Train on months 1-4, test on months 5-6
- Warn: Backtest metrics won't match live performance if overlapped

---

## Test 4: Indicator Configuration

**Prompt:**
```
I want to add RSI confirmation to my LSTM signals. Should I use RSI(14), RSI(7), or RSI(21)?
```

**Expected:** Skill should trigger on "RSI" + "configuration"
**Skill response should:**
- Reference RSI(14) as standard (from SKILL.md)
- Explain: 14 = standard, 7 = faster, 21 = slower
- Point to indicators.rsi_period in config reference
- Note: RSI helps but avoid over-engineering signals

---

## Test 5: Hyperparameter Tuning Workflow

**Prompt:**
```
My strategy has too many false signals (200 trades/day). How should I adjust parameters?
```

**Expected:** Skill should trigger on "hyperparameter" or "tuning"
**Skill response should:**
- Reference common tuning scenarios from SKILL.md
- Suggest: Raise prediction_threshold (0.002 → 0.005)
- Recommend single-parameter tuning workflow
- Link to configuration best practices section

---

## Test 6: Feature Engineering

**Prompt:**
```
I'm adding 10 new technical indicators to improve model accuracy. Will this help?
```

**Expected:** Skill should trigger on "features" + "LSTM model"
**Skill response should:**
- Warn: More features ≠ better accuracy
- Reference ml-trading-patterns.md feature hierarchy
- Explain: Simple features (price, volume) often dominate
- Suggest: Test new features on validation set first

---

## Test 7: Drawdown Management

**Prompt:**
```
My max drawdown went from 15% to 45% after a market crash.
What's a reasonable drawdown limit for a trading bot?
```

**Expected:** Skill should trigger on "drawdown" + "risk"
**Skill response should:**
- Reference max_daily_loss circuit breaker (5%)
- Explain max acceptable drawdown: 20-30%
- Point to risk-management-specs.md for recovery calculations
- Suggest reducing leverage if DD > 30%

---

## Test 8: Live Trading Adjustment

**Prompt:**
```
My backtest showed 15% annual return with 0.8 Sharpe ratio, but I'm considering going live.
Should I use the same parameters I backtested?
```

**Expected:** Skill should trigger on "live trading" + "backtest parameters"
**Skill response should:**
- Reference live trading adjustments section
- Recommend de-risking: Reduce position size 30% → 20%
- Widen stop loss: 1% → 1.5%
- Explain: Account for real slippage, gaps, partial fills
- Point to monitoring checklist

---

## Test 9: Configuration Validation

**Prompt:**
```
Before I train the model, how can I make sure my config.yaml is valid?
```

**Expected:** Skill should trigger on "config" + "validate"
**Skill response should:**
- Mention validate_config.py script
- Show usage: `python .claude/skills/crypto-ml-trading/scripts/validate_config.py`
- Explain what it checks (ranges, consistency, red flags)
- Note: Script catches common errors before expensive training

---

## Test 10: Complete Pipeline

**Prompt:**
```
I want to run a full backtest from scratch: fetch data, train the LSTM, and backtest the strategy.
What's the recommended workflow?
```

**Expected:** Skill should trigger on "pipeline" + "backtest"
**Skill response should:**
- Reference core architecture pattern from SKILL.md
- Mention quick_backtest.sh script
- Show usage: `bash .claude/skills/crypto-ml-trading/scripts/quick_backtest.sh`
- Outline steps: validate → fetch → train → backtest → analyze

---

## Manual Testing Checklist

Use this checklist to verify skill functionality:

- [ ] **Trigger test:** Ask about LSTM architecture, skill responds with design rationale
- [ ] **Standards reference:** Ask about risk/reward, skill cites 2.5:1 target
- [ ] **File links:** Skill references backtesting-guide.md, ml-trading-patterns.md, etc.
- [ ] **Code examples:** Skill includes Python/bash examples from references
- [ ] **Warnings:** Skill warns about common pitfalls (data leakage, overfitting, etc.)
- [ ] **Script mention:** For automation questions, skill suggests validate_config.py or quick_backtest.sh
- [ ] **Workflow guidance:** Skill provides step-by-step procedures
- [ ] **Metric context:** Skill explains why targets matter (Sharpe >0.5, DD <20%, etc.)

## Skill Activation Signals

The skill should automatically load when Claude detects:

**Keywords (any of):**
- LSTM, neural network, deep learning, price prediction
- Backtesting, backtest, out-of-sample, walk-forward
- Crypto trading, scalping, perpetual futures, OKX, CCXT
- Risk management, position sizing, stop loss, take profit
- Technical indicators, RSI, MACD, Bollinger Bands
- Hyperparameter tuning, model optimization
- Sharpe ratio, max drawdown, win rate, profit factor
- config.yaml, strategy parameters

**Contexts (any of):**
- Working in crypto-scalping-bot project
- Discussing ML trading strategy
- Configuring LSTM model
- Setting up backtesting framework
- Optimizing trading parameters

## Expected Skill Behavior

✅ **Should do:**
- Reference specific standards from SKILL.md
- Link to appropriate reference docs
- Provide code templates and examples
- Warn about common pitfalls
- Guide hyperparameter tuning workflow
- Suggest utility scripts for automation

❌ **Should NOT do:**
- Provide step-by-step tutorials (that's not guidelines)
- Generate new trading strategies
- Give financial advice
- Recommend specific symbols/timeframes
- Claim to predict crypto prices

## Troubleshooting

**Skill not triggering?**
- Ensure you're in the crypto-scalping-bot project
- Use keyword triggers from "Skill Activation Signals" above
- Try more specific phrases: "LSTM backtesting" instead of "test model"

**Skill references missing files?**
- Verify all reference files exist:
  - references/ml-trading-patterns.md ✓
  - references/backtesting-guide.md ✓
  - references/risk-management-specs.md ✓
  - scripts/validate_config.py ✓
  - scripts/quick_backtest.sh ✓

**Need to update skill?**
- Edit SKILL.md for guidelines updates
- Update references/ for detailed docs
- Modify scripts/ for tool improvements
- Reload Claude Code to pick up changes
