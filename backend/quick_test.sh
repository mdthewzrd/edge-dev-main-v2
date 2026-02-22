#!/bin/bash
# Quick RENATA V2 Test Script
# Just run this to see RENATA working!

cd "/Users/michaeldurante/ai dev/ce-hub/projects/edge-dev-main-v2/backend"

echo "🤖 Testing RENATA V2..."
echo ""

echo "1️⃣  Generating Backside B scanner..."
python renata_cli.py -r "Generate a Backside B scanner"
echo ""

echo "2️⃣  Creating implementation plan..."
python renata_cli.py -r "Plan D2 momentum strategy"
echo ""

echo "3️⃣  Listing available tools..."
python renata_cli.py -r "What tools can you use?"
echo ""

echo "✅ All done!"
