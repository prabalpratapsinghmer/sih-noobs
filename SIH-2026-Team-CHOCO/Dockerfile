# Multi-stage production build for CyberCell Frontend
FROM node:20-bookworm-slim AS builder

WORKDIR /app

# Copy package manifests and install dependencies
COPY package*.json ./
RUN npm ci --prefer-offline 2>/dev/null || npm install

# Copy source code and build production artifact
COPY . .
RUN npm run build

# Runner stage: Lightweight Nginx Alpine server
FROM nginx:alpine AS runner

WORKDIR /usr/share/nginx/html

# Clean default assets and copy compiled SPA bundle
RUN rm -rf ./*
COPY --from=builder /app/dist .
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
