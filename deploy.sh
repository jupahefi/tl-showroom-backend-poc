#!/bin/bash

set -e

echo "🚀 Iniciando despliegue del backend..."

PROJECT_PATH="/opt/easyengine/sites/tl-showroom.equalitech.xyz/app/backend"
cd "$PROJECT_PATH"

echo "📥 Actualizando código fuente desde Git..."
git pull origin main

echo "🐳 Construyendo imagen de Docker..."
docker-compose build --no-cache

echo "🔄 Reiniciando backend..."
docker-compose down
docker-compose up -d

echo "🔍 Verificando estado del backend..."
docker ps | grep showroom-api

echo "🔗 Conectando backend a la red de EasyEngine..."
if docker network connect tl-showroomequalitechxyz_tl-showroom.equalitech.xyz showroom-api; then
    echo "✅ Conexión de red exitosa."
else
    echo "⚠️ Advertencia: No se pudo conectar showroom-api a la red de EasyEngine. Verifica manualmente."
fi

echo "✅ Despliegue del backend completado."
