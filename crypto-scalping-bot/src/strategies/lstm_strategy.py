"""
LSTM-based scalping strategy for crypto perpetual futures.
"""

import numpy as np
import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover
import yaml
from typing import Optional


class LSTMScalpingStrategy(Strategy):
    """
    LSTM-based scalping strategy for perpetual futures trading.

    Combines LSTM price predictions with technical indicator confirmations
    to generate long/short signals with built-in risk management.

    Signal Generation:
        1. LSTM predicts next period's normalized price
        2. Calculate predicted price change percentage
        3. Check if change exceeds threshold (filters noise)
        4. Confirm with RSI (avoid overbought/oversold)
        5. Confirm with MACD (trend alignment)
        6. Execute with stop-loss and take-profit

    Strategy Parameters (optimizable):
        - prediction_threshold: Min predicted price change (default 0.05%)
        - rsi_oversold/overbought: RSI bounds (30/70)
        - stop_loss_pct: Stop loss percentage (0.5%)
        - take_profit_pct: Take profit percentage (1%)
        - position_size: Fraction of equity per trade (95%)

    Example:
        >>> from backtesting import Backtest
        >>> bt = Backtest(data, LSTMScalpingStrategy, cash=10000)
        >>> stats = bt.run()
        >>> print(stats)
    """

    # Strategy parameters (can be optimized)
    prediction_threshold = 0.0005  # Minimum predicted price change (0.05% - lowered for more trades)
    rsi_oversold = 30
    rsi_overbought = 70
    stop_loss_pct = 0.005        # 0.5% stop loss
    take_profit_pct = 0.01       # 1% take profit
    position_size = 0.95         # Use 95% of available equity

    def init(self) -> None:
        """
        Initialize strategy: load predictions and calculate signal strength.

        Expects DataFrame with columns:
            - Predicted_Norm: LSTM predictions (normalized)
            - Actual_Norm: Actual prices (normalized)
            - Close: Real prices for position sizing
            - RSI, MACD, MACD_Signal: Technical indicators

        Calculates:
            - price_change_predicted: % change from previous actual to current prediction
            - Prints diagnostic info about prediction distribution
        """
        # PHASE 3.1: Get price change predictions directly from model
        self.price_change_predicted = self.data.Predicted_Change  # LSTM now predicts % changes
        self.current_price = self.data.Close  # Real prices for position sizing
        
        # No need to calculate predicted changes - model does this now!
        
        # Debug: Check if prediction changes make sense
        pred_changes = self.price_change_predicted
        pred_mean = pred_changes.mean()
        pred_std = pred_changes.std()
        
        print(f"\n{'='*60}")
        print(f"Strategy Initialization - Prediction Analysis")
        print(f"{'='*60}")
        print(f"Prediction changes mean: {pred_mean*100:.4f}%")
        print(f"Prediction changes std: {pred_std*100:.4f}%")
        print(f"Prediction changes range: {pred_changes.min()*100:.4f}% to {pred_changes.max()*100:.4f}%")
        print(f"Strategy threshold: ±{self.prediction_threshold*100:.4f}%")
        
        # Count how many predictions exceed threshold
        bullish_signals = (pred_changes > self.prediction_threshold).sum()
        bearish_signals = (pred_changes < -self.prediction_threshold).sum()
        print(f"Potential bullish signals: {bullish_signals} ({bullish_signals/len(pred_changes)*100:.2f}%)")
        print(f"Potential bearish signals: {bearish_signals} ({bearish_signals/len(pred_changes)*100:.2f}%)")
        print(f"{'='*60}\n")

        # Technical indicators from data
        self.rsi = self.data.RSI
        self.macd = self.data.MACD
        self.macd_signal = self.data.MACD_Signal

    def next(self) -> None:
        """
        Execute strategy logic for each new candle.

        Flow:
            1. If in position: check exit conditions (stop/target/reversal)
            2. If flat: evaluate long/short entry conditions
            3. Execute trades with risk management
        """
        # Skip if not enough data
        if len(self.data) < 2:
            return

        current_prediction = self.price_change_predicted[-1]
        current_rsi = self.rsi[-1]
        current_macd = self.macd[-1]
        current_macd_signal = self.macd_signal[-1]

        # If we have a position, check stop-loss and take-profit
        if self.position:
            self._manage_position()
            return

        # Generate long signal
        if self._should_go_long(current_prediction, current_rsi, current_macd, current_macd_signal):
            self._open_long()

        # Generate short signal
        elif self._should_go_short(current_prediction, current_rsi, current_macd, current_macd_signal):
            self._open_short()

    def _should_go_long(self, prediction: float, rsi: float, macd: float, macd_signal: float) -> bool:
        """
        Evaluate long entry conditions.

        Args:
            prediction: Predicted price change (%)
            rsi: Current RSI value (0-100)
            macd: MACD line value
            macd_signal: MACD signal line value

        Returns:
            True if all conditions met:
                - Prediction > prediction_threshold (bullish LSTM)
                - RSI < rsi_overbought (room to move up)
                - MACD > MACD_signal (trend confirmation)
        """
        prediction_bullish = prediction > self.prediction_threshold
        rsi_ok = rsi < self.rsi_overbought
        macd_bullish = macd > macd_signal

        return prediction_bullish and rsi_ok and macd_bullish

    def _should_go_short(self, prediction: float, rsi: float, macd: float, macd_signal: float) -> bool:
        """
        Evaluate short entry conditions.

        Args:
            prediction: Predicted price change (%)
            rsi: Current RSI value (0-100)
            macd: MACD line value
            macd_signal: MACD signal line value

        Returns:
            True if all conditions met:
                - Prediction < -prediction_threshold (bearish LSTM)
                - RSI > rsi_oversold (room to move down)
                - MACD < MACD_signal (downtrend confirmation)
        """
        prediction_bearish = prediction < -self.prediction_threshold
        rsi_ok = rsi > self.rsi_oversold
        macd_bearish = macd < macd_signal

        return prediction_bearish and rsi_ok and macd_bearish

    def _open_long(self) -> None:
        """Open a long position with risk management."""
        # Use position_size as a fraction of equity (0-1)
        # With FractionalBacktest, this represents the fraction of equity to use
        size = self.position_size  # e.g., 0.95 = 95% of equity
        
        # Set stop loss and take profit
        entry_price = self.data.Close[-1]
        sl_price = entry_price * (1 - self.stop_loss_pct)
        tp_price = entry_price * (1 + self.take_profit_pct)

        self.buy(size=size, sl=sl_price, tp=tp_price)

    def _open_short(self) -> None:
        """Open a short position with risk management."""
        # Use position_size as a fraction of equity (0-1)
        # With FractionalBacktest, this represents the fraction of equity to use
        size = self.position_size  # e.g., 0.95 = 95% of equity
        
        # Set stop loss and take profit
        entry_price = self.data.Close[-1]
        sl_price = entry_price * (1 + self.stop_loss_pct)
        tp_price = entry_price * (1 - self.take_profit_pct)

        self.sell(size=size, sl=sl_price, tp=tp_price)

    def _manage_position(self) -> None:
        """
        Manage existing position with trailing stop and exit conditions.
        """
        current_prediction = self.price_change_predicted[-1]

        # Exit long if prediction turns bearish
        if self.position.is_long and current_prediction < -self.prediction_threshold:
            self.position.close()

        # Exit short if prediction turns bullish
        elif self.position.is_short and current_prediction > self.prediction_threshold:
            self.position.close()


