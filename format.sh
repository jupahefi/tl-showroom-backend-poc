#!/bin/bash

# Script to format code using Black

echo "🎨 Formatting code with Black..."

# Run Black with the same configuration as in pyproject.toml
black --line-length 100 --target-version py38 .

# Check the exit code
if [ $? -eq 0 ]; then
    echo "✅ Code formatting completed successfully."
else
    echo "❌ Code formatting failed. Please check the error messages above."
    exit 1
fi