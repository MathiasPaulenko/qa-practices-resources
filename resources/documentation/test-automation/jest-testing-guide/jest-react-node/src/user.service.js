const { getUser } = require('./api');

async function loadDashboard(id) {
  const user = await getUser(id);
  return { user };
}

module.exports = { loadDashboard };
