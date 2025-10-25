# Troubleshooting Guide

Comprehensive solutions for common issues when setting up and running the crypto scalping bot.

---

## Table of Contents

1. [Installation & Setup Issues](#installation--setup-issues)
2. [Data Fetching Issues](#data-fetching-issues)
3. [Model Training Issues](#model-training-issues)
4. [Backtesting Issues](#backtesting-issues)
5. [General Debugging Tips](#general-debugging-tips)

---

## Installation & Setup Issues

### Issue: `pip install -r requirements.txt` fails with TensorFlow

**Symptom**:
```
ERROR: Could not find a version that satisfies the requirement tensorflow==2.15.0
ERROR: No matching distribution found for tensorflow
```

**Cause**: TensorFlow unavailable for your Python version or platform (e.g., Python 3.12, Apple Silicon M1/M2).

**Solution**:
```bash
# Check Python version (must be 3.8-3.11 for TensorFlow 2.15)
python --version

# If 3.12+, use Python 3.11
brew install python@3.11  # macOS
python3.11 -m venv venv
source venv/bin/activate

# For Apple Silicon (M1/M2), use tensorflow-macos
pip install tensorflow-macos tensorflow-metal

# For other platforms, try latest TensorFlow
pip install tensorflow  # auto-selects compatible version
```

**Prevention**: Use Python 3.9-3.11 for best compatibility.

---

### Issue: `ModuleNotFoundError: No module named 'ccxt'`

**Symptom**:
```
ModuleNotFoundError: No module named 'ccxt'
```

**Cause**: Dependencies not installed or wrong virtual environment active.

**Solution**:
```bash
# Verify you're in virtual environment
which python  # Should show path to venv/bin/python

# If not activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep ccxt
```

**Prevention**: Always activate venv before running scripts.

---

### Issue: `config.yaml not found` or `FileNotFoundError`

**Symptom**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'config/config.yaml'
```

**Cause**: Running scripts from wrong directory.

**Solution**:
```bash
# Always run from project root
cd crypto-scalping-bot

# Verify config exists
ls config/config.yaml

# Run scripts with proper path
python run_pipeline.py
# OR
python src/data/fetch_data.py
```

**Prevention**: Set project root as working directory in IDE.

---

### Issue: `.env` file errors or API key issues

**Symptom**:
```
Warning: OKX API credentials not found
```

**Cause**: `.env` file missing or incorrectly formatted (not needed for backtesting, only live data).

**Solution**:
```bash
# For backtesting, ignore this warning (uses public API)

# For live data fetching, create .env
cp .env.example .env

# Edit with your credentials
nano .env
```

`.env` format:
```
OKX_API_KEY=your_api_key_here
OKX_API_SECRET=your_secret_here
OKX_PASSPHRASE=your_passphrase_here
```

**Note**: API credentials NOT required for historical data backtesting.

---

### Issue: Dependency version conflicts

**Symptom**:
```
ERROR: pip's dependency resolver does not currently take into account all the packages...
```

**Cause**: Conflicting package versions (e.g., NumPy 2.0 vs TensorFlow).

**Solution**:
```bash
# Create fresh virtual environment
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install with specific versions
pip install numpy==1.24.3
pip install tensorflow==2.15.0
pip install -r requirements.txt

# Check for conflicts
pip check
```

**Prevention**: Use virtual environment, pin versions in requirements.txt.

---

## Data Fetching Issues

### Issue: OKX API rate limit errors

**Symptom**:
```
ccxt.RateLimitExceeded: okx {"code":"50011","msg":"Rate limit reached"}
Error fetching data: Rate limit exceeded
```

**Cause**: Too many requests too quickly (OKX limit: 20 requests/second).

**Solution**:

Edit `src/data/fetch_data.py` line 117:
```python
# Increase delay from 100ms to 200ms
self.exchange.sleep(200)  # Was: 100
```

Or fetch smaller date ranges:
```bash
# Split into monthly chunks
# Edit config/config.yaml
backtesting:
  start_date: "2024-01-01"
  end_date: "2024-01-31"  # One month only
```

**Prevention**: Keep 100-200ms delay, avoid concurrent fetch scripts.

---

### Issue: No data fetched or empty DataFrame

**Symptom**:
```
Total candles fetched: 0
Data saved to data/BTC_USDT_USDT_1m_20240101_to_20240131.csv
[Empty CSV file]
```

**Causes & Solutions**:

**1. Date range in future**
```yaml
# config.yaml
backtesting:
  start_date: "2025-12-01"  # Future date!
  end_date: "2025-12-31"
```
Solution: Use past dates only.

**2. Symbol format incorrect**
```yaml
trading:
  symbol: BTC-USDT  # Wrong format
```
Solution: Use CCXT format: `BTC/USDT:USDT` for perpetual futures.

**3. Timeframe not supported**
```yaml
trading:
  timeframe: 30s  # Not supported
```
Solution: Use supported timeframes: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`.

**Verification**:
```python
# Test in Python console
import ccxt
exchange = ccxt.okx()
exchange.load_markets()
print(exchange.markets['BTC/USDT:USDT'])  # Should print market info
```

---

### Issue: SSL certificate verification errors

**Symptom**:
```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Cause**: Corporate firewall, outdated certificates, or system time incorrect.

**Solutions**:

**1. Update certificates (macOS)**
```bash
/Applications/Python\ 3.11/Install\ Certificates.command
```

**2. Check system time**
```bash
date  # Verify correct date/time
```

**3. Temporarily disable SSL verification (NOT for production)**
```python
# In fetch_data.py, line 42
self.exchange = ccxt.okx({
    'enableRateLimit': True,
    'options': {'defaultType': 'swap'},
    'verify': False  # TEMPORARY WORKAROUND
})
```

**Prevention**: Keep system time accurate, update OS certificates.

---

### Issue: Data gaps or missing candles

**Symptom**:
```
Date range: 2024-01-01 to 2024-03-31
Total rows: 124,523
Expected rows: 129,600  # 90 days * 1440 minutes
```

**Cause**: Exchange downtime, API errors, or delisted markets.

**Solutions**:

**1. Check for exchange outages**
```bash
# Verify exchange was operational during date range
# Check OKX status page or Twitter
```

**2. Re-fetch specific ranges**
```python
# Manually fetch missing periods
from src.data.fetch_data import OKXDataFetcher
fetcher = OKXDataFetcher()
df = fetcher.fetch_ohlcv('2024-01-15', '2024-01-16')  # Missing day
```

**3. Accept gaps for preprocessing**
```python
# Preprocessing will drop NaN rows automatically
# Check data/processed_data.csv for final count
```

**Prevention**: Fetch extra buffer days, validate data after fetching.

---

## Model Training Issues

### Issue: Out of memory (OOM) errors during training

**Symptom**:
```
tensorflow.python.framework.errors_impl.ResourceExhaustedError: OOM when allocating tensor
```

**Cause**: Insufficient GPU/RAM, batch size too large, or dataset too big.

**Solutions**:

**1. Reduce batch size** (edit `config/config.yaml`):
```yaml
model:
  batch_size: 16  # Was: 32
```

**2. Reduce sequence length**:
```yaml
model:
  lookback_periods: 30  # Was: 60
```

**3. Use CPU instead of GPU**:
```bash
# Before running
export CUDA_VISIBLE_DEVICES=""
python src/models/train_lstm.py
```

**4. Reduce dataset size**:
```yaml
backtesting:
  start_date: "2024-02-01"  # Shorter period
  end_date: "2024-03-31"
```

**Prevention**: Start small, monitor RAM/GPU usage with `nvidia-smi` or Activity Monitor.

---

### Issue: Model not converging (loss not decreasing)

**Symptom**:
```
Epoch 1/50
loss: 0.1234 - val_loss: 0.1235
Epoch 10/50
loss: 0.1233 - val_loss: 0.1234  # No improvement
```

**Causes & Solutions**:

**1. Learning rate too low**
```yaml
model:
  learning_rate: 0.01  # Increase from 0.001
```

**2. Data not normalized**
Check `data/processed_data.csv` - values should be in [0,1] range.

**3. Too much dropout**
```yaml
model:
  dropout_rate: 0.1  # Reduce from 0.2
```

**4. Insufficient features**
```yaml
model:
  features:
    - close
    - volume
    - rsi_14
    # Add more indicators
```

**Diagnosis**:
```python
# Check data distribution
import pandas as pd
df = pd.read_csv('data/processed_data.csv')
print(df[['close', 'rsi_14', 'macd']].describe())
# All values should be in reasonable ranges
```

---

### Issue: Overfitting (low training loss, high validation loss)

**Symptom**:
```
Epoch 30/50
loss: 0.001 - val_loss: 0.150  # Large gap
```

**Cause**: Model memorizing training data, not generalizing.

**Solutions**:

**1. Increase dropout**
```yaml
model:
  dropout_rate: 0.3  # Increase from 0.2
```

**2. Early stopping working correctly**
Check for message: `Restoring model weights from the end of the best epoch`

**3. Reduce model complexity**
```yaml
model:
  lstm_units: [32]  # Simpler than [64, 32]
```

**4. More training data**
Fetch longer period (6+ months recommended).

**Verification**:
Plot training history:
```bash
# After training
open models/training_history.png
# Check if train and val losses track together
```

---

### Issue: Low directional accuracy (<55%)

**Symptom**:
```
Evaluation Metrics:
direction_accuracy: 0.512000  # Only 51.2%
```

**Cause**: Model barely better than random (50%).

**Solutions**:

**1. Check data quality**
```python
import pandas as pd
df = pd.read_csv('data/processed_data.csv')
print(df.isnull().sum())  # Should be 0 for all columns
```

**2. Train longer**
```yaml
model:
  epochs: 100  # Increase from 50
```

**3. Add more features**
Include indicators like EMA, volume_ratio, price_change.

**4. Try different timeframe**
```yaml
trading:
  timeframe: 5m  # Less noise than 1m
```

**Acceptance**: 55-60% directional accuracy is realistic for 1m scalping.

---

### Issue: NaN loss during training

**Symptom**:
```
Epoch 5/50
loss: nan - val_loss: nan
```

**Cause**: Exploding gradients, data contains NaN/Inf, or learning rate too high.

**Solutions**:

**1. Check data for NaN**
```python
import pandas as pd
df = pd.read_csv('data/processed_data.csv')
print(df.isnull().sum())
print((df == float('inf')).sum())
```

**2. Reduce learning rate**
```yaml
model:
  learning_rate: 0.0001  # Much lower
```

**3. Gradient clipping** (edit `lstm_model.py` line 113):
```python
optimizer = keras.optimizers.Adam(
    learning_rate=learning_rate,
    clipnorm=1.0  # Add gradient clipping
)
```

**Prevention**: Always validate data preprocessing, start with low learning rate.

---

## Backtesting Issues

### Issue: No trades executed (# Trades: 0)

**Symptom**:
```
BACKTEST RESULTS
Total Trades: 0
Return: 0.00%
```

**Causes & Solutions**:

**1. Prediction threshold too high**

Edit `src/strategies/lstm_strategy.py` line 43:
```python
prediction_threshold = 0.0001  # Lower from 0.0005
```

Or use aggressive strategy:
```bash
# In backtest_runner.py, change strategy_class
strategy_class=AggressiveLSTMStrategy  # More sensitive
```

**2. Indicators too restrictive**

Check if RSI/MACD blocking all signals:
```python
# In lstm_strategy.py, temporarily disable confirmations (lines 157-158)
# return prediction_bullish  # Ignore RSI and MACD
```

**3. Predictions not aligned**

Check `backtest_runner.py` output for:
```
Prediction changes mean: 0.0000%  # Should NOT be zero
```

If zero, predictions misaligned with backtest data.

**Diagnosis**:
```python
# Check predictions file
import pandas as pd
preds = pd.read_csv('data/predictions.csv')
print(preds.head())
print(preds['predicted'].describe())  # Should vary, not constant
```

---

### Issue: All trades are losers (Win Rate: 0%)

**Symptom**:
```
Win Rate: 0.00%
All trades hit stop-loss
```

**Cause**: Model predicting wrong direction or stop-loss too tight.

**Solutions**:

**1. Check model direction accuracy**
```python
# Re-run model evaluation
python src/models/train_lstm.py
# Look for direction_accuracy in output
# Should be >50%, ideally >55%
```

**2. Widen stop-loss**
```yaml
# In lstm_strategy.py or config
stop_loss_pct: 0.01  # Increase from 0.005
```

**3. Verify strategy logic**
Ensure predictions match trade direction:
```python
# Add debug logging in lstm_strategy.py next() method
print(f"Prediction: {current_prediction}, Position: {self.position}")
```

---

### Issue: Suspiciously good results (Sharpe >5, Return >1000%)

**Symptom**:
```
Return: 2547.32%
Sharpe Ratio: 8.24
Max Drawdown: 0.12%
```

**Cause**: Lookahead bias, data leakage, or bugs.

**Diagnosis**:

**1. Check for lookahead bias**
```python
# Verify predictions datetime <= actuals datetime
preds = pd.read_csv('data/predictions.csv')
preds['datetime'] = pd.to_datetime(preds['datetime'])
print((preds['datetime'].diff() < 0).sum())  # Should be 0
```

**2. Verify commission applied**
```python
# In backtest_runner.py, line 272
print(f"Commission: {runner.config['backtesting']['commission']}")
# Should be 0.0004, not 0
```

**3. Check for bugs**
Review strategy logic for accidental position flipping or indicator errors.

**Prevention**: Always test on out-of-sample data, compare to simple baseline strategy.

---

### Issue: Cannot open backtest plot HTML

**Symptom**:
```
FileNotFoundError: results/backtest_plot.html not found
```

**Cause**: Backtest failed before plotting, or results directory missing.

**Solutions**:

**1. Check for backtest errors**
```bash
# Re-run with verbose output
python src/backtest/backtest_runner.py
# Look for error messages before "Backtest plot saved"
```

**2. Create results directory**
```bash
mkdir -p results
```

**3. Check backtesting.py installation**
```bash
pip show backtesting
# Verify version and dependencies
```

**Workaround**: Skip plotting, analyze CSV results:
```bash
cat results/backtest_results.csv
```

---

### Issue: Poor performance vs expectations

**Symptom**:
```
Return: -15.32%
Sharpe Ratio: -0.84
```

**Cause**: Multiple factors (model accuracy, market regime, parameters).

**Systematic Diagnosis**:

**1. Check model accuracy**
```bash
python src/models/train_lstm.py
# direction_accuracy should be >55%
```

**2. Inspect trades**
```bash
open results/backtest_plot.html
# Look for patterns: always stopped out? wrong entries?
```

**3. Compare strategies**
```bash
cat results/strategy_comparison.csv
# Try Conservative or Aggressive variants
```

**4. Test simple baseline**
```python
# Implement buy-and-hold in backtest_runner.py
# Compare to LSTM strategy
```

**5. Check market regime**
```bash
# Plot price action
# Crypto in 2024: mostly uptrend
# Scalping strategies often underperform trending markets
```

**Acceptance**: Scalping is hard. Negative returns common during development.

---

## General Debugging Tips

### Enable Debug Logging

**Add to scripts**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Intermediate Outputs

**After each pipeline step**:
```bash
# After fetch
ls -lh data/*.csv
head -20 data/BTC_USDT_USDT_1m_*.csv

# After preprocess
head -20 data/processed_data.csv
wc -l data/processed_data.csv

# After training
ls -lh models/lstm_model.keras
ls -lh data/predictions.csv

# After backtest
ls -lh results/
```

### Verify Python Environment

```bash
which python  # Should be in venv
python --version  # Should be 3.8-3.11
pip list  # Check installed packages
```

### Reset to Clean State

**When everything breaks**:
```bash
# Delete all generated files
rm -rf data/*.csv
rm -rf models/lstm_model.keras models/checkpoints/
rm -rf results/*

# Recreate venv
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Re-run pipeline from scratch
python run_pipeline.py
```

### Search Error Messages

**Use exact error text**:
```bash
# Google search:
"tensorflow ResourceExhaustedError OOM when allocating tensor"

# GitHub issues:
https://github.com/search?q=ccxt+RateLimitExceeded&type=issues
```

---

## Getting Help

**Still stuck? Try:**

1. **Check logs**: Enable debug logging, read full error stack trace
2. **Verify setup**: Run through QUICKSTART.md step-by-step
3. **Test components**: Run each module independently (fetch → preprocess → train → backtest)
4. **Read code**: Scripts have extensive comments explaining logic
5. **Check ADRs**: [docs/adr/](adr/) explains design decisions and constraints

**Common misconceptions:**
- "Model should predict every candle perfectly" → No, 55-60% directional accuracy is good
- "Backtest return should match live trading" → No, expect 30-50% degradation
- "More features = better model" → No, often causes overfitting
- "API keys required for backtesting" → No, only for live data/trading

---

## Related Documentation

- Known Limitations: [LIMITATIONS.md](LIMITATIONS.md)
- Architecture Decisions: [docs/adr/](adr/)
- API Reference: [docs/api/](api/)
- Quick Start: [QUICKSTART.md](../QUICKSTART.md)

---

**Last Updated**: 2025-01-25
**Version**: 1.0
