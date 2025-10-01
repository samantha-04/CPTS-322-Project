#!/bin/bash

# Build and Run Script for React + Flask Frontend

echo "🚀 Setting up React + Flask Frontend..."

# Check if node_modules exists, if not install dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
fi

# Build the React app
echo "🔨 Building React app..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ React build successful!"
    echo "🌐 Starting Flask server..."
    python3 app.py
else
    echo "❌ React build failed!"
    exit 1
fi
