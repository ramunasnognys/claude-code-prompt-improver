"""
Test LSTM strategy with verbose debugging.
"""
import pandas as pd
import numpy as np
from backtesting import Strategy
from backtesting.lib import FractionalBacktest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'src'))

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


class VerboseLSTMStrategy(Strategy):
    """LSTM strategy with verbose debugging"""

    prediction_threshold = 0.0005
    rsi_oversold = 30
    rsi_overbought = 70
    stop_loss_pct = 0.005
    take_profit_pct = 0.01
    position_size = 0.95

    def init(self):
        self.price_change_predicted = self.data.Predicted_Change
        self.current_price = self.data.Close
        self.rsi = self.data.RSI
        self.macd = self.data.MACD
        self.macd_signal = self.data.MACD_Signal

        self.checked_bars = 0
        self.signals_found = 0
        self.log_count = 0

    def next(self):
        if len(self.data) < 2:
            return

        self.checked_bars += 1

        current_prediction = self.price_change_predicted[-1]
        current_rsi = self.rsi[-1]
        current_macd = self.macd[-1]
        current_macd_signal = self.macd_signal[-1]

        # Log first 5 bars to see what's happening
        if self.log_count < 5:
            self.log_count += 1
            idx = len(self.data) - 1
            print(f"\nBar {len(self.data)} (index {idx}):")
            print(f"  Prediction: {current_prediction:.8f} (from index {idx})")
            print(f"  RSI: {current_rsi:.2f}")
            print(f"  MACD: {current_macd:.4f}")
            print(f"  MACD_Signal: {current_macd_signal:.4f}")
            print(f"  Close: {self.data.Close[-1]:.8f}")
            print(f"  MACD array length: {len(self.macd)}")
            print(f"  Full MACD array (first 10): {self.macd[:10]}")
            print(f"  Full MACD_Signal array (first 10): {self.macd_signal[:10]}")

        # Check long conditions
        if not self.position:
            pred_bullish = current_prediction > self.prediction_threshold
            rsi_ok = current_rsi < self.rsi_overbought
            macd_bullish = current_macd > current_macd_signal

            # Log first 10 potential signals
            if self.signals_found < 10 and pred_bullish and rsi_ok and macd_bullish:
                self.signals_found += 1
                print(f"\n=== Signal #{self.signals_found} at bar {len(self.data)} ===")
                print(f"Prediction: {current_prediction:.6f} > {self.prediction_threshold} = {pred_bullish}")
                print(f"RSI: {current_rsi:.2f} < {self.rsi_overbought} = {rsi_ok}")
                print(f"MACD: {current_macd:.2f} > {current_macd_signal:.2f} = {macd_bullish}")
                print(f"Close price: {self.data.Close[-1]:.6f}")
                print(f"Equity: {self.equity:.2f}")

                # Try to buy
                entry_price = self.data.Close[-1]
                sl_price = entry_price * (1 - self.stop_loss_pct)
                tp_price = entry_price * (1 + self.take_profit_pct)

                print(f"Attempting buy: size={self.position_size}, SL={sl_price:.6f}, TP={tp_price:.6f}")
                self.buy(size=self.position_size, sl=sl_price, tp=tp_price)
                print(f"Position after buy: {self.position}")


print("Testing with VerboseLSTMStrategy")
print("="*60)

bt = FractionalBacktest(
    bt_data,
    VerboseLSTMStrategy,
    cash=10000,
    commission=0.0004,
    exclusive_orders=True
)

results = bt.run()
print(f"\n{'='*60}")
print(f"Final Results:")
print(f"Checked bars: {results._strategy.checked_bars}")
print(f"Signals found: {results._strategy.signals_found}")
print(f"Trades executed: {results['# Trades']}")
print(f"Return: {results['Return [%]']}%")
