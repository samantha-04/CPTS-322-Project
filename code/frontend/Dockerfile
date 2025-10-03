# Multi-stage build: Node.js for React build, Python for Flask serve
FROM node:18-alpine AS react-build

# Set working directory for React build
WORKDIR /app

# Copy package files
COPY code/frontend/package*.json ./

# Install npm dependencies (including dev dependencies needed for build)
RUN npm ci

# Copy React source code
COPY code/frontend/src ./src
COPY code/frontend/public ./public

# Build React app
RUN npm run build

# Python stage for Flask server
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy frontend code (including Flask app)
COPY code/frontend/ ./frontend/

# Copy built React app from previous stage
COPY --from=react-build /app/build ./frontend/build

EXPOSE 8000

CMD ["python", "frontend/app.py"]
