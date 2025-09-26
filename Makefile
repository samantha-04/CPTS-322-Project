# Flask Web Application Makefile
# Provides easy commands for development and deployment

.PHONY: help install run build docker-run docker-build docker-stop clean test setup

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup       - Setup environment and install dependencies"
	@echo "  make install     - Install Python dependencies"
	@echo "  make run         - Run Flask app locally"
	@echo "  make build       - Build Docker image"
	@echo "  make docker-run  - Run app using Docker Compose (foreground)"
	@echo "  make docker-start- Run app using Docker Compose (background)"
	@echo "  make docker-stop - Stop Docker containers"
	@echo "  make docker-build- Build and run with Docker Compose"
	@echo "  make clean       - Clean up Python cache files"
	@echo "  make test        - Run basic connectivity test"
	@echo "  make logs        - View Docker container logs"
	@echo "  make docker-pull - Pull Python base image manually"
	@echo "  make docker-reset- Reset Docker and rebuild"

# Setup environment - check for Python and install tools
setup:
	@echo "Setting up development environment..."
	@echo "Checking for Python..."
	@if command -v python3 >/dev/null 2>&1; then \
		echo "Python3 found: $$(python3 --version)"; \
		python3 -m pip install --upgrade pip; \
	elif command -v python >/dev/null 2>&1; then \
		echo "Python found: $$(python --version)"; \
		python -m pip install --upgrade pip; \
	else \
		echo "Python not found. Please install Python first."; \
		echo "On Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"; \
		echo "On WSL: Install Python from Windows Store or use apt"; \
		exit 1; \
	fi

# Install Python dependencies
install: setup
	@if command -v python3 >/dev/null 2>&1; then \
		python3 -m pip install -r requirements.txt; \
	elif command -v python >/dev/null 2>&1; then \
		python -m pip install -r requirements.txt; \
	else \
		echo "Python not found. Run 'make setup' first."; \
		exit 1; \
	fi

# Run Flask app locally (development mode)
runFlask:
	@if command -v python3 >/dev/null 2>&1; then \
		python3 app.py; \
	elif command -v python >/dev/null 2>&1; then \
		python app.py; \
	else \
		echo "Python not found. Run 'make setup' first."; \
		exit 1; \
	fi

# Pull Python base image manually (fixes credential issues)
docker-pull:
	docker pull python:3.9-slim

# Build Docker image (with manual pull first)
build: docker-pull
	docker build -t flask-web-app .

# Run using Docker Compose (recommended)
run:
	docker-compose up

# Run using Docker Compose in background (detached)
start:
	docker-compose up -d
	@echo "✓ Flask app started in background"
	@echo "Access at: http://localhost:5000"
	@echo "Use 'make stop' to stop"
	@echo "Use 'make logs' to view logs"

# Build and run using Docker Compose (with manual pull first)
build: docker-pull
	docker-compose up --build

# Reset Docker and rebuild everything
reset:
	@echo "Cleaning up Docker..."
	-docker-compose down
	-docker rmi flask-web-app 2>/dev/null || true
	@echo "Pulling fresh images..."
	docker pull python:3.9-slim
	@echo "Building and starting..."
	docker-compose up --build

# Stop Docker containers
stop:
	docker-compose down

# View Docker logs
logs:
	docker-compose logs -f

# Clean up Python cache files and Docker images
clean:
	@echo "Cleaning Python cache files..."
	-find . -type f -name "*.pyc" -delete 2>/dev/null || true
	-find . -type d -name "__pycache__" -delete 2>/dev/null || true
	-find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaning Docker..."
	-docker system prune -f

# Basic connectivity test
test:
	@echo "Testing Flask app connectivity..."
	@if curl -s http://localhost:5000/api/hello >/dev/null 2>&1; then \
		echo "✓ App is running and accessible!"; \
		curl -s http://localhost:5000/api/hello; \
	else \
		echo "✗ App not accessible. Try:"; \
		echo "  make run        (for local)"; \
		echo "  make docker-run (for Docker)"; \
	fi

# Development setup (install deps and run)
dev: install run

# Full Docker setup (pull, build and run)
docker: docker-reset

# Restart Docker containers
restart: docker-stop docker-run