export const config: WebdriverIO.Config = {
  runner: 'local',
  tsConfigPath: './tsconfig.json',
  specs: ['./tests/appointments.wdio.spec.ts'],
  capabilities: [{
    browserName: 'chrome',
    'goog:chromeOptions': { args: ['--headless=new'] }
  }],
  logLevel: 'warn',
  framework: 'mocha',
  reporters: ['spec', ['allure', { outputDir: 'allure-results' }]],
  mochaOpts: { ui: 'bdd', timeout: 60000 },
  maxInstances: 4
};
