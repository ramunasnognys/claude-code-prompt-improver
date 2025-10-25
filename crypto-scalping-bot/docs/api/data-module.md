# Data Module API Reference

The data module handles fetching historical OHLCV data from exchanges and preprocessing it with technical indicators for model training.

**Module Path**: `src/data/`

**Files**:
- `fetch_data.py` - Exchange data retrieval via CCXT
- `preprocess.py` - Technical indicators and sequence creation

---

## Table of Contents

1. [OKXDataFetcher](#okxdatafetcher)
2. [DataPreprocessor](#datapreprocessor)
3. [Usage Examples](#usage-examples)

---

## OKXDataFetcher

**Class**: `OKXDataFetcher`
**File**: `src/data/fetch_data.py`
**Purpose**: Fetch historical OHLCV data from OKX perpetual futures exchange

### Constructor

```python
OKXDataFetcher(config_path: str = 'config/config.yaml') -> None
```

**Parameters**:
- `config_path` (str): Path to YAML configuration file. Default: `'config/config.yaml'`

**Raises**:
- `FileNotFoundError`: If config file doesn't exist
- `KeyError`: If required config keys (`trading.symbol`, `trading.timeframe`) missing

**Attributes**:
- `config` (dict): Loaded configuration dictionary
- `exchange` (ccxt.okx): CCXT OKX exchange instance
- `symbol` (str): Trading pair in CCXT format (e.g., `'BTC/USDT:USDT'`)
- `timeframe` (str): Candlestick timeframe (e.g., `'1m'`, `'5m'`, `'1h'`)

**Example**:
```python
from src.data.fetch_data import OKXDataFetcher

fetcher = OKXDataFetcher('config/config.yaml')
print(f"Fetching {fetcher.symbol} on {fetcher.timeframe}")
```

---

### Methods

#### fetch_ohlcv

```python
fetch_ohlcv(
    start_date: str,
    end_date: Optional[str] = None,
    limit: int = 1000
) -> pd.DataFrame
```

Fetch OHLCV data for specified date range with automatic pagination.

**Parameters**:
- `start_date` (str): Start date in 'YYYY-MM-DD' format (e.g., `'2024-01-01'`)
- `end_date` (str, optional): End date in 'YYYY-MM-DD' format. Defaults to today
- `limit` (int): Candles per API request. Max 1000 for OKX. Default: 1000

**Returns**:
- `pd.DataFrame`: OHLCV data with columns:
  - `timestamp` (int): Unix timestamp in milliseconds
  - `open` (float): Opening price
  - `high` (float): Highest price in period
  - `low` (float): Lowest price in period
  - `close` (float): Closing price
  - `volume` (float): Trading volume
  - `datetime` (datetime): Human-readable timestamp

**Raises**:
- `ValueError`: If date format invalid
- `ccxt.RateLimitExceeded`: If API rate limit hit (20 req/s for OKX)
- `ccxt.NetworkError`: If network/connection issues

**Implementation Notes**:
- Automatically handles pagination for large date ranges
- Removes duplicate timestamps
- Includes 100ms delay between requests to respect rate limits
- Filters to exact date boundaries after fetching

**Example**:
```python
fetcher = OKXDataFetcher()

# Fetch 3 months of 1-minute data
df = fetcher.fetch_ohlcv('2024-01-01', '2024-03-31')
print(f"Fetched {len(df)} candles")
print(df.head())

# Output:
#    timestamp      open      high       low     close     volume              datetime
# 0  1704067200000  42150.5  42175.0  42140.2  42160.8  1234.56  2024-01-01 00:00:00
```

---

#### save_data

```python
save_data(df: pd.DataFrame, filename: Optional[str] = None) -> Path
```

Save OHLCV data to CSV in the `data/` directory.

**Parameters**:
- `df` (pd.DataFrame): DataFrame containing OHLCV data with `'datetime'` column
- `filename` (str, optional): Custom output filename. Auto-generated if None
  Format: `{SYMBOL}_{TIMEFRAME}_{START}_to_{END}.csv`

**Returns**:
- `pathlib.Path`: Path object pointing to saved CSV file

**Side Effects**:
- Creates `data/` directory if it doesn't exist
- Overwrites file if it already exists

**Example**:
```python
df = fetcher.fetch_ohlcv('2024-01-01', '2024-01-31')
filepath = fetcher.save_data(df)
print(f"Saved to: {filepath}")

# Output:
# Saved to: data/BTC_USDT_USDT_1m_20240101_to_20240131.csv

# Custom filename
filepath = fetcher.save_data(df, filename='my_custom_data.csv')
```

---

## DataPreprocessor

**Class**: `DataPreprocessor`
**File**: `src/data/preprocess.py`
**Purpose**: Add technical indicators and create sequences for LSTM training

### Constructor

```python
DataPreprocessor(config_path: str = 'config/config.yaml') -> None
```

**Parameters**:
- `config_path` (str): Path to YAML configuration file

**Attributes**:
- `config` (dict): Loaded configuration
- `scaler` (MinMaxScaler): Scikit-learn scaler for normalization (None until fit)

---

### Methods

#### add_technical_indicators

```python
add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame
```

Calculate and append technical indicators to OHLCV DataFrame.

**Parameters**:
- `df` (pd.DataFrame): Input DataFrame with columns: `datetime`, `open`, `high`, `low`, `close`, `volume`

**Returns**:
- `pd.DataFrame`: Original data plus indicator columns:
  - `rsi_14` (float): 14-period RSI [0-100]
  - `macd` (float): MACD line
  - `macd_signal` (float): MACD signal line
  - `macd_diff` (float): MACD histogram (macd - signal)
  - `bb_upper` (float): Upper Bollinger Band
  - `bb_middle` (float): Middle Bollinger Band (20-period SMA)
  - `bb_lower` (float): Lower Bollinger Band
  - `bb_width` (float): Band width (upper - lower)
  - Additional features: `price_change`, `volume_change`, `hl_range`, `sma_10`, `sma_30`, `ema_10`, `volume_sma_20`, `volume_ratio`

**Side Effects**:
- Adds ~20 new columns to DataFrame
- First ~60 rows will have NaN values (indicator warmup period)

**Dependencies**:
- Requires `pandas_ta` library
- Indicator parameters from `config.yaml` (`indicators` section)

**Example**:
```python
from src.data.preprocess import DataPreprocessor
import pandas as pd

df = pd.read_csv('data/BTC_USDT_USDT_1m_20240101_to_20240131.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

preprocessor = DataPreprocessor()
df_with_indicators = preprocessor.add_technical_indicators(df)

print(df_with_indicators.columns)
# ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'datetime',
#  'rsi_14', 'macd', 'macd_signal', 'bb_upper', 'bb_lower', ...]

print(df_with_indicators[['close', 'rsi_14', 'macd']].head(20))
```

---

#### create_sequences

```python
create_sequences(
    df: pd.DataFrame,
    lookback: int = 60
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]
```

Create LSTM input sequences from time-series data with normalization.

**Parameters**:
- `df` (pd.DataFrame): Preprocessed data with technical indicators
- `lookback` (int): Number of historical periods per sequence. Default: 60

**Returns**:
- Tuple of:
  - `X` (np.ndarray): Input sequences, shape `(n_samples, lookback, n_features)`
  - `y` (np.ndarray): Target values (next-period close), shape `(n_samples,)`
  - `indices` (np.ndarray): Original DataFrame indices for each sample

**Process**:
1. Select features from `config['model']['features']` (default: close, volume, rsi_14, macd, bb_upper, bb_lower)
2. Normalize features to [0,1] using MinMaxScaler
3. Create sliding window sequences of length `lookback`
4. Target is next-period normalized close price

**Side Effects**:
- Fits `self.scaler` on the feature data (call `save_scaler()` to persist)

**Implementation Notes**:
- First `lookback` samples are lost (need history to create sequences)
- All features normalized to [0,1] range (required for LSTM)
- Scaler must be saved for inverse transform during inference

**Example**:
```python
preprocessor = DataPreprocessor()
df = preprocessor.add_technical_indicators(raw_df)

X, y, indices = preprocessor.create_sequences(df, lookback=60)

print(f"X shape: {X.shape}")  # (n_samples, 60, 6)
print(f"y shape: {y.shape}")  # (n_samples,)
print(f"Number of features: {X.shape[2]}")  # 6

# Split for training
train_size = int(len(X) * 0.7)
X_train, y_train = X[:train_size], y[:train_size]
X_test, y_test = X[train_size:], y[train_size:]
```

---

#### save_scaler

```python
save_scaler(filepath: str = 'models/scaler.pkl') -> None
```

Save fitted MinMaxScaler to pickle file for later use.

**Parameters**:
- `filepath` (str): Output path for scaler. Default: `'models/scaler.pkl'`

**Raises**:
- `ValueError`: If scaler not fitted (call `create_sequences()` first)

**Side Effects**:
- Creates `models/` directory if it doesn't exist
- Overwrites existing scaler file

**Example**:
```python
preprocessor = DataPreprocessor()
X, y, indices = preprocessor.create_sequences(df)

# Save scaler for later inverse transform
preprocessor.save_scaler('models/scaler.pkl')
```

---

#### load_scaler

```python
load_scaler(filepath: str = 'models/scaler.pkl') -> None
```

Load previously saved scaler from pickle file.

**Parameters**:
- `filepath` (str): Path to saved scaler. Default: `'models/scaler.pkl'`

**Raises**:
- `FileNotFoundError`: If scaler file doesn't exist

**Side Effects**:
- Sets `self.scaler` to loaded scaler instance

**Example**:
```python
preprocessor = DataPreprocessor()
preprocessor.load_scaler('models/scaler.pkl')

# Now can use scaler for inverse transform
predictions_normalized = model.predict(X_test)
predictions_real = preprocessor.scaler.inverse_transform(predictions_normalized)
```

---

## Usage Examples

### Complete Data Fetching and Preprocessing Pipeline

```python
from src.data.fetch_data import OKXDataFetcher
from src.data.preprocess import DataPreprocessor
import pandas as pd

# Step 1: Fetch data
print("Fetching data from OKX...")
fetcher = OKXDataFetcher('config/config.yaml')
df = fetcher.fetch_ohlcv('2024-01-01', '2024-03-31')
filepath = fetcher.save_data(df)
print(f"Fetched {len(df)} candles, saved to {filepath}")

# Step 2: Add technical indicators
print("Adding technical indicators...")
preprocessor = DataPreprocessor('config/config.yaml')
df_processed = preprocessor.add_technical_indicators(df)

# Save processed data
df_processed.to_csv('data/processed_data.csv', index=False)
print(f"Processed data with {len(df_processed.columns)} columns")

# Step 3: Create sequences for LSTM
print("Creating sequences...")
X, y, indices = preprocessor.create_sequences(df_processed, lookback=60)
preprocessor.save_scaler()

print(f"Created {len(X)} sequences")
print(f"Input shape: {X.shape}")  # (n_samples, 60, 6)
print(f"Target shape: {y.shape}")  # (n_samples,)

# Step 4: Split data
train_size = int(len(X) * 0.7)
val_size = int(len(X) * 0.15)

X_train = X[:train_size]
y_train = y[:train_size]

X_val = X[train_size:train_size + val_size]
y_val = y[train_size:train_size + val_size]

X_test = X[train_size + val_size:]
y_test = y[train_size + val_size:]

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
```

### Running as Scripts

Both modules have `main()` functions for standalone execution:

```bash
# Fetch data based on config.yaml dates
cd crypto-scalping-bot
python src/data/fetch_data.py

# Preprocess latest data file
python src/data/preprocess.py
```

### Custom Configuration

```python
# Use custom config file
fetcher = OKXDataFetcher('config/custom_config.yaml')

# Override config values programmatically
preprocessor = DataPreprocessor('config/config.yaml')
preprocessor.config['indicators']['rsi_period'] = 21  # Override RSI period
df = preprocessor.add_technical_indicators(raw_df)
```

---

## Design Notes

### Rate Limiting

`OKXDataFetcher` implements automatic rate limiting:
- 100ms sleep between requests (10 req/s, well under OKX limit of 20 req/s)
- CCXT's `enableRateLimit` option provides additional protection
- For large date ranges (>6 months), consider increasing sleep to 150-200ms

### Data Quality

No automatic data cleaning is performed. Users should:
- Check for missing candles: `df['datetime'].diff().value_counts()`
- Verify no gaps: `len(df)` should match expected count
- Inspect for outliers: `df.describe()`, plot price action

### Normalization Strategy

MinMaxScaler chosen over StandardScaler:
- LSTM works better with [0,1] bounded inputs
- Preserves relative relationships between features
- Makes threshold tuning more intuitive

**Caveat**: Sensitive to outliers (extreme prices). Consider robust scaling for volatile assets.

### Memory Considerations

For large datasets:
- 1 year of 1m data ≈ 525,600 candles ≈ 50MB RAM (raw)
- With indicators: ~200MB RAM
- Sequences: ~500MB RAM (60 lookback, 6 features)

**Recommendation**: Process in chunks for multi-year datasets.

---

## Related Documentation

- Configuration: `config/config.yaml` (exchange, trading, indicators sections)
- Architecture Decision: [ADR-0004](../adr/0004-okx-exchange.md) on OKX selection
- Troubleshooting: [TROUBLESHOOTING.md](../TROUBLESHOOTING.md#data-fetching-issues)
- Next Step: [models-module.md](models-module.md) for LSTM training

---

**Source Code**: `src/data/fetch_data.py`, `src/data/preprocess.py`
**Dependencies**: ccxt, pandas, pandas_ta, scikit-learn, numpy
**Last Updated**: 2025-01-25
