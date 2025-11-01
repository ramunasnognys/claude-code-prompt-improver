#!/usr/bin/env python3
"""
Validate crypto trading bot configuration.

Checks config.yaml for:
- Missing required fields
- Invalid value ranges
- Logical inconsistencies
- Risk management red flags
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def load_config(config_path: str) -> Dict:
    """Load YAML configuration."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Config not found: {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Invalid YAML: {e}")
        sys.exit(1)


def validate_exchange(config: Dict) -> List[str]:
    """Validate exchange configuration."""
    errors = []
    exchange = config.get('exchange', {})

    if not exchange.get('name'):
        errors.append("exchange.name is required")
    elif exchange['name'] not in ['okx', 'binance', 'bybit', 'kraken']:
        errors.append(f"exchange.name '{exchange['name']}' not tested")

    return errors


def validate_trading(config: Dict) -> List[str]:
    """Validate trading parameters."""
    errors = []
    trading = config.get('trading', {})

    # Symbol format
    symbol = trading.get('symbol')
    if not symbol:
        errors.append("trading.symbol is required")
    elif ':' not in symbol:
        errors.append(f"trading.symbol must be futures format (e.g., BTC/USDT:USDT), got {symbol}")

    # Timeframe
    tf = trading.get('timeframe')
    if tf not in ['1m', '5m', '15m', '1h', '4h', '1d']:
        errors.append(f"trading.timeframe '{tf}' invalid")

    # Risk parameters
    capital = trading.get('initial_capital', 0)
    if capital < 100:
        errors.append(f"trading.initial_capital {capital} too small (min 100)")

    # Position sizing
    max_pos = trading.get('max_position_size', 0)
    if max_pos <= 0 or max_pos > 1:
        errors.append(f"trading.max_position_size {max_pos} must be 0-1")

    # Leverage
    lev = trading.get('leverage', 0)
    if lev < 1 or lev > 125:
        errors.append(f"trading.leverage {lev} must be 1-125")
    elif lev > 10:
        print(f"⚠️  High leverage {lev}x - risk of liquidation")

    # Stop loss
    sl = trading.get('stop_loss_pct', 0)
    if sl <= 0 or sl >= 0.1:  # 10% max
        errors.append(f"trading.stop_loss_pct {sl:.4f} invalid (should be 0.001-0.1)")

    # Take profit
    tp = trading.get('take_profit_pct', 0)
    if tp <= 0 or tp >= 0.5:  # 50% max
        errors.append(f"trading.take_profit_pct {tp:.4f} invalid (should be 0.001-0.5)")

    # Risk/reward ratio
    if sl > 0 and tp > 0:
        rr_ratio = tp / sl
        if rr_ratio < 0.5:
            errors.append(f"Risk/reward ratio {rr_ratio:.2f} too low (min 0.5)")
        elif rr_ratio < 1.0:
            print(f"⚠️  Risk/reward {rr_ratio:.2f} - need >50% win rate")

    # Daily loss limit
    daily_loss = trading.get('max_daily_loss', 0)
    if daily_loss <= 0 or daily_loss > 0.5:
        errors.append(f"trading.max_daily_loss {daily_loss:.2%} invalid")

    # Open positions
    max_open = trading.get('max_open_positions', 0)
    if max_open < 1 or max_open > 10:
        errors.append(f"trading.max_open_positions {max_open} should be 1-10")

    # Position size total check
    total_exposure = max_open * max_pos
    if total_exposure > 2.0:
        print(f"⚠️  Total exposure {total_exposure:.0%} is very high")

    return errors


def validate_model(config: Dict) -> List[str]:
    """Validate LSTM model parameters."""
    errors = []
    model = config.get('model', {})

    # Type
    if model.get('type') != 'lstm':
        errors.append(f"model.type must be 'lstm'")

    # Lookback
    lookback = model.get('lookback_periods', 0)
    if lookback < 10 or lookback > 500:
        errors.append(f"model.lookback_periods {lookback} should be 10-500")

    # LSTM units
    units = model.get('lstm_units', [])
    if not units:
        errors.append("model.lstm_units is required")
    elif not all(isinstance(u, int) and u > 0 for u in units):
        errors.append(f"model.lstm_units {units} must be positive integers")
    elif len(units) < 1:
        errors.append("model.lstm_units must have at least 1 layer")
    elif len(units) > 5:
        print("⚠️  More than 5 LSTM layers - may overfit")

    # Dropout
    dropout = model.get('dropout_rate', 0)
    if dropout < 0 or dropout > 0.8:
        errors.append(f"model.dropout_rate {dropout} must be 0-0.8")

    # Epochs
    epochs = model.get('epochs', 0)
    if epochs < 5 or epochs > 500:
        errors.append(f"model.epochs {epochs} should be 5-500")

    # Batch size
    batch = model.get('batch_size', 0)
    if batch < 4 or batch > 512:
        errors.append(f"model.batch_size {batch} should be 4-512")

    # Learning rate
    lr = model.get('learning_rate', 0)
    if lr < 0.00001 or lr > 0.1:
        errors.append(f"model.learning_rate {lr} should be 0.00001-0.1")

    # Features
    features = model.get('features', [])
    if not features:
        errors.append("model.features is required")
    elif len(features) < 2:
        errors.append(f"model.features should have >2, got {len(features)}")
    elif len(features) > 50:
        print(f"⚠️  Many features ({len(features)}) - check for redundancy")

    return errors


