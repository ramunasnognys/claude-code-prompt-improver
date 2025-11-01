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

    Strategy Parameters (Phase 2 optimized):
        - prediction_threshold: Min predicted price change (0.2%, Phase 2.1)
        - rsi_oversold/overbought: RSI bounds (25/75, Phase 2.3)
        - stop_loss_pct: Stop loss percentage (1%, Phase 2.1)
        - take_profit_pct: Take profit percentage (2%, Phase 2.1, 2:1 RR)
        - position_size: Fraction of equity per trade (30%, Phase 2.2)

    Example:
        >>> from backtesting import Backtest
        >>> bt = Backtest(data, LSTMScalpingStrategy, cash=10000)
        >>> stats = bt.run()
        >>> print(stats)
    """

    # Strategy parameters (can be optimized)
    # PHASE 2 OPTIMIZED PARAMETERS (2025-10-25)
    prediction_threshold = 0.002   # 0.2% minimum price change (Phase 2.1: quality over quantity)
    rsi_oversold = 25              # Phase 2.3: expanded RSI range
    rsi_overbought = 75            # Phase 2.3: expanded RSI range
    stop_loss_pct = 0.01           # 1% stop loss (Phase 2.1: survive noise)
    take_profit_pct = 0.02         # 2% take profit (Phase 2.1: 2:1 risk/reward)
    position_size = 0.3            # 30% of equity (Phase 2.2: conservative sizing, reduced max DD)

    # PHASE 2.3 TRADE FILTERS (Quality over Quantity)
    # Testing showed volume filter alone performs BEST (return -2.96%, Sharpe -0.54)
    # ADX filter alone or combined with volume performed worse
    adx_threshold = 0.0            # Disabled (testing showed ADX filter worsens results)
    volume_threshold = 0.2         # Min volume ratio vs 20-period SMA (0.2 = 20% above avg)

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

        # Note: Indicators accessed directly from self.data in next() method

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
        # Access indicators directly from data to get current bar values
        current_rsi = self.data.RSI[-1]
        current_macd = self.data.MACD[-1]
        current_macd_signal = self.data.MACD_Signal[-1]

        # PHASE 2.3: Extract ADX and volume for trade filters
        current_adx = self.data.ADX[-1]
        current_volume = self.data.Volume[-1]
        current_volume_sma = self.data.Volume_SMA[-1]

        # If we have a position, check stop-loss and take-profit
        if self.position:
            self._manage_position()
            return

        # Generate long signal (Phase 2.3: added ADX and volume filters)
        if self._should_go_long(current_prediction, current_rsi, current_macd, current_macd_signal,
                                current_adx, current_volume, current_volume_sma):
            self._open_long()

        # Generate short signal (Phase 2.3: added ADX and volume filters)
        elif self._should_go_short(current_prediction, current_rsi, current_macd, current_macd_signal,
                                   current_adx, current_volume, current_volume_sma):
            self._open_short()

    def _should_go_long(self, prediction: float, rsi: float, macd: float, macd_signal: float,
                       adx: float, volume: float, volume_sma: float) -> bool:
        """
        Evaluate long entry conditions.

        Args:
            prediction: Predicted price change (%)
            rsi: Current RSI value (0-100)
            macd: MACD line value
            macd_signal: MACD signal line value
            adx: Current ADX value (trend strength)
            volume: Current volume
            volume_sma: 20-period volume SMA

        Returns:
            True if all conditions met:
                - Prediction > prediction_threshold (bullish LSTM)
                - RSI < rsi_overbought (room to move up)
                - MACD > MACD_signal (trend confirmation)
                - ADX > adx_threshold (trending market, Phase 2.3)
                - Volume > volume_threshold * volume_sma (sufficient liquidity, Phase 2.3)
        """
        prediction_bullish = prediction > self.prediction_threshold
        rsi_ok = rsi < self.rsi_overbought
        macd_bullish = macd > macd_signal

        # PHASE 2.3: Add trend and volume filters
        adx_ok = adx > self.adx_threshold
        volume_ok = volume > (self.volume_threshold * volume_sma)

        return prediction_bullish and rsi_ok and macd_bullish and adx_ok and volume_ok

    def _should_go_short(self, prediction: float, rsi: float, macd: float, macd_signal: float,
                        adx: float, volume: float, volume_sma: float) -> bool:
        """
        Evaluate short entry conditions.

        Args:
            prediction: Predicted price change (%)
            rsi: Current RSI value (0-100)
            macd: MACD line value
            macd_signal: MACD signal line value
            adx: Current ADX value (trend strength)
            volume: Current volume
            volume_sma: 20-period volume SMA

        Returns:
            True if all conditions met:
                - Prediction < -prediction_threshold (bearish LSTM)
                - RSI > rsi_oversold (room to move down)
                - MACD < MACD_signal (downtrend confirmation)
                - ADX > adx_threshold (trending market, Phase 2.3)
                - Volume > volume_threshold * volume_sma (sufficient liquidity, Phase 2.3)
        """
        prediction_bearish = prediction < -self.prediction_threshold
        rsi_ok = rsi > self.rsi_oversold
        macd_bearish = macd < macd_signal

        # PHASE 2.3: Add trend and volume filters
        adx_ok = adx > self.adx_threshold
        volume_ok = volume > (self.volume_threshold * volume_sma)

        return prediction_bearish and rsi_ok and macd_bearish and adx_ok and volume_ok

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

    PHASE 2 UPDATED: Maintains 2:1 risk/reward with tighter ranges.

    Characteristics:
        - More sensitive (0.15% threshold) - more trades than default
        - 2:1 risk management (0.75% SL, 1.5% TP) - maintains RR ratio
        - Higher leverage (50% equity) - balanced risk (Phase 2 compliant)

    Use when:
        - High confidence in model accuracy
        - Liquid markets with tight spreads
        - Can handle higher trade frequency

    Risk: Higher drawdown potential, more sensitive to noise
    """
    prediction_threshold = 0.0015  # 0.15% threshold (more sensitive than default 0.2%)
    rsi_oversold = 25              # Same as default
    rsi_overbought = 75            # Same as default
    stop_loss_pct = 0.0075         # 0.75% stop (tighter, still > commission)
    take_profit_pct = 0.015        # 1.5% target (2:1 ratio maintained)
    position_size = 0.5            # 50% of equity (Phase 2 compliant, less than old 98%)
    adx_threshold = 0.0            # Disabled (same as default)
    volume_threshold = 0.2         # Volume filter enabled


class ConservativeLSTMStrategy(LSTMScalpingStrategy):
    """
    Conservative variant for stable, lower-risk trading.

    PHASE 2 UPDATED: Wider targets, minimal position size.

    Characteristics:
        - Less sensitive (0.3% threshold) - fewer, higher-quality trades
        - Wide risk management (1.5% SL, 3% TP) - 2:1 ratio, room for volatility
        - Minimal leverage (20% equity) - maximum capital preservation

    Use when:
        - Model accuracy uncertain
        - Volatile or illiquid markets
        - Priority is capital preservation

    Risk: Fewer opportunities, may miss quick reversals
    """
    prediction_threshold = 0.003  # 0.3% threshold (less sensitive than default 0.2%)
    rsi_oversold = 25             # Same as default
    rsi_overbought = 75           # Same as default
    stop_loss_pct = 0.015         # 1.5% stop (wider for volatility)
    take_profit_pct = 0.03        # 3% target (2:1 ratio maintained)
    position_size = 0.2           # 20% of equity (ultra-conservative)
    adx_threshold = 0.0           # Disabled (same as default)
    volume_threshold = 0.2        # Volume filter enabled
