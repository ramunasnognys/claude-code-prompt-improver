"""
Fetch historical OHLCV data from OKX perpetual futures.
"""

import ccxt
import pandas as pd
import yaml
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class OKXDataFetcher:
    """
    Fetch and save historical OHLCV data from OKX perpetual futures exchange.

    This class handles data retrieval via the CCXT library, managing pagination,
    rate limiting, and data cleaning for backtesting purposes.

    Example:
        >>> fetcher = OKXDataFetcher('config/config.yaml')
        >>> df = fetcher.fetch_ohlcv('2024-01-01', '2024-03-31')
        >>> filepath = fetcher.save_data(df)
    """

    def __init__(self, config_path: str = 'config/config.yaml') -> None:
        """
        Initialize the data fetcher with configuration.

        Args:
            config_path: Path to YAML configuration file containing trading symbol and timeframe

        Raises:
            FileNotFoundError: If config file doesn't exist
            KeyError: If required config keys are missing
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Initialize OKX exchange (public API, no auth needed for historical data)
        self.exchange = ccxt.okx({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',  # Perpetual futures
            }
        })

        self.symbol = self.config['trading']['symbol']
        self.timeframe = self.config['trading']['timeframe']

    def fetch_ohlcv(self, start_date: str, end_date: Optional[str] = None, limit: int = 1000) -> pd.DataFrame:
        """
        Fetch OHLCV (Open, High, Low, Close, Volume) data for specified date range.

        Automatically handles pagination and rate limiting when fetching large date ranges.
        Removes duplicate timestamps and filters to exact date boundaries.

        Args:
            start_date: Start date in 'YYYY-MM-DD' format (e.g., '2024-01-01')
            end_date: End date in 'YYYY-MM-DD' format. Defaults to today if None
            limit: Candles per API request. Max 1000 for OKX, increase for efficiency

        Returns:
            DataFrame with columns:
                - timestamp (int): Unix timestamp in milliseconds
                - open (float): Opening price
                - high (float): Highest price in period
                - low (float): Lowest price in period
                - close (float): Closing price
                - volume (float): Trading volume
                - datetime (datetime): Human-readable timestamp

        Example:
            >>> df = fetcher.fetch_ohlcv('2024-01-01', '2024-01-31')
            >>> print(df.head())
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')

        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')

        print(f"Fetching {self.symbol} {self.timeframe} data from {start_date} to {end_date}")

        all_candles = []
        current_dt = start_dt

        # Pagination loop: fetch data in chunks until reaching end_date
        while current_dt < end_dt:
            # CCXT expects 'since' parameter in milliseconds
            since = int(current_dt.timestamp() * 1000)

            try:
                # Fetch one batch of candles (up to 'limit' count)
                candles = self.exchange.fetch_ohlcv(
                    self.symbol,
                    timeframe=self.timeframe,
                    since=since,  # Start from this timestamp
                    limit=limit  # Max candles per request
                )

                if not candles:
                    break  # No more data available

                all_candles.extend(candles)

                # Update current_dt to last fetched candle's timestamp
                # This ensures next iteration starts where this one ended
                last_timestamp = candles[-1][0]
                current_dt = datetime.fromtimestamp(last_timestamp / 1000)

                print(f"Fetched {len(candles)} candles. Current date: {current_dt.strftime('%Y-%m-%d %H:%M')}")

                # Rate limiting: small delay to avoid hitting API limits
                # OKX allows ~20 requests/second, 100ms = 10 req/s (safe)
                self.exchange.sleep(100)

            except Exception as e:
                print(f"Error fetching data: {e}")
                break

        # Convert to DataFrame
        df = pd.DataFrame(
            all_candles,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )

        # Remove duplicates and sort
        df = df.drop_duplicates(subset=['timestamp']).sort_values('timestamp')

        # Convert timestamp to datetime
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

        # Filter to exact date range
        df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

        print(f"Total candles fetched: {len(df)}")

        return df

    def save_data(self, df: pd.DataFrame, filename: Optional[str] = None) -> Path:
        """
        Save OHLCV data to CSV file in the data directory.

        Filename is auto-generated from symbol, timeframe, and date range if not specified.

        Args:
            df: DataFrame containing OHLCV data with 'datetime' column
            filename: Custom output filename. Auto-generated if None
                     Format: {SYMBOL}_{TIMEFRAME}_{START_DATE}_to_{END_DATE}.csv

        Returns:
            Path object pointing to saved CSV file

        Example:
            >>> filepath = fetcher.save_data(df)
            >>> print(filepath)  # data/BTC_USDT_USDT_1m_20240101_to_20240131.csv
        """
        if filename is None:
            # Create filename from symbol and date range
            start_date = df['datetime'].min().strftime('%Y%m%d')
            end_date = df['datetime'].max().strftime('%Y%m%d')
            symbol_clean = self.symbol.replace('/', '_').replace(':', '_')
            filename = f"{symbol_clean}_{self.timeframe}_{start_date}_to_{end_date}.csv"

        # Create data directory if it doesn't exist
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)

        filepath = data_dir / filename
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")

        return filepath


def main() -> None:
    """
    Main execution: fetch data based on config and display statistics.

    Loads date range from config.yaml, fetches OHLCV data, displays summary statistics,
    and saves to CSV file.
    """
    # Load config to get date range
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    fetcher = OKXDataFetcher()

    # Fetch historical data
    start_date = config['backtesting']['start_date']
    end_date = config['backtesting']['end_date']

    df = fetcher.fetch_ohlcv(start_date, end_date)

    # Display basic statistics
    print("\nData Statistics:")
    print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")
    print(f"Total rows: {len(df)}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print("\nFirst few rows:")
    print(df.head())
    print("\nPrice statistics:")
    print(df[['open', 'high', 'low', 'close', 'volume']].describe())

    # Save to CSV
    fetcher.save_data(df)


if __name__ == '__main__':
    main()
