# Multi-stage build: Node.js for React build, nginx for serving
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

# Nginx stage for serving static files
FROM nginx:alpine

# Copy custom nginx config
COPY code/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built React app from previous stage
COPY --from=react-build /app/build /usr/share/nginx/html

# Copy VERSION file for reference
COPY code/frontend/VERSION /usr/share/nginx/html/VERSION

EXPOSE 8000

CMD ["nginx", "-g", "daemon off;"]
