FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/etc/letsencrypt/live/equalitech.xyz/privkey.pem", "--ssl-certfile", "/etc/letsencrypt/live/equalitech.xyz/fullchain.pem"]
