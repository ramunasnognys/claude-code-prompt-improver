#!/bin/bash
# Phase 3.1 Validation Script - Run after training completes

echo "================================================================"
echo "PHASE 3.1 VALIDATION"
echo "================================================================"

cd /Users/ramunasnognys/Developer/workspace/prompt-improver/crypto-scalping-bot

# Wait for training to complete
echo "Waiting for training to complete..."
while ps aux | grep -q "[p]ython src/models/lstm_model.py"; do
    sleep 30
    echo "  Still training... (checking every 30s)"
done

echo "✅ Training completed!"
echo ""

# Check if model was saved
if [ ! -f "models/lstm_model.keras" ]; then
    echo "❌ Error: Model file not found!"
    exit 1
fi

echo "Step 1: Generating predictions on test set..."
python -c "
import pandas as pd
import numpy as np
from pathlib import Path
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import pickle

print('Loading Phase 3.1 model...')
model = keras.models.load_model('models/lstm_model.keras')

print('Loading processed data...')
df = pd.read_csv('data/processed_data.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

print('Loading scaler...')
with open('data/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Filter to test period only (Mar 16-31)
test_df = df[df['datetime'] >= '2024-03-16'].copy()
print(f'Test period: {test_df[\"datetime\"].min()} to {test_df[\"datetime\"].max()}')
print(f'Test samples: {len(test_df)}')

# Load 14 features as configured
import yaml
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)
features = config['model']['features']
print(f'Using {len(features)} features: {features}')

test_features = test_df[features].values
test_scaled = scaler.transform(test_features)

# Create sequences
lookback = 60
X_test, dates = [], []
for i in range(lookback, len(test_scaled)):
    X_test.append(test_scaled[i-lookback:i])
    dates.append(test_df['datetime'].iloc[i])

X_test = np.array(X_test)

print(f'Generating predictions for {len(X_test)} samples...')
# Model now outputs price changes directly (with bias correction applied)
predictions = model.predict(X_test, verbose=0)

# Note: predictions are already price CHANGES (not absolute prices)
# and bias correction is already applied by the model
results = pd.DataFrame({
    'predicted': predictions.flatten(),
    'datetime': dates
})

# For backtest compatibility, we still need an 'actual' column
# Use a dummy value since we're predicting changes now
results['actual'] = 0.5  # Dummy value for compatibility

results.to_csv('data/predictions.csv', index=False)
print(f'✅ Predictions saved: {len(results)} samples')
print(f'Date range: {results[\"datetime\"].min()} to {results[\"datetime\"].max()}')

# Analyze predictions
print(f'\\nPrediction Analysis:')
print(f'  Mean: {predictions.mean()*100:.4f}%')
print(f'  Std: {predictions.std()*100:.4f}%')
print(f'  Min: {predictions.min()*100:.4f}%')
print(f'  Max: {predictions.max()*100:.4f}%')
print(f'  Positive: {(predictions > 0).sum()} ({(predictions > 0).sum()/len(predictions)*100:.1f}%)')
print(f'  Negative: {(predictions < 0).sum()} ({(predictions < 0).sum()/len(predictions)*100:.1f}%)')
" 2>&1 | tee prediction_generation.log

if [ $? -ne 0 ]; then
    echo "❌ Error generating predictions!"
    exit 1
fi

echo ""
echo "Step 2: Running backtest..."
python run_pipeline.py --skip-fetch --skip-train 2>&1 | tee backtest_phase3_1.log

echo ""
echo "================================================================"
echo "PHASE 3.1 VALIDATION COMPLETE"
echo "================================================================"
echo ""
echo "Results saved to:"
echo "  - results/backtest_results.csv"
echo "  - results/strategy_comparison.csv"
echo "  - backtest_phase3_1.log"
echo ""
echo "Compare with Phase 2.1:"
echo "  Conservative: -0.45% → ???"
echo "  Default: -1.42% → ???"
echo ""
