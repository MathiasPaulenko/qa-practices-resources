// core/config/environment.ts
export const environment = {
  baseURL: process.env.BASE_URL || 'https://app.qa.local',
  apiURL: process.env.API_URL || 'https://api.qa.local',
  credentials: {
    username: process.env.TEST_USER || 'ana@qa.local',
    password: process.env.TEST_PASSWORD || '',
  },
  timeouts: {
    navigation: 10_000,
    action: 5_000,
  },
};
