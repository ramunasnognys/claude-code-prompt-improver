#!/bin/bash

# Stripe Product Setup Script
# Creates Stripe products and prices for the SaaS app
# Run: bash scripts/setup-stripe-products.sh

set -e

echo "Creating Stripe Products and Prices..."
echo ""

# Check if stripe CLI is installed
if ! command -v stripe &> /dev/null; then
    echo "Error: Stripe CLI not installed"
    echo "Install: https://stripe.com/docs/stripe-cli"
    exit 1
fi

echo "Creating Pro Plan Product..."
PRO_PRODUCT=$(stripe products create \
  --name="Pro Plan" \
  --description="Advanced features with priority support")

PRO_PRODUCT_ID=$(echo $PRO_PRODUCT | jq -r '.id')
echo "Pro Product ID: $PRO_PRODUCT_ID"

echo ""
echo "Creating Pro Monthly Price..."
PRO_MONTHLY=$(stripe prices create \
  --product=$PRO_PRODUCT_ID \
  --unit-amount=1499 \
  --currency=usd \
  --recurring.interval=month)

PRO_MONTHLY_ID=$(echo $PRO_MONTHLY | jq -r '.id')
echo "Pro Monthly Price ID: $PRO_MONTHLY_ID"

echo ""
echo "Creating Pro Yearly Price..."
PRO_YEARLY=$(stripe prices create \
  --product=$PRO_PRODUCT_ID \
  --unit-amount=14390 \
  --currency=usd \
  --recurring.interval=year)

PRO_YEARLY_ID=$(echo $PRO_YEARLY | jq -r '.id')
echo "Pro Yearly Price ID: $PRO_YEARLY_ID"

echo ""
echo "Creating Enterprise Plan Product..."
ENTERPRISE_PRODUCT=$(stripe products create \
  --name="Enterprise Plan" \
  --description="Custom integrations with dedicated support")

ENTERPRISE_PRODUCT_ID=$(echo $ENTERPRISE_PRODUCT | jq -r '.id')
echo "Enterprise Product ID: $ENTERPRISE_PRODUCT_ID"

echo ""
echo "Creating Enterprise Monthly Price..."
ENTERPRISE_MONTHLY=$(stripe prices create \
  --product=$ENTERPRISE_PRODUCT_ID \
  --unit-amount=9999 \
  --currency=usd \
  --recurring.interval=month)

ENTERPRISE_MONTHLY_ID=$(echo $ENTERPRISE_MONTHLY | jq -r '.id')
echo "Enterprise Monthly Price ID: $ENTERPRISE_MONTHLY_ID"

echo ""
echo "Creating Enterprise Yearly Price..."
ENTERPRISE_YEARLY=$(stripe prices create \
  --product=$ENTERPRISE_PRODUCT_ID \
  --unit-amount=95990 \
  --currency=usd \
  --recurring.interval=year)

ENTERPRISE_YEARLY_ID=$(echo $ENTERPRISE_YEARLY | jq -r '.id')
echo "Enterprise Yearly Price ID: $ENTERPRISE_YEARLY_ID"

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Add these to your .env file:"
echo ""
echo "NEXT_PUBLIC_STRIPE_PRICE_ID_PRO_MONTHLY=$PRO_MONTHLY_ID"
echo "NEXT_PUBLIC_STRIPE_PRICE_ID_PRO_YEARLY=$PRO_YEARLY_ID"
echo "NEXT_PUBLIC_STRIPE_PRICE_ID_ENTERPRISE_MONTHLY=$ENTERPRISE_MONTHLY_ID"
echo "NEXT_PUBLIC_STRIPE_PRICE_ID_ENTERPRISE_YEARLY=$ENTERPRISE_YEARLY_ID"
echo ""
