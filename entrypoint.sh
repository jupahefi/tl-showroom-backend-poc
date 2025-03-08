#!/bin/bash
echo "🚀 Iniciando API con HTTPS..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 \
    --ssl-keyfile /etc/letsencrypt/live/equalitech.xyz/privkey.pem \
    --ssl-certfile /etc/letsencrypt/live/equalitech.xyz/fullchain.pem
