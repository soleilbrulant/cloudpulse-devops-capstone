# Stage 1: Build the React + Vite static bundle
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve using hardened Nginx Alpine
FROM nginx:alpine

# Remove default configuration
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration with reverse proxy
COPY nginx.conf /etc/nginx/conf.d/cloudpulse.conf

# Copy compiled static assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
