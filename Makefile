# Flask Web Application Makefile
# Provides easy commands for development and deployment of frontend/backend services

.PHONY: help setup install clean test dev status
.PHONY: build run start stop restart logs reset
.PHONY: frontend backend both
.PHONY: build-frontend build-backend build-all
.PHONY: run-frontend run-backend run-all
.PHONY: test-frontend test-backend test-all

# Color codes for output
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
BLUE=\033[0;34m
NC=\033[0m # No Color

# Default target - show help
help:
	@echo "$(BLUE)📋 Available Commands:$(NC)"
	@echo ""
	@echo "$(GREEN)🚀 Quick Start:$(NC)"
	@echo "  make setup          - Setup development environment"
	@echo "  make dev            - Install dependencies and run both services"
	@echo "  make run            - Run both frontend and backend services"
	@echo ""
	@echo "$(GREEN)🔧 Development:$(NC)"
	@echo "  make install        - Install Python dependencies"
	@echo "  make frontend       - Run frontend only (port 8000)"
	@echo "  make backend        - Run backend only (port 5646)"
	@echo "  make both           - Run both services locally"
	@echo ""
	@echo "$(GREEN)🐳 Docker Commands:$(NC)"
	@echo "  make build          - Build Docker images"
	@echo "  make start          - Start services in background"
	@echo "  make stop           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs           - View service logs"
	@echo "  make reset          - Clean rebuild everything"
	@echo ""
	@echo "$(GREEN)🧪 Testing & Utilities:$(NC)"
	@echo "  make test           - Test both services"
	@echo "  make status         - Check service status"
	@echo "  make clean          - Clean cache and unused Docker resources"
	@echo ""
	@echo "$(YELLOW)📍 Service URLs:$(NC)"
	@echo "  Frontend: http://localhost:8000"
	@echo "  Backend:  http://localhost:5646"

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================

setup:
	@echo "$(GREEN)🔧 Setting up development environment...$(NC)"
	@if command -v python3 >/dev/null 2>&1; then \
		echo "✓ Python3 found: $$(python3 --version)"; \
		python3 -m pip install --upgrade pip; \
	elif command -v python >/dev/null 2>&1; then \
		echo "✓ Python found: $$(python --version)"; \
		python -m pip install --upgrade pip; \
	else \
		echo "$(RED)✗ Python not found. Please install Python first.$(NC)"; \
		echo "On macOS: brew install python"; \
		echo "On Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ Environment setup complete!$(NC)"

install: setup
	@echo "$(GREEN)📦 Installing Python dependencies...$(NC)"
	@if command -v python3 >/dev/null 2>&1; then \
		python3 -m pip install -r requirements.txt; \
	else \
		python -m pip install -r requirements.txt; \
	fi
	@echo "$(GREEN)✓ Dependencies installed!$(NC)"

# ============================================================================
# LOCAL DEVELOPMENT
# ============================================================================

frontend:
	@echo "$(GREEN)🎨 Starting frontend service (port 8000)...$(NC)"
	@cd frontend && \
	if command -v python3 >/dev/null 2>&1; then \
		python3 app.py; \
	else \
		python app.py; \
	fi

backend:
	@echo "$(GREEN)⚙️ Starting backend service (port 5646)...$(NC)"
	@cd backend/api && \
	if command -v python3 >/dev/null 2>&1; then \
		python3 app.py; \
	else \
		python app.py; \
	fi

both:
	@echo "$(GREEN)🚀 Starting both services...$(NC)"
	@echo "$(YELLOW)Note: This will run in foreground. Use Ctrl+C to stop.$(NC)"
	@echo "$(YELLOW)For background mode, use 'make start'$(NC)"
	@trap 'kill 0' INT; \
	make backend & \
	make frontend & \
	wait

# ============================================================================
# DOCKER COMMANDS
# ============================================================================

build:
	@echo "$(GREEN)🔨 Building Docker images...$(NC)"
	docker-compose build

run:
	@echo "$(GREEN)🚀 Starting services with Docker Compose...$(NC)"
	docker-compose up

start:
	@echo "$(GREEN)🚀 Starting services in background...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services started!$(NC)"
	@echo "$(BLUE)📍 Access URLs:$(NC)"
	@echo "  Frontend: http://localhost:8000"
	@echo "  Backend:  http://localhost:5646"
	@echo ""
	@echo "$(YELLOW)💡 Useful commands:$(NC)"
	@echo "  make logs    - View logs"
	@echo "  make status  - Check status"
	@echo "  make stop    - Stop services"

stop:
	@echo "$(YELLOW)🛑 Stopping services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped!$(NC)"

restart: stop start

logs:
	@echo "$(BLUE)📋 Viewing service logs... (Ctrl+C to exit)$(NC)"
	docker-compose logs -f

reset:
	@echo "$(YELLOW)🔄 Resetting Docker environment...$(NC)"
	docker-compose down -v --remove-orphans
	docker system prune -f
	@echo "$(GREEN)🔨 Rebuilding and starting...$(NC)"
	docker-compose up --build -d
	@echo "$(GREEN)✓ Reset complete!$(NC)"

# ============================================================================
# TESTING & STATUS
# ============================================================================

test-frontend:
	@echo "$(BLUE)🧪 Testing frontend service...$(NC)"
	@if curl -s http://localhost:8000/hello >/dev/null 2>&1; then \
		echo "$(GREEN)✓ Frontend is running and accessible!$(NC)"; \
		curl -s http://localhost:8000/hello | python3 -m json.tool; \
	else \
		echo "$(RED)✗ Frontend not accessible at http://localhost:8000$(NC)"; \
	fi

test-backend:
	@echo "$(BLUE)🧪 Testing backend service...$(NC)"
	@if curl -s http://localhost:5646/health >/dev/null 2>&1; then \
		echo "$(GREEN)✓ Backend is running and accessible!$(NC)"; \
		curl -s http://localhost:5646/health | python3 -m json.tool; \
	else \
		echo "$(RED)✗ Backend not accessible at http://localhost:5646$(NC)"; \
	fi

test: test-frontend test-backend

status:
	@echo "$(BLUE)📊 Service Status:$(NC)"
	@echo ""
	@echo "$(YELLOW)🐳 Docker Services:$(NC)"
	@docker-compose ps 2>/dev/null || echo "$(RED)Docker Compose not running$(NC)"
	@echo ""
	@echo "$(YELLOW)🌐 Service Health:$(NC)"
	@printf "Frontend (8000): "
	@if curl -s http://localhost:8000/hello >/dev/null 2>&1; then \
		echo "$(GREEN)✓ Running$(NC)"; \
	else \
		echo "$(RED)✗ Not responding$(NC)"; \
	fi
	@printf "Backend (5646):  "
	@if curl -s http://localhost:5646/health >/dev/null 2>&1; then \
		echo "$(GREEN)✓ Running$(NC)"; \
	else \
		echo "$(RED)✗ Not responding$(NC)"; \
	fi

# ============================================================================
# MAINTENANCE
# ============================================================================

clean:
	@echo "$(YELLOW)🧹 Cleaning up...$(NC)"
	@echo "Removing Python cache files..."
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaning Docker resources..."
	@docker system prune -f >/dev/null 2>&1 || true
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

# ============================================================================
# CONVENIENCE ALIASES
# ============================================================================

dev: install both
docker: reset