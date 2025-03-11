#!/bin/bash

# Script to run tests in Docker

echo "🐳 Running tests in Docker..."

# Run docker-compose for testing
docker-compose -f docker-compose.test.yml up --build

# Check the exit code
if [ $? -eq 0 ]; then
    echo "✅ Docker tests completed successfully."
else
    echo "❌ Docker tests failed. Please check the error messages above."
    exit 1
fi

# Clean up containers
echo "🧹 Cleaning up Docker containers..."
docker-compose -f docker-compose.test.yml down

echo "✅ Docker test environment cleaned up."