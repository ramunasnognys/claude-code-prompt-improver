#!/bin/bash
# Quick results checker for Phase 3.1

cd /Users/ramunasnognys/Developer/workspace/prompt-improver/crypto-scalping-bot

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           PHASE 3.1 RESULTS CHECKER                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if training is complete
if ps aux | grep -q "[p]ython src/models/lstm_model.py"; then
    echo "⏳ Training still in progress..."
    EPOCH=$(grep "Epoch [0-9]" training_phase3_1.log | tail -1 | awk '{print $2}')
    echo "   Current: $EPOCH"
    echo "   ETA: ~10-12 minutes"
    echo ""
    echo "Monitor: tail -f training_phase3_1.log"
    exit 0
fi

echo "✅ Training complete!"
echo ""

# Check if validation completed
if [ ! -f "results/strategy_comparison.csv" ] || [ $(wc -l < results/strategy_comparison.csv) -lt 3 ]; then
    echo "⏳ Validation in progress or queued..."
    echo "   Check: tail -f validation_phase3_1.log"
    exit 0
fi

echo "✅ Validation complete!"
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                        RESULTS                                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Show strategy comparison
echo "PHASE 2.1 BASELINE:"
echo "  Conservative: -0.45%"
echo "  Default:      -1.42%"
echo ""

echo "PHASE 3.1 RESULTS:"
cat results/strategy_comparison.csv | column -t -s,

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                      ANALYSIS                                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Extract Conservative result
CONS_RETURN=$(grep "Conservative" results/strategy_comparison.csv | cut -d',' -f2)
DEFAULT_RETURN=$(grep -v "Conservative\|Aggressive\|Strategy" results/strategy_comparison.csv | head -1 | cut -d',' -f2)

echo "Conservative Return: $CONS_RETURN"
echo "Default Return: $DEFAULT_RETURN"
echo ""

# Check success
if [ ! -z "$CONS_RETURN" ]; then
    CONS_NUM=$(echo $CONS_RETURN | tr -d '%' | awk '{print int($1)}')
    if [ $CONS_NUM -gt 1 ]; then
        echo "🎉 SUCCESS! Conservative is profitable!"
        echo "   Target achieved: +3-5% goal"
    elif [ $CONS_NUM -gt -1 ]; then
        echo "✅ CLOSE! Nearly profitable"
        echo "   Just ${CONS_RETURN} from breakeven"
    else
        echo "⚠️  Still unprofitable but check if improved"
    fi
fi

echo ""
echo "Full results:"
echo "  - results/backtest_results.csv"
echo "  - backtest_phase3_1.log"
echo ""
