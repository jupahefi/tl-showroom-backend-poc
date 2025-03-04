#!/bin/bash
echo "🚀 Iniciando API..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
