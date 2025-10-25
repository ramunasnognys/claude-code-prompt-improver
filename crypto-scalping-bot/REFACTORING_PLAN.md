 Specification for approval
────────────────────────────────────────────────────────────────────────────────────

 Analysis of Current Performance

 Current Results (March 17-31, 2024):
 •  Conservative: -4.79% return (best, but still losing)
 •  Default: -21.02% return
 •  Aggressive: -44.41% return (worst)

 Key Issues Identified:

 1. Data Leakage & Overfitting:
   •  Model trained on Jan-Mar 2024 (129K samples)
   •  Backtest on last 2 weeks of March (overlaps training data!)
   •  LSTM likely memorized patterns that don't generalize
   •  70/15/15 split means test set is IN the backtest period

 2. Strategy Problems:
   •  Extremely low prediction threshold (0.05% = 0.5 basis points)
   •  95% position size too aggressive with tight stops
   •  Commission (0.04%) eats into tiny profit targets
   •  Stop-loss (0.5%) < commission + slippage (0.05% total) = guaranteed loss on
      stops
   •  Model predicts -2.5% mean error (consistently underestimates)

 3. Model Architecture Issues:
   •  Only 6 features (missing volume indicators, market microstructure)
   •  60-period lookback may be too short for meaningful patterns
   •  30 epochs insufficient for convergence
   •  Normalized predictions have systematic bias

 4. No Walk-Forward Validation:
   •  Single train/test split prone to overfitting
   •  No out-of-sample period testing
   •  Parameters not optimized per market regime

 Refactoring Plan to Achieve Profitability

 Phase 1: Fix Data Leakage & Validation (CRITICAL)

 1.1 Implement Proper Train/Test Split
 •  Train: Jan 1 - Feb 28, 2024 (2 months)
 •  Validation: Mar 1-15, 2024 (2 weeks)
 •  Test/Backtest: Mar 16-31, 2024 (2 weeks, completely unseen)
 •  Ensures zero data leakage

 1.2 Add Walk-Forward Validation
 •  Rolling window: Train on N days, test on next M days
 •  Retrain model every week with expanding window
 •  Prevents overfitting to specific market regime

 Phase 2: Fix Strategy Risk/Reward Math

 2.1 Recalibrate Thresholds Based on Costs
 •  Minimum profitable trade: 2 × (commission + slippage) = 2 × 0.05% = 0.1%
 •  New prediction_threshold: 0.002 (0.2% minimum move)
 •  Risk/reward ratio: Target 2:1 minimum (TP = 2 × SL)
 •  Stop-loss: 0.01 (1% to survive noise)
 •  Take-profit: 0.02 (2% for positive expectancy)

 2.2 Conservative Position Sizing
 •  Reduce default position_size: 0.3 (30% of equity)
 •  Kelly criterion sizing based on win rate and profit factor
 •  Scale up only after profitability proven

 2.3 Add Trade Filters
 •  Minimum RSI distance from extremes (RSI 25-75 instead of 30-70)
 •  Require MACD confirmation + ADX > 20 (trending market)
 •  Avoid trading during low volume periods (<20% of avg volume)
 •  Add time-based filters (avoid first/last hour, low liquidity periods)

 Phase 3: Enhance Model Architecture

 3.1 Expand Feature Set
 •  Add ATR (volatility adjustment for stops)
 •  Add volume profile features (volume_ratio, volume_sma changes)
 •  Add price momentum (ROC, momentum indicators)
 •  Add higher timeframe context (5m/15m SMA as features)
 •  Total features: 12-15 (from current 6)

 3.2 Improve LSTM Training
 •  Increase epochs: 50 (from 30, with early stopping)
 •  Add batch normalization layers
 •  Tune dropout: 0.3 (stronger regularization)
 •  Add L2 regularization to Dense layer
 •  Experiment with bidirectional LSTM
 •  Increase lookback: 120 periods (2 hours context)

 3.3 Address Prediction Bias
 •  Model currently underestimates by -2.5% (systematic error)
 •  Add bias correction layer or post-processing
 •  Consider predicting price CHANGE instead of absolute price
 •  Experiment with classification (up/down/neutral) instead of regression

 Phase 4: Advanced Strategy Improvements

 4.1 Multi-Timeframe Analysis
 •  Use 1m for signals, 5m for trend filter
 •  Only long when 5m trend is up, short when down
 •  Add 15m moving averages as support/resistance

 4.2 Dynamic Stop-Loss & Take-Profit
 •  ATR-based stops: SL = 1.5 × ATR (adapts to volatility)
 •  Trailing stops: Move SL to breakeven after 50% of TP reached
 •  Time-based exits: Close after N bars if no movement

 4.3 Market Regime Detection
 •  Classify market as trending/ranging using ADX
 •  Use aggressive strategy in trending markets (ADX > 25)
 •  Use conservative or no trading in ranging markets (ADX < 20)

 Phase 5: Parameter Optimization

 5.1 Grid Search Optimization
 •  Optimize: prediction_threshold, stop_loss_pct, take_profit_pct, position_size
 •  Constraint: TP must be ≥ 2 × SL
 •  Maximize: Sharpe ratio with min 100 trades
 •  Use walk-forward validation for robustness

 5.2 Ensemble Methods
 •  Train 3 models on different feature sets
 •  Use voting: Only trade when 2/3 models agree
 •  Reduces false signals, improves win rate

 Phase 6: Validation & Testing

 6.1 Out-of-Sample Testing
 •  Test on completely different period (April 2024 data)
 •  Test on different asset (ETH/USDT)
 •  Test on different market regime (bear market data)

 6.2 Monte Carlo Simulation
 •  Randomize trade order to test robustness
 •  Stress test with 2x commissions, 3x slippage
 •  Ensure positive expectancy across scenarios

 Expected Improvements

 Conservative Estimates (after refactoring):
 •  Win rate: 35-40% (from 32-34%)
 •  Average win/loss ratio: 2.5:1 (from 1.5:1)
 •  Max drawdown: <10% (from 25%)
 •  Monthly return: 3-8% (from -21%)
 •  Sharpe ratio: >1.0 (from -215)

 Key Success Metrics:
 •  Profit factor > 1.5
 •  Sharpe ratio > 1.0
 •  Win rate > 35% with 2:1 RR ratio
 •  Maximum 3 consecutive losses without circuit breaker

 Implementation Order (Priority)

 1. CRITICAL: Fix data leakage (Phase 1.1) - Without this, all results are invalid
 2. HIGH: Fix risk/reward math (Phase 2) - Current setup mathematically
    unprofitable
 3. HIGH: Expand features + retrain (Phase 3.1-3.2) - Model needs more information
 4. MEDIUM: Add trade filters (Phase 2.3) - Quality over quantity
 5. MEDIUM: Walk-forward validation (Phase 1.2) - Ensures robustness
 6. LOW: Advanced features (Phase 3.3, 4, 5) - Optimization after baseline works

 Would you like me to proceed with this refactoring plan?