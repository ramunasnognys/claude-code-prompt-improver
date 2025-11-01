#!/bin/bash
# Quick backtest runner - execute standard pipeline

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Config
CONFIG_FILE="${1:-config/config.yaml}"
SKIP_DATA="${SKIP_DATA:-false}"
SKIP_TRAIN="${SKIP_TRAIN:-false}"

echo -e "${BLUE}=== Crypto Trading Bot Quick Backtest ===${NC}\n"

# Step 1: Validate config
echo -e "${BLUE}[1/5]${NC} Validating configuration..."
if python .claude/skills/crypto-ml-trading/scripts/validate_config.py "$CONFIG_FILE"; then
    echo -e "${GREEN}✓ Config valid${NC}\n"
else
    echo -e "${RED}✗ Config validation failed${NC}"
    exit 1
fi

# Step 2: Fetch data (optional)
if [ "$SKIP_DATA" = "false" ]; then
    echo -e "${BLUE}[2/5]${NC} Fetching market data..."
    if python -m src.data.fetch_data; then
        echo -e "${GREEN}✓ Data fetched${NC}\n"
    else
        echo -e "${RED}✗ Data fetch failed${NC}"
        exit 1
    fi
else
    echo -e "${BLUE}[2/5]${NC} Skipping data fetch (--skip-data)\n"
fi

# Step 3: Train model (optional)
if [ "$SKIP_TRAIN" = "false" ]; then
    echo -e "${BLUE}[3/5]${NC} Training LSTM model..."
    if python -m src.models.train_lstm; then
        echo -e "${GREEN}✓ Model trained${NC}\n"
    else
        echo -e "${RED}✗ Model training failed${NC}"
        exit 1
    fi
else
    echo -e "${BLUE}[3/5]${NC} Skipping training (--skip-train)\n"
fi

# Step 4: Run backtest
echo -e "${BLUE}[4/5]${NC} Running backtest..."
if python run_pipeline.py --skip-fetch --skip-train; then
    echo -e "${GREEN}✓ Backtest complete${NC}\n"
else
    echo -e "${RED}✗ Backtest failed${NC}"
    exit 1
fi

# Step 5: Show results
echo -e "${BLUE}[5/5]${NC} Analyzing results..."
if [ -f "results/backtest_stats.csv" ]; then
    echo -e "${GREEN}✓ Results summary:${NC}"
    echo ""
    # Show last few lines of stats
    tail -5 results/backtest_stats.csv | column -t -s','
    echo ""
    echo -e "Full results: ${BLUE}results/backtest_stats.csv${NC}"
    echo -e "Plots: ${BLUE}results/*.png${NC}"
else
    echo -e "${RED}✗ Results file not found${NC}"
    exit 1
fi

echo -e "\n${GREEN}=== Backtest Pipeline Complete ===${NC}"
