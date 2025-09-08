# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app sources
COPY . .

# Make entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
