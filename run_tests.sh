#!/bin/bash

# Script to run tests and verify the testing setup

echo "🧪 Running tests to verify the testing setup..."

# Install dependencies if needed
if [ "$1" == "--install" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Load test environment variables
echo "📝 Loading test environment variables..."
export $(grep -v '^#' .env.test | xargs)

# Remove existing test database if it exists
echo "🗑️ Cleaning up old test database..."
if [ -f "./test.db" ]; then
    rm ./test.db
fi

# Run the tests with coverage
echo "🚀 Running tests with coverage..."
TEST_DATABASE_URL=sqlite:///./test.db PYTHONPATH=. pytest --cov=. --cov-report=html

# Check the exit code
if [ $? -eq 0 ]; then
    echo "✅ Tests passed! The testing setup is working correctly."
    echo "📊 Coverage report generated in the htmlcov/ directory."
else
    echo "❌ Tests failed. Please check the error messages above."
    echo "📊 A partial coverage report may have been generated in the htmlcov/ directory."
    exit 1
fi
