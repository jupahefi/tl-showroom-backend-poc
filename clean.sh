#!/bin/bash

# Script to clean up temporary files and directories

echo "🧹 Cleaning up temporary files and directories..."

# Remove pytest cache
echo "Removing .pytest_cache..."
rm -rf .pytest_cache

# Remove coverage reports
echo "Removing coverage reports..."
rm -rf htmlcov
rm -rf .coverage

# Remove test database
echo "Removing test database..."
rm -f test.db

# Remove __pycache__ directories
echo "Removing __pycache__ directories..."
find . -type d -name __pycache__ -exec rm -rf {} +

# Remove IDE specific directories
echo "Removing IDE specific directories..."
rm -rf .idea
rm -rf .vscode

# Remove redundant root-level files that have been refactored into the app package
echo "Removing redundant root-level files..."
rm -f routes.py
rm -f crud.py
rm -f schemas.py
rm -f models.py

echo "✅ Cleanup completed successfully."
