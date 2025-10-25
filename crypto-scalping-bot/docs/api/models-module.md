# Models Module API Reference

The models module implements the LSTM neural network for cryptocurrency price prediction.

**Module Path**: `src/models/`

**Files**:
- `lstm_model.py` - LSTM price predictor class and training pipeline
- `train_lstm.py` - Training script (imports from lstm_model.py)

---

## Table of Contents

1. [LSTMPricePredictor](#lstmpri cepredictor)
2. [Usage Examples](#usage-examples)
3. [Training Pipeline](#training-pipeline)

---

## LSTMPricePredictor

**Class**: `LSTMPricePredictor`
**File**: `src/models/lstm_model.py`
**Purpose**: LSTM neural network for predicting next-period cryptocurrency prices

### Architecture

**Model Type**: Sequential stacked LSTM with dropout regularization

**Default Configuration** (from `config/config.yaml`):
- Layers: 2 LSTM layers with [64, 32] units
- Dropout: 0.2 (20%) after each LSTM layer
- Output: Dense layer with 1 unit (price prediction)
- Optimizer: Adam with learning rate 0.001
- Loss: Mean Squared Error (MSE)
- Metrics: Mean Absolute Error (MAE)

**Input**: `(timesteps, features)` sequences (default: 60 timesteps, 6 features)
**Output**: Single predicted price (normalized [0,1])

---

### Constructor

```python
LSTMPricePredictor(config_path: str = 'config/config.yaml') -> None
```

**Parameters**:
- `config_path` (str): Path to YAML configuration file containing model architecture and training parameters

**Attributes**:
- `config` (dict): Loaded configuration dictionary
- `model` (keras.Model): Keras Sequential model (None until `build_model()` called)
- `history` (keras.callbacks.History): Training history (None until `train()` called)

**Example**:
```python
from src.models.lstm_model import LSTMPricePredictor

model = LSTMPricePredictor('config/config.yaml')
print(model.config['model']['lstm_units'])  # [64, 32]
```

---

### Methods

#### build_model

```python
build_model(input_shape: Tuple[int, int]) -> keras.Model
```

Build and compile stacked LSTM model architecture.

**Parameters**:
- `input_shape` (Tuple[int, int]): Shape of input sequences as `(timesteps, features)`. Example: `(60, 6)` for 60 timesteps and 6 features

**Returns**:
- `keras.Model`: Compiled Keras Sequential model ready for training

**Side Effects**:
- Sets `self.model` to compiled model
- Prints model summary to console

**Architecture Details**:
- First LSTM layer: `return_sequences=True` if multiple layers, else `False`
- Subsequent LSTM layers: `return_sequences=True` for all except last
- Dropout after each LSTM layer
- Final Dense(1) layer for single price output

**Configuration Used** (from `config.yaml`):
- `model.lstm_units`: List of units per layer (e.g., `[64, 32]`)
- `model.dropout_rate`: Dropout probability (e.g., `0.2`)
- `model.learning_rate`: Adam optimizer LR (e.g., `0.001`)

**Example**:
```python
model_obj = LSTMPricePredictor()
model = model_obj.build_model(input_shape=(60, 6))
model.summary()

# Output:
# Model: "sequential"
# _________________________________________________________________
#  Layer (type)                Output Shape              Param #
# =================================================================
#  lstm (LSTM)                 (None, 60, 64)            18176
#  dropout (Dropout)           (None, 60, 64)            0
#  lstm_1 (LSTM)               (None, 32)                12416
#  dropout_1 (Dropout)         (None, 32)                0
#  dense (Dense)               (None, 1)                 33
# =================================================================
# Total params: 30,625
```

---

#### train

```python
train(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None
) -> callbacks.History
```

Train the LSTM model with automatic callbacks for optimization.

**Parameters**:
- `X_train` (np.ndarray): Training sequences, shape `(n_samples, timesteps, features)`
- `y_train` (np.ndarray): Training targets, shape `(n_samples,)`
- `X_val` (np.ndarray, optional): Validation sequences. If None, monitors training loss only
- `y_val` (np.ndarray, optional): Validation targets

**Returns**:
- `keras.callbacks.History`: Training history with loss and metrics per epoch

**Side Effects**:
- Calls `build_model()` if `self.model` is None (auto-builds from X_train shape)
- Creates `models/checkpoints/` directory
- Saves best model to `models/checkpoints/best_model.keras`
- Sets `self.history` to training history
- Restores best weights after training (via EarlyStopping)

**Callbacks Applied**:
1. **EarlyStopping**:
   - Monitors: `val_loss` (or `loss` if no validation)
   - Patience: 10 epochs
   - Restores best weights automatically

2. **ReduceLROnPlateau**:
   - Monitors: `val_loss` (or `loss`)
   - Factor: 0.5 (halves learning rate)
   - Patience: 5 epochs
   - Min LR: 1e-7

3. **ModelCheckpoint**:
   - Saves: `models/checkpoints/best_model.keras`
   - Saves best model only (based on monitored metric)

**Configuration Used**:
- `model.epochs`: Maximum training epochs (e.g., `50`)
- `model.batch_size`: Samples per gradient update (e.g., `32`)

**Example**:
```python
from src.data.preprocess import DataPreprocessor
import numpy as np

# Prepare data
preprocessor = DataPreprocessor()
X, y, indices = preprocessor.create_sequences(df, lookback=60)

# Split
train_size = int(len(X) * 0.7)
val_size = int(len(X) * 0.15)

X_train = X[:train_size]
y_train = y[:train_size]
X_val = X[train_size:train_size + val_size]
y_val = y[train_size:train_size + val_size]

# Train
model = LSTMPricePredictor()
history = model.train(X_train, y_train, X_val, y_val)

print(f"Final training loss: {history.history['loss'][-1]:.6f}")
print(f"Final validation loss: {history.history['val_loss'][-1]:.6f}")
```

**Training Output Example**:
```
Training model for up to 50 epochs...
Epoch 1/50
1234/1234 [==============================] - 25s 20ms/step - loss: 0.0234 - mae: 0.0987 - val_loss: 0.0198 - val_mae: 0.0856
Epoch 2/50
1234/1234 [==============================] - 23s 19ms/step - loss: 0.0187 - mae: 0.0823 - val_loss: 0.0165 - val_mae: 0.0745
...
Epoch 00015: early stopping
Restoring model weights from the end of the best epoch: 5.
```

---

#### predict

```python
predict(X: np.ndarray) -> np.ndarray
```

Make predictions with the trained model.

**Parameters**:
- `X` (np.ndarray): Input sequences, shape `(n_samples, timesteps, features)`

**Returns**:
- `np.ndarray`: Predictions, shape `(n_samples, 1)`. Values in [0,1] (normalized)

**Raises**:
- `ValueError`: If model not trained (call `train()` or `load_model()` first)

**Example**:
```python
# Predict on test set
X_test = X[train_size + val_size:]
predictions = model.predict(X_test)

print(predictions.shape)  # (n_test_samples, 1)
print(predictions[:5])    # First 5 predictions
# [[0.6234],
#  [0.6198],
#  [0.6245],
#  [0.6289],
#  [0.6301]]
```

---

#### evaluate

```python
evaluate(X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]
```

Evaluate model performance with comprehensive metrics.

**Parameters**:
- `X_test` (np.ndarray): Test sequences, shape `(n_samples, timesteps, features)`
- `y_test` (np.ndarray): True target values, shape `(n_samples,)`

**Returns**:
- `Dict[str, float]`: Metrics dictionary with keys:
  - `'mse'`: Mean Squared Error
  - `'mae'`: Mean Absolute Error
  - `'rmse'`: Root Mean Squared Error
  - `'direction_accuracy'`: Percentage of correct up/down predictions (0-1)

**Side Effects**:
- Prints metrics to console

**Direction Accuracy Calculation**:
```python
# Measures if model predicts direction correctly (up vs down)
# Critical for trading: predicting magnitude less important than direction
actual_direction = np.sign(np.diff(y_test))      # +1 for up, -1 for down
pred_direction = np.sign(np.diff(predictions))
direction_accuracy = np.mean(actual_direction == pred_direction)
```

**Example**:
```python
metrics = model.evaluate(X_test, y_test)

# Output:
# Evaluation Metrics:
# mse: 0.000234
# mae: 0.012456
# rmse: 0.015297
# direction_accuracy: 0.567890

# Access specific metrics
print(f"Direction accuracy: {metrics['direction_accuracy'] * 100:.2f}%")
# Direction accuracy: 56.79%
```

**Interpreting Direction Accuracy**:
- `50%`: No better than random (coin flip)
- `55-60%`: Good for 1-minute scalping
- `60-65%`: Excellent
- `>65%`: Likely overfitting, test on out-of-sample data

---

#### plot_training_history

```python
plot_training_history(save_path: str = 'models/training_history.png') -> None
```

Generate and save training history plots.

**Parameters**:
- `save_path` (str): Output path for plot image. Default: `'models/training_history.png'`

**Generates**:
- 2-panel figure:
  - Left: Loss (MSE) over epochs (train and validation)
  - Right: MAE over epochs (train and validation)

**Side Effects**:
- Saves plot to `save_path`
- Closes figure after saving (doesn't display)

**Raises**:
- Early return if `self.history` is None (no training performed)

**Example**:
```python
model.train(X_train, y_train, X_val, y_val)
model.plot_training_history('results/training_history.png')

# Open in browser or image viewer
# !open results/training_history.png
```

**What to Look For**:
- Train and val losses should decrease together (good generalization)
- Large gap between train and val = overfitting
- Flat lines = model not learning (increase LR or reduce dropout)
- Val loss decreasing then increasing = early stopping working correctly

---

#### save_model

```python
save_model(filepath: str = 'models/lstm_model.keras') -> None
```

Save the trained model to disk.

**Parameters**:
- `filepath` (str): Output path for model file. Default: `'models/lstm_model.keras'`

**Side Effects**:
- Creates parent directory if it doesn't exist
- Saves entire model (architecture + weights + optimizer state)

**Format**: Keras 3.0 format (`.keras` extension recommended over legacy `.h5`)

**Example**:
```python
model.train(X_train, y_train, X_val, y_val)
model.save_model('models/lstm_model_20240125.keras')
print("Model saved successfully")
```

---

#### load_model

```python
load_model(filepath: str = 'models/lstm_model.keras') -> None
```

Load a previously trained model from disk.

**Parameters**:
- `filepath` (str): Path to saved model file. Default: `'models/lstm_model.keras'`

**Side Effects**:
- Sets `self.model` to loaded model
- Can immediately call `predict()` or `evaluate()` after loading

**Raises**:
- `OSError`: If file doesn't exist
- `ValueError`: If file corrupted or incompatible Keras version

**Example**:
```python
# Load and use pre-trained model
model = LSTMPricePredictor()
model.load_model('models/lstm_model.keras')

# Make predictions
predictions = model.predict(X_test)
```

---

## Usage Examples

### Complete Training Pipeline

```python
from src.models.lstm_model import LSTMPricePredictor
from src.data.preprocess import DataPreprocessor
import pandas as pd

# Load processed data
df = pd.read_csv('data/processed_data.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

# Create sequences
preprocessor = DataPreprocessor()
X, y, indices = preprocessor.create_sequences(df, lookback=60)

# Split: 70% train, 15% val, 15% test
train_size = int(len(X) * 0.7)
val_size = int(len(X) * 0.15)

X_train, y_train = X[:train_size], y[:train_size]
X_val, y_val = X[train_size:train_size + val_size], y[train_size:train_size + val_size]
X_test, y_test = X[train_size + val_size:], y[train_size + val_size:]

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

# Build and train model
model = LSTMPricePredictor()
history = model.train(X_train, y_train, X_val, y_val)

# Evaluate
metrics = model.evaluate(X_test, y_test)
print(f"Test RMSE: {metrics['rmse']:.6f}")
print(f"Test Direction Accuracy: {metrics['direction_accuracy']*100:.2f}%")

# Save
model.save_model()
model.plot_training_history()

# Save predictions for backtesting
test_predictions = model.predict(X_test)
results_df = pd.DataFrame({
    'actual': y_test,
    'predicted': test_predictions.flatten(),
    'datetime': df['datetime'].iloc[indices[train_size + val_size:]]
})
results_df.to_csv('data/predictions.csv', index=False)
print("Predictions saved to data/predictions.csv")
```

### Loading and Using Pre-Trained Model

```python
# Load existing model
model = LSTMPricePredictor()
model.load_model('models/lstm_model.keras')

# Load new data
new_df = pd.read_csv('data/new_data.csv')
preprocessor = DataPreprocessor()
preprocessor.load_scaler('models/scaler.pkl')  # Must use same scaler!

X_new, y_new, indices = preprocessor.create_sequences(new_df, lookback=60)

# Predict
predictions = model.predict(X_new)
print(predictions[:10])
```

### Custom Model Architecture

```python
# Modify config programmatically
model = LSTMPricePredictor()
model.config['model']['lstm_units'] = [128, 64, 32]  # 3 layers
model.config['model']['dropout_rate'] = 0.3          # More dropout
model.config['model']['learning_rate'] = 0.0005      # Lower LR

# Build with custom config
model.build_model(input_shape=(60, 6))
history = model.train(X_train, y_train, X_val, y_val)
```

---

## Training Pipeline

The module includes a `main()` function implementing the complete training pipeline:

**File**: `src/models/lstm_model.py` (lines 318-397)

**Steps**:
1. Load latest CSV from `data/` directory
2. Add technical indicators via DataPreprocessor
3. Create sequences with 60-period lookback
4. Split 70/15/15 (train/val/test)
5. Train model with callbacks
6. Evaluate on test set
7. Plot training history
8. Save model and predictions

**Run as script**:
```bash
cd crypto-scalping-bot
python src/models/train_lstm.py

# Or directly:
python -m src.models.lstm_model
```

**Expected Output**:
```
Loading and preprocessing data...
Data split:
Training: 45000 samples
Validation: 9643 samples
Test: 9643 samples

Model Architecture:
... [model summary] ...

Training model for up to 50 epochs...
Epoch 1/50 ... loss: 0.0234 - val_loss: 0.0198
...
Epoch 00015: early stopping

=== Test Set Performance ===
Evaluation Metrics:
mse: 0.000234
mae: 0.012456
rmse: 0.015297
direction_accuracy: 0.567890

Training history plot saved to models/training_history.png
Model saved to models/lstm_model.keras
Predictions saved to data/predictions.csv

=== Training Complete ===
```

---

## Design Notes

### Why LSTM?

See [ADR-0001](../adr/0001-lstm-model-choice.md) for full rationale:
- Natural fit for sequential time-series data
- Captures temporal dependencies automatically
- Proven track record in financial prediction
- Fast inference (<50ms per prediction)

### Normalization Requirement

**Critical**: Model expects normalized inputs [0,1]
- Features scaled by MinMaxScaler during preprocessing
- Predictions output in normalized space
- Strategy uses normalized predictions directly (see [ADR-0005](../adr/0005-normalized-predictions.md))

### Callbacks and Early Stopping

**EarlyStopping with patience=10**:
- Prevents overtraining beyond optimal point
- Automatically restores best weights
- Validation loss is ground truth for generalization

**ReduceLROnPlateau**:
- Dynamically lowers learning rate when stuck
- Helps escape local minima
- Final LR often 10-100x lower than initial

### Overfitting Prevention

**Built-in mechanisms**:
1. Dropout (0.2) after each LSTM layer
2. EarlyStopping monitors validation loss
3. Train/val split ensures out-of-sample evaluation

**Additional recommendations**:
- Use minimum 3 months of data
- Don't tune hyperparameters on test set
- Validate on different time period (walk-forward)

### Performance Expectations

**Realistic metrics for 1m crypto scalping**:
- RMSE: 0.01-0.02 (normalized space)
- Direction accuracy: 55-60%
- Training time: 5-15 minutes (GPU), 30-60 min (CPU)

**Warning signs**:
- Direction accuracy <52%: Model not learning
- Direction accuracy >65%: Likely overfitting
- Val loss > 2x train loss: Severe overfitting

---

## Related Documentation

- Data preparation: [data-module.md](data-module.md)
- Strategy implementation: [strategies-module.md](strategies-module.md)
- Architecture decision: [ADR-0001](../adr/0001-lstm-model-choice.md)
- Troubleshooting: [TROUBLESHOOTING.md](../TROUBLESHOOTING.md#model-training-issues)

---

**Source Code**: `src/models/lstm_model.py`
**Dependencies**: tensorflow, keras, numpy, pandas, matplotlib, pyyaml
**Last Updated**: 2025-01-25
