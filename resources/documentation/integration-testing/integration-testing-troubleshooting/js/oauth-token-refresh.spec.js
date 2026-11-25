// OAuth client-credentials refresh in test setup.
// The URL is a placeholder — point it at your provider's token endpoint.

let authToken;

beforeAll(async () => {
  const tokenResponse = await fetch('https://auth.staging.internal/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: process.env.API_CLIENT_ID,
      client_secret: process.env.API_CLIENT_SECRET,
    }),
  });
  const { access_token } = await tokenResponse.json();
  authToken = access_token;
});

function getAuthHeader() {
  return { Authorization: `Bearer ${authToken}` };
}

module.exports = { getAuthHeader };
