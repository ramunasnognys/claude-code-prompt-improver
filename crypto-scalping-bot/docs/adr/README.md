# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records documenting key technical and architectural decisions made during the development of the crypto scalping bot.

## What is an ADR?

Architecture Decision Records capture important architectural decisions along with their context and consequences. They help understand why certain technical choices were made and serve as institutional knowledge.

## Format

We use the MADR (Markdown ADR) format with the following sections:

- **Status**: proposed | accepted | deprecated | superseded
- **Context**: The issue motivating this decision
- **Decision**: The change being proposed or implemented
- **Consequences**: Positive and negative outcomes of this decision

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-0001](0001-lstm-model-choice.md) | LSTM Model for Price Prediction | Accepted |
| [ADR-0002](0002-backtesting-framework.md) | Backtesting.py Framework Selection | Accepted |
| [ADR-0003](0003-technical-indicators.md) | Technical Indicator Selection | Accepted |
| [ADR-0004](0004-okx-exchange.md) | OKX Exchange and Perpetual Futures | Accepted |
| [ADR-0005](0005-normalized-predictions.md) | Normalized Predictions Approach | Accepted |

## Creating New ADRs

1. Copy the template: `cp adr-template.md NNNN-title.md`
2. Fill in all sections with specific details
3. Update this index
4. Submit for review with status "proposed"
5. Update status to "accepted" once approved

## Lifecycle

- **Proposed**: Under discussion
- **Accepted**: Decision approved and implemented
- **Deprecated**: No longer recommended but still in use
- **Superseded**: Replaced by a newer ADR (link to replacement)
