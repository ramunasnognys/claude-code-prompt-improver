# ADR-0004: OKX Exchange and Perpetual Futures

## Status

Accepted

## Context

Need crypto exchange for data and potential live trading. Requirements:
- 1-minute historical data availability (min 6 months back)
- Perpetual futures support (USDT-margined)
- API access without authentication (for historical data)
- Reasonable rate limits (fetch 100K+ candles)
- Reliable uptime and data quality
- Supported by CCXT library

Exchanges evaluated:
1. **OKX**: 1m data, USDT perps, free historical API, 20 req/s limit
2. **Binance**: Market leader, good data, but geo-restricted (US, Canada)
3. **Bybit**: Good API, but limited free historical data
4. **Deribit**: BTC/ETH only, USD-margined (not USDT), options focus
5. **FTX**: Best API, but defunct (bankruptcy 2022)

Perpetual futures vs spot:
- **Spot**: Cash-settled, can only go long, no leverage
- **Perps**: Can short, leverage up to 125x, funding rates, 24/7 liquidity

## Decision

Use **OKX Perpetual Futures (USDT-margined)** via CCXT library.

Configuration:
- Symbol format: `BTC/USDT:USDT` (base/quote:settlement)
- Default type: `swap` (perpetual contract)
- Timeframe: `1m` (1-minute candles)
- Historical data: Free API, no authentication required
- Rate limit: 20 req/s (100ms delay between requests)

Rationale:
- OKX provides unlimited historical 1m data for free
- USDT-margined perps more intuitive than coin-margined (P&L in USDT not BTC)
- Available globally (not geo-restricted like Binance)
- CCXT support excellent, same code works for other exchanges if needed
- Competitive fees (0.02% maker, 0.04% taker)
- Good API stability and uptime

## Consequences

### Positive

- Can fetch years of historical data without paid subscription
- Perpetual futures enable shorting (essential for scalping strategies)
- USDT settlement simplifies P&L accounting (no BTC conversion needed)
- CCXT abstraction makes switching exchanges easy (change 1 line of config)
- Rate limits generous enough for backtesting (1000 candles/request)
- Sandbox/testnet available for paper trading before live

### Negative

- Funding rates not modeled in backtests (impacts multi-day positions)
- Data quality issues possible (gaps, wrong candles) though rare
- API changes occasionally break CCXT compatibility (mitigated by version pinning)
- Not available in some jurisdictions (users must check local regulations)
- Perpetual futures more complex than spot (liquidation risk with leverage)
- Exchange risk (hack, insolvency) though OKX is top-tier

### Neutral

- Must handle rate limiting (100ms sleep between requests)
- Symbol format differs from other exchanges (requires CCXT normalization)
- Data fetched incrementally (max 1000 candles/request, pagination needed)
- Live trading requires KYC and API key setup (not needed for backtesting)
- Fees slightly higher than maker-only strategies (0.04% vs 0.02%)

## References

- CCXT OKX documentation: https://docs.ccxt.com/en/latest/exchange-markets.html#okx
- Implementation: `src/data/fetch_data.py` (OKXDataFetcher)
- Configuration: `config/config.yaml` exchange section
- OKX API docs: https://www.okx.com/docs-v5/en/
- Related ADR: [ADR-0002](0002-backtesting-framework.md) on commission modeling
