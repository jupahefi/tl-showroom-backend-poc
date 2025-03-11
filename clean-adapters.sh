#!/bin/bash

# Script to clean up redundant adapter implementations in the codebase

echo "🧹 Cleaning up redundant adapter implementations..."

# Remove redundant API adapter directory
echo "Removing app/core/adapters/api directory..."
rm -rf app/core/adapters/api

# Clean up redundant files in DB adapter directory while preserving files used by tests
echo "Cleaning up app/core/adapters/db directory..."
# Create a temporary directory to store files we want to keep
mkdir -p temp_db_files
# Copy the sqlalchemy_models.py file that's used by tests
cp app/core/adapters/db/sqlalchemy_models.py temp_db_files/
# Remove the DB adapter directory
rm -rf app/core/adapters/db
# Recreate the directory structure
mkdir -p app/core/adapters/db
# Move the preserved files back
mv temp_db_files/sqlalchemy_models.py app/core/adapters/db/
# Remove the temporary directory
rm -rf temp_db_files

# Update the adapters/__init__.py file to avoid import errors
echo "Updating app/core/adapters/__init__.py..."
cat > app/core/adapters/__init__.py << EOF
# This file is intentionally left empty after cleanup
# The adapter implementations have been consolidated
EOF

# Update the adapters/db/__init__.py file to avoid import errors
echo "Updating app/core/adapters/db/__init__.py..."
cat > app/core/adapters/db/__init__.py << EOF
# This file contains only the models needed for tests
# The adapter implementations have been consolidated
EOF

echo "✅ Cleanup of redundant adapter implementations completed successfully."
