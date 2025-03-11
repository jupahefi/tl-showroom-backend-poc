#!/bin/bash

# Script to run linting with flake8

echo "🔍 Running linting with flake8..."

# Run flake8 (configuration is already in setup.cfg)
flake8 .

# Check the exit code
if [ $? -eq 0 ]; then
    echo "✅ Linting passed successfully."
else
    echo "❌ Linting found issues. Please check the error messages above."
    exit 1
fi