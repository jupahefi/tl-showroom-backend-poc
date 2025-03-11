#!/bin/bash

# Script to clean up redundant directories in the codebase

echo "Cleaning up redundant directories..."

# Remove redundant input directory
echo "Removing app/core/adapters/input directory..."
rm -rf app/core/adapters/input

# Remove redundant output directory
echo "Removing app/core/adapters/output directory..."
rm -rf app/core/adapters/output

echo "Clean up complete!"