def validate_backtesting(config: Dict) -> List[str]:
    """Validate backtesting parameters."""
    errors = []
    bt = config.get('backtesting', {})

    # Dates
    start = bt.get('start_date')
    end = bt.get('end_date')

    if not start or not end:
        errors.append("backtesting.start_date and end_date required")
    elif start >= end:
        errors.append(f"start_date {start} >= end_date {end}")

    # Commission
    comm = bt.get('commission', 0)
    if comm < 0:
        errors.append(f"backtesting.commission {comm:.6f} cannot be negative")
    elif comm > 0.01:  # 1%
        print(f"⚠️  Commission {comm:.4%} seems high")

    # Slippage
    slip = bt.get('slippage', 0)
    if slip < 0 or slip > 0.01:
        errors.append(f"backtesting.slippage {slip:.6f} should be 0-0.01")

    return errors


def validate_indicators(config: Dict) -> List[str]:
    """Validate technical indicator parameters."""
    errors = []
    ind = config.get('indicators', {})

    # RSI period
    rsi = ind.get('rsi_period', 0)
    if rsi < 5 or rsi > 50:
        errors.append(f"indicators.rsi_period {rsi} should be 5-50")

    # MACD parameters
    fast = ind.get('macd_fast', 0)
    slow = ind.get('macd_slow', 0)
    if fast >= slow:
        errors.append(f"macd_fast {fast} must be < macd_slow {slow}")

    # Bollinger Bands
    bb_period = ind.get('bb_period', 0)
    if bb_period < 5 or bb_period > 100:
        errors.append(f"indicators.bb_period {bb_period} should be 5-100")

    bb_std = ind.get('bb_std', 0)
    if bb_std < 1 or bb_std > 4:
        errors.append(f"indicators.bb_std {bb_std} should be 1-4")

    return errors


def check_consistency(config: Dict) -> List[str]:
    """Check logical consistency across sections."""
    warnings = []

    # Model features vs preprocessing
    features = config.get('model', {}).get('features', [])
    if 'adx_14' in features:
        strategy = config.get('model', {})
        print("⚠️  ADX in features but Phase 2.3 tests show it hurts Sharpe")

    # Fee impact on profitability
    commission = config.get('backtesting', {}).get('commission', 0)
    tp = config.get('trading', {}).get('take_profit_pct', 0)
    sl = config.get('trading', {}).get('stop_loss_pct', 0)

    round_trip_cost = commission * 2
    if round_trip_cost > tp:
        warnings.append(f"Round-trip fee {round_trip_cost:.4%} > take_profit {tp:.4%} - unprofitable")

    return warnings


def main(config_path: str = 'config/config.yaml'):
    """Run all validations."""
    config = load_config(config_path)

    all_errors = []
    all_warnings = []

    print("🔍 Validating crypto trading config...\n")

    # Run validators
    validators = [
        ("Exchange", validate_exchange),
        ("Trading", validate_trading),
        ("Model", validate_model),
        ("Backtesting", validate_backtesting),
        ("Indicators", validate_indicators),
    ]

    for name, validator in validators:
        errors = validator(config)
        if errors:
            print(f"❌ {name} Configuration:")
            for err in errors:
                print(f"   - {err}")
            all_errors.extend(errors)
        else:
            print(f"✅ {name} Configuration: OK")

    # Consistency checks
    warnings = check_consistency(config)
    if warnings:
        print(f"\n⚠️  Warnings:")
        for warn in warnings:
            print(f"   - {warn}")
        all_warnings.extend(warnings)

    # Summary
    print(f"\n{'='*60}")
    if all_errors:
        print(f"❌ {len(all_errors)} critical error(s) found")
        print(f"⚠️  {len(all_warnings)} warning(s)")
        sys.exit(1)
    elif all_warnings:
        print(f"✅ Configuration valid")
        print(f"⚠️  {len(all_warnings)} warning(s) - review recommended")
        sys.exit(0)
    else:
        print(f"✅ Configuration valid - no issues found")
        sys.exit(0)


if __name__ == '__main__':
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config/config.yaml'
    main(config_path)
