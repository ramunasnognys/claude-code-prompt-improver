"""
Debug script to test why strategy isn't executing trades.
"""
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
try:
    from backtesting.lib import FractionalBacktest
except ImportError:
    FractionalBacktest = None
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'src'))

from strategies.lstm_strategy import LSTMScalpingStrategy

# Load prepared backtest data
df = pd.read_csv('data/processed_data.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

predictions_df = pd.read_csv('data/predictions.csv')

# Prepare predictions
predictions_normalized = predictions_df['predicted'].values
actuals_normalized = predictions_df['actual'].values

# Align predictions
pred_dates = pd.to_datetime(predictions_df['datetime'])
pred_dict = dict(zip(pred_dates, predictions_normalized))
actual_dict = dict(zip(pred_dates, actuals_normalized))

df['predicted_normalized'] = df['datetime'].map(pred_dict)
df['actual_normalized'] = df['datetime'].map(actual_dict)

# Filter to rows with predictions
df_with_preds = df[df['predicted_normalized'].notna()].copy()

# Prepare backtest data
bt_data = pd.DataFrame({
    'Open': df_with_preds['open'].values,
    'High': df_with_preds['high'].values,
    'Low': df_with_preds['low'].values,
    'Close': df_with_preds['close'].values,
    'Volume': df_with_preds['volume'].values,
}, index=pd.to_datetime(df_with_preds['datetime']))

# Add indicators
bt_data['RSI'] = df_with_preds['rsi_14'].values
bt_data['MACD'] = df_with_preds['macd'].values
bt_data['MACD_Signal'] = df_with_preds['macd_signal'].values
bt_data['Predicted_Change'] = df_with_preds['predicted_normalized'].values
bt_data['Actual_Norm'] = df_with_preds['actual_normalized'].values

# Drop NaN
bt_data = bt_data.dropna()

print(f"Data shape: {bt_data.shape}")
print(f"\nFirst 5 rows:")
print(bt_data.head())
print(f"\nData types:")
print(bt_data.dtypes)

# Test with simple strategy first
class DebugStrategy(Strategy):
    """Minimal strategy for debugging"""

    def init(self):
        self.pred = self.data.Predicted_Change
        self.trade_count = 0
        print("\n=== Strategy Init ===")
        print(f"Data length: {len(self.data)}")
        print(f"Predictions shape: {len(self.pred)}")
        print(f"First 5 predictions: {self.pred[:5]}")

    def next(self):
        # Try to enter on first valid signal
        if len(self.data) < 2:
            return

        if not self.position:
            # Always try to buy on 100th bar as a test
            if len(self.data) == 100:
                print(f"\nBar 100 - Attempting to buy")
                print(f"Close: {self.data.Close[-1]}")
                print(f"Equity: {self.equity}")

                # Try different size specifications
                entry_price = self.data.Close[-1]
                sl_price = entry_price * 0.995  # 0.5% stop loss
                tp_price = entry_price * 1.01   # 1% take profit

                print(f"Entry: {entry_price}, SL: {sl_price}, TP: {tp_price}")
                self.buy(size=0.1, sl=sl_price, tp=tp_price)
                self.trade_count += 1
                print(f"Trade count after buy: {self.trade_count}")

# Test with regular Backtest
print("\n" + "="*60)
print("Testing with standard Backtest class")
print("="*60)

bt = Backtest(
    bt_data,
    DebugStrategy,
    cash=10000,
    commission=0.0004,
    exclusive_orders=True
)

results = bt.run()
print(f"\nTrades executed: {results['# Trades']}")

# Test with FractionalBacktest if available
if FractionalBacktest is not None:
    print("\n" + "="*60)
    print("Testing with FractionalBacktest class")
    print("="*60)

    bt_frac = FractionalBacktest(
        bt_data,
        DebugStrategy,
        cash=10000,
        commission=0.0004,
        exclusive_orders=True
    )

    results_frac = bt_frac.run()
    print(f"\nTrades executed: {results_frac['# Trades']}")

    # Now test with actual LSTM strategy
    print("\n" + "="*60)
    print("Testing LSTM Strategy with FractionalBacktest")
    print("="*60)

    bt_lstm = FractionalBacktest(
        bt_data,
        LSTMScalpingStrategy,
        cash=10000,
        commission=0.0004,
        exclusive_orders=True
    )

    results_lstm = bt_lstm.run()
    print(f"\nTrades executed: {results_lstm['# Trades']}")
    print(f"Return: {results_lstm['Return [%]']}%")

else:
    print("\nFractionalBacktest not available")
