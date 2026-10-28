FROM node:20-alpine

WORKDIR /app
COPY server.js .

EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O - http://localhost:8080/health || exit 1

CMD ["node", "server.js"]
