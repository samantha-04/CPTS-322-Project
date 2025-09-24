# Flask Web Application

A minimal web application built with Python Flask backend, JavaScript frontend, and Docker containers.

## Quick Start with Makefile

The project includes a Makefile for easy command execution:

```bash
# View all available commands
make help

# Run locally (install dependencies and start Flask)
make dev

# Run with Docker (recommended)
make docker-build

# Stop Docker containers
make docker-stop
```

## Available Make Commands

- `make install` - Install Python dependencies
- `make run` - Run Flask app locally
- `make build` - Build Docker image
- `make docker-run` - Run app using Docker Compose
- `make docker-build` - Build and run with Docker Compose
- `make docker-stop` - Stop Docker containers
- `make clean` - Clean up Python cache files
- `make test` - Test app connectivity
- `make logs` - View Docker container logs
- `make dev` - Install dependencies and run locally
- `make restart` - Restart Docker containers

## Project Structure

```
CPTS-322-Project/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── Makefile           # Build automation commands
├── templates/
│   └── index.html     # HTML template
├── static/
│   └── app.js         # Frontend JavaScript
└── README.md          # This file
```

## Features

- Flask backend with REST API endpoints
- Frontend with JavaScript for API interactions
- Docker containerization
- CORS enabled for cross-origin requests
- Simple UI for testing API endpoints
- Makefile for easy command execution

## API Endpoints

- `GET /` - Serves the main HTML page
- `GET /api/hello` - Returns a hello message
- `GET /api/data` - Returns sample data array

## Running the Application

### Quick Start (Recommended)
```bash
make docker-build
```

### Option 1: Using Docker
```bash
make docker-build    # Build and run with Docker Compose
# OR
make docker-run      # Run with existing Docker image
```

### Option 2: Running Locally
```bash
make dev            # Install dependencies and run Flask app
# OR
make install        # Install dependencies only
make run           # Run Flask app
```

### Option 3: Manual Commands
```bash
# Docker
docker-compose up --build

# Local
pip install -r requirements.txt
python app.py
```

## Usage

1. Start the application using any method above
2. Open your browser and navigate to `http://localhost:5000`
3. Click "Say Hello" to test the hello API endpoint
4. Click "Fetch Data" to retrieve sample data from the backend
5. Click "Clear" to clear the output display

## Development

- Flask runs in debug mode for development
- The Docker volume mount allows for live code reloading
- Frontend JavaScript uses async/await for API calls
- CORS is enabled for frontend-backend communication
- Use `make logs` to view container logs during development

## Testing

- Run `make test` to check if the app is running and accessible
- The test command will attempt to connect to the `/api/hello` endpoint

## AI Usage
Used AI to create the bones of the file system for web hosting
