# Pinned integration test environment — same image for local, CI and staging
FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY .

ENV NODE_ENV=test
ENV API_TIMEOUT=30000
ENV RATE_LIMIT_ENABLED=true

CMD ["npm", "run", "test:integration"]
