#!/bin/bash

# Script to run tests with coverage report

echo "🧪 Running tests with coverage report..."

# Run pytest with coverage
pytest --cov=. --cov-report=html

# Check the exit code
if [ $? -eq 0 ]; then
    echo "✅ Tests passed! Coverage report generated."
    echo "📊 Coverage report is available in the htmlcov/ directory."
else
    echo "❌ Tests failed. Please check the error messages above."
    echo "📊 A partial coverage report may have been generated in the htmlcov/ directory."
    exit 1
fi