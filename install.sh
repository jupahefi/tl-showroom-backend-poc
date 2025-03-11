#!/bin/bash

# Script to install dependencies

echo "📦 Installing dependencies..."

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Check the exit code
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully."
else
    echo "❌ Failed to install dependencies. Please check the error messages above."
    exit 1
fi