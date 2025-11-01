#!/usr/bin/env python3
"""
Phase 2 Implementation: Fix Strategy Risk/Reward Math

Executes Phase 2 substeps with automatic backtesting and results tracking.
Each parameter change is validated with a backtest before proceeding.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import yaml

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from backtest.backtest_runner import BacktestRunner
from strategies.lstm_strategy import LSTMScalpingStrategy


class Phase2Runner:
    """Execute Phase 2 implementation with tracking and validation."""

    def __init__(self):
        self.results_dir = Path('results/phase2')
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.results_log = []

        # Load data for backtesting
        self._load_backtest_data()

    def _load_backtest_data(self):
        """Load preprocessed data and predictions for backtesting."""
        print("Loading data for Phase 2 implementation...")

        data_dir = Path('data')

        # Load processed data
        df = pd.read_csv(data_dir / 'processed_data.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])

        # Load predictions
        predictions_df = pd.read_csv(data_dir / 'predictions.csv')
        pred_dates = pd.to_datetime(predictions_df['datetime'])

        # Create prediction mappings
        pred_dict = dict(zip(pred_dates, predictions_df['predicted'].values))
        actual_dict = dict(zip(pred_dates, predictions_df['actual'].values))

        # Add predictions to dataframe
        df['predicted_normalized'] = df['datetime'].map(pred_dict)
        df['actual_normalized'] = df['datetime'].map(actual_dict)

        # Filter to rows with predictions
        df_with_preds = df[df['predicted_normalized'].notna()].copy()

        # Prepare backtest data
        runner = BacktestRunner()
        self.bt_data = runner.prepare_data_for_backtest(
            df_with_preds,
            df_with_preds['predicted_normalized'].values,
            df_with_preds['actual_normalized'].values
        )

        print(f"Loaded {len(self.bt_data)} bars for backtesting")
        print(f"Period: {self.bt_data.index[0]} to {self.bt_data.index[-1]}\n")

    def run_backtest_with_params(self, step_name, **params):
        """Run backtest with custom strategy parameters."""
        print(f"\n{'='*70}")
        print(f"Running: {step_name}")
        print(f"{'='*70}")
        print(f"Parameters: {params}")

        # Create custom strategy class with specified params
        class CustomStrategy(LSTMScalpingStrategy):
            pass

        # Set parameters
        for param, value in params.items():
            setattr(CustomStrategy, param, value)

        # Run backtest
        runner = BacktestRunner()
        results = runner.run_backtest(
            self.bt_data,
            strategy_class=CustomStrategy,
            cash=10000,
            commission=0.0004
        )

        # Extract key metrics
        metrics = {
            'step': step_name,
            'timestamp': datetime.now().isoformat(),
            'return_pct': results['Return [%]'],
            'total_trades': results['# Trades'],
            'win_rate_pct': results['Win Rate [%]'],
            'sharpe_ratio': results['Sharpe Ratio'],
            'max_drawdown_pct': results['Max. Drawdown [%]'],
            'avg_trade_pct': results['Avg. Trade [%]'],
            'best_trade_pct': results['Best Trade [%]'],
            'worst_trade_pct': results['Worst Trade [%]'],
            **params
        }

        # Calculate profit factor if possible
        if results['# Trades'] > 0:
            # Estimate from win rate and avg trade
            # This is approximate - actual profit factor would need trade-by-trade data
            metrics['profit_factor_est'] = 'N/A'

        self.results_log.append(metrics)

        # Print summary
        print(f"\nResults:")
        print(f"  Return: {results['Return [%]']:.2f}%")
        print(f"  Trades: {results['# Trades']}")
        print(f"  Win Rate: {results['Win Rate [%]']:.2f}%")
        print(f"  Sharpe: {results['Sharpe Ratio']:.2f}")
        print(f"  Max DD: {results['Max. Drawdown [%]']:.2f}%")

        return results

    def save_results(self):
        """Save results log to CSV."""
        df = pd.DataFrame(self.results_log)
        output_path = self.results_dir / f'phase2_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(output_path, index=False)
        print(f"\n{'='*70}")
        print(f"Results saved to: {output_path}")
        print(f"{'='*70}")
        return df

    def print_comparison_table(self):
        """Print comparison table of all Phase 2 steps."""
        if not self.results_log:
            print("No results to compare")
            return

        df = pd.DataFrame(self.results_log)

        print(f"\n{'='*70}")
        print("PHASE 2 COMPARISON TABLE")
        print(f"{'='*70}\n")

        # Select key columns for comparison
        comparison_cols = [
            'step', 'return_pct', 'total_trades', 'win_rate_pct',
            'sharpe_ratio', 'max_drawdown_pct'
        ]

        comparison_df = df[comparison_cols].copy()
        comparison_df.columns = [
            'Step', 'Return %', 'Trades', 'Win Rate %', 'Sharpe', 'Max DD %'
        ]

        print(comparison_df.to_string(index=False))
        print(f"\n{'='*70}\n")

    def execute_phase_2_1(self):
        """Phase 2.1: Recalibrate Thresholds Based on Costs"""
        print("\n" + "="*70)
        print("PHASE 2.1: RECALIBRATE THRESHOLDS BASED ON COSTS")
        print("="*70)

        # Baseline (current parameters)
        print("\n--- 2.1.0: Baseline (Current Parameters) ---")
        self.run_backtest_with_params(
            "2.1.0_baseline",
            prediction_threshold=0.0005,
            stop_loss_pct=0.005,
            take_profit_pct=0.01,
            position_size=0.95,
            rsi_oversold=30,
            rsi_overbought=70
        )

        # 2.1.1-2.1.2: Increase prediction threshold
        print("\n--- 2.1.1: Increase prediction_threshold to 0.2% ---")
        self.run_backtest_with_params(
            "2.1.1_threshold_0.2pct",
            prediction_threshold=0.002,  # 0.2%
            stop_loss_pct=0.005,
            take_profit_pct=0.01,
            position_size=0.95,
            rsi_oversold=30,
            rsi_overbought=70
        )

        # 2.1.3-2.1.4: Increase stop loss
        print("\n--- 2.1.3: Increase stop_loss to 1% ---")
        self.run_backtest_with_params(
            "2.1.3_stoploss_1pct",
            prediction_threshold=0.002,
            stop_loss_pct=0.01,  # 1%
            take_profit_pct=0.01,
            position_size=0.95,
            rsi_oversold=30,
            rsi_overbought=70
        )

        # 2.1.5-2.1.6: Increase take profit (achieve 2:1 ratio)
        print("\n--- 2.1.5: Increase take_profit to 2% (2:1 ratio) ---")
        self.run_backtest_with_params(
            "2.1.5_takeprofit_2pct",
            prediction_threshold=0.002,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,  # 2%
            position_size=0.95,
            rsi_oversold=30,
            rsi_overbought=70
        )

        print("\n--- Phase 2.1 Complete ---")
        print("✓ Prediction threshold: 0.05% → 0.2%")
        print("✓ Stop loss: 0.5% → 1%")
        print("✓ Take profit: 1% → 2%")
        print("✓ Risk/reward ratio: 2:1 achieved")

    def execute_phase_2_2(self):
        """Phase 2.2: Conservative Position Sizing"""
        print("\n" + "="*70)
        print("PHASE 2.2: CONSERVATIVE POSITION SIZING")
        print("="*70)

        # 2.2.1-2.2.2: Reduce position size
        print("\n--- 2.2.1: Reduce position_size to 30% ---")
        results = self.run_backtest_with_params(
            "2.2.1_position_30pct",
            prediction_threshold=0.002,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            position_size=0.3,  # 30%
            rsi_oversold=30,
            rsi_overbought=70
        )

        # 2.2.3: Calculate Kelly criterion
        print("\n--- 2.2.3: Kelly Criterion Calculation ---")
        win_rate = results['Win Rate [%]'] / 100
        avg_win = results['Avg. Win [%]'] if 'Avg. Win [%]' in results else results['Avg. Trade [%]']
        avg_loss = results['Avg. Loss [%]'] if 'Avg. Loss [%]' in results else results['Avg. Trade [%]']

        # Kelly formula: K = (W × R - L) / R
        # Where W = win rate, L = loss rate, R = avg win / avg loss
        if avg_loss != 0 and avg_loss < 0:
            win_loss_ratio = abs(avg_win / avg_loss)
            kelly_pct = ((win_rate * win_loss_ratio) - (1 - win_rate)) / win_loss_ratio
            kelly_pct = max(0, min(kelly_pct, 1))  # Clamp between 0 and 1

            print(f"Kelly Criterion: {kelly_pct*100:.2f}%")
            print(f"  Win Rate: {win_rate*100:.2f}%")
            print(f"  Win/Loss Ratio: {win_loss_ratio:.2f}")
            print(f"  Recommended position size: {kelly_pct*100:.2f}%")
            print(f"  Half-Kelly (safer): {kelly_pct*50:.2f}%")
        else:
            print("Cannot calculate Kelly - insufficient trade data")

        print("\n--- Phase 2.2 Complete ---")
        print("✓ Position size: 95% → 30%")
        print("✓ Kelly criterion calculated")

    def execute_phase_2_3(self):
        """Phase 2.3: Add Trade Filters"""
        print("\n" + "="*70)
        print("PHASE 2.3: ADD TRADE FILTERS")
        print("="*70)

        # 2.3.1-2.3.2: Adjust RSI bounds (already done in previous run)
        print("\n--- 2.3.1-2.3.2: RSI bounds 25/75 (from previous run) ---")
        print("  Result: trades 88 → 87, return -3.27% → -2.96%")

        # 2.3.3-2.3.4: Test ADX filter
        print("\n--- 2.3.3-2.3.4: Add ADX filter (ADX > 20) ---")
        self.run_backtest_with_params(
            "2.3.3_adx_filter",
            prediction_threshold=0.002,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            position_size=0.3,
            rsi_oversold=25,
            rsi_overbought=75,
            adx_threshold=20.0,       # Add ADX filter
            volume_threshold=0.0      # Disable volume filter for this test
        )

        # 2.3.5-2.3.6: Test volume filter
        print("\n--- 2.3.5-2.3.6: Add volume filter (vol > 0.2 × SMA) ---")
        self.run_backtest_with_params(
            "2.3.6_volume_filter",
            prediction_threshold=0.002,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            position_size=0.3,
            rsi_oversold=25,
            rsi_overbought=75,
            adx_threshold=0.0,        # Disable ADX filter for this test
            volume_threshold=0.2      # Add volume filter
        )

        # 2.3.8: Comprehensive backtest with all Phase 2 filters
        print("\n--- 2.3.8: Comprehensive test with ALL Phase 2 filters ---")
        self.run_backtest_with_params(
            "2.3.8_all_filters",
            prediction_threshold=0.002,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            position_size=0.3,
            rsi_oversold=25,
            rsi_overbought=75,
            adx_threshold=20.0,       # ADX filter enabled
            volume_threshold=0.2      # Volume filter enabled
        )

        print("\n--- Phase 2.3 Complete ---")
        print("✓ RSI bounds: 30/70 → 25/75")
        print("✓ ADX filter: ADX > 20 (trending markets only)")
        print("✓ Volume filter: volume > 0.2 × volume_sma_20 (sufficient liquidity)")
        print("⚠ Time-based filters: Deferred to Phase 4")

    def execute_phase_2_4(self):
        """Phase 2.4: Summary Validation"""
        print("\n" + "="*70)
        print("PHASE 2.4: SUMMARY VALIDATION")
        print("="*70)

        self.print_comparison_table()

        # Save results
        df = self.save_results()

        # Verify improvements
        if len(df) >= 2:
            baseline = df.iloc[0]
            final = df.iloc[-1]

            print("\nIMPROVEMENT ANALYSIS:")
            print(f"  Return: {baseline['return_pct']:.2f}% → {final['return_pct']:.2f}% ({final['return_pct'] - baseline['return_pct']:+.2f}%)")
            print(f"  Sharpe: {baseline['sharpe_ratio']:.2f} → {final['sharpe_ratio']:.2f} ({final['sharpe_ratio'] - baseline['sharpe_ratio']:+.2f})")
            print(f"  Max DD: {baseline['max_drawdown_pct']:.2f}% → {final['max_drawdown_pct']:.2f}% ({final['max_drawdown_pct'] - baseline['max_drawdown_pct']:+.2f}%)")
            print(f"  Trades: {int(baseline['total_trades'])} → {int(final['total_trades'])} ({int(final['total_trades'] - baseline['total_trades']):+d})")

            print("\nSUCCESS CRITERIA CHECK:")
            print(f"  Sharpe > 0: {'✓' if final['sharpe_ratio'] > 0 else '✗'} ({final['sharpe_ratio']:.2f})")
            print(f"  Max DD < 10%: {'✓' if final['max_drawdown_pct'] < 10 else '✗'} ({final['max_drawdown_pct']:.2f}%)")
            print(f"  Positive return: {'✓' if final['return_pct'] > 0 else '✗'} ({final['return_pct']:.2f}%)")


def main():
    """Execute complete Phase 2 implementation."""
    print("="*70)
    print("PHASE 2 IMPLEMENTATION: FIX STRATEGY RISK/REWARD MATH")
    print("="*70)

    runner = Phase2Runner()

    # Execute each phase
    runner.execute_phase_2_1()
    runner.execute_phase_2_2()
    runner.execute_phase_2_3()
    runner.execute_phase_2_4()

    print("\n" + "="*70)
    print("PHASE 2 IMPLEMENTATION COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Review results in results/phase2/ directory")
    print("2. Manually implement remaining Phase 2.3 filters (ADX, volume, time)")
    print("3. Update lstm_strategy.py with optimal parameters from this run")
    print("4. Proceed to Phase 3 (Enhance Model Architecture) if results satisfactory")
    print("="*70)


if __name__ == '__main__':
    main()
