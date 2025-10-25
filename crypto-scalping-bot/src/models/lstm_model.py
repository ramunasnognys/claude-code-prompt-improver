"""
LSTM model for crypto price prediction.
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
import yaml
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Optional, Tuple, Dict, Any


class LSTMPricePredictor:
    """
    LSTM neural network for predicting cryptocurrency prices.

    Implements a multi-layer LSTM architecture with dropout regularization,
    early stopping, learning rate reduction, and model checkpointing.

    Architecture:
        - Input: (timesteps, features) sequences
        - LSTM layers with configurable units (e.g., [64, 32])
        - Dropout layers for regularization
        - Dense output layer (single price prediction)
        - Optimizer: Adam with configurable learning rate
        - Loss: MSE (Mean Squared Error)

    Example:
        >>> model = LSTMPricePredictor('config/config.yaml')
        >>> history = model.train(X_train, y_train, X_val, y_val)
        >>> predictions = model.predict(X_test)
        >>> metrics = model.evaluate(X_test, y_test)
        >>> model.save_model('models/lstm_model.keras')
    """

    def __init__(self, config_path: str = 'config/config.yaml') -> None:
        """
        Initialize LSTM model with configuration.

        Args:
            config_path: Path to YAML config with model architecture and training params

        Attributes:
            config: Loaded configuration dictionary
            model: Keras Sequential model (None until build_model called)
            history: Training history (None until train called)
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.model = None
        self.history = None

    def build_model(self, input_shape: Tuple[int, int]) -> keras.Model:
        """
        Build and compile stacked LSTM model architecture.

        Creates sequential LSTM layers based on config, with dropout between layers.
        The return_sequences parameter is automatically set to maintain temporal
        dimension for all but the last LSTM layer.

        Args:
            input_shape: Tuple of (timesteps, features), e.g., (60, 6)

        Returns:
            Compiled Keras model ready for training

        Example:
            >>> model_obj = LSTMPricePredictor()
            >>> model = model_obj.build_model((60, 6))  # 60 timesteps, 6 features
            >>> model.summary()  # View architecture

        Note:
            Config parameters used:
                - lstm_units: List of units per layer, e.g., [64, 32]
                - dropout_rate: Dropout probability (0-1)
                - learning_rate: Adam optimizer learning rate
        """
        lstm_units = self.config['model']['lstm_units']
        dropout_rate = self.config['model']['dropout_rate']
        learning_rate = self.config['model']['learning_rate']

        model = keras.Sequential()

        # First LSTM layer
        # return_sequences=True preserves temporal dimension for next LSTM layer
        # Only set to False for the last LSTM layer before Dense output
        model.add(layers.LSTM(
            lstm_units[0],
            return_sequences=True if len(lstm_units) > 1 else False,  # True if more layers follow
            input_shape=input_shape
        ))
        model.add(layers.Dropout(dropout_rate))

        # Additional LSTM layers
        # Enumerate over remaining layers (skip first, already added)
        for i, units in enumerate(lstm_units[1:]):
            # return_seq: True for all but last LSTM layer
            # Example: [64, 32] -> i=0 is last, return_seq=False
            # Example: [64, 32, 16] -> i=0,1 have return_seq=True,False
            return_seq = i < len(lstm_units) - 2
            model.add(layers.LSTM(units, return_sequences=return_seq))
            model.add(layers.Dropout(dropout_rate))

        # Output layer
        model.add(layers.Dense(1))

        # Compile model
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        model.compile(
            optimizer=optimizer,
            loss='mse',
            metrics=['mae']
        )

        self.model = model

        print("\nModel Architecture:")
        model.summary()

        return model

    def train(self, X_train: np.ndarray, y_train: np.ndarray, X_val: Optional[np.ndarray] = None, y_val: Optional[np.ndarray] = None) -> callbacks.History:
        """
        Train the LSTM model with automatic callbacks for optimization and checkpointing.

        Implements:
            - EarlyStopping: Stops training if validation loss doesn't improve (patience=10)
            - ReduceLROnPlateau: Reduces learning rate by 0.5 if loss plateaus (patience=5)
            - ModelCheckpoint: Saves best model based on validation/training loss

        Args:
            X_train: Training sequences, shape (n_samples, timesteps, features)
            y_train: Training targets, shape (n_samples,)
            X_val: Validation sequences (optional). If None, monitors training loss
            y_val: Validation targets (optional)

        Returns:
            History object with training metrics (loss, MAE, val_loss, val_mae)

        Example:
            >>> history = model.train(X_train, y_train, X_val, y_val)
            >>> print(f"Final loss: {history.history['loss'][-1]}")
            >>> model.plot_training_history()

        Note:
            Best model weights are automatically restored after training.
            Checkpoints saved to models/checkpoints/best_model.keras
        """
        if self.model is None:
            input_shape = (X_train.shape[1], X_train.shape[2])
            self.build_model(input_shape)

        epochs = self.config['model']['epochs']
        batch_size = self.config['model']['batch_size']

        # Callbacks
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss' if X_val is not None else 'loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )

        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss' if X_val is not None else 'loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )

        checkpoint_dir = Path('models/checkpoints')
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

        model_checkpoint = callbacks.ModelCheckpoint(
            checkpoint_dir / 'best_model.keras',
            monitor='val_loss' if X_val is not None else 'loss',
            save_best_only=True,
            verbose=1
        )

        callback_list = [early_stopping, reduce_lr, model_checkpoint]

        # Train model
        validation_data = (X_val, y_val) if X_val is not None else None

        print(f"\nTraining model for up to {epochs} epochs...")
        self.history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=validation_data,
            callbacks=callback_list,
            verbose=1
        )

        return self.history

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions with the trained model.

        Args:
            X (np.array): Input sequences

        Returns:
            np.array: Predictions
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")

        return self.model.predict(X, verbose=0)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        Evaluate model performance with comprehensive metrics.

        Calculates regression metrics (MSE, MAE, RMSE) plus directional accuracy
        to measure how well the model predicts price movement direction.

        Args:
            X_test: Test sequences, shape (n_samples, timesteps, features)
            y_test: True target values, shape (n_samples,)

        Returns:
            Dictionary with metrics:
                - mse: Mean Squared Error
                - mae: Mean Absolute Error
                - rmse: Root Mean Squared Error
                - direction_accuracy: % of correct up/down predictions (0-1)

        Example:
            >>> metrics = model.evaluate(X_test, y_test)
            >>> print(f"RMSE: {metrics['rmse']:.4f}")
            >>> print(f"Direction accuracy: {metrics['direction_accuracy']*100:.2f}%")

        Note:
            Direction accuracy measures if predicted price changes match actual
            changes (ignoring magnitude). Critical for trading strategies.
        """
        predictions = self.predict(X_test)

        mse = np.mean((predictions.flatten() - y_test) ** 2)
        mae = np.mean(np.abs(predictions.flatten() - y_test))
        rmse = np.sqrt(mse)

        # Direction accuracy: did we predict up/down movement correctly?
        # np.diff() calculates consecutive differences: [a,b,c] -> [b-a, c-b]
        # np.sign() converts to direction: positive->1, negative->-1, zero->0
        # Compare predicted direction vs actual direction for each timestep
        actual_direction = np.sign(np.diff(y_test))  # True price movement direction
        pred_direction = np.sign(np.diff(predictions.flatten()))  # Predicted direction
        direction_accuracy = np.mean(actual_direction == pred_direction)  # % correct

        metrics = {
            'mse': mse,
            'mae': mae,
            'rmse': rmse,
            'direction_accuracy': direction_accuracy
        }

        print("\nEvaluation Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value:.6f}")

        return metrics

    def plot_training_history(self, save_path: str = 'models/training_history.png') -> None:
        """Plot training and validation loss."""
        if self.history is None:
            print("No training history available.")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

        # Loss plot
        ax1.plot(self.history.history['loss'], label='Training Loss')
        if 'val_loss' in self.history.history:
            ax1.plot(self.history.history['val_loss'], label='Validation Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss (MSE)')
        ax1.set_title('Model Loss')
        ax1.legend()
        ax1.grid(True)

        # MAE plot
        ax2.plot(self.history.history['mae'], label='Training MAE')
        if 'val_mae' in self.history.history:
            ax2.plot(self.history.history['val_mae'], label='Validation MAE')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('MAE')
        ax2.set_title('Mean Absolute Error')
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Training history plot saved to {save_path}")
        plt.close()

    def save_model(self, filepath: str = 'models/lstm_model.keras') -> None:
        """Save the trained model."""
        Path(filepath).parent.mkdir(exist_ok=True)
        self.model.save(filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath: str = 'models/lstm_model.keras') -> None:
        """Load a trained model."""
        self.model = keras.models.load_model(filepath)
        print(f"Model loaded from {filepath}")


def main() -> None:
    """
    Complete LSTM training pipeline: load data, preprocess, train, evaluate, save.

    Performs 70/15/15 train/val/test split, trains model, evaluates performance,
    plots training history, and saves model + predictions.
    """
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))

    from data.preprocess import DataPreprocessor

    print("Loading and preprocessing data...")

    # Load processed data
    data_dir = Path('data')
    csv_files = list(data_dir.glob('*.csv'))

    if not csv_files:
        print("No data files found. Run fetch_data.py first.")
        sys.exit(1)

    latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)
    df = pd.read_csv(latest_file)
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Preprocess data
    preprocessor = DataPreprocessor()
    df_processed = preprocessor.add_technical_indicators(df)
    X, y, indices = preprocessor.create_sequences(df_processed, lookback=60)
    preprocessor.save_scaler()

    # DATE-BASED SPLIT TO PREVENT DATA LEAKAGE (Phase 1.1)
    # Train: Jan 1 - Feb 28, 2024
    # Validation: Mar 1 - Mar 15, 2024
    # Test: Mar 16 - Mar 31, 2024 (will be used for backtesting)
    
    train_end = pd.Timestamp('2024-02-28 23:59:59')
    val_end = pd.Timestamp('2024-03-15 23:59:59')
    
    # Get datetime array for indices
    datetime_array = df_processed['datetime'].iloc[indices].values
    datetime_array = pd.to_datetime(datetime_array)
    
    # Create masks for each split
    train_mask = datetime_array <= train_end
    val_mask = (datetime_array > train_end) & (datetime_array <= val_end)
    test_mask = datetime_array > val_end
    
    # Split data based on dates
    X_train = X[train_mask]
    y_train = y[train_mask]
    
    X_val = X[val_mask]
    y_val = y[val_mask]
    
    X_test = X[test_mask]
    y_test = y[test_mask]
    
    # Print split information with dates
    print(f"\n{'='*70}")
    print("DATA SPLIT (Date-Based - No Data Leakage)")
    print(f"{'='*70}")
    print(f"Training:   {len(X_train):6d} samples | {datetime_array[train_mask].min()} to {datetime_array[train_mask].max()}")
    print(f"Validation: {len(X_val):6d} samples | {datetime_array[val_mask].min()} to {datetime_array[val_mask].max()}")
    print(f"Test:       {len(X_test):6d} samples | {datetime_array[test_mask].min()} to {datetime_array[test_mask].max()}")
    print(f"{'='*70}")
    print("⚠️  IMPORTANT: Test set is completely unseen and will be used for backtesting")
    print(f"{'='*70}\n")

    # Train model
    model = LSTMPricePredictor()
    model.train(X_train, y_train, X_val, y_val)

    # Evaluate on test set
    print("\n=== Test Set Performance ===")
    metrics = model.evaluate(X_test, y_test)

    # Plot training history
    model.plot_training_history()

    # Save model
    model.save_model()

    # Save predictions for analysis (only test set for backtesting)
    test_predictions = model.predict(X_test)
    test_datetimes = datetime_array[test_mask]
    
    results_df = pd.DataFrame({
        'actual': y_test,
        'predicted': test_predictions.flatten(),
        'datetime': test_datetimes
    })

    results_path = data_dir / 'predictions.csv'
    results_df.to_csv(results_path, index=False)
    print(f"\nPredictions saved to {results_path}")
    print(f"⚠️  Predictions are for TEST SET ONLY (Mar 16-31, 2024)")
    print(f"   These will be used for out-of-sample backtesting.")

    print("\n=== Training Complete ===")
    print("Next step: Run backtesting with the trained model")


if __name__ == '__main__':
    main()
