# Stage 1: Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Build arguments
ARG REACT_APP_API_URL

# Export to environment for react-scripts
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm i

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Runtime stage
FROM node:20-alpine

WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy built application
COPY --from=builder /app/build ./build

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Run app
CMD ["serve", "-s", "build", "-l", "3000"]
