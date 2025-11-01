# ML Trading Architecture Patterns

## LSTM Design Rationale

### Why Stacked LSTM?

**Sequential architecture:** Each layer learns different temporal scales
- **Layer 1 (128 units):** Fast patterns (1-10 min)
- **Layer 2 (64 units):** Medium patterns (10-60 min)
- **Layer 3 (32 units):** Slow patterns (60+ min)

**Compression:** 128 → 64 → 32 progressively concentrates information into price signal

### Dropout Mechanics

**Problem:** Overfitting on training data
```
train_loss: 0.001 ← Memorized patterns
test_loss: 0.05   ← Fails on new data (overfitted)
```

**Solution:** Dropout 0.3 randomly disables 30% neurons during training
```
Forces redundancy → Generalizes better → Lower test loss
```

**Side effect:** Increases training loss slightly (expected, good sign)

## Feature Engineering Hierarchy

### Core Features (Always Include)

| Feature | Why | Calculation |
|---------|-----|-----------|
| Close | Price signal | Last candle close |
| Volume | Liquidity + conviction | Trading volume |
| RSI | Overbought/oversold | (Avg up / (Avg up + Avg down)) * 100 |
| MACD | Trend momentum | Fast EMA - Slow EMA |
| BB Upper/Lower | Volatility bands | SMA ± (2 × StdDev) |

### Secondary Features (Conditional)

Add only if improving validation metrics:

| Feature | When to Add | Caution |
|---------|------------|---------|
| ADX | Trend strength needed | Phase 2.3: disabled (hurts Sharpe) |
| ATR | Volatility sizing | Normalized (divide by close) |
| EMA | Trend confirmation | Use fast (10) not slow (200) |
| Volume Ratio | Signal liquidity | volume / sma(volume, 20) |

### Feature Scaling Importance

```python
# BAD: Raw features have different scales
close: 40,000-42,000
volume: 1M-10M
rsi: 0-100

# GOOD: Normalize to [-1, 1] or [0, 1]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

**Why:** Gradient descent converges faster when features are similar magnitude

## Training Loop Best Practices

### Data Leakage Detection Checklist

```python
# ✅ GOOD: Features only use past data
close_today = prices[t-1]  # Yesterday's close
sma_today = mean(prices[t-120:t])  # Last 120 periods

# ❌ BAD: Features peek into future
close_today = prices[t]  # Today's actual
sma_today = mean(prices[t:t+120])  # Future data!
```

### Validation Strategy

```
Train:      Jan 1 - Feb 28 (60 days)
Validation: Mar 1 - Mar 15 (15 days)
Test:       Mar 16 - Mar 31 (16 days) ← Completely new data
```

**Sequential split:** No randomization (time-series order matters)

### Early Stopping Interpretation

```
Epoch 1:  val_loss = 0.050
Epoch 5:  val_loss = 0.035 ↓
Epoch 10: val_loss = 0.032 ↓
Epoch 15: val_loss = 0.033 ↑ ← Start overfitting
Epoch 20: val_loss = 0.037 ↑

Early Stop at epoch 15 (patience=10 means wait 10 epochs)
→ Save weights from epoch 15 (best validation)
```

## Hyperparameter Sensitivity

### Learning Rate (0.0005)

Too high (0.01):
```
loss: 0.15 → 0.12 → 0.50 → 1.20 ✗ (diverges)
```

Too low (0.00001):
```
loss: 0.15 → 0.14999 → 0.14998... (barely moving)
```

Optimal (0.0005):
```
loss: 0.15 → 0.05 → 0.03 → 0.025 (smooth convergence)
```

**Phase 3.1 change:** 0.001 → 0.0005 improved stability for volatile crypto

### Batch Size (64)

Trade-off: GPU memory vs gradient stability

| Size | Pros | Cons |
|------|------|------|
| 16 | More updates/epoch | Noisy gradients |
| 64 | Stable gradients | Fewer updates/epoch |
| 256 | Parallel efficiency | May miss local patterns |

**For crypto:** Use 64 (balance stable convergence + fast training)

## Prediction Correction (Phase 3.1)

### Problem: Systematic Bias

```
LSTM predictions:      [0.001, 0.0005, -0.001, 0.002]
Actual changes:        [0.003, 0.002, -0.002, 0.005]

Mean bias = mean(pred - actual) = -0.0015
→ Model consistently underestimates by 0.15%
```

### Solution: Bias Correction

```python
# Step 1: Calculate bias on validation set
bias = mean(val_predictions) - mean(val_actuals)
scale = std(val_actuals) / std(val_predictions)

# Step 2: Apply to test predictions
corrected = (predictions - bias) * scale

# Result: Unbiased predictions with correct variance
```

### Why It Works

- **Removes systematic error:** Predictions align with actual distribution
- **Matches variance:** Not too conservative/aggressive
- **No overfitting:** Learned from validation (unseen) data

## Feature Importance (Learned)

In LSTM, layer weights implicitly weight features:

```python
# Feature importance: gradient of loss w.r.t. input
gradients = model.gradients(X, y)
importance = abs(gradients).mean(axis=0)

# Top features usually:
# 1. Close price (50-60% importance)
# 2. Recent volume (15-20%)
# 3. Technical indicators (20-30%)
```

**Insight:** Simple features (price + volume) often dominate complex ones
