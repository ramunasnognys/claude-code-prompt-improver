"""
Data preprocessing and feature engineering for LSTM model.
"""

import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands
import yaml
from sklearn.preprocessing import MinMaxScaler
import pickle
from pathlib import Path
from typing import Tuple, List


class DataPreprocessor:
    """
    Preprocess OHLCV data and engineer technical indicator features for LSTM training.

    Handles technical indicator calculation, feature scaling, sequence creation,
    and inverse transformations for prediction interpretation.

    Example:
        >>> preprocessor = DataPreprocessor()
        >>> df_with_indicators = preprocessor.add_technical_indicators(raw_df)
        >>> X, y, indices = preprocessor.create_sequences(df_with_indicators, lookback=60)
        >>> preprocessor.save_scaler('data/scaler.pkl')
    """

    def __init__(self, config_path: str = 'config/config.yaml') -> None:
        """
        Initialize preprocessor with configuration.

        Args:
            config_path: Path to YAML config file with indicator parameters and features list

        Attributes:
            scaler: MinMaxScaler for normalizing features to [0, 1]
            feature_columns: List of feature names used for training
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.scaler = MinMaxScaler()
        self.feature_columns = []

    def add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate and add technical indicators to OHLCV DataFrame.

        Adds momentum (RSI), trend (MACD, SMA, EMA), volatility (Bollinger Bands),
        and derived features (price changes, volume ratios).

        Args:
            df: Raw OHLCV DataFrame with columns: open, high, low, close, volume

        Returns:
            DataFrame with added features:
                - rsi_14: Relative Strength Index
                - macd, macd_signal, macd_diff: MACD indicators
                - bb_upper, bb_middle, bb_lower, bb_width: Bollinger Bands
                - price_change, volume_change: Percentage changes
                - hl_range: High-low range normalized by close
                - sma_10, sma_30, ema_10: Moving averages
                - volume_sma_20, volume_ratio: Volume indicators

        Example:
            >>> df_features = preprocessor.add_technical_indicators(raw_df)
            >>> print(df_features.columns)  # Shows all original + technical indicators
        """
        df = df.copy()

        # RSI
        rsi_period = self.config['indicators']['rsi_period']
        rsi = RSIIndicator(close=df['close'], window=rsi_period)
        df['rsi_14'] = rsi.rsi()

        # MACD
        macd_fast = self.config['indicators']['macd_fast']
        macd_slow = self.config['indicators']['macd_slow']
        macd_signal = self.config['indicators']['macd_signal']
        macd = MACD(
            close=df['close'],
            window_slow=macd_slow,
            window_fast=macd_fast,
            window_sign=macd_signal
        )
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()

        # Bollinger Bands
        bb_period = self.config['indicators']['bb_period']
        bb_std = self.config['indicators']['bb_std']
        bb = BollingerBands(
            close=df['close'],
            window=bb_period,
            window_dev=bb_std
        )
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()
        df['bb_width'] = bb.bollinger_wband()

        # Additional features
        df['price_change'] = df['close'].pct_change()
        df['volume_change'] = df['volume'].pct_change()

        # High-low range
        df['hl_range'] = (df['high'] - df['low']) / df['close']

        # Moving averages
        df['sma_10'] = df['close'].rolling(window=10).mean()
        df['sma_30'] = df['close'].rolling(window=30).mean()
        df['ema_10'] = df['close'].ewm(span=10, adjust=False).mean()

        # Volume indicators
        df['volume_sma_20'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma_20']

        return df

    def create_sequences(self, df: pd.DataFrame, lookback: int = 60, target_col: str = 'close') -> Tuple[np.ndarray, np.ndarray, pd.Index]:
        """
        Create 3D sequences for LSTM input from time series data.

        Applies MinMaxScaler to normalize features, then creates sliding window sequences
        where each X[i] contains lookback timesteps of features, and y[i] is the target value.

        Args:
            df: DataFrame with technical indicators (output of add_technical_indicators)
            lookback: Number of past timesteps in each sequence (window size)
            target_col: Feature to predict (typically 'close' price)

        Returns:
            Tuple containing:
                - X: Input sequences, shape (num_sequences, lookback, num_features)
                - y: Target values, shape (num_sequences,) - scaled values
                - indices: Original DataFrame indices for alignment

        Example:
            >>> X, y, idx = preprocessor.create_sequences(df, lookback=60)
            >>> print(X.shape)  # (n_samples, 60, 6) if 6 features
            >>> print(y.shape)  # (n_samples,)

        Note:
            Features are scaled using MinMaxScaler. Call save_scaler() to persist
            the scaler for inverse transforming predictions later.
        """
        # Select feature columns based on config
        feature_names = self.config['model']['features']

        # Ensure all features exist
        available_features = [f for f in feature_names if f in df.columns]
        if len(available_features) < len(feature_names):
            missing = set(feature_names) - set(available_features)
            print(f"Warning: Missing features {missing}. Using available features.")

        self.feature_columns = available_features

        # Drop NaN values (from indicators)
        df = df.dropna()

        # Extract features
        features = df[self.feature_columns].values

        # Normalize features
        features_scaled = self.scaler.fit_transform(features)

        # Create sliding window sequences for LSTM
        # Each X[i] contains lookback timesteps of all features
        # Each y[i] is the target value at timestep i
        X, y = [], []

        for i in range(lookback, len(features_scaled)):
            # Sequence: features from [i-lookback] to [i-1] (lookback timesteps)
            # Example: lookback=60, i=100 -> features[40:100]
            X.append(features_scaled[i - lookback:i])

            # Target: predict the target_col value at timestep i
            # Extract scaled close price at position i
            y.append(features_scaled[i, self.feature_columns.index(target_col)])

        X = np.array(X)
        y = np.array(y)

        print(f"Created {len(X)} sequences with shape {X.shape}")

        return X, y, df.index[lookback:]

    def inverse_transform_predictions(self, predictions: np.ndarray, feature_idx: int = 0) -> np.ndarray:
        """
        Convert scaled LSTM predictions back to original price scale.

        Since MinMaxScaler was fit on multi-feature data, we need to reconstruct
        a dummy array with the same shape to inverse transform correctly.

        Args:
            predictions: Scaled predictions from model, shape (n_samples,) or (n_samples, 1)
            feature_idx: Index of predicted feature in feature_columns list (0 for 'close')

        Returns:
            Unscaled predictions in original price units

        Example:
            >>> predictions_scaled = model.predict(X_test)  # Scaled [0,1]
            >>> predictions_real = preprocessor.inverse_transform_predictions(predictions_scaled)
            >>> print(predictions_real)  # Actual prices like [45000.5, 45100.2, ...]
        """
        # MinMaxScaler was fit on multi-feature array shape (n_samples, n_features)
        # To inverse transform single feature, reconstruct dummy array with same shape
        # Fill target feature column with predictions, rest with zeros
        n_features = len(self.feature_columns)
        dummy = np.zeros((len(predictions), n_features))
        dummy[:, feature_idx] = predictions.flatten()  # Place predictions in correct column

        # Debug: Verify feature order and scaling
        print(f"\nInverse transform debug:")
        print(f"  Feature columns: {self.feature_columns}")
        print(f"  Using feature_idx: {feature_idx} = '{self.feature_columns[feature_idx]}'")
        print(f"  Input (scaled) sample: {predictions[:3]}")

        # Inverse transform the dummy array
        # Only the target column will be correctly scaled; others are meaningless
        unscaled = self.scaler.inverse_transform(dummy)

        print(f"  Output (unscaled) sample: {unscaled[:3, feature_idx]}")

        return unscaled[:, feature_idx]

    def save_scaler(self, filepath: str = 'data/scaler.pkl') -> None:
        """Save the fitted scaler for later use."""
        Path(filepath).parent.mkdir(exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Scaler saved to {filepath}")

    def load_scaler(self, filepath: str = 'data/scaler.pkl') -> None:
        """Load a previously fitted scaler."""
        with open(filepath, 'rb') as f:
            self.scaler = pickle.load(f)
        # Restore feature columns from config
        self.feature_columns = self.config['model']['features']
        print(f"Scaler loaded from {filepath}")


def main() -> None:
    """
    Test preprocessing pipeline on most recent OHLCV data file.

    Loads latest CSV, adds indicators, creates sequences, saves scaler and processed data.
    """
    import sys
    from pathlib import Path

    # Load the most recent raw OHLCV data file
    data_dir = Path('data')
    csv_files = list(data_dir.glob('*.csv'))

    if not csv_files:
        print("No data files found. Run fetch_data.py first.")
        sys.exit(1)

    # Filter for raw OHLCV data files (exclude processed outputs)
    exclude_files = {'predictions.csv', 'processed_data.csv'}
    raw_data_files = []

    for csv_file in csv_files:
        if csv_file.name in exclude_files:
            continue
        
        # Quick check: raw OHLCV data should have these columns
        try:
            temp_df = pd.read_csv(csv_file, nrows=1)
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            if all(col in temp_df.columns for col in required_cols):
                raw_data_files.append(csv_file)
        except Exception:
            continue

    if not raw_data_files:
        print("No raw OHLCV data files found. Run fetch_data.py first.")
        print("Expected columns: open, high, low, close, volume, datetime")
        sys.exit(1)

    # Get the most recent raw data file
    latest_file = max(raw_data_files, key=lambda p: p.stat().st_mtime)
    print(f"Loading data from {latest_file}")

    df = pd.read_csv(latest_file)
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Initialize preprocessor
    preprocessor = DataPreprocessor()

    # Add technical indicators
    print("\nAdding technical indicators...")
    df_with_indicators = preprocessor.add_technical_indicators(df)

    print("\nFeatures added:")
    print(df_with_indicators.columns.tolist())

    # Create sequences
    print("\nCreating sequences for LSTM...")
    X, y, indices = preprocessor.create_sequences(df_with_indicators, lookback=60)

    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")

    # Save preprocessor
    preprocessor.save_scaler()

    # Save processed data
    output_file = data_dir / 'processed_data.csv'
    df_with_indicators.to_csv(output_file, index=False)
    print(f"\nProcessed data saved to {output_file}")


if __name__ == '__main__':
    main()