class AggressiveLSTMStrategy(LSTMScalpingStrategy):
    """
    Aggressive scalping variant for high-frequency trading.

    Characteristics:
        - Very sensitive (0.02% threshold) - more trades
        - Tight risk management (0.3% SL, 0.6% TP) - quick exits
        - High leverage (98% equity) - maximize capital efficiency

    Use when:
        - High confidence in model accuracy
        - Liquid markets with tight spreads
        - Can handle higher trade frequency

    Risk: Higher drawdown potential, more sensitive to noise
    """
    prediction_threshold = 0.0002  # 0.02% threshold (very sensitive)
    stop_loss_pct = 0.003        # 0.3% stop
    take_profit_pct = 0.006      # 0.6% target
    position_size = 0.98         # 98% of equity


class ConservativeLSTMStrategy(LSTMScalpingStrategy):
    """
    Conservative variant for stable, lower-risk trading.

    Characteristics:
        - Less sensitive (0.1% threshold) - fewer, higher-quality trades
        - Wide risk management (1% SL, 2% TP) - room for volatility
        - Lower leverage (50% equity) - preserve capital

    Use when:
        - Model accuracy uncertain
        - Volatile or illiquid markets
        - Priority is capital preservation

    Risk: Fewer opportunities, may miss quick reversals
    """
    prediction_threshold = 0.001  # 0.1% threshold (less sensitive than default)
    stop_loss_pct = 0.01         # 1% stop
    take_profit_pct = 0.02       # 2% target
    position_size = 0.5          # 50% of equity
