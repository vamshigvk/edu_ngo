# --- Stage 1: build the static bundle -----------------------------------
FROM node:20-alpine AS build

WORKDIR /app

# Install deps against the lockfile for reproducible builds.
COPY package.json package-lock.json ./
RUN npm ci

# Build. VITE_API_BASE is left empty so the app makes same-origin requests
# that nginx (below) reverse-proxies to the backend — no CORS needed.
COPY . .
RUN npm run build

# --- Stage 2: serve with nginx -------------------------------------------
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
