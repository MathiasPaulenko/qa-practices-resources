// Bottleneck 2.x — stay below the provider's documented rate limit for live calls
const Bottleneck = require('bottleneck');

const rateLimiter = new Bottleneck({
  maxConcurrent: 1,
  minTime: 1000, // 1 request per second per connector
});

async function callLiveApi(url) {
  return rateLimiter.schedule(() => fetch(url));
}

module.exports = { rateLimiter, callLiveApi };